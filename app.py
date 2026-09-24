"""
Entry point for deployment platforms that expect a top-level app.py
(Streamlit Community Cloud, Render, Railway, Heroku-style buildpacks, etc.).

The actual application code lives in src/main.py so it can be reused/imported
independently of how it's launched. This file just runs it.
"""
import runpy
from pathlib import Path

MAIN_SCRIPT = Path(__file__).parent / "src" / "main.py"

runpy.run_path(str(MAIN_SCRIPT), run_name="__main__")
