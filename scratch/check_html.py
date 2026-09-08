import re
from pathlib import Path

app_path = Path("app.py")
content = app_path.read_text(encoding="utf-8")

# Check all st.markdown occurrences
matches = re.finditer(r'st\.markdown\(\s*f?["\']{3}(.*?)["\']{3}', content, re.DOTALL)
count = 0
for match in matches:
    block = match.group(1)
    lines = block.splitlines()
    for idx in range(len(lines) - 1):
        if lines[idx].strip() == "" and re.match(r"^\s{4,}\S", lines[idx + 1]):
            print(f"Risk at line {idx+1}: {lines[idx+1][:60]}")
            count += 1

print(f"Total potential markdown code-block triggers found in app.py: {count}")
