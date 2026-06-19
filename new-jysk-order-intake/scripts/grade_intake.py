import os
import sys
import json

def run_grading(file_path, grading_json_path, eval_id):
    print(f"Grading {file_path} (eval_id={eval_id}) -> {grading_json_path}")
    expectations = []
    
    valid_file = False
    content = ""
    try:
        with open(file_path, "r") as f:
            content = f.read()
        valid_file = True
        evidence_1 = f"Successfully read file {file_path} with {len(content)} characters."
    except Exception as e:
        evidence_1 = f"Failed to read file: {str(e)}"
        
    expectations.append({
        "text": "Intake output file exists and is readable",
        "passed": valid_file,
        "evidence": evidence_1
    })
    
    if not valid_file:
        for text in [
            "Conforms to JYSK Opportunity Space template format",
            "Has Problem validated with: [Name] | [DD-MM-YYYY] line",
            "Accurately maps tasks to all required departments"
        ]:
            expectations.append({
                "text": text,
                "passed": False,
                "evidence": "Cannot evaluate because the file could not be read."
            })
        summary = {"total": 4, "passed": 1, "failed": 3, "pass_rate": 0.25}
        with open(grading_json_path, "w") as f:
            json.dump({"summary": summary, "expectations": expectations}, f, indent=2)
        return

    # Check JYSK Opportunity Space template markers
    template_marker = "## 🔍 OPPORTUNITY SPACE" in content
    has_headers = (
        "**Problem / Need statement**" in content and
        "**Root cause**" in content and
        "**Affected stakeholders**" in content and
        "**Business impact**" in content and
        "**In scope**" in content and
        "**Out of scope**" in content and
        "**Regulatory or architectural constraints**" in content and
        "**Current workarounds**" in content
    )
    
    expectations.append({
        "text": "Conforms to JYSK Opportunity Space template format",
        "passed": template_marker and has_headers,
        "evidence": "Successfully found JYSK Opportunity Space template headers." if (template_marker and has_headers) else f"Template marker found: {template_marker}. Standard headers found: {has_headers}."
    })
    
    # Check validation line
    has_validation_line = "Problem validated with:" in content
    expectations.append({
        "text": "Contains validation sign-off line",
        "passed": has_validation_line,
        "evidence": "Found validation sign-off line." if has_validation_line else "Validation sign-off line is missing."
    })
    
    # Check department mapping accuracy
    correct_depts = False
    dept_evidence = ""
    if int(eval_id) == 0:
        # Needs IT Stores, IT Server, IT Network
        stores_found = "IT Stores" in content or "POS" in content or "terminal" in content
        server_found = "IT Server" in content or "virtual machine" in content or "server" in content
        network_found = "IT Network" in content or "network" in content
        correct_depts = stores_found and server_found and network_found
        dept_evidence = f"Stores task: {stores_found}, Server task: {server_found}, Network task: {network_found}."
    else:
        # Needs Container Platform, IT Client, IT Network
        container_found = "Container Platform" in content or "OpenShift" in content or "Kubernetes" in content
        client_found = "IT Client" in content or "Windows 11" in content or "Intune" in content or "client" in content
        network_found = "IT Network" in content or "firewall" in content or "port" in content
        correct_depts = container_found and client_found and network_found
        dept_evidence = f"Container task: {container_found}, Client task: {client_found}, Network task: {network_found}."
        
    expectations.append({
        "text": "Accurately maps tasks to all involved departments",
        "passed": correct_depts,
        "evidence": f"Mapped departments check: {dept_evidence}"
    })
    
    # Calculate summary
    total_assertions = len(expectations)
    passed_assertions = sum(1 for exp in expectations if exp["passed"])
    failed_assertions = total_assertions - passed_assertions
    pass_rate = passed_assertions / total_assertions if total_assertions > 0 else 0.0
    
    summary = {
        "total": total_assertions,
        "passed": passed_assertions,
        "failed": failed_assertions,
        "pass_rate": pass_rate
    }
    
    os.makedirs(os.path.dirname(grading_json_path), exist_ok=True)
    with open(grading_json_path, "w") as f:
        json.dump({
            "summary": summary,
            "expectations": expectations
        }, f, indent=2)
    print(f"Grading written to {grading_json_path}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python grade_intake.py <file_path> <grading_json_path> <eval_id>")
        sys.exit(1)
    run_grading(sys.argv[1], sys.argv[2], sys.argv[3])
