import importlib.util
from pathlib import Path
import sys


BACKEND_DIR = Path(__file__).resolve().parent / "backend"
BACKEND_MAIN = BACKEND_DIR / "main.py"

# Allow `uvicorn main:app` to work when the service starts from repo root.
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

spec = importlib.util.spec_from_file_location("render_backend_main", BACKEND_MAIN)
if spec is None or spec.loader is None:
    raise ImportError(f"Could not load backend app from {BACKEND_MAIN}")

module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

app = module.app
