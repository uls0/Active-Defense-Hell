# HELL: Honeypot Exploitation & Lethal Logging
## Active Defense Infrastructure and Autonomous Threat Mitigation

HELL is an advanced active defense system designed for the detection, deceleration, and neutralization of adversarial network activity. It utilizes multi-layer tarpits, adaptive AI-driven analysis, and high-aggression counter-measures to mitigate threats from automated bots, human red teams, and autonomous pentesting agents.

### Core Technical Specifications

- **Adaptive AI Engine:** Integrated with Google Gemini 1.5 Flash for real-time behavioral analysis and classification of network requests.
- **Multi-Protocol Tarpits:**
    - **SMTP (Port 25):** RFC-compliant session deceleration.
    - **MySQL (Port 3306):** Authentication handshake loops and delayed response cycles.
    - **SSH/RDP/Redis:** Service-specific protocol fuzzing and connection freezing.
- **Active Counter-Measures:**
    - **Gzip Decompression Bomb:** Delivery of high-ratio compressed payloads (10GB+ expanded) to exhaust attacker system resources.
    - **Entropy Stream:** Continuous delivery of high-entropy binary data to saturate inbound bandwidth and buffer limits.
    - **JS Fork-Bomb:** Client-side execution of recursive Web Workers to exhaust CPU/RAM in browser-based tools.
- **Threat Intelligence Integration:** Automated IP address blacklisting and reporting via VirusTotal Community API.

### Infrastructure Requirements

- **Runtime:** Docker 20.10+ / Docker Compose 2.0+
- **Language:** Python 3.9 (for native monitoring)
- **Connectivity:** Outbound access to Google Cloud and VirusTotal APIs (optional).

### Deployment Protocol

1. **Initialization:**
   ```bash
   git clone https://github.com/uls0/Active-Defense-Hell.git
   cd Active-Defense-Hell
   ```

2. **Configuration:**
   Rename `.env.example` to `.env` and populate the following parameters:
   - `GEMINI_API_KEY`: Google AI Studio credential.
   - `VT_API_KEY`: VirusTotal API credential.
   - `MY_IP`: Administrator IP for whitelist bypass.

3. **Execution:**
   ```bash
   docker-compose up -d --build
   ```

4. **Audit and Monitoring:**
   Execute `python monitor_hell.py` for real-time logs and attack telemetry.

### Security Disclaimer
This software is intended for defensive security research. Operation of active counter-measures should be conducted in accordance with local legal frameworks and internal security policies. The developer assumes no liability for unauthorized or improper use.

---
**Developed by Ulises Guzman & Gemini CLI**
**Version 1.1.0-Gold**
