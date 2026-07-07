"""Adversary emulation scaffolding for PTAF's offensive simulation module.

IMPORTANT -- SAFETY MODEL
--------------------------
Every "technique" in this file is a *simulation*: it logs a structured
finding describing what a real adversary action would have done, and does
NOT perform any real credential harvesting, exploitation, lateral movement,
or contact with any system other than the local machine running PTAF. This
mirrors the safety model described in CONTRIBUTING.md and modules/offensive
/README.md.

This module is scaffolding, not a finished product: it defines the
interface real technique implementations should follow, plus a couple of
fully-simulated examples so the shape is concrete. Real, safe
implementations (e.g. actually checking for a known-bad IAM policy in an
account you own) are welcome via PRs that keep to this safety model.
"""

from __future__ import annotations

import json
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("ptaf.offensive")


@dataclass
class Finding:
    """A single, structured result emitted by a simulated technique.

    Findings are the hand-off point to the defensive and AI-analysis
    modules -- keep this shape stable.
    """

    technique_id: str
    technique_name: str
    tactic: str
    status: str  # "simulated" | "skipped" | "error"
    summary: str
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    run_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_json(self) -> str:
        return json.dumps(self.__dict__, indent=2, default=str)


class Technique:
    """Base class every simulated technique should subclass.

    Subclasses must set technique_id, technique_name and tactic
    (see attack_techniques.yaml for reference IDs) and implement the
    simulate() method below.
    """

    technique_id: str = "T0000"
    technique_name: str = "Unnamed Technique"
    tactic: str = "Unknown"

    def simulate(self, scope: "SimulationScope") -> Finding:
        raise NotImplementedError


@dataclass
class SimulationScope:
    """Explicit, user-provided scope for a simulation run.

    Nothing in this module should ever act outside of what's declared here.
    The default scope only ever refers to the local machine.
    """

    label: str = "local-only"
    allow_network: bool = False
    notes: str = ""


class CredentialHarvestingSimulation(Technique):
    """Non-malicious simulation of T1110-style credential access.

    This does NOT attempt to harvest, guess, or use any real credential.
    It only demonstrates the finding shape a real (safe, scoped) check
    would produce, e.g. "would have flagged accounts with no MFA".
    """

    technique_id = "T1110"
    technique_name = "Brute Force (simulated)"
    tactic = "Credential Access"

    def simulate(self, scope: SimulationScope) -> Finding:
        logger.info("Simulating %s in scope=%s", self.technique_id, scope.label)
        return Finding(
            technique_id=self.technique_id,
            technique_name=self.technique_name,
            tactic=self.tactic,
            status="simulated",
            summary=(
                "No real credential access attempted. This is a placeholder "
                "finding demonstrating the output shape a real, scoped "
                "check (e.g. 'accounts without MFA') would produce."
            ),
            details={"scope": scope.label, "accounts_checked": 0},
        )


class LateralMovementPathMapping(Technique):
    """Simulated T1021 lateral-movement path mapping.

    Produces an example attack-path graph structure from static, made-up
    data -- it does not scan or connect to any real host.
    """

    technique_id = "T1021"
    technique_name = "Remote Services (path mapping, simulated)"
    tactic = "Lateral Movement"

    def simulate(self, scope: SimulationScope) -> Finding:
        logger.info("Simulating %s in scope=%s", self.technique_id, scope.label)
        example_path = [
            {"node": "workstation-01", "edge": "RDP (example)"},
            {"node": "jump-host-01", "edge": "SSH (example)"},
            {"node": "domain-controller-01", "edge": None},
        ]
        return Finding(
            technique_id=self.technique_id,
            technique_name=self.technique_name,
            tactic=self.tactic,
            status="simulated",
            summary="Example attack-path graph for visualization -- static demo data.",
            details={"scope": scope.label, "path": example_path},
        )


REGISTRY: dict[str, type[Technique]] = {
    CredentialHarvestingSimulation.technique_id: CredentialHarvestingSimulation,
    LateralMovementPathMapping.technique_id: LateralMovementPathMapping,
}


def run_technique(technique_id: str, scope: SimulationScope | None = None) -> Finding:
    """Look up and run a single simulated technique by ATT&CK ID."""
    scope = scope or SimulationScope()
    technique_cls = REGISTRY.get(technique_id)
    if technique_cls is None:
        return Finding(
            technique_id=technique_id,
            technique_name="Unknown",
            tactic="Unknown",
            status="error",
            summary="No registered technique for id=" + repr(technique_id) + ".",
        )
    return technique_cls().simulate(scope)


def run_all(scope: SimulationScope | None = None) -> list[Finding]:
    """Run every registered technique and return their findings."""
    scope = scope or SimulationScope()
    return [technique_cls().simulate(scope) for technique_cls in REGISTRY.values()]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    for finding in run_all():
        print(finding.to_json())
