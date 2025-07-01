import re
import os

# Vulnerable pattern to look for
VULN_PATTERN = r'File file = new File\("/var/data/" \+ fileName\);'

# Secure code to replace it with
SAFE_CODE = '''File baseDir = new File("/var/data/");
File file = new File(baseDir, fileName).getCanonicalFile();
if (!file.getPath().startsWith(baseDir.getCanonicalPath())) {
    throw new SecurityException("Invalid file path");
}'''

def fix_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    if 'File file = new File("/var/data/" + fileName);' in content:
        print("🔧 Vulnerability found. Fixing...")
        content = re.sub(VULN_PATTERN, SAFE_CODE, content)
        with open(file_path, 'w') as f:
            f.write(content)

        os.system("git config --global user.name 'AutoFix Bot'")
        os.system("git config --global user.email 'bot@example.com'")
        os.system(f"git add {file_path}")
        os.system("git commit -m 'Fix: Path Traversal Vulnerability'")
        os.system("git push")
    else:
        print("✅ No vulnerability found.")

fix_file("FileLoader.java")
