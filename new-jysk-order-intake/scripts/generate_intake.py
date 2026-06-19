import os
import re
import sys
import json
import argparse
from datetime import datetime

# JYSK IT Operations Department Mapping
DEPARTMENTS = {
    "IT Server": ["server", "vmware", "hypervisor", "storage", "san", "backup", "datacenter", "database", "sql", "linux", "windows", "ad", "active directory"],
    "IT Network": ["network", "switch", "router", "firewall", "vlan", "vpn", "dns", "wifi", "bandwidth", "wan", "lan", "routing", "port"],
    "IT Client": ["client", "laptop", "pc", "desktop", "deployment", "windows 11", "sccm", "intune", "mdm", "office", "teams", "printer"],
    "IT Stores": ["store", "register", "pos", "terminal", "receipt", "scanner", "printer", "cash", "payment", "pax", "retail", "backoffice"],
    "Container Platform": ["container", "kubernetes", "k8s", "openshift", "docker", "pod", "helm", "registry", "microservice", "namespace", "ingress"]
}

def analyze_departments(text):
    """Heuristically identifies which departments are involved based on keyword scanning."""
    involved = []
    text_lower = text.lower()
    for dept, keywords in DEPARTMENTS.items():
        matched = []
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                matched.append(kw)
        if matched:
            involved.append((dept, matched))
    return involved

def to_sentence_case(text):
    """Formats text to sentence case, preserving short uppercase acronyms."""
    if not text:
        return text
    words = text.split()
    if not words:
        return text
    first_word = words[0]
    if not (first_word.isupper() and len(first_word) > 1):
        first_word = first_word[0].upper() + first_word[1:] if len(first_word) > 1 else first_word.upper()
    return " ".join([first_word] + words[1:])

def parse_intake(raw_text):
    """Parses raw text and extracts Opportunity Space fields where possible."""
    # Attempt to extract fields based on common headers or list structures
    # We will initialize defaults
    title = ""
    problem = ""
    root_cause = "[Pending validation during Review stage]"
    stakeholders = []
    impact = "[Quantified impact pending review]"
    in_scope = []
    out_scope = ["[Pending final scoping]"]
    constraints = ["[None identified yet]"]
    workarounds = "[No current workarounds documented]"
    
    # Try to extract title from first line
    lines = [l.strip() for l in raw_text.strip().split("\n") if l.strip()]
    if lines:
        title = to_sentence_case(lines[0])
        # Clean title if it contains prefixes
        title = re.sub(r'^(title|subject|name|epic|feature):\s*', '', title, flags=re.IGNORECASE)
        
    # Standard field extraction heuristics
    text_lower = raw_text.lower()
    
    # Impact heuristic
    impact_match = re.search(r'(?:impact|business impact|cost of inaction):\s*([^\n]+)', raw_text, re.IGNORECASE)
    if impact_match:
        impact = impact_match.group(1).strip()
        
    # Problem heuristic
    problem_match = re.search(r'(?:problem|need|need statement|description):\s*([^\n]+)', raw_text, re.IGNORECASE)
    if problem_match:
        problem = problem_match.group(1).strip()
    elif len(lines) > 1:
        problem = lines[1]
        
    # Stakeholder heuristic
    stakeholder_match = re.finditer(r'(?:stakeholder|affected|users):\s*([^\n]+)', raw_text, re.IGNORECASE)
    for m in stakeholder_match:
        stakeholders.append(m.group(1).strip())
        
    # Scope heuristics
    in_scope_matches = re.finditer(r'(?:in scope|scope|features needed|deliverables):\s*([^\n]+)', raw_text, re.IGNORECASE)
    for m in in_scope_matches:
        in_scope.append(m.group(1).strip())
        
    return {
        "title": title or "New IT Operations Initiative",
        "problem": problem or raw_text.strip()[:150] + "...",
        "root_cause": root_cause,
        "stakeholders": stakeholders or ["[Requester / Business Unit]"],
        "impact": impact,
        "in_scope": in_scope or ["[Refer to problem description]"],
        "out_scope": out_scope,
        "constraints": constraints,
        "workarounds": workarounds
    }

