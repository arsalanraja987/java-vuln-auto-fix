import re
import os
import subprocess

# Pattern and replacement
VULN_PATTERN = r'File file = new File\("/var/data/" \+ fileName\);'
SAFE_CODE = '''File baseDir = new File("/var/data/");
File file = new File(baseDir, fileName).getCanonicalFile();
if (!file.getPath().startsWith(baseDir.getCanonicalPath())) {
    throw new SecurityException("Invalid file path");
}'''

def fix_file(file_path):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    with open(file_path, 'r') as f:
        content = f.read()

    if 'File file = new File("/var/data/" + fileName);' in content:
        print("🔧 Vulnerability found. Fixing...")
        content = re.sub(VULN_PATTERN, SAFE_CODE, content)
        with open(file_path, 'w') as f:
            f.write(content)

        # Git auto commit
        subprocess.run(["git", "config", "--global", "user.name", "AutoFix Bot"])
        subprocess.run(["git", "config", "--global", "user.email", "bot@example.com"])
        subprocess.run(["git", "add", file_path])
        subprocess.run(["git", "commit", "-m", "Fix: Path Traversal Vulnerability"])
        subprocess.run(["git", "push"])
    else:
        print("✅ No vulnerability found.")

fix_file("FileLoader.java")
