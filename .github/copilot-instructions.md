---
applyTo: "**"
---
# Løvel Website Project — Complete Guide

Welcome! This document provides complete context for working on the **løvel.dk** website.

---

## 📋 Project Overview

**løvel.dk** is a static website for the village of Løvel, Viborg Kommune. It provides information about:
- Childcare facilities (dagtilbud)
- Local organizations & sports clubs (foreninger)
- Community information
- Local businesses (erhverv)
- Media gallery

**Technology Stack:**
- **Python** — Static site generator (`build.py`)
- **JSON** — Configuration file (`site-data.json`)
- **HTML/CSS/JavaScript** — Front-end (vanilla, no frameworks)
- **Responsive Design** — Mobile-first approach

---

## 🏗️ Architecture at a Glance

The site uses a **three-layer architecture**:

```
src/site-data.json (data)
        ↓
src/page_builder.py (logic) → calculates paths, metadata
        ↓
src/html_generator.py (rendering) → creates HTML from metadata
        ↓
src/build.py (orchestration) → coordinates everything
        ↓
20+ HTML pages (output)
```

**Key Files:**
- `src/site-data.json` — All page content (titles, descriptions, sections, images)
- `src/page_builder.py` — Business logic (path calculations, metadata generation)
- `src/html_generator.py` — HTML rendering from structured data
- `src/templates.py` — Reusable HTML components
- `src/build.py` — Orchestrates the build process
- `assets/styles.css` — All styling

---

## 📂 Project Structure

```
lovel_hjemmeside_repo_new/
├── .github/
│   └── copilot-instructions.md  ← You are here
├── src/
│   ├── build.py                 → Main orchestration script
│   ├── page_builder.py           → Logic (no HTML)
│   ├── html_generator.py         → Rendering (no logic)
│   ├── templates.py              → HTML components
│   └── site-data.json            → All page content
├── assets/
│   └── styles.css                → All styling
├── media/                        → Images for pages
│   ├── dagtilbud/
│   ├── foreninger/
│   ├── informationer/
│   ├── film/
│   ├── Galleri/
│   └── shared/
├── dagtilbud/                    → Generated pages
│   ├── boernehave/
│   ├── dagpleje/
│   ├── skole/
│   └── vuggestue/
├── foreninger/                   → Generated pages
│   ├── amatoerscenen/
│   ├── luif/
│   └── (8+ other associations)
├── informationer/                → Generated pages
│   ├── byens-loeve/
│   ├── byfest/
│   ├── byggegrunde/
│   ├── huse-til-salg/
│   ├── placering/
│   └── vandvaerket/
├── index.html                    → Generated home page
├── erhverv.html                  → Generated businesses page
├── medier.html                   → Generated media page
└── README.md
```

---

## 📝 Folder Structure Overview

- `/dagtilbud/` — Childcare and school pages (vuggestue, børnehave, dagpleje, skole)
- `/foreninger/` — Local associations and clubs (e.g., LUIF, seniorforening, borgerforening)
- `/informationer/` — Practical information (vandværk, byfest, placering, byens løve)
- `/media/` — Images and videos, organized by category (dagtilbud, foreninger, informationer, shared/general, shared/logos, film, erhverv)

---

## 💾 Data Source

**All page content is stored in `/src/site-data.json`**

Each page object uses a unique key (e.g., `"dagtilbud/vuggestue"`) and contains:
- `title` — Page title
- `description` — Meta description for search engines
- `hero_image` — Hero/banner image path
- `sections` — Array of content sections

**Example page structure:**

```json
{
  "title": "Page Title",
  "description": "Meta description for search engines",
  "hero_image": "path/to/image.jpg",
  "sections": [
    {
      "type": "header",
      "title": "Section Header",
      "id": "section-id",
      "collapsible": true
    },
    {
      "type": "text",
      "paragraphs": [
        "Paragraph 1",
        "Paragraph 2"
      ],
      "id": "section-id",
      "collapsible": true
    }
  ]
}
```

**Available section types:**
- `header` — Collapsible header
- `text` — Text paragraphs
- `images` — Image grid/gallery
- `button` — Call-to-action button
- `slideshow` — Auto-playing image carousel (5s interval)

