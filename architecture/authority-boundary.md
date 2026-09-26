# ASR authority boundary

## Decision

`heimgewebe/asr` is the canonical semantic authority for the
`audio.transcribe` capability.

The authority identifier is `heimgewebe_asr_open_engine`.

## Ownership

### asr

Owns:

- engine/model registry and routing policy;
- local runtime setup rules;
- transcript and route-result contracts;
- local-first/cloud-escalation invariants;
- golden-corpus and benchmark semantics;
- the canonical ASR CLI.

Does not own:

- which host currently provides the capability;
- host hardware truth;
- digitization workflow/export;
- audio-device routing.

### heim-pc

Owns:

- host-local capability location and installation projection;
- host/runtime observation;
- compatibility entrypoints during migration;
- host-specific deployment and cache migration.

It must not fork ASR policy, transcript contracts or engine routing.

### digitalisierer

Owns:

- media-to-transcript workflow;
- local-only consumer policy;
- domain mapping;
- TXT/JSON/SRT/VTT publication;
- source/output provenance and human review.

It must not install or route ASR engines.

## One runtime, one cache

Moving the authority out of `heim-pc` must not duplicate model weights or
virtual environments. The host cutover migrates the existing
`~/.local/cache/heim-pc/asr-open-engine` tree to
`~/.local/cache/heimgewebe/asr` (or establishes a compatibility alias) before
the canonical locator changes.

## Compatibility

The historical `heim-pc.asr-*` wire identities are superseded by
`heimgewebe.asr-*`. During the cutover, host wrappers may preserve the old
entrypoint path, but new consumers bind only to the generic authority and
generic wire contracts.

## Migration source

The initial extraction is based on `heimgewebe/heim-pc` main commit
`549f8896476f266c1b50d77c2db8423f94a377bf`.
