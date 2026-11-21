from pathlib import Path

ICON_DIR = Path("assets/icons")


def load_svg(category: str, name: str, size: int = 20):
    icon_path = ICON_DIR / category / f"{name}.svg"

    if not icon_path.exists():
        return f"<span>Icon not found: {name}</span>"

    svg = icon_path.read_text(encoding="utf-8")

    # SVG ka size replace karo
    svg = svg.replace('width="24"', f'width="{size}"')
    svg = svg.replace('height="24"', f'height="{size}"')

    return svg

def sidebar_title(icon, title):
    return f"""
    <div style="display:flex;align-items:center;gap:8px;margin:12px 0 8px 0;">
        {icon}
        <span style="font-size:17px;font-weight:600;">{title}</span>
    </div>
    """