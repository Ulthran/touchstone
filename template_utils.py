from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"


def render_template(name: str, **kwargs) -> str:
    """Load a text template and render it with the given keyword arguments."""
    path = TEMPLATE_DIR / f"{name}.txt"
    content = path.read_text()
    return content.format(**kwargs)
