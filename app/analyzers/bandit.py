import subprocess
import os

def bandit_analyzer(filePath):
    result = subprocess.run(
        ["bandit", "-r", filePath],
        capture_output=True,
        text=True
    )
    os.remove(filePath)
    return result.stdout