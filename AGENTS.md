# Skills Repository Agent Guide

This repository is a collection of self-contained, installable Claude/OpenCode skills. Each subdirectory (e.g., `new-nextjs-project`, `new-jysk-pptx`) represents a single, modular skill.

---

## 1. JYSK PowerPoint Skill (`new-jysk-pptx/`)

This skill generates JYSK brand-compliant PowerPoint presentations using `python-pptx`. 

### Crucial Execution Facts (High Risk of Failure)
*   **Template Sync & Checks**: JYSK templates are updated online twice a year (mid-August and mid-February). **Always** run the template check before building or troubleshooting:
    *   *Check Online Status*: `python3 scripts/update_templates.py --check`
    *   *Sync/Download Updates*: `python3 scripts/update_templates.py --update`
*   **Verdana Font & Color Constraints**: Font must always be `Verdana`. The text color must be JYSK Dark Grey (RGB: `86, 86, 85` / `#565655`).
*   **Headlines Casing**: Titles must use **Sentence case** (*Uppercase* first letter, lowercase otherwise). Avoid ALL CAPS unless referencing JYSK product lines (e.g. *WELLPUR*).
*   **Agenda & Standard Title Sizes**: Agenda slide title must be exactly `40pt`. Standard slide title must be `28pt` bold. 

### Core Commands
*   **Generate Slides (JSON mode)**:
    ```bash
    python3 scripts/generate_jysk_pptx.py --input /path/to/slides.json
    ```
*   **Generate Slides (CLI fast mode)**:
    ```bash
    python3 scripts/generate_jysk_pptx.py --template "indoor" --title "My Title" --slides "Agenda|  - Item 1|  - Item 2"
    ```
*   **Verify/Grade Output Programmatically**:
    ```bash
    python3 scripts/grade_pptx.py <output.pptx> <grading_output.json>
    ```

---

## 2. NextJS Project Skill (`new-nextjs-project/`)

A specialized skill for scaffolding new NextJS projects.
*   Check `new-nextjs-project/SKILL.md` for conventions and version selection scripts.

---

## 3. JYSK Order Intake Skill (`new-jysk-order-intake/`)

This skill parses and structures raw JYSK IT Operations order intake requests, formats the official **Opportunity Space** template for Jira, and maps cross-departmental linked tasks.

### Crucial Execution Facts
*   **Interactive Interview First**: **DO NOT speculate or guess** the Opportunity Space details if not explicitly provided. **Proactively interview the user** with targeted questions to fill out the template fields before running the generator.
*   **The Intake Gates**:
    *   Review Stage requires signing off on the **Opportunity Space** before moving to Analysis.
    *   Analysis Stage requires signing off on the **Solution Space** before moving to Backlog.
*   **Cross-Departmental Mappings**: Tasks must be mapped to correct departments based on keywords (`IT Server`, `IT Network`, `IT Client`, `IT Stores`, `Container Platform`).

### Core Commands
*   **Process Intake Request**:
    ```bash
    python3 scripts/generate_intake.py --input /path/to/raw_intake.txt --output /path/to/jira_ready.md
    ```
*   **Verify/Grade Intake Output**:
    ```bash
    python3 scripts/grade_intake.py <norway_pax.md> <grading_output.json> <eval_id>
    ```

---

## 4. General Dependencies

If Python package issues occur, libraries can be installed using the break system packages flag:
```bash
python3 -m pip install python-pptx pyyaml --break-system-packages
```
