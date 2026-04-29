from groq import Groq
from app.config import GROQ_API_KEY
import json

def ai_analyzer(issues):
    if not issues:
        return {}
    client = Groq(api_key=GROQ_API_KEY)
    prompt = f"""Your role is a security engineer trying to clearify some security issues in python code file. The issues are scanned by bandit so it is in json, I hope you to provide me with: 
    1. the priority of those issues
    2. a brief intro on why i need to fix this and what is this
    3. a fixed version of the issue and why it is fixed please provide the output in json where each item is: 
    - 'issue_index': which issue this refers to (0-based)
    - 'priority': 1 (fix immediately) to 3 (fix when possible)
    - 'explanation': plain English explanation of the risk
    - 'fix': the corrected code snippet
    - 'fix_reason': why this fix works
    - do not include anything outside the JSON
    - the priority 1 means nedd to be fixed immediately, 2 mean fix before next release, 3 means ifx when possible
    Here is the bandit output: {issues}"""
    try:
        response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
        )
        result = json.loads(response.choices[0].message.content)

    except Exception as e:
        result = {"error": str(e)}

    return result



