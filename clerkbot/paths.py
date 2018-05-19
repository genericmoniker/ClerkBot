from pathlib import Path

CONF_DIR = Path('/conf')  # Docker
if not CONF_DIR.exists():
    CONF_DIR = Path.home() / 'clerkbot' / 'conf'

OUTPUT_DIR = Path('/output')  # Docker
if not OUTPUT_DIR.exists():
    OUTPUT_DIR = Path.home() / 'clerkbot' / 'output'
