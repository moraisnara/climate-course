"""
build_all.py — rebuild every figure in Class 1.

    cd class_impacts && python figures_src/build_all.py

Each figNN_*.py is a standalone script that imports climstyle and writes
<name>.pdf and <name>.png into ../figures/. Nothing in figures/ is ever
hand-edited: edit the script and rerun this.
"""
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

scripts = sorted(f for f in os.listdir(HERE)
                 if f.startswith("fig") and f.endswith(".py"))

for s in scripts:
    print(s)
    runpy.run_path(os.path.join(HERE, s), run_name="__main__")

print(f"\n{len(scripts)} figures rebuilt into figures/")
