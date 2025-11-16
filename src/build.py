#!/usr/bin/env python3
"""
Build script for Løvel website
Generates HTML pages from templates and data
"""

import json
import os
from pathlib import Path
from datetime import datetime

# Configuration
SITE_ROOT = Path(__file__).parent.parent
SRC_DIR = SITE_ROOT / "src"
OUTPUT_DIR = SITE_ROOT
ASSET_DIR = SITE_ROOT / "assets"

# Load site data
with open(SRC_DIR / "site-data.json") as f:
    SITE_DATA = json.load(f)

# Template functions
def get_root_path(page_path: str) -> str:
    """Get relative path to root from current page."""
    # Count slashes and add 1 for the file itself
    depth = page_path.count("/") + 1 if page_path else 0
    return "../" * depth if depth > 0 else ""

def render_section(section: dict, root_path: str) -> str:
    """Render a single section."""
    section_type = section.get("type")
    is_collapsible = section.get("collapsible", False)
    section_id = section.get("id", "")
    
    if section_type == "header":
        if is_collapsible and section_id:
            title = section.get('title', '')
            return f"<div class='section collapsible-header collapsed' data-section='{section_id}'><div class='container'><h2 class='collapse-toggle' role='button' tabindex='0' aria-expanded='false' aria-label='Expand {title} section'>{title}</h2></div></div>\n"
        return f"<div class='section'><div class='container'><h1>{section.get('title', '')}</h1></div></div>\n"
    
    elif section_type == "text":
        is_collapsible = section.get("collapsible", False)
        section_id = section.get("id", "")
        collapse_class = "collapsible-content collapsed" if is_collapsible else ""
        collapse_attr = f"data-section='{section_id}'" if is_collapsible and section_id else ""
        return f"<div class='section {collapse_class}' {collapse_attr}><div class='container'>{section.get('content', '')}</div></div>\n"
    
    elif section_type == "content":
        layout = section.get("layout", "single")
        columns = section.get("columns", [])
        is_collapsible = section.get("collapsible", False)
        section_id = section.get("id", "")
        collapse_class = "collapsible-content collapsed" if is_collapsible else ""
        collapse_attr = f"data-section='{section_id}'" if is_collapsible and section_id else ""
        
        if layout == "two-col":
            # Check if any column has width="2" to use ratio layout
            has_ratio = any(col.get("width") == "2" for col in columns)
            row_class = "cols-2-ratio" if has_ratio else "cols-2"
            html = f"<div class='section {collapse_class}' {collapse_attr}><div class='container'><div class='row {row_class}'>"
            for col in columns:
                # Support optional 'width' property (e.g., '1' or '2' for 1:2 ratio)
                width = col.get("width", "1")
                col_style = f" style='grid-column: span {width};'" if width != "1" and not has_ratio else ""
                html += f"<div class='col'{col_style}>"
                if col.get("type") == "text":
                    html += col.get("content", "")
                elif col.get("type") == "map":
                    src = col.get("src", "")
                    alt = col.get("alt", "")
                    html += f"<iframe src='{src}' style='border: 1px solid #ccc; width: 100%; height: 400px;' frameborder='0'></iframe>"
                elif col.get("type") == "image":
                    src = col.get("src", "")
                    alt = col.get("alt", "")
                    html += f"<div class='img-container'><img src='{root_path}{src}' alt='{alt}'></div>"
                elif col.get("type") == "gallery":
                    html += "<div class='gallery'>"
                    for img in col.get("images", []):
                        src = img.get("src", "")
                        alt = img.get("alt", "")
                        html += f"<div class='img-container'><img src='{root_path}{src}' alt='{alt}'></div>"
                    html += "</div>"
                html += "</div>"
            html += "</div></div></div>\n"
            return html
        else:
            html = f"<div class='section {collapse_class}' {collapse_attr}><div class='container'>"
            for col in columns:
                if col.get("type") == "text":
                    html += col.get("content", "")
                elif col.get("type") == "map":
                    src = col.get("src", "")
                    alt = col.get("alt", "")
                    html += f"<iframe src='{src}' style='border: 1px solid #ccc; width: 100%; height: 400px;' frameborder='0'></iframe>"
                elif col.get("type") == "image":
                    src = col.get("src", "")
                    alt = col.get("alt", "")
                    html += f"<div class='img-container'><img src='{root_path}{src}' alt='{alt}'></div>"
                elif col.get("type") == "gallery":
                    html += "<div class='gallery'>"
                    for img in col.get("images", []):
                        src = img.get("src", "")
                        alt = img.get("alt", "")
                        html += f"<div class='img-container'><img src='{root_path}{src}' alt='{alt}'></div>"
                    html += "</div>"
            html += "</div></div>\n"
            return html
    
    return ""

