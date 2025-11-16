# Quick Start Guide

## Getting Started in 5 Minutes

### 1. **View the Website**

```bash
# Start a local server
cd /home/hrindom/lovel.dk
python3 -m http.server 8000

# Open in browser: http://localhost:8000
```

### 2. **Edit Content**

All content lives in one file:

```bash
# Open the content file
nano src/site-data.json

# Make your changes, save, exit
```

### 3. **Rebuild the Site**

```bash
# Generate HTML from your changes
python3 src/build.py

# All pages updated! ✅
```

### 4. **See Your Changes**

Refresh your browser at `http://localhost:8000`

---

## Common Tasks

### Adding a New Page

1. Edit `src/site-data.json`
2. Add new page entry:

```json
{
  "pages": {
    "min-nye-side": {
      "title": "Min Nye Side",
      "description": "Beskrivelse af siden",
      "sections": [
        {
          "type": "header",
          "title": "Velkommen"
        },
        {
          "type": "text",
          "content": "<p>Dit indhold her</p>"
        }
      ]
    }
  }
}
```

3. Run `python3 src/build.py`
4. Page is now at: `min-nye-side.html` (or subdirectories for nested pages)

### Updating Content

1. Find the page ID in `src/site-data.json`
2. Edit the content in the `sections` array
3. Run `python3 src/build.py`
4. Done!

### Adding Images

1. Place image in `media/` folder
2. Reference in JSON with: `"src": "media/your-image.jpg"`
3. Run build script

### Changing Colors/Style

Edit `assets/styles.css`:

```css
:root {
    --primary: #e0f7b6;        /* Change brand color here */
    --text: #000;              /* Text color */
    --bg: #fff;                /* Background */
}
```

### Creating Two-Column Layouts

```json
{
  "type": "content",
  "layout": "two-col",
  "columns": [
    {
      "type": "image",
      "src": "media/image.jpg"
    },
    {
      "type": "text",
      "content": "<h2>Title</h2><p>Text content</p>"
    }
  ]
}
```

---

## File Structure

```
📁 lovel.dk/
├── 📄 index.html              ← Homepage (GENERATED)
├── 📄 erhverv.html            ← Business (GENERATED)
├── 📄 film.html               ← Film (GENERATED)
│
├── 📁 src/                    ← SOURCE FILES (edit these)
│   ├── build.py               ← Build script
│   ├── site-data.json         ← ⭐ ALL CONTENT HERE
│   └── template.html          ← Reference template
│
├── 📁 assets/
│   └── styles.css             ← Styling
│
├── 📁 media/                  ← Images & media
│   └── 1009/
│       └── forside.jpg
│
├── 📁 dagtilbud/
│   ├── dagpleje/index.html    ← GENERATED
│   ├── vuggestue/index.html   ← GENERATED
│   └── ...
│
├── 📁 foreninger/
│   ├── luif/index.html        ← GENERATED
│   └── ...
│
└── 📁 informationer/
    ├── placering/index.html   ← GENERATED
    └── ...
```

**Key:** Only edit files in `src/` folder!

---

## Workflow

```
┌─────────────────────────┐
│ 1. Edit site-data.json  │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ 2. Run build.py         │
│    python3 src/build.py │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ 3. HTML files generated │
│    (all pages updated)  │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ 4. Refresh browser      │
│    See your changes ✅  │
└─────────────────────────┘
```

---

## Section Types

### header
Large section header with title
```json
{
  "type": "header",
  "title": "Section Title"
}
```

### text
HTML text content
```json
{
  "type": "text",
  "content": "<h2>Title</h2><p>Paragraph</p>"
}
```

### content
Two-column or single column layout
```json
{
  "type": "content",
  "layout": "two-col",
  "columns": [
    { "type": "text", "content": "..." },
    { "type": "image", "src": "..." }
  ]
}
```

### image
Standalone image
```json
{
  "type": "image",
  "src": "media/image.jpg",
  "alt": "Image description"
}
```

---

## HTML Structure

Each generated page includes:

- ✅ Semantic HTML5 markup
- ✅ Mobile-responsive design
- ✅ Navigation menu with dropdowns
- ✅ Sticky header
- ✅ Footer with contact info
- ✅ Proper meta tags for SEO
- ✅ Clean, minimal CSS

---

## Troubleshooting

### Images not showing?
- Check path in JSON: `"src": "media/..."`
- Ensure image exists in `media/` folder
- Path is relative to root

### Links not working?
- Check page ID in JSON matches file structure
- Ensure page exists in site-data.json
- Run build.py to regenerate

### Styling looks wrong?
- Clear browser cache (Ctrl+Shift+Delete)
- Check `assets/styles.css` for CSS errors
- Verify responsive breakpoints on mobile

### Build fails?
- Check JSON syntax (valid JSON?)
- Ensure all required fields present
- Look for Python error messages

---

## Tips

1. **Backup first** - Keep backup of site-data.json
2. **One change at a time** - Make small changes, test
3. **Use consistent formatting** - Keep JSON clean
4. **Test on mobile** - Check responsive design
5. **Keep it simple** - Stick to standard section types

---

## Next Steps

- [ ] Review site structure in `src/site-data.json`
- [ ] Add content for all pages
- [ ] Test all links and navigation
- [ ] Verify mobile responsiveness
- [ ] Deploy to your web server

---

## Support

For help with specific pages, check:
- `README.md` - Full documentation
- `ARCHITECTURE.md` - Technical details
- `REIMPLEMENTATION.md` - What changed

**Happy editing! 🚀**