def format_opportunity_space(fields):
    """Renders a standard JYSK Opportunity Space template with pre-populated fields."""
    today = datetime.now().strftime("%d-%m-%Y")
    
    stakeholders_md = "\n".join([f"- {s}" for s in fields["stakeholders"]])
    in_scope_md = "\n".join([f"- {s}" for s in fields["in_scope"]])
    out_scope_md = "\n".join([f"- {s}" for s in fields["out_scope"]])
    constraints_md = "\n".join([f"- {c}" for c in fields["constraints"]])
    
    return f"""## 🔍 OPPORTUNITY SPACE
*Stage: Review | Complete and sign off before moving to Analysis*

**Problem / Need statement**
> {fields["problem"]}

**Root cause**
> {fields["root_cause"]}

**Affected stakeholders**
{stakeholders_md}

**Business impact**
> {fields["impact"]}

**In scope**
{in_scope_md}

**Out of scope**
{out_scope_md}

**Regulatory or architectural constraints**
{constraints_md}

**Current workarounds**
> {fields["workarounds"]}

**Problem validated with:** [Pending Reviewer Name] | [DD-MM-YYYY]"""

def format_jira_tasks(parent_title, dept_findings):
    """Generates cross-departmental linked Jira tasks."""
    tasks = []
    for dept, matches in dept_findings:
        tasks.append({
            "title": f"[{dept}] Support for {parent_title}",
            "department": dept,
            "description": f"Evaluate and deliver departmental requirements for the feature '{parent_title}'.\n\nIdentified keywords in intake: {', '.join(matches)}\n\n**To Be Completed during Solution Space (Analysis):**\n- Core tasks involved\n- Technical solution design\n- Key dependencies and effort estimates\n- Status of readiness for Backlog",
            "status": "Funnel"
        })
    return tasks

def main():
    parser = argparse.ArgumentParser(description="JYSK IT Operations Order Intake Tool")
    parser.add_argument("--input", help="Path to raw intake description file")
    parser.add_argument("--output", help="Path to save generated Jira templates (Markdown)")
    parser.add_argument("--depts", help="Comma-separated list of departments (override automatic detection)")
    args = parser.parse_args()

    # Read input text
    raw_text = ""
    if args.input:
        with open(args.input, "r") as f:
            raw_text = f.read()
    else:
        # Read from stdin
        print("Reading intake request from stdin (Ctrl+D when finished)...", file=sys.stderr)
        raw_text = sys.stdin.read()
        
    if not raw_text.strip():
        print("Error: Empty intake request.", file=sys.stderr)
        sys.exit(1)
        
    # Analyze and Extract
    fields = parse_intake(raw_text)
    
    # Department Analysis
    if args.depts:
        selected = [d.strip() for d in args.depts.split(",") if d.strip()]
        dept_findings = [(d, ["Manual override"]) for d in selected if d in DEPARTMENTS]
    else:
        dept_findings = analyze_departments(raw_text)
        
    # Format templates
    opportunity_md = format_opportunity_space(fields)
    tasks = format_jira_tasks(fields["title"], dept_findings)
    
    # Compile output markdown
    output_md = f"""# 📋 JYSK IT Operations Intake Output

## 🎫 Parent Feature Ticket
*   **Title**: {fields["title"]}
*   **Stage**: **FUNNEL**
*   **Description**:
```markdown
{opportunity_md}
```

---

## 🔗 Linked Cross-Departmental Tasks
*The following {len(tasks)} tasks have been identified and mapped based on the technology requirements:*

"""
    for i, t in enumerate(tasks, 1):
        output_md += f"""### Task {i}: {t["title"]}
*   **Assigned Team**: `{t["department"]}`
*   **Stage**: **FUNNEL**
*   **Description**:
```markdown
{t["description"]}
```

"""

    if args.output:
        with open(args.output, "w") as f:
            f.write(output_md)
        print(f"Success: Jira templates compiled and saved to {args.output}")
    else:
        print(output_md)

if __name__ == "__main__":
    main()
