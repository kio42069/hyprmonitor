#!/usr/bin/python
import os

SRC_DIR = "src"
OUT_DIR = "dist"
SCRIPTS = ["reader.py", "monitor.py"]
FILES_TO_INLINE = ["variables.py", "utils.py"]

START_MARKER = "#$$$"
END_MARKER = "#@@@"
SHEBANG = "#!/usr/bin/python"

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def extract_replacement_code():
    code_parts = []
    for fname in FILES_TO_INLINE:
        path = os.path.join(SRC_DIR, fname)
        code = read_file(path).strip()
        code_parts.append(f"# Begin {fname}\n{code}\n# End {fname}")
    return "\n\n".join(code_parts)

def process_script(filename):
    path = os.path.join(SRC_DIR, filename)
    content = read_file(path)

    pre, _, rest = content.partition(START_MARKER)
    _, _, post = rest.partition(END_MARKER)

    inlined_code = extract_replacement_code()
    combined = f"{pre.strip()}\n\n{inlined_code}\n\n{post.lstrip()}"

    # Add shebang at the top, avoiding duplicate shebangs
    if not combined.startswith("#!"):
        combined = f"{SHEBANG}\n\n{combined}"

    return combined

def build():
    os.makedirs(OUT_DIR, exist_ok=True)

    for script in SCRIPTS:
        result = process_script(script)
        out_path = os.path.join(OUT_DIR, script)
        with open(out_path, "w") as f:
            f.write(result)
        os.chmod(out_path, 0o755)

    print("✅ Build complete. Scripts saved to ./dist")

if __name__ == "__main__":
    build()
