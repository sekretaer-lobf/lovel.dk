"""
Page builder logic - orchestrates data and generates page structure
Separation: Logic only, no HTML generation
"""

from datetime import datetime
from pathlib import Path


def get_root_path(page_path: str) -> str:
    """Get relative path to root from current page."""
    depth = page_path.count("/") + 1 if page_path else 0
    return "../" * depth if depth > 0 else ""


def get_page_path(page_id: str) -> str:
    """Convert page_id to filesystem path."""
    if page_id == "home":
        return ""
    return page_id


def is_home_page(page_id: str) -> bool:
    """Check if page is home page."""
    return page_id == "home"


def get_css_path(page_id: str, root_path: str) -> str:
    """Get correct CSS path for page."""
    if "/" in page_id:
        return root_path + "assets/styles.css"
    return "assets/styles.css"


def get_last_updated() -> str:
    """Get current date in Danish format."""
    return datetime.now().strftime("%d. %B %Y")


def build_page_metadata(page_id: str, page_data: dict, site_data: dict) -> dict:
    """
    Build all metadata needed for page rendering.
    Pure data transformation - no HTML.
    """
    page_path = get_page_path(page_id)
    root_path = get_root_path(page_path)
    is_home = is_home_page(page_id)
    
    return {
        "page_id": page_id,
        "page_path": page_path,
        "root_path": root_path,
        "is_home": is_home,
        "css_path": get_css_path(page_id, root_path),
        "title": page_data.get("title", ""),
        "description": page_data.get("description", site_data['site']['description']),
        "has_hero": is_home and "hero" in page_data,
        "hero": page_data.get("hero", {}),
        "sections": page_data.get("sections", []),
        "last_updated": get_last_updated(),
    }


def get_output_file(page_id: str, output_dir: Path) -> Path:
    """Determine output file path for page."""
    if "/" in page_id:
        page_dir = output_dir / page_id
        page_dir.mkdir(parents=True, exist_ok=True)
        return page_dir / "index.html"
    elif page_id == "home":
        return output_dir / "index.html"
    else:
        return output_dir / f"{page_id}.html"
