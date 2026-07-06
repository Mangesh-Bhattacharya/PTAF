# Purple Team Automation Framework (PTAF)

**AI-Driven Offensive + Defensive Security Automation for Mid-Level Practitioners**

Author: [Mangesh Bhattacharya](https://github.com/Mangesh-Bhattacharya) — Cybersecurity Practitioner | MITS-AI Graduate (Ontario Tech University) | Threat Intelligence & Automation

---

## Project Vision

PTAF is a free, open-source Purple Team automation framework built to help mid-level cybersecurity practitioners simulate real-world adversarial behavior, strengthen defensive controls, and accelerate security engineering workflows.

It is designed to run on Kali Linux, Ubuntu, and cloud shells, enabling practitioners to:

- Execute safe, controlled offensive simulations
- Automatically map defensive gaps
- Generate remediation guidance
- Produce Purple Team reports
- Collaborate with contributors from across the security community

The long-term goal is to make PTAF a practical, well-documented Purple Team automation toolkit for defenders, SOC analysts, threat hunters, and aspiring security engineers.

## Core Capabilities

### 1. Offensive Simulation Modules (Safe & Controlled)

- Credential harvesting simulation (non-malicious)
- Phishing emulation
- Web application misconfiguration checks
- Cloud IAM misconfiguration detection
- Lateral movement path mapping
- Attack path visualization

### 2. Defensive Automation Modules

- Log correlation (SIEM-agnostic)
- MITRE ATT&CK mapping
- Alert quality scoring
- Detection gap identification
- Automated defensive recommendations
- Purple Team report generation (PDF/Markdown)

### 3. AI-Driven Analysis

- Threat pattern clustering
- Behavioral anomaly detection
- Automated defensive tuning suggestions
- Attack replay analysis

### 4. Collaboration Features

- Modular plugin system
- Clear contribution guidelines
- Issue templates for new modules
- Community roadmap
- Periodic "Purple Team Challenges" for contributors

## Technical Requirements

- **Language:** Python
- **OS:** Kali Linux, Ubuntu, Windows Subsystem for Linux
- **Dependencies:** Open-source libraries only
- **Architecture:** Modular, agent-based
- **Output formats:** JSON, Markdown, PDF
- **Integrations:** Sysmon, Suricata, Zeek, Sigma rules, MITRE ATT&CK

## Community & Collaboration

PTAF aims to be a collaboration point for SOC analysts, threat hunters, red teamers, blue teamers, purple teamers, and AI-security researchers.

Contributors are encouraged to:

- Add new modules
- Improve detection logic
- Submit Purple Team exercises
- Share defensive tuning strategies

## Installation (Kali Linux)

```bash
git clone https://github.com/Mangesh-Bhattacharya/PTAF.git
cd PTAF
sudo chmod +x install.sh
./install.sh
```

## Usage Example

```bash
ptaf --simulate lateral_movement --analyze --report
```

> Note: PTAF is in early scaffolding. Modules above describe the intended architecture and are being implemented incrementally — see [Contributing](#contributing) to help build them out.

## Repository Structure

```
PTAF/
├── install.sh              # Setup script
├── requirements.txt        # Python dependencies
├── modules/
│   ├── offensive/          # Safe, controlled simulation modules
│   ├── defensive/          # Detection & defensive automation modules
│   └── ai_analysis/        # AI-driven analysis plugins
└── docs/                   # Documentation and Purple Team exercises
```

## Contributing

Contributions are welcome, including:

- New attack simulation modules
- New defensive detection logic
- New AI-analysis plugins
- Documentation improvements
- Purple Team exercises

Open an issue or submit a pull request to get involved.

## About the Author

Mangesh Bhattacharya is a cybersecurity practitioner and Master's student in Complex Networks / AI-Security (MITS, Ontario Tech University), building AI-driven security automation tools including [CyberSentinel-AI](https://github.com/Mangesh-Bhattacharya/CyberSentinel-AI) and [AI-Automated-Security-Engineer](https://github.com/Mangesh-Bhattacharya/AI-Automated-Security-Engineer).

## License

Released under the [MIT License](LICENSE).
