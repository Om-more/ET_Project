<p align="center">
  <img width="1200" height="675" alt="banner" src="https://github.com/user-attachments/assets/817bf006-67a1-4c8b-80c3-598e90569269" /><img width="2105" height="644" alt="architecture-diagram" src="https://github.com/user-attachments/assets/15ce2554-9104-48f8-932d-3e89e83326ce" />
 
</p>
App Link: https://etproject-qbxhm67rw8famf7e7nknvd.streamlit.app/
<h1 align="center">MAPAO</h1>
<p align="center"><b>Multi-Agent Predictive Attribution &amp; Orchestration for Cyber Resilience</b></p>
<p align="center">An AI-powered, human-in-the-loop cyber resilience platform for Critical National Infrastructure —
correlating raw telemetry into attack episodes, attributing them to MITRE ATT&amp;CK techniques, predicting the
adversary's next move, and triggering graded, auditable containment.</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-hackathon%20prototype-1E2761?style=for-the-badge" alt="status"/>
  <img src="https://img.shields.io/badge/license-MIT-00A9B5?style=for-the-badge" alt="license"/>
  <img src="https://img.shields.io/badge/python-3.10+-1E2761?style=for-the-badge&logo=python&logoColor=white" alt="python"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-backend-009688?style=flat-square&logo=fastapi&logoColor=white" alt="fastapi"/>
  <img src="https://img.shields.io/badge/Streamlit-SOC%20dashboard-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="streamlit"/>
  <img src="https://img.shields.io/badge/XGBoost-TTP%20classification-1E2761?style=flat-square" alt="xgboost"/>
  <img src="https://img.shields.io/badge/LSTM-next--step%20prediction-4FD8DE?style=flat-square" alt="lstm"/>
  <img src="https://img.shields.io/badge/Isolation%20Forest-anomaly%20detection-00A9B5?style=flat-square" alt="isolation-forest"/>
  <img src="https://img.shields.io/badge/Groq-AI%20reasoning-F55036?style=flat-square" alt="groq"/>
  <img src="https://img.shields.io/badge/MITRE%20ATT%26CK-technique%20mapping-1E2761?style=flat-square" alt="mitre"/>
  <img src="https://img.shields.io/badge/CICIDS2017-dataset-5B6478?style=flat-square" alt="cicids"/>
</p>

<p align="center">
  <a href="#overview">Overview</a> ·
  <a href="#the-problem">The Problem</a> ·
  <a href="#why-this-segment">Why This Segment</a> ·
  <a href="#system-architecture">Architecture</a> ·
  <a href="#layer-by-layer-breakdown">Layers</a> ·
  <a href="#live-system-demonstration">Live Demo</a> ·
  <a href="#tech-stack">Tech Stack</a> ·
  <a href="#getting-started">Getting Started</a> ·
  <a href="#roadmap">Roadmap</a> ·
  <a href="#license">License</a>
</p>

---

## Overview

**MAPAO** (*MITRE-Aware Predictive Autonomous Orchestrator*) is a research prototype built for the **AI-Powered
Cyber Resilience Platform** challenge track, scoped specifically to two connected capabilities:

1. **APT Campaign Attribution & Prediction** — once suspicious activity is observed, map it against the MITRE
   ATT&CK framework to identify which known technique or campaign it resembles, and predict the attacker's
   likely next step.
2. **A lightweight Autonomous Orchestrator** — once a technique is identified with sufficient confidence,
   trigger a pre-approved, low-risk containment action automatically, with a human-approval gate for anything
   higher-impact.

Attribution and orchestration are naturally sequential — attribution tells you *what is happening*, orchestration
decides *what to do about it*. MAPAO treats the hand-off between the two as a first-class architectural boundary
rather than two disconnected tools glued together after the fact.

## The Problem

India's public institutions and critical infrastructure are under sustained attack. CERT-In handled over
**1.59 million** cybersecurity incidents in 2023 alone, a number that kept climbing through 2024–25. Real incidents
show the cost — AIIMS Delhi was paralysed for over two weeks by ransomware in 2022, and CBSE suffered a data breach
in 2024 followed by a coordinated attack on its exam infrastructure in early 2026.

Over **70%** of government IT infrastructure runs on end-of-life systems, giving attackers easy entry points. But
the deeper failure is *speed*: breaches are typically discovered **weeks to months** after the attacker first got
in — long after Advanced Persistent Threats (APTs) have moved through a network using slow, deliberately quiet
techniques designed to blend in with normal activity.

## Why This Segment

We chose the attribution + orchestration pairing over the other illustrative directions (raw behavioural anomaly
detection, vulnerability prioritisation, security digital twins) for three reasons:

- It maps most directly onto the challenge statement's own verbs — *"maps attack progression"* and *"orchestrates
  containment actions."*
