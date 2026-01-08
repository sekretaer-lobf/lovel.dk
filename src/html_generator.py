"""
HTML generation - builds complete HTML pages
Separation: Only HTML markup, no logic/orchestration
"""

from templates import (
    render_header, render_text_section, render_two_column_section,
    render_navbar
)


def render_section(section: dict, root_path: str) -> str:
    """
    Dispatch section rendering to appropriate template.
    Pure HTML generation based on section data.
    """
    section_type = section.get("type")
    is_collapsible = section.get("collapsible", False)
    section_id = section.get("id", "")
    
    if section_type == "header":
        return render_header(section.get('title', ''), is_collapsible, section_id)
    
    elif section_type == "text":
        return render_text_section(
            content=section.get('content'),
            title=section.get('title'),
            paragraphs=section.get('paragraphs'),
            bullets=section.get('bullets'),
            is_collapsible=is_collapsible,
            section_id=section_id
        )
    
    elif section_type == "content":
        layout = section.get("layout", "single")
        columns = section.get("columns", [])
        
        if layout == "two-col":
            return render_two_column_section(columns, root_path, is_collapsible, section_id)
        else:
            # Single column layout
            from templates import render_iframe_column, render_map_column, render_image_column
            html = f"<div class='section'><div class='container'>"
            for col in columns:
                col_type = col.get("type")
                if col_type == "text":
                    html += col.get("content", "")
                elif col_type == "iframe":
                    html += render_iframe_column(col.get("src", ""), col.get("alt", ""))
                elif col_type == "map":
                    html += render_map_column(col.get("src", ""), col.get("alt", ""))
                elif col_type == "image":
                    html += render_image_column(col.get("src", ""), root_path, col.get("alt", ""))
            html += "</div></div>\n"
            return html
    
    elif section_type == "video":
        video_id = section.get("video_id", "")
        if video_id:
            from templates import render_video_column
            return f"<div class='section'><div class='container'><div class='row cols-1'><div class='col'>" + render_video_column(video_id) + "</div></div></div></div>\n"
    
    elif section_type == "slider":
        images = section.get("images", [])
        if images:
            from templates import render_slider
            slider_html = render_slider(images, root_path)
            return f"<div class='section'><div class='container'>" + slider_html + "</div></div>\n"
    
    return ""


def render_page_head(metadata: dict) -> str:
    """Generate HTML head section."""
    return f"""<!DOCTYPE html>
<html lang="da">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="robots" content="index, follow">
    <meta name="description" content="{metadata['description']}">
    <title>{metadata['title']} - Løvel - lige i nærheden</title>
    <link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,700" rel="stylesheet">
    <link href="{metadata['css_path']}" rel="stylesheet">
</head>
<body>"""


def render_page_navbar(pages: dict, metadata: dict) -> str:
    """Generate navigation bar."""
    return render_navbar(pages, metadata['root_path'], metadata['is_home'])


def render_page_hero(metadata: dict) -> str:
    """Generate hero section if applicable."""
    if not metadata['has_hero']:
        return ""
    
    hero = metadata['hero']
    return f"""    <div class="hero" style="background-image: url('{metadata['root_path']}{hero.get('image', '')}');">
        <div class="container">
            <h1>{hero.get('title', '')}</h1>
            <h3>{hero.get('subtitle', '')}</h3>
        </div>
    </div>
"""


def render_page_main(metadata: dict) -> str:
    """Generate main content sections."""
    html = "    <main>\n"
    html += render_page_hero(metadata)
    
    # Add sections
    for section in metadata['sections']:
        html += render_section(section, metadata['root_path'])
    
    html += "    </main>\n"
    return html


def render_page_footer(metadata: dict) -> str:
    """Generate footer section."""
    root_path = metadata['root_path']
    last_updated = metadata['last_updated']
    
    return f"""
    <button id="scrollToTop" aria-label="Tilbage til toppen">↑</button>

    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <p><strong>Henvendelser vedr. hjemmesiden:</strong></p>
                    <p><a href="mailto:support@lovel.dk">support@lovel.dk</a></p>
                </div>
                <div class="footer-section">
                    <p>© 2025 | Løvel - lige i nærheden</p>
                    <p><small>Sidst opdateret: {last_updated}</small></p>
                </div>
            </div>
        </div>
    </footer>
"""


def render_page_scripts() -> str:
    """Generate JavaScript code."""
    return """
    <script>
        // Scroll to top button
        const scrollToTopBtn = document.getElementById('scrollToTop');
        
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                scrollToTopBtn.classList.add('show');
            } else {
                scrollToTopBtn.classList.remove('show');
            }
        });
        
        scrollToTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });

        // Mobile menu toggle
        const toggle = document.getElementById('navbar-toggle');
        const menu = document.getElementById('navbar-menu');
        
        if (toggle && menu) {
            toggle.addEventListener('click', function() {
                menu.classList.toggle('active');
            });
        }
        
        // Dropdown menus
        document.querySelectorAll('.dropdown').forEach(dropdown => {
            const toggle = dropdown.querySelector('.dropdown-toggle');
            if (toggle) {
                toggle.addEventListener('click', function(e) {
                    e.preventDefault();
                    dropdown.classList.toggle('active');
                });
            }
        });

        // Collapsible sections
        document.querySelectorAll('.collapse-toggle').forEach(toggle => {
            toggle.addEventListener('click', function() {
                const header = this.closest('.collapsible-header');
                if (!header) return;
                
                const sectionId = header.getAttribute('data-section');
                if (!sectionId) return;
                
                // Toggle header itself
                header.classList.toggle('collapsed');
                this.setAttribute('aria-expanded', header.classList.contains('collapsed') ? 'true' : 'false');
                
                // Find and toggle ALL consecutive content sections with the same ID
                let nextElement = header.nextElementSibling;
                while (nextElement) {
                    if (nextElement.classList.contains('collapsible-content') && 
                        nextElement.getAttribute('data-section') === sectionId) {
                        nextElement.classList.toggle('collapsed');
                        nextElement = nextElement.nextElementSibling;
                    } else if (nextElement.classList.contains('collapsible-header')) {
                        // Stop when we hit the next header
                        break;
                    } else {
                        nextElement = nextElement.nextElementSibling;
                    }
                }
            });

            // Handle keyboard Enter/Space
            toggle.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.click();
                }
            });
        });
    </script>
</body>
</html>"""


def render_complete_page(metadata: dict, pages: dict) -> str:
    """
    Assemble complete HTML page from components.
    Pure HTML generation - orchestration handled by caller.
    """
    html = render_page_head(metadata)
    html += render_page_navbar(pages, metadata)
    html += render_page_main(metadata)
    html += render_page_footer(metadata)
    html += render_page_scripts()
    return html
