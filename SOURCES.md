# Sources and provenance

All example code, models and teaching prose in this pack are authored for this workshop. The concurrency scenario is a standard check-then-act pattern, not an empirical ranking of bug frequency.

- Python asyncio synchronization primitives: https://docs.python.org/3/library/asyncio-sync.html
- Python asyncio queues: https://docs.python.org/3/library/asyncio-queue.html
- Python asyncio tasks and scheduling: https://docs.python.org/3/library/asyncio-task.html
- TLA+ tools command-line documentation: https://github.com/tlaplus/tlaplus/blob/master/USE.md
- Pinned tools release: https://github.com/tlaplus/tlaplus/releases/tag/v1.7.4
- TLA+ learning material: https://lamport.azurewebsites.net/video/videos.html
- Learn TLA+: https://learntla.com/

The model was authored directly in TLA+, not obtained by running an LLM extraction experiment. The prompt supports that workshop experiment. Evidence files record the actual Python and TLC runs performed while preparing the pack. Do not interpret the prompt or reference answer as evidence that a particular LLM reliably extracts correct models.

The TLA+ tools are third-party software. This repository does not distribute the jar; see `THIRD_PARTY_NOTICES.md`, `tools/TLA-TOOLS-LICENSE.txt`, and the release source for their licences and notices.

Workshop code and prose are original to this pack and licensed as described in `README.md`: Apache-2.0 for code and models, CC BY 4.0 for documentation and slides.
