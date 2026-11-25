"""Check the files published from the repository root."""

from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urljoin, urlsplit

from build import SITE_DATA, SITE_ROOT
from html_generator import render_complete_page
from page_builder import build_page_metadata, get_output_file


LEGACY_PAGES = {"foreninger/haandbold-lrv-skals/index.html"}


class LocalReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.urls.extend(attrs[key] for key in ("href", "src") if attrs.get(key))
        self.urls.extend(re.findall(r"url\(['\"]?([^)'\"]+)", attrs.get("style") or ""))
        if tag == "meta" and attrs.get("http-equiv") == "refresh":
            _, separator, url = (attrs.get("content") or "").partition("url=")
            if separator:
                self.urls.append(url.strip())


def check_site():
    tracked = subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=SITE_ROOT, text=True, encoding="utf-8",
    )
    files = set(tracked.rstrip("\0").split("\0"))
    expected = set(LEGACY_PAGES)
    missing_redirects = LEGACY_PAGES - files
    errors = [f"Missing legacy page: {name}" for name in sorted(missing_redirects)]

    pages = SITE_DATA["pages"]
    for page_id, data in pages.items():
        path = get_output_file(page_id, SITE_ROOT)
        name = path.relative_to(SITE_ROOT).as_posix()
        expected.add(name)
        rendered = render_complete_page(build_page_metadata(page_id, data, SITE_DATA), pages)
        if name not in files or not path.is_file() or path.read_text(encoding="utf-8") != rendered:
            errors.append(f"Regenerate and stage {name}")

    html_files = {name for name in files if name.endswith(".html")}
    errors.extend(f"Unexpected HTML page: {name}" for name in sorted(html_files - expected))
    for name in sorted(html_files):
        path = SITE_ROOT / name
        if not path.is_file():
            errors.append(f"Missing tracked page: {name}")
            continue
        parser = LocalReferences()
        parser.feed(path.read_text(encoding="utf-8"))
        public_path = name.removesuffix("index.html") if Path(name).name == "index.html" else name
        for reference in parser.urls:
            if reference.startswith(("#", "//")) or urlsplit(reference).scheme:
                continue
            target = unquote(urlsplit(urljoin("https://lovel.dk/" + public_path, reference)).path)
            target = target.lstrip("/")
            if not target or target.endswith("/"):
                target += "index.html"
            if target not in files or not (SITE_ROOT / target).is_file():
                errors.append(f"{name}: missing local reference {reference!r}")

    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Validated {len(html_files)} pages and their local links.")


if __name__ == "__main__":
    check_site()
