---
applyTo: "**"
---
# Project Introduction for LLM Conversations

## Project Overview
This project is a static website for the village of Løvel, Viborg Kommune. It provides information about local institutions, associations, events, and practical details for residents and visitors.

## Folder Structure
- `/dagtilbud/` — Childcare and school pages (vuggestue, børnehave, dagpleje, skole)
- `/foreninger/` — Local associations and clubs (e.g., LUIF, seniorforening, borgerforening)
- `/informationer/` — Practical information (vandværk, byfest, placering, byens løve)
- `/film/` — Local film and media
- `/media/` — Images and videos, organized by category (dagtilbud, foreninger, informationer, shared/general, shared/logos, film, erhverv)

## Data Source
- All page content is stored in `/src/site-data.json` under the `"pages"` key.
- Each page uses a unique key (e.g., `"dagtilbud/vuggestue"`) and contains structured sections, images, and metadata.

## Build System
- The build script (`build.py`) reads `site-data.json` and generates static HTML files.
- Pages are generated into folders matching their keys (e.g., `/foreninger/luif/index.html`).
- Media references in JSON use relative paths (e.g., `media/foreninger/fodbold.jpg`).

## Conventions
- Images are stored in `/media/` subfolders by category.
- Navigation is generated dynamically from `site-data.json`.
- New pages or sections should be added to `site-data.json` and referenced in the appropriate folder.
- For slideshows, use a section with `"type": "slideshow"` and an `"images"` array.

## Recent Features
- Slideshow support on the Film page (auto-play, 5s interval, container width).
- Improved media folder structure for easier maintenance.
- All associations and information pages are now included in `site-data.json`.

## How to Extend
- Add new content by updating `site-data.json` and placing images in the correct `/media/` subfolder.
- For new page types or layouts, update both the JSON and the build script as needed.

## Contact
For questions about structure, conventions, or extending the project, refer to this file or ask for clarification.

---

*This file is intended for future LLM conversations to provide quick context and ensure consistent, high-quality assistance.*