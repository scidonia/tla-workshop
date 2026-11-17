-------------------------- MODULE Reservation --------------------------
EXTENDS Integers, Sequences, FiniteSets
CONSTANTS Clients, Capacity, Fixed
ASSUME /\ IsFiniteSet(Clients) /\ Clients # {}
       /\ Capacity \in Nat /\ Fixed \in BOOLEAN
VARIABLES remaining, booked, requests, clientPC, workerPC, reply, result
vars == <<remaining, booked, requests, clientPC, workerPC, reply, result>>

Init ==
    /\ remaining = Capacity
    /\ booked = {}
    /\ requests = <<>>
    /\ clientPC = [c \in Clients |-> "ready"]
    /\ workerPC = [c \in Clients |-> "idle"]
    /\ reply = [c \in Clients |-> "empty"]
    /\ result = [c \in Clients |-> "none"]

Send(c) ==
    /\ clientPC[c] = "ready"
    /\ requests' = Append(requests, c)
    /\ clientPC' = [clientPC EXCEPT ![c] = "waiting"]
    /\ UNCHANGED <<remaining, booked, workerPC, reply, result>>

Dispatch ==
    /\ Len(requests) > 0
    /\ LET c == Head(requests) IN
           /\ workerPC[c] = "idle"
           /\ workerPC' = [workerPC EXCEPT ![c] = "check"]
    /\ requests' = Tail(requests)
    /\ UNCHANGED <<remaining, booked, clientPC, reply, result>>

\* In the code, Check runs without suspension until the audit await or reply.
\* A rejected request publishes its reply in this same atomic action.
Check(c) ==
    /\ workerPC[c] = "check"
    /\ IF remaining > 0
          THEN /\ workerPC' = [workerPC EXCEPT ![c] = "audit"]
               /\ UNCHANGED reply
          ELSE /\ workerPC' = [workerPC EXCEPT ![c] = "done"]
               /\ reply' = [reply EXCEPT ![c] = "full"]
    /\ UNCHANGED <<remaining, booked, requests, clientPC, result>>

\* Completion of the audit resumes the task, which commits and publishes
\* without another await. No explicit audit log: only its suspension matters.
Commit(c) ==
    /\ workerPC[c] = "audit"
    /\ IF ~Fixed \/ remaining > 0
          THEN /\ remaining' = remaining - 1
               /\ booked' = booked \cup {c}
               /\ reply' = [reply EXCEPT ![c] = "ok"]
          ELSE /\ UNCHANGED <<remaining, booked>>
               /\ reply' = [reply EXCEPT ![c] = "full"]
    /\ workerPC' = [workerPC EXCEPT ![c] = "done"]
    /\ UNCHANGED <<requests, clientPC, result>>

Receive(c) ==
    /\ clientPC[c] = "waiting"
    /\ reply[c] # "empty"
    /\ result' = [result EXCEPT ![c] = reply[c]]
    /\ reply' = [reply EXCEPT ![c] = "empty"]
    /\ clientPC' = [clientPC EXCEPT ![c] = "done"]
    /\ UNCHANGED <<remaining, booked, requests, workerPC>>

Done == \A c \in Clients : clientPC[c] = "done"
\* Explicit final self-loop keeps TLC deadlock detection useful elsewhere.
Finish == Done /\ UNCHANGED vars
Next == Dispatch \/ (\E c \in Clients :
           Send(c) \/ Check(c) \/ Commit(c) \/ Receive(c)) \/ Finish
Spec == Init /\ [][Next]_vars

TypeOK ==
    /\ remaining \in (-Cardinality(Clients))..Capacity
    /\ booked \subseteq Clients
    /\ requests \in Seq(Clients)
    /\ Len(requests) <= Cardinality(Clients)
    /\ clientPC \in [Clients -> {"ready", "waiting", "done"}]
    /\ workerPC \in [Clients -> {"idle", "check", "audit", "done"}]
    /\ reply \in [Clients -> {"empty", "ok", "full"}]
    /\ result \in [Clients -> {"none", "ok", "full"}]
NoOversell == Cardinality(booked) <= Capacity
StockNonnegative == remaining >= 0
Accounting == remaining + Cardinality(booked) = Capacity
ReplySound == \A c \in Clients :
    (reply[c] = "ok" \/ result[c] = "ok") => c \in booked
FullWhenExhausted == \A c \in Clients :
    (reply[c] = "full" \/ result[c] = "full") => remaining <= 0

\* Optional extension. Assumes dispatch, audit completion and each client
\* eventually run when continuously enabled. No failures or retries.
FairSpec == Spec /\ WF_vars(Dispatch)
    /\ \A c \in Clients :
           WF_vars(Send(c)) /\ WF_vars(Check(c))
           /\ WF_vars(Commit(c)) /\ WF_vars(Receive(c))
AllReplied == <>Done
=============================================================================
