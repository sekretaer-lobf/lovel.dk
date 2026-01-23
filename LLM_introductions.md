# Løvel Website Project — Quick Start Guide

Welcome! This document provides essential context for working on the **løvel.dk** website.

---

## 📋 Project Overview

**løvel.dk** is a static website for the town of Løvel, Denmark. It features information about:
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
20 HTML pages (output)
```

**Key Files:**
- `src/site-data.json` — All page content (titles, descriptions, sections, images)
- `src/page_builder.py` — Business logic (path calculations, metadata generation)
- `src/html_generator.py` — HTML rendering from structured data
- `src/templates.py` — Reusable HTML components
- `src/build.py` — Orchestrates the build process
- `assets/styles.css` — All styling

---

## 🚀 Quick Start

### Build the site:
```bash
cd /home/hrindom/lovel.dk
python3 src/build.py
```

This generates 20 HTML files in the appropriate directories.

### View locally:
```bash
# The build.py serves on port 8000
# Open: http://localhost:8000
```

---

## 📝 Common Tasks

### Add a new page:
1. Edit `src/site-data.json` — add your page object with `title`, `description`, `sections`
2. Run `python3 src/build.py` — it automatically calculates paths and generates HTML

### Update page content:
1. Edit `src/site-data.json` — modify the relevant page's `sections`
2. Run `python3 src/build.py`

### Change styling:
1. Edit `assets/styles.css`
2. Run `python3 src/build.py` (CSS is copied to output)

### Add a new organization/activity:
1. Edit the relevant page in `src/site-data.json` (e.g., `foreninger/luif`)
2. Add sections with `type: "header"`, `type: "text"`, etc.
3. Run `python3 src/build.py`

---

## 🎨 Content Structure (site-data.json)

Each page has this structure:
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

## 📂 Project Structure

```
/home/hrindom/lovel.dk/
├── src/
│   ├── build.py              → Main orchestration script
│   ├── page_builder.py        → Logic (no HTML)
│   ├── html_generator.py      → Rendering (no logic)
│   ├── templates.py           → HTML components
│   └── site-data.json         → All page content
├── assets/
│   └── styles.css             → All styling
├── media/                     → Images for pages
├── foreninger/                → Generated pages
├── dagtilbud/                 → Generated pages
├── informationer/             → Generated pages
└── index.html                 → Generated home page
```

---

## ⚙️ Current Features

- ✅ **20+ pages** generated from single JSON config
- ✅ **Collapsible sections** with smooth animations
- ✅ **Responsive design** (mobile to desktop)
- ✅ **Image galleries** with lightbox
- ✅ **Danish date formatting** (auto-updated)
- ✅ **Clean CSS** with CSS variables for theming
- ✅ **Semantic HTML** with proper accessibility

---

## 🐛 Debugging Tips

**Pages not generating?**
- Check `src/site-data.json` for syntax errors (missing commas, brackets)
- Verify all section `type` values are valid

**Styling looks wrong?**
- Check `assets/styles.css` for CSS variable definitions
- Look for typos in class names in `html_generator.py`

**Build fails?**
- Check Python syntax: `python3 -m py_compile src/build.py`
- Verify JSON syntax: `python3 -m json.tool src/site-data.json`

---

## 📌 Key Contacts & Info

**Recent Updates:**
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

- Always run `python3 src/build.py` after changes
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

**Last Updated:** January 23, 2026

Start by reviewing `src/site-data.json` to understand the current content structure, then check `src/build.py` to see how everything ties together.
