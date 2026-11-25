# Løvel.dk

Løvel.dk is a static community website. The page content lives in
`src/site-data.json`. The Python builder renders it into HTML in the repository
root and the `dagtilbud/`, `foreninger/`, and `informationer/` directories.
Shared styles live in `assets/styles.css` and public media lives in `media/`.

## Update and preview

1. Edit `src/site-data.json` for content or the Python templates under `src/`
   for shared markup and behavior.
2. Run `python3 src/build.py` from the repository root.
3. Run `python3 -m http.server 8000` and open
   [the local preview](http://localhost:8000/).
4. Stage the source changes, generated HTML, and any new assets, then run
   `python3 src/check_site.py`. The check uses Git to identify public files.

Use Python 3.9 or newer. The builder is deterministic and has no Python package
dependencies. If you remove or rename a page, retire the old generated file
explicitly. Keep a redirect for an existing URL when its content has moved.

## Publishing

Open a pull request with both the source changes and generated HTML.
The **Validate site** workflow checks that generated pages match the source,
reports unexpected HTML, and checks local page and asset references. Merge
after the check passes. The custom domain is declared in `CNAME`. The workflow
validates the checked-in files and leaves the hosting configuration in place.

The old LRV-Skals Håndbold URL is intentionally kept as a redirect to LUIF.
It is a hand-maintained exception to the generated pages.
