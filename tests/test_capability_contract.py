import json
from pathlib import Path


ROOT = Path(__file__).parent.parent
CAPABILITY = ROOT / "manifest" / "asr-capability.v1.json"


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_capability_contract_binds_authority_and_wire_contracts() -> None:
    capability = _load(CAPABILITY)
    transcript_path = ROOT / str(capability["transcript_contract"])
    policy_path = ROOT / str(capability["engine_policy"])
    golden_path = ROOT / str(capability["golden_corpus_contract"])

    transcript = _load(transcript_path)
    policy = _load(policy_path)

    assert capability["capability"] == "audio.transcribe"
    assert capability["authority"] == "heimgewebe_asr_open_engine"
    assert capability["authority_kind"] == "capability_authority"
    assert capability["policy_resolution"] == "read_at_execution_time"
    assert capability["consumer_engine_pinning_allowed"] is False
    assert capability["automatic_cloud_escalation_allowed"] is False
    assert capability["metered_cloud_requires_explicit_per_run_opt_in"] is True

    assert capability["transcript_kind"] == transcript["kind"]
    assert capability["transcript_kind"] == "heimgewebe.asr-transcript"
    assert capability["route_result_kind"] == "heimgewebe.asr-route-result"
    assert policy["routing"]["default_strategy"] == "local-first"
    assert policy["routing"]["automatic_cloud_escalation"] is False
    assert policy["invariants"]["default_path_local_inference_only"] is True
    assert policy["invariants"]["metered_cloud_requires_explicit_per_run_opt_in"] is True

    assert (ROOT / str(capability["entrypoint"])).is_file()
    assert transcript_path.is_file()
    assert policy_path.is_file()
    assert golden_path.is_file()


def test_runbook_uses_generic_authority_contract() -> None:
    runbook = (ROOT / "runbooks/asr-local-transcription.md").read_text(encoding="utf-8")
    assert "heimgewebe_asr_open_engine" in runbook
    assert "heim_pc_asr_open_engine" not in runbook
    assert "manifest/asr-capability.v1.json" in runbook
    assert "manifest/operator-entry.v1.json" not in runbook


def test_golden_privacy_docs_bind_generic_asr_repository() -> None:
    architecture = (ROOT / "architecture/asr-golden-corpus.md").read_text(encoding="utf-8")
    assert "innerhalb des ASR-Repositories" in architecture
    assert "innerhalb des Heim-PC-Repositories" not in architecture
