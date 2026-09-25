# asr

Canonical local-first ASR capability for Heimgewebe.

This repository owns the reusable speech-to-text authority: engine routing,
transcript contracts, engine/model policy, local runtime setup semantics and
benchmark evidence. It does **not** own a particular host, audio device or
digitization workflow.

## Authority boundary

- **asr** owns `audio.transcribe`, authority `heimgewebe_asr_open_engine`,
  transcript/route contracts, engine policy and benchmark semantics.
- **heim-pc** owns host-local discovery/projection: its operator-entry tells
  consumers where the capability is installed on that host. It may keep a
  compatibility wrapper, but it is not the ASR semantic authority.
- **digitalisierer** consumes `audio.transcribe` and owns transcription
  workflow, TXT/JSON/SRT/VTT export, review and provenance. It does not own
  model routing, model caches or ASR runtime installation.
- **audio** remains the Heim-PC audio/hardware configuration repository; it is
  not the speech-to-text authority.

The machine-readable authority declaration is
[`manifest/asr-capability.v1.json`](manifest/asr-capability.v1.json).

## Contracts

The public v1 wire identities are:

- `heimgewebe.asr-transcript`
- `heimgewebe.asr-route-result`
- `heimgewebe.asr-dual-local-evidence`
- `heimgewebe.asr-golden-corpus-contract`

Unavailable language, timestamps and speakers remain null/empty rather than
being invented. The current transcript contract does not expose confidence.

## Runtime policy

The default path is local-only and zero incremental cost. The current quality
default is faster-whisper `large-v3`, with Qwen as local quality fallback and
Parakeet as the speed/low-VRAM comparator. Automatic cloud escalation is
forbidden. Metered cloud adapters remain representable only behind explicit
per-run authorization; consumers may impose stricter policy.

Runtime state and model caches live outside Git:

- `~/.local/state/heimgewebe/asr/`
- `~/.local/cache/heimgewebe/asr/`

There must be one cache/runtime authority per host. Host migrations move or
alias existing state; they do not create a second model cache.

## CLI

```bash
python3 scripts/asr_engine.py doctor
python3 scripts/asr_engine.py route --audio /path/to/audio.m4a --json
python3 scripts/asr_engine.py transcribe --audio /path/to/audio.m4a
```

See [architecture/asr-engine.md](architecture/asr-engine.md),
[architecture/authority-boundary.md](architecture/authority-boundary.md) and
[runbooks/asr-local-transcription.md](runbooks/asr-local-transcription.md).

## Provenance

The initial capability extraction was reconstructed from
`heimgewebe/heim-pc` main at
`549f8896476f266c1b50d77c2db8423f94a377bf`. Host-local installation and
locator changes are intentionally performed separately so the capability can be
reviewed without silently mutating runtime state.

## Validation

```bash
python3 -m pytest -q
python3 -m compileall -q scripts tests
```
