# Offensive Simulation Modules

Safe, controlled simulation modules that emulate adversarial behavior without
causing real harm. Intended scope (see the top-level README for context):

- Credential harvesting simulation (non-malicious)
- Phishing emulation
- Web application misconfiguration checks
- Cloud IAM misconfiguration detection
- Lateral movement path mapping
- Attack path visualization

## Status

This is a scaffolding placeholder. No modules are implemented yet -- see the
top-level Contributing section if you'd like to build one out.

## Design guidelines for contributors

- Every module must be safe by default: no destructive actions, no real
  credential exfiltration, no contact with systems outside an explicit,
  user-provided scope.
- Modules should emit structured (JSON) findings that the defensive and
  AI-analysis modules can consume.
- Document any external service or network access a module requires.
