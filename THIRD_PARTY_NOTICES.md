# Third-party notices

## TLA+ tools

This repository does not distribute `tla2tools.jar`. The pinned tools release
is v1.7.4 (TLC 2.19, 8 August 2024), from
<https://github.com/tlaplus/tlaplus/releases/tag/v1.7.4>. The Nix development
shell provides the jar from nixpkgs `tlaplus` 1.7.4; without Nix, `SETUP.md`
downloads it.

The upstream jar contains:

- Microsoft Research code under the MIT License, reproduced in
  `tools/TLA-TOOLS-LICENSE.txt`.
- JavaMail 1.6.3 classes and related `javax` classes. The jar carries the
  Eclipse Public License 2.0 text at `META-INF/LICENSE.txt`.

The upstream artifact is used unmodified. If you redistribute the jar, retain
the license texts inside it and check the artifact hash recorded in
`tools/TLC-SHA256.txt`.

SHA-256:
`936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`

## Workshop material

The Python, TLA+, prose, and slide content in this repository is original to
the workshop; `SOURCES.md` records the external references used.