---

## 🚀 Quick Start

### Build the site:
```bash
cd c:\Users\...\lovel_hjemmeside_repo_new
python src/build.py
```

This generates 20+ HTML files in the appropriate directories.

### View locally:
The build script serves on port 8000 — open http://localhost:8000

---

## 📌 Common Tasks

### Add a new page:
1. Edit `src/site-data.json` — add your page object with `title`, `description`, `sections`
2. Run `python src/build.py` — it automatically calculates paths and generates HTML

### Update page content:
1. Edit `src/site-data.json` — modify the relevant page's `sections`
2. Run `python src/build.py`

### Change styling:
1. Edit `assets/styles.css`
2. Run `python src/build.py` (CSS is copied to output)

### Add a new organization/activity:
1. Edit the relevant page in `src/site-data.json` (e.g., `foreninger/luif`)
2. Add sections with `type: "header"`, `type: "text"`, etc.
3. Run `python src/build.py`

---

## 🔍 Understanding the Build Process

1. **Data Input** — `site-data.json` loaded with all page definitions
2. **Logic Layer** — `page_builder.py` processes data:
   - Calculates relative paths (`../../assets/styles.css`)
   - Determines output locations
   - Builds metadata dictionaries
3. **Rendering Layer** — `html_generator.py` generates HTML:
   - Renders sections based on type
   - Creates navigation
   - Adds responsive structure
4. **Orchestration** — `build.py` coordinates everything:
   - Loops through all pages
   - Calls logic layer → rendering layer
   - Writes HTML files to disk

---

## ⚙️ Current Features

- ✅ **20+ pages** generated from single JSON config
- ✅ **Collapsible sections** with smooth animations
- ✅ **Responsive design** (mobile to desktop)
- ✅ **Image galleries** with lightbox
- ✅ **Slideshow support** (auto-play, 5s interval)
- ✅ **Danish date formatting** (auto-updated)
- ✅ **Clean CSS** with CSS variables for theming
- ✅ **Semantic HTML** with proper accessibility

---

## 🛠️ Conventions

- Images are stored in `/media/` subfolders by category
- Navigation is generated dynamically from `site-data.json`
- New pages or sections should be added to `site-data.json` and referenced in the appropriate folder
- For slideshows, use a section with `"type": "slideshow"` and an `"images"` array
- Media references in JSON use relative paths (e.g., `media/foreninger/fodbold.jpg`)
- Pages are generated into folders matching their keys (e.g., `/foreninger/luif/index.html`)

---

## 🐛 Debugging Tips

**Pages not generating?**
- Check `src/site-data.json` for syntax errors (missing commas, brackets)
- Verify all section `type` values are valid

**Styling looks wrong?**
- Check `assets/styles.css` for CSS variable definitions
- Look for typos in class names in `html_generator.py`

**Build fails?**
- Check Python syntax: `python -m py_compile src/build.py`
- Verify JSON syntax: `python -m json.tool src/site-data.json`

---

## 📌 Key Info

**Recent Updates:**
- Slideshow support on the Film page (auto-play, 5s interval, container width)
- Improved media folder structure for easier maintenance
- All associations and information pages included in `site-data.json`
- Contact information for activities organized into dedicated sections
- Gallery CSS refined for better responsive behavior
- Collapsible section headers styled for better readability
- Multiple LUIF activities documented (10+ afdelinger)

**Important Pages:**
- Home: `/` (index.html)
- LUIF Activities: `/foreninger/luif/`
- Childcare: `/dagtilbud/`
- Information: `/informationer/`
- Businesses: `/erhverv.html`
- Media: `/medier.html`

---

## 💡 Best Practices

- Always run `python src/build.py` after changes
- Keep `site-data.json` indentation consistent (2 spaces)
- Use meaningful `id` values for sections (lowercase, hyphenated)
- Test on mobile devices to verify responsive design
- Use relative paths for media (`media/folder/image.jpg`)

---

## 🔗 External Resources

- LUIF website: http://www.luif.minisite.dk/
- Local information: Check `/informationer/` pages
- Image assets: See `/media/` directory structure

---

*This file is intended for LLM conversations to provide context and ensure consistent, high-quality assistance.*