- It's buildable end-to-end in a short timeframe using the public MITRE ATT&CK knowledge base and
  synthetic attack-sequence data, without requiring live production telemetry.
- Attribution and orchestration are naturally sequential, so together they form one coherent pipeline rather than
  two disconnected builds.

The system assumes an alert or suspicious log sequence as input, and focuses on what happens next: **identification
and response** — not full-scale UEBA-style behavioural detection.

### The gap this project targets

A review of existing approaches — statistical/clustering attribution, Bayesian sequence models, threat-intel graph
fusion, rule-based SOAR, and agentic AI response — surfaces three consistent gaps:

| # | Gap | MAPAO's answer |
|---|---|---|
| 1 | Attribution research is validated on static, historical benchmarks — real-time drift is unproven | Episode & Memory + Learning & Governance layers keep a rolling narrative and recalibrate against live outcomes |
| 2 | No credible system removes the human approval gate for high-impact, irreversible actions | The Response Layer structurally requires human sign-off above a risk threshold — not an afterthought |
| 3 | Attribution and orchestration are rarely studied as one connected pipeline | MAPAO is one pipeline with a shared *episode* object — the hand-off is an explicit architectural contract |

## System Architecture

MAPAO is a human-in-the-loop autonomous defense pipeline that converts raw security telemetry into **episodes**,
maps those episodes to MITRE ATT&CK tactics and techniques, predicts the attacker's likely next move, and triggers
approved containment actions once confidence crosses a defined threshold.

<p align="center">
  <img width="1366" height="768" alt="dashboard-screenshot" src="https://github.com/user-attachments/assets/0d8f8c2c-3282-4347-ae60-14ae83507696" />
<img width="2105" height="644" alt="architecture-diagram" src="https://github.com/user-attachments/assets/ffbafde7-b67e-44fd-9801-9a9174816015" />

</p>

<p align="center"><i>Left-to-right, five-layer flow — from raw telemetry ingestion through to governance and feedback.</i></p>

## Layer-by-Layer Breakdown

### 1 · Telemetry Layer
The ingestion boundary of the system. Pulls in endpoint logs, network flows, authentication logs, DNS records,
email metadata, CMDB context, and OT/ICS event streams, then runs them through a streaming collector, parser,
normalisation step, time alignment, and a trust-scoring pass. Output: a **standardised security event** — a
common schema every downstream layer can consume.

### 2 · Episode & Memory Layer
Individual events are rarely meaningful in isolation; APT activity is defined by slow, related sequences. This
layer's event-to-episode builder groups related events into incident windows, an episodic memory stores recent
narratives and prior outcomes, and a lightweight knowledge store links entities, time, and context across
episodes — giving the system continuity across a slow-moving attack.

### 3 · Intelligence Layer
Where attribution and prediction happen, via four cooperating agents:

- **TTP Mapper Agent** — maps an episode to MITRE ATT&CK tactics and techniques.
- **Predictive Planner Agent** — forecasts the attacker's likely next-stage move.
- **Causal Affordance Agent** — selects which response options are actually feasible given current network topology.
- **Risk Scorer** — combines attribution confidence, blast radius, and asset criticality into a single confidence score.

Together, these agents produce the **technique ID + confidence score** — the explicit hand-off object that closes
the attribution–orchestration gap.

### 4 · Response Layer
The SOAR Orchestrator executes pre-approved actions — isolate host, revoke token, block IP, snapshot VM, disable
account — once confidence clears the autonomous-action threshold. Anything above that threshold routes to a
**human approval gate** before execution. Every automated step, gated or not, is wrapped in rollback capability
and audit logging.

### 5 · Learning & Governance Layer
Closes the loop rather than treating deployment as a one-time event. Analyst feedback, incident outcomes, and
playbook success/failure rates feed back into model updates, threshold calibration, and policy refinement.
Role-based access control, explainability reports, and compliance logs sit alongside this feedback loop, so
recalibration is auditable rather than opaque.

### Illustrative demo flow

1. Simulate login anomalies and suspicious process behaviour as input telemetry.
2. The Episode & Memory Layer groups these events into a probable intrusion chain.
3. The TTP Mapper Agent tags the chain with the relevant ATT&CK stages.
4. The Predictive Planner Agent forecasts likely lateral movement as the probable next step.
5. The SOAR Orchestrator isolates the affected host and revokes credentials once the Risk Scorer's confidence
   threshold is met.
6. A dashboard surfaces the explainable reasoning behind the action and its rollback status.

## Live System Demonstration

<p align="center">
  <img width="1366" height="768" alt="dashboard-screenshot" src="https://github.com/user-attachments/assets/31c9a247-b8d7-4489-be81-838b9e993ccf" />
</p>

<p align="center"><i>Event Feed → AI Reasoning → SOAR Control, running end-to-end. Here the system matches a
simulated episode to <b>T1563.001 (SSH Hijacking)</b> with a 0.49 confidence score, and routes the decision to
the Analyst Queue since it falls short of the autonomous-action threshold.</i></p>

