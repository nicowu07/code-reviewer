import subprocess
import os
import json

def bandit_analyzer(filePath):
    try:
        result = subprocess.run(
            ["bandit", "-r", filePath, "-f", "json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 2:
            return [], [], 2
        issue_num, issues, returnCode = parse_bandit_output(result.stdout)
        return issue_num, issues, returnCode
    finally:
            if os.path.exists(filePath):
                os.remove(filePath)

def parse_bandit_output(jsonOutput):
    try:
        data = json.loads(jsonOutput)
    except:
        return [], [], 1
    totals = data["metrics"].get("_totals", {})
    issue_num = {k: v for k, v in totals.items() if k.startswith("SEVERITY") or k.startswith("CONFIDENCE")}
    issues = []
    for i in data["results"]:
        detail = {}
        detail["code"] = i["code"]
        detail["issue_confidence"] = i["issue_confidence"]
        detail["issue_severity"] = i["issue_severity"]
        detail["issue_text"] = i["issue_text"]
        issues.append(detail)
    returnCode = 0
    return issue_num, issues, returnCode