def build_navigation(root_path: str, is_home: bool) -> str:
    """Build navigation menu dynamically from site data."""
    pages = SITE_DATA['pages']
    
    # Organize pages by category
    dagtilbud_pages = {k: v for k, v in pages.items() if k.startswith('dagtilbud/')}
    foreninger_pages = {k: v for k, v in pages.items() if k.startswith('foreninger/')}
    informationer_pages = {k: v for k, v in pages.items() if k.startswith('informationer/')}
    
    nav = f"""<nav class="navbar" role="navigation">
        <div class="container">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" id="navbar-toggle">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a href="{root_path}index.html" class="logo">Løvel</a>
            </div>
            <div class="navbar-menu" id="navbar-menu">
                <ul class="nav-list">
                    <li><a href="{root_path}index.html" class="{'active' if is_home else ''}">Forside</a></li>
"""
    
    # Informationer dropdown (moved after Forside)
    if informationer_pages:
        nav += """                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle">Informationer</a>
                        <ul class="dropdown-menu">
"""
        for page_id in sorted(informationer_pages.keys()):
            title = informationer_pages[page_id].get('title', page_id.split('/')[-1])
            nav += f'                            <li><a href="{root_path}{page_id}/">{title}</a></li>\n'
        nav += """                        </ul>
                    </li>
"""
    
    # Dagtilbud dropdown
    if dagtilbud_pages:
        nav += """                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle">Dagtilbud</a>
                        <ul class="dropdown-menu">
"""
        # Custom order: vuggestue, dagpleje, børnehave, skole
        dagtilbud_order = ['dagtilbud/vuggestue', 'dagtilbud/dagpleje', 'dagtilbud/boernehave', 'dagtilbud/skole']
        for page_id in dagtilbud_order:
            if page_id in dagtilbud_pages:
                title = dagtilbud_pages[page_id].get('title', page_id.split('/')[-1])
                nav += f'                            <li><a href="{root_path}{page_id}/">{title}</a></li>\n'
        nav += """                        </ul>
                    </li>
"""
    
    # Foreninger dropdown
    if foreninger_pages:
        nav += """                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle">Foreninger</a>
                        <ul class="dropdown-menu">
"""
        for page_id in sorted(foreninger_pages.keys()):
            title = foreninger_pages[page_id].get('title', page_id.split('/')[-1])
            nav += f'                            <li><a href="{root_path}{page_id}/">{title}</a></li>\n'
        nav += """                        </ul>
                    </li>
"""
    
    # Check for erhverv page
    if 'erhverv' in pages:
        nav += f'                    <li><a href="{root_path}erhverv/">Erhverv</a></li>\n'
    
    # Check for film page - display as regular link (not dropdown)
    if 'film' in pages:
        nav += f"""                    <li><a href="{root_path}film.html">Film</a></li>
"""
    
    nav += """                </ul>
            </div>
        </div>
    </nav>"""
    
    return nav

