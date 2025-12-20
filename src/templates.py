"""
HTML Component Templates for Løvel website
Separates HTML rendering from data and build logic
"""

def render_header(title: str, is_collapsible: bool = False, section_id: str = "") -> str:
    """Render a page section header."""
    if is_collapsible and section_id:
        return f"<div class='section collapsible-header collapsed' data-section='{section_id}'><div class='container'><h2 class='collapse-toggle' role='button' tabindex='0' aria-expanded='false' aria-label='Expand {title} section'>{title}</h2></div></div>\n"
    return f"<div class='section'><div class='container'><h1>{title}</h1></div></div>\n"


def render_text_section(content: str = None, title: str = None, paragraphs: list = None, bullets: list = None, is_collapsible: bool = False, section_id: str = "") -> str:
    """
    Render a text-only section.
    Supports both old format (content as HTML string) and new format (title + paragraphs + bullets).
    
    Bullets format: [{"title": "Group Title", "items": ["item1", "item2"]}, ...]
    """
    collapse_class = "collapsible-content collapsed" if is_collapsible else ""
    collapse_attr = f"data-section='{section_id}'" if is_collapsible and section_id else ""
    
    # Build HTML content
    html_content = ""
    
    if content:
        # Old format - pre-rendered HTML
        html_content = content
    else:
        # New format - build from title and paragraphs
        if title:
            html_content += f"<h3>{title}</h3>"
        
        if paragraphs:
            for para in paragraphs:
                html_content += f"<p>{para}</p>"
        
        if bullets:
            for bullet_group in bullets:
                group_title = bullet_group.get("title")
                items = bullet_group.get("items", [])
                
                if group_title:
                    html_content += f"<p><strong>{group_title}</strong></p>"
                
                if items:
                    html_content += "<ul>"
                    for item in items:
                        html_content += f"<li>{item}</li>"
                    html_content += "</ul>"
    
    return f"<div class='section {collapse_class}' {collapse_attr}><div class='container'>{html_content}</div></div>\n"


def render_text_column(content: str = None, title: str = None, paragraphs: list = None, bullets: list = None) -> str:
    """
    Render a text column in two-column layout.
    Can accept either:
    - content: pre-rendered HTML string (old format)
    - title + paragraphs: new format with title and paragraph list
    - bullets: list of bullet point groups with titles and items
    
    Bullets format: [{"title": "Group Title", "items": ["item1", "item2"]}, ...]
    """
    if content:
        # Old format - already HTML
        return content
    
    # New format - build from title and paragraphs
    html = ""
    if title:
        html += f"<h2>{title}</h2>"
    
    if paragraphs:
        for para in paragraphs:
            html += f"<p>{para}</p>"
    
    if bullets:
        for bullet_group in bullets:
            group_title = bullet_group.get("title")
            items = bullet_group.get("items", [])
            
            if group_title:
                html += f"<p><strong>{group_title}</strong></p>"
            
            if items:
                html += "<ul>"
                for item in items:
                    html += f"<li>{item}</li>"
                html += "</ul>"
    
    return html


def render_image_column(src: str, root_path: str, alt: str = "") -> str:
    """Render an image column in two-column layout."""
    return f"<div class='img-container'><img src='{root_path}{src}' alt='{alt}'></div>"


def render_map_column(src: str, alt: str = "") -> str:
    """Render an OpenStreetMap iframe column."""
    return f"<iframe src='{src}' style='border: 1px solid #ccc; width: 100%; height: 400px;' frameborder='0'></iframe>"


def render_gallery(images: list, root_path: str) -> str:
    """Render a gallery of images."""
    html = "<div class='gallery'>"
    for img in images:
        src = img.get("src", "")
        alt = img.get("alt", "")
        html += f"<div class='img-container'><img src='{root_path}{src}' alt='{alt}'></div>"
    html += "</div>"
    return html


def render_video_column(video_id: str) -> str:
    """Render a YouTube video embed in a column."""
    return f"""<div class='video-container' style='position: relative; width: 100%; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 8px;'>
    <iframe style='position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; border-radius: 8px;' src='https://www.youtube.com/embed/{video_id}?rel=0&showinfo=0' allowfullscreen='' allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture'></iframe>
</div>"""


def render_two_column_section(
    columns: list, 
    root_path: str, 
    is_collapsible: bool = False, 
    section_id: str = ""
) -> str:
    """
    Render a two-column layout section.
    
    Columns should have:
    - type: "text", "image", "gallery", or "map"
    - For text columns: either content (HTML string) or title + paragraphs
    - For image/map: src, alt
    - For gallery: images list
    - width: (optional) "1" or "2" for column width ratio
    """
    # Check if any column has width="2" to use ratio layout
    has_ratio = any(col.get("width") == "2" for col in columns)
    row_class = "cols-2-ratio" if has_ratio else "cols-2"
    
    collapse_class = "collapsible-content collapsed" if is_collapsible else ""
    collapse_attr = f"data-section='{section_id}'" if is_collapsible and section_id else ""
    
    html = f"<div class='section {collapse_class}' {collapse_attr}><div class='container'><div class='row {row_class}'>"
    
    for col in columns:
        col_type = col.get("type")
        width = col.get("width", "1")
        col_style = f" style='grid-column: span {width};'" if width != "1" and not has_ratio else ""
        
        html += f"<div class='col'{col_style}>"
        
        if col_type == "text":
            # Support both old (content) and new (title + paragraphs + bullets) formats
            content = col.get("content")
            title = col.get("title")
            paragraphs = col.get("paragraphs")
            bullets = col.get("bullets")
            html += render_text_column(content, title, paragraphs, bullets)
        elif col_type == "image":
            html += render_image_column(col.get("src", ""), root_path, col.get("alt", ""))
        elif col_type == "map":
            html += render_map_column(col.get("src", ""), col.get("alt", ""))
        elif col_type == "gallery":
            html += render_gallery(col.get("images", []), root_path)
        elif col_type == "video":
            html += render_video_column(col.get("video_id", ""))
        
        html += "</div>"
    
    html += "</div></div></div>\n"
    return html


