# Security Policy

## Supported versions

PTAF is pre-1.0 and under active scaffolding. Security fixes are made
against the `main` branch only until a versioned release process exists.

| Version | Supported |
| ------- | --------- |
| main    | ✅ |

## Reporting a vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities.

Instead, report it privately:

- Use GitHub's [private vulnerability reporting](../../security/advisories/new)
  for this repository (Security tab -> "Report a vulnerability"), or
- Open a draft security advisory if the option above is unavailable.

Please include:

- A description of the issue and its potential impact
- Steps to reproduce (proof-of-concept code, if applicable)
- Affected module(s) / file(s) / commit
- Any suggested remediation, if you have one

## What to expect

- Acknowledgement of your report as soon as possible.
- An assessment of severity and an estimated timeline for a fix.
- Credit in the fix's release notes, if you'd like it (optional).

## Scope notes specific to PTAF

Because PTAF includes offensive-simulation scaffolding, two categories of
"security issue" are especially relevant and should be reported the same
way as a normal vulnerability:

1. **A module behaves in a way that isn't safe-by-default** -- e.g. it
   could exfiltrate real credentials, contact systems outside an explicit
   user-provided scope, or otherwise cause real-world harm rather than a
   controlled simulation.
2. **A detection/defensive module produces misleading results** in a way
   that could cause a real detection gap (e.g. a Sigma rule with a logic
   error that silently never fires).

## Responsible disclosure

We ask that you give us a reasonable opportunity to fix an issue before any
public disclosure, and that you avoid accessing or modifying data that
isn't yours while investigating a report.