def render_page(page_id: str, page_data: dict) -> str:
    """Render a complete HTML page."""
    # Handle home page path
    if page_id == "home":
        page_path = ""
    else:
        page_path = page_id
    
    root_path = get_root_path(page_path)
    
    # Determine if it's home page
    is_home = page_id == "home"
    
    # Fix asset paths for nested pages
    css_path = root_path + "assets/styles.css" if "/" in page_id else "assets/styles.css"
    
    # Build navigation dynamically
    nav_html = build_navigation(root_path, is_home)
    
    # Build HTML
    html = f"""<!DOCTYPE html>
<html lang="da">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="robots" content="index, follow">
    <meta name="description" content="{page_data.get('description', SITE_DATA['site']['description'])}">
    <title>{page_data.get('title', '')} - Løvel - lige i nærheden</title>
    <link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,700" rel="stylesheet">
    <link href="{css_path}" rel="stylesheet">
</head>
<body>
    {nav_html}

    <main>
"""
    
    # Add hero section if present
    if is_home and "hero" in page_data:
        hero = page_data["hero"]
        html += f"""        <div class="hero" style="background-image: url('{root_path}{hero.get('image', '')}');">
            <div class="container">
                <h1>{hero.get('title', '')}</h1>
                <h3>{hero.get('subtitle', '')}</h3>
            </div>
        </div>
"""
    
    # Add sections
    for section in page_data.get("sections", []):
        html += render_section(section, root_path)
    
    # Footer
    html += f"""    </main>

    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <p><strong>Henvendelser vedr. hjemmesiden:</strong></p>
                    <p><a href="mailto:support@lovel.dk">support@lovel.dk</a></p>
                </div>
                <div class="footer-section">
                    <p>© 2025 | Løvel - lige i nærheden</p>
                </div>
            </div>
        </div>
    </footer>

    <script>
        // Mobile menu toggle
        const toggle = document.getElementById('navbar-toggle');
        const menu = document.getElementById('navbar-menu');
        
        if (toggle && menu) {{
            toggle.addEventListener('click', function() {{
                menu.classList.toggle('active');
            }});
        }}
        
        // Dropdown menus
        document.querySelectorAll('.dropdown').forEach(dropdown => {{
            const toggle = dropdown.querySelector('.dropdown-toggle');
            if (toggle) {{
                toggle.addEventListener('click', function(e) {{
                    e.preventDefault();
                    dropdown.classList.toggle('active');
                }});
            }}
        }});

        // Collapsible sections
        document.querySelectorAll('.collapse-toggle').forEach(toggle => {{
            toggle.addEventListener('click', function() {{
                const header = this.closest('.collapsible-header');
                if (!header) return;
                
                const sectionId = header.getAttribute('data-section');
                if (!sectionId) return;
                
                // Toggle header itself
                header.classList.toggle('collapsed');
                this.setAttribute('aria-expanded', header.classList.contains('collapsed') ? 'true' : 'false');
                
                // Find and toggle ALL consecutive content sections with the same ID
                let nextElement = header.nextElementSibling;
                while (nextElement) {{
                    if (nextElement.classList.contains('collapsible-content') && 
                        nextElement.getAttribute('data-section') === sectionId) {{
                        nextElement.classList.toggle('collapsed');
                        nextElement = nextElement.nextElementSibling;
                    }} else if (nextElement.classList.contains('collapsible-header')) {{
                        // Stop when we hit the next header
                        break;
                    }} else {{
                        nextElement = nextElement.nextElementSibling;
                    }}
                }}
            }});

            // Handle keyboard Enter/Space
            toggle.addEventListener('keydown', function(e) {{
                if (e.key === 'Enter' || e.key === ' ') {{
                    e.preventDefault();
                    this.click();
                }}
            }});
        }});
    </script>
</body>
</html>"""
    
    return html

def build_site():
    """Build the entire site."""
    print("🏗️  Building Løvel website...")
    
    for page_id, page_data in SITE_DATA["pages"].items():
        # Handle index files
        if "/" in page_id:
            output_dir = OUTPUT_DIR / page_id
            output_file = output_dir / "index.html"
            output_dir.mkdir(parents=True, exist_ok=True)
        elif page_id == "home":
            output_file = OUTPUT_DIR / "index.html"
        else:
            output_file = OUTPUT_DIR / f"{page_id}.html"
        
        # Generate and write HTML
        html_content = render_page(page_id, page_data)
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"  ✓ Generated {output_file.relative_to(SITE_ROOT)}")
    
    print("✅ Build complete!")

if __name__ == "__main__":
    build_site()