## Current Scope

App Link: https://etproject-qbxhm67rw8famf7e7nknvd.streamlit.app/

The implemented system is capable of:

- Detecting anomalous behaviour
- Building attack episodes instead of isolated alerts
- Mapping incidents to MITRE ATT&CK techniques
- Predicting probable attacker progression
- Calculating contextual risk
- Simulating automated containment actions
- Providing explainable AI-assisted recommendations
- Maintaining analyst feedback for future improvements

## Tech Stack

| Layer | Technologies |
|---|---|
| **Backend API** | FastAPI |
| **SOC Dashboard** | Streamlit |
| **Anomaly Detection** | Isolation Forest (scikit-learn) |
| **TTP Classification** | XGBoost |
| **Next-Step Attack Prediction** | LSTM sequence model |
| **AI Reasoning** | Groq-powered planner (explanations, incident summaries, containment recommendations, executive reports) |
| **Knowledge Base** | MITRE ATT&CK |
| **Training Data** | CICIDS2017 (preprocessed via an automated dataset loader) |
| **Testing** | Automated test suite, end-to-end execution pipeline |

## Getting Started

> Prototype quick-start — adjust paths/entry points to match your local checkout.

```bash
# 1. Clone the repository
git clone https://github.com/<your-org>/mapao.git
cd mapao

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Train / load models (first run only)
python scripts/train_models.py

# 5. Start the FastAPI backend
uvicorn app.main:app --reload --port 8000

# 6. In a second terminal, launch the SOC dashboard
streamlit run dashboard/app.py
```

Then load a sample event file (e.g. `data/raw/sample_events.json`) from the **Event Feed** panel to build an
episode and watch it flow through attribution, risk scoring, and the SOAR gate.

## Project Structure

```
mapao/
├── app/                  # FastAPI backend
│   ├── ingestion/         # Telemetry collectors, parsers, normalisation
│   ├── episodes/          # Episode Builder & Episodic Memory
│   ├── intelligence/       # TTP Mapper, Predictive Planner, Causal Affordance, Risk Scorer
│   ├── response/          # SOAR Orchestrator, approval gate, rollback & audit logging
│   └── governance/         # Feedback loop, threshold calibration, RBAC
├── models/                # Serialized ML models (Isolation Forest, XGBoost, LSTM)
├── dashboard/             # Streamlit SOC dashboard
├── data/                  # Datasets & sample event feeds
├── scripts/               # Training, evaluation, and data pipelines
└── tests/                 # Automated test suite
```

## Roadmap

### Short-term
- **Additional datasets** — CICIDS2018, UNSW-NB15, CSE-CIC-IDS2018, TON_IoT, Edge-IIoT, DARPA Intrusion Evaluation
- **Advanced models** — Graph Neural Networks, Transformer-based sequence prediction, autoencoder anomaly detection, Temporal Graph Networks, Bayesian risk estimation
- **Threat intelligence** — CVE/NVD sync, STIX/TAXII live feeds, VirusTotal enrichment, OpenCTI integration
- **Response automation** — Microsoft Sentinel, Splunk Enterprise Security, IBM QRadar, Elastic Security

### Research extensions
- **Adaptive learning** — continual learning from analyst feedback, online model updates, active learning
- **Multi-agent collaboration** — distributed autonomous cyber-defense agents, federated security intelligence
- **Predictive cyber resilience** — dynamic attack graph generation, resilience scoring of critical assets
- **Explainable AI** — human-interpretable risk scoring, transparent decision fusion

### Enterprise deployment
Kubernetes · Dockerized microservices · Kafka streaming · Redis caching · PostgreSQL/Neo4j · multi-tenancy · RBAC ·
high availability · horizontal scaling · cloud-native monitoring

### Version milestones

| Version | Milestone |
|---|---|
| **v1.0** | Hackathon prototype with episode-based detection, ML models, MITRE mapping, dashboard, and SOAR simulation |
| **v1.5** | Improved datasets, better model performance, enhanced visualizations, comprehensive testing |
| **v2.0** | Real-time streaming architecture with Kafka, SIEM integration, and cloud deployment |
| **v3.0** | Multi-agent autonomous cyber defense with graph intelligence, continual learning, enterprise-grade orchestration |
| **v4.0** | Production-ready AI cyber resilience platform for critical infrastructure with predictive defense and scalable cloud-native deployment |

## Contributing

Issues and pull requests are welcome. Please open an issue first to discuss significant changes, and make sure
new modules stay within the layer boundaries described in [System Architecture](#system-architecture) so the
attribution → orchestration contract stays intact.

## License

Released under the [MIT License](LICENSE).

---

<p align="center"><sub>MAPAO — Multi-Agent Predictive Attribution &amp; Orchestration for Cyber Resilience.</sub></p>