def render_hero_section(hero_data: dict, root_path: str) -> str:
    """Render the hero/banner section at top of page."""
    image = hero_data.get("image", "")
    title = hero_data.get("title", "")
    subtitle = hero_data.get("subtitle", "")
    
    html = f"""<section class="hero" style="background-image: url('{root_path}{image}'); background-size: cover; background-position: center;">
    <div class="hero-content">
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
</section>
"""
    return html


def render_business_card(title: str, content: str) -> str:
    """Render a business card component."""
    return f"""<div class='business-card' style='padding: var(--spacing); border: 1px solid var(--border); border-radius: var(--radius); margin-bottom: var(--spacing);'>
    <h4>{title}</h4>
    {content}
</div>"""


def render_business_grid(cards: list) -> str:
    """Render a grid of business cards."""
    html = "<div class='section'><div class='container'><div class='business-grid'>"
    for card in cards:
        html += render_business_card(card.get("title", ""), card.get("content", ""))
    html += "</div></div></div>"
    return html


def render_contact_form(form_action: str) -> str:
    """Render the contact form."""
    return f"""<form action="{form_action}" method="POST" style="max-width: 600px; margin: 2rem 0;">
    <div style="margin-bottom: 1rem;">
        <label for="name" style="display: block; margin-bottom: 0.5rem; font-weight: bold;">Navn:</label>
        <input type="text" id="name" name="name" required style="width: 100%; padding: 0.5rem; border: 1px solid #ddd; border-radius: 4px; font-family: inherit;">
    </div>
    <div style="margin-bottom: 1rem;">
        <label for="email" style="display: block; margin-bottom: 0.5rem; font-weight: bold;">Email:</label>
        <input type="email" id="email" name="email" required style="width: 100%; padding: 0.5rem; border: 1px solid #ddd; border-radius: 4px; font-family: inherit;">
    </div>
    <div style="margin-bottom: 1rem;">
        <label for="subject" style="display: block; margin-bottom: 0.5rem; font-weight: bold;">Emne:</label>
        <input type="text" id="subject" name="subject" required style="width: 100%; padding: 0.5rem; border: 1px solid #ddd; border-radius: 4px; font-family: inherit;">
    </div>
    <div style="margin-bottom: 1rem;">
        <label for="message" style="display: block; margin-bottom: 0.5rem; font-weight: bold;">Besked:</label>
        <textarea id="message" name="message" rows="6" required style="width: 100%; padding: 0.5rem; border: 1px solid #ddd; border-radius: 4px; font-family: inherit;"></textarea>
    </div>
    <button type="submit" style="background-color: #1e5a96; color: white; padding: 0.75rem 1.5rem; border: none; border-radius: 4px; font-size: 1rem; cursor: pointer; font-weight: bold;">Send besked</button>
</form>
<p><small><em>Bemærk: Du skal selv opsætte Formspree-URL'en ovenfor for at aktivere kontaktformularen. Se dokumentation for detaljer.</em></small></p>"""


def render_scroll_to_top_button() -> str:
    """Render the scroll-to-top button."""
    return """<button id="scrollToTop" aria-label="Tilbage til toppen">↑</button>"""


def render_footer(navigation_links: list, last_updated: str) -> str:
    """
    Render the footer with navigation links and last updated date.
    
    navigation_links: list of dicts with 'title' and 'url' keys
    last_updated: formatted date string
    """
    html = """<footer>
        <div class="container">
            <div class="footer-section">
                <h3>Løvel</h3>
                <p>Løvel - lige i nærheden</p>
                <p><a href="mailto:support@lovel.dk">support@lovel.dk</a></p>
            </div>
            
            <div class="footer-section">
                <h3>Navigation</h3>
                <ul class="footer-nav">
"""
    for link in navigation_links:
        html += f'                    <li><a href="{link["url"]}">{link["title"]}</a></li>\n'
    
    html += f"""                </ul>
            </div>
            
            <div class="footer-section footer-info">
                <p><small>Sidst opdateret: {last_updated}</small></p>
            </div>
        </div>
    </footer>
"""
    return html


def render_navbar(pages: dict, root_path: str, is_home: bool) -> str:
    """
    Render the navigation bar.
    
    pages: dict of all pages organized by category
    root_path: relative path to site root
    is_home: whether this is the home page
    """
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
        # Custom sort order for dagtilbud
        dagtilbud_order = [
            'dagtilbud/vuggestue',
            'dagtilbud/dagpleje',
            'dagtilbud/boernehave',
            'dagtilbud/skole'
        ]
        sorted_dagtilbud = [k for k in dagtilbud_order if k in dagtilbud_pages]
        
        nav += """                    <li class="dropdown">
                        <a href="#" class="dropdown-toggle">Dagtilbud</a>
                        <ul class="dropdown-menu">
"""
        for page_id in sorted_dagtilbud:
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
    
    # Top-level pages (Film, Erhverv)
    nav += f"""                    <li><a href="{root_path}erhverv.html">Erhverv</a></li>
                    <li><a href="{root_path}film.html">Film</a></li>
                </ul>
            </div>
        </div>
    </nav>
"""
    return nav
