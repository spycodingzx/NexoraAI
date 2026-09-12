"""Sweep all core plugins for import errors."""

import sys, importlib, glob, traceback

sys.path.insert(0, ".")
sys.path.insert(0, "core/services")
sys.path.insert(0, "core/tabs")

files = sorted(
    glob.glob("core/services/*.py")
    + glob.glob("core/tabs/*.py")
    + glob.glob("core/ui/*.py")
    + glob.glob("core/utils/*.py")
    + glob.glob("core/core/*.py")
    + glob.glob("plugins/*.py")
)

fails = []
for f in files:
    if "__pycache__" in f or f.endswith(".old") or f.endswith(".backup"):
        continue
    modpath = f.replace("/", ".").replace(".py", "")
    try:
        importlib.import_module(modpath)
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        origin = tb[-1] if tb else None
        loc = f'{origin.filename.split("printify_clean/")[-1]}:{origin.lineno}' if origin else "?"
        fails.append((modpath, type(e).__name__, str(e)[:150], loc))

print(f"\n=== {len(fails)} IMPORT FAILURES ===")
for mod, etype, emsg, loc in fails:
    print(f"\nFAIL [{etype}] {mod}")
    print(f"     at {loc}")
    print(f"     {emsg}")
print()
