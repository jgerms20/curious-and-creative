"""pytest setup: put the project root on sys.path so `import earlobe` works from any directory."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
