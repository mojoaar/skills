---
name: new-jysk-order-intake
description: Use this skill whenever the user wants to ingest, parse, process, or format JYSK IT Operations order intake requests. This skill structures requests into the 'Funnel' stage of the IT Operations Portfolio board, pre-populating JYSK's official Opportunity Space template, and mapping linked tasks to cross-departmental teams (IT Server, IT Network, IT Client, IT Stores, Container Platform).
---

# JYSK IT Operations Order Intake Skill

A specialized skill to ingest, parse, and process raw JYSK IT Operations work requests and format them into perfectly structured Jira Feature and linked Task templates ready to be placed in the **Funnel** stage of the IT Operations Portfolio Board.

## JYSK IT Operations Intake Discipline

All incoming Epics and Features on the IT Operations Portfolio Board must go through a structured intake and refinement discipline to prevent building the wrong thing or building duplicate solutions.

### Portfolio Board Stages & Gates
1.  **FUNNEL**: The entry point where an item is created in Jira and a Portfolio owner is assigned.
2.  **REVIEW**: The stage where the **Opportunity Space** is investigated and completed.
    *   *Gate*: Cannot move to Analysis until the Opportunity Space description is signed off: `Problem validated with: [Name] | [DD-MM-YYYY]`.
3.  **ANALYSIS**: The stage where the **Solution Space** is completed.
    *   *Gate*: Cannot move to Backlog until the Solution Space description is signed off: `Solution aligned with: [Name] | [DD-MM-YYYY]`.
4.  **BACKLOG**: Prioritised and ready for active delivery commitment.
5.  **IMPLEMENTATION**: Active delivery.
6.  **DONE**: Outcome documented and business benefits noted.

---

## Supported Cross-Departmental Teams

When an intake request is parsed, the skill identifies tech requirements and generates linked sub-tasks assigned to the following JYSK IT Operations departments:
*   `IT Server` (hypervisors, AD, storage, SQL, linux, VM hosting)
*   `IT Network` (routing, switches, firewalls, ports, WAN/LAN, VPN)
*   `IT Client` (MDM, Intune, laptops, desktops, deployment, Office)
*   `IT Stores` (POS registers, terminals, retail printing, backoffice, store networks)
*   `Container Platform` (Kubernetes, Docker, OpenShift, Helm, pods)

---

## Workflow: How to Process JYSK Order Intakes

### 1. Proactively Interview the User (Mandatory First Step)
To ensure the high-fidelity validation expected by JYSK IT Operations, **DO NOT guess, make up, or speculate** on any Opportunity Space placeholders. Instead, **ALWAYS conduct a short, targeted interview with the user** to extract exact real-world facts for the Opportunity Space fields.

Ask brief questions to collect:
1.  **Problem Statement**: What is broken, missing, or suboptimal? (Written as impact, using the requester's language).
2.  **Root Cause**: What is the underlying cause, not just the symptom?
3.  **Affected Stakeholders**: Who/which teams experience this pain?
4.  **Business Impact**: What is the cost of inaction (hours lost, frequency, revenue risk, operational dependency)?
5.  **In Scope / Out of Scope**: What is explicitly included vs. excluded?
6.  **Current Workarounds**: How are they coping today?
7.  **Departments Involved**: Heuristically scan the intake and ask: *"Based on your description, I suggest involving [IT Client / IT Network / IT Server / Container Platform / IT Stores]. Does this department mapping look correct?"*

### 2. Save and Run the Automatic Analyzer Script
Once the user provides the answers, save the compiled descriptions to a local text file and run the Python script:

```bash
python3 /Users/mojoaar/AI/skills/new-jysk-order-intake/scripts/generate_intake.py \
  --input /path/to/intake_description.txt \
  --output /path/to/jira_ready_output.md
```

*Note: The script heuristically parses fields (Problem statement, affected stakeholders, business impact, scope) and scans for tech keywords to automatically map linked tasks to correct departments (`IT Server`, `IT Network`, `IT Client`, `IT Stores`, `Container Platform`).*

### 3. Present Output to User
The script outputs a beautifully compiled Markdown document that contains:
*   A **Feature** ticket pre-populated with the JYSK-compliant **Opportunity Space Template** ready for copy-pasting.
*   **Linked Tasks** specifically assigned to each involved department.

Present this structured result directly to the user.
