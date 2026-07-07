"""Sanity tests for the offensive simulation scaffolding.

These only verify the *safety contract* and output shape -- that running a
technique never raises, never claims to have contacted a real system, and
always returns a well-formed Finding. They are not a substitute for real
technique-specific tests once modules/offensive gains real implementations.
"""

from modules.offensive.emulation import (
    Finding,
    REGISTRY,
    SimulationScope,
    run_all,
    run_technique,
)


def test_registry_is_not_empty():
    assert len(REGISTRY) > 0


def test_run_all_returns_a_finding_per_registered_technique():
    findings = run_all()
    assert len(findings) == len(REGISTRY)
    for finding in findings:
        assert isinstance(finding, Finding)
        assert finding.status in {"simulated", "skipped", "error"}


def test_every_finding_declares_a_technique_id_and_tactic():
    for finding in run_all():
        assert finding.technique_id
        assert finding.tactic


def test_unknown_technique_id_returns_error_status_not_an_exception():
    finding = run_technique("T9999-does-not-exist")
    assert finding.status == "error"


def test_default_scope_is_local_only():
    scope = SimulationScope()
    assert scope.allow_network is False
    assert scope.label == "local-only"


def test_finding_serializes_to_json():
    finding = run_all()[0]
    payload = finding.to_json()
    assert finding.technique_id in payload
