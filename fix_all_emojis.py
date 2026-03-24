# fix_all_emojis.py
import re

file_path = r"D:\smart assist ai\Ai-ChatBot\Chatbot\crawler\crawler\spiders\website_scrap.py"

# Define replacements for all common Unicode emojis
replacements = {
    r'\\U0001f680': '',      # 🚀
    r'\\u2705': '',          # ✅
    r'\\u274c': 'X ',        # ❌
    r'\\U0001f389': '',      # 🎉
    r'\\u2757': '!',         # ❗
    r'\\u26a0': 'Warning:',  # ⚠
    r'\\u26d4': 'Stop:',     # ⛔
    r'\\U0001f4ca': 'Chart:',# 📊
    r'\\U0001f4c4': 'Doc:',  # 📄
    r'\\u2b50': 'Star:',     # ⭐
    r'\\U0001f4dd': 'Note:', # 📝
    r'\\U0001f4be': 'Save:', # 💾
    r'\\U0001f4cb': 'Clip:', # 📋
    r'\\U0001f4c8': 'Stats:',# 📈
    r'\\u1f310': 'Web:',     # 🌐
}

print("Reading file...")
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("Replacing Unicode characters...")
for pattern, replacement in replacements.items():
    content = re.sub(pattern, replacement, content)

# Also fix any literal Unicode characters (not escaped)
literal_replacements = {
    '🚀': '',
    '✅': '',
    '❌': 'X',
    '🎉': '',
    '❗': '!',
    '⚠': 'Warning:',
    '⛔': 'Stop:',
    '📊': 'Stats:',
    '📄': 'Doc:',
    '⭐': 'Star:',
    '📝': 'Note:',
    '💾': 'Save:',
    '📋': 'Clip:',
    '📈': 'Stats:',
    '🌐': 'Web:',
}

for char, replacement in literal_replacements.items():
    content = content.replace(char, replacement)

# Add UTF-8 encoding fix at the TOP of the file
encoding_fix = """import sys
import io

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    
    # Set environment for subprocesses
    import os
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUTF8'] = '1'

"""

# Insert after shebang and encoding comments, before other imports
lines = content.split('\n')
new_lines = []
for line in lines:
    if line.startswith('#!') or line.startswith('# -*- coding:'):
        new_lines.append(line)
        continue
    if line.strip().startswith('import ') or line.strip().startswith('from '):
        # Insert our fix before the first import
        if encoding_fix:
            new_lines.append('')
            new_lines.append(encoding_fix.strip())
            encoding_fix = None
        new_lines.append(line)
    else:
        new_lines.append(line)

print("Writing fixed file...")
with open(file_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print(f"Fixed {file_path}")
print("All Unicode emojis have been removed or replaced.")
