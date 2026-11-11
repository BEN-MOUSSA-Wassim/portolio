"""Dependency-free structural checks for the static portfolio."""

from __future__ import annotations

import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.headings: list[tuple[str, dict[str, str]]] = []
        self.images: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.assets: list[str] = []
        self.lang = ""
        self.meta_names: set[str] = set()
        self.meta_properties: set[str] = set()
        self.canonical = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value or "" for key, value in attrs}
        if tag == "html":
            self.lang = data.get("lang", "")
        if element_id := data.get("id"):
            self.ids.append(element_id)
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.headings.append((tag, data))
        if tag == "img":
            self.images.append(data)
            if data.get("src"):
                self.assets.append(data["src"])
        if tag == "a":
            self.links.append(data)
        if tag in {"script", "link", "source"}:
            for key in ("src", "href", "srcset"):
                if data.get(key):
                    self.assets.append(data[key])
        if tag == "meta":
            if data.get("name"):
                self.meta_names.add(data["name"])
            if data.get("property"):
                self.meta_properties.add(data["property"])
        if tag == "link" and data.get("rel") == "canonical":
            self.canonical = data.get("href", "")


def local_path(reference: str) -> Path | None:
    reference = reference.split()[0]
    parsed = urlparse(reference)
    if parsed.scheme or reference.startswith(("#", "mailto:", "tel:")):
        return None
    clean = unquote(parsed.path).lstrip("/")
    return ROOT / clean


def main() -> int:
    failures: list[str] = []
    parser = SiteParser()
    html = INDEX.read_text(encoding="utf-8")
    parser.feed(html)

    if parser.lang != "en":
        failures.append("The document language must be English.")
    if len([tag for tag, _ in parser.headings if tag == "h1"]) != 1:
        failures.append("The page must contain exactly one h1.")
    if len(parser.ids) != len(set(parser.ids)):
        failures.append("Duplicate element IDs detected.")

    missing_alt = [image.get("src", "<inline>") for image in parser.images if not image.get("alt")]
    if missing_alt:
        failures.append(f"Images missing alt text: {', '.join(missing_alt)}")

    for link in parser.links:
        href = link.get("href", "")
        if not href:
            failures.append("Anchor without href detected.")
        if href.startswith("#") and href[1:] not in parser.ids:
            failures.append(f"Broken page fragment: {href}")
        if link.get("target") == "_blank" and "noopener" not in link.get("rel", "").split():
            failures.append(f"External target missing noopener: {href}")

    for reference in parser.assets + [link.get("href", "") for link in parser.links]:
        path = local_path(reference)
        if path and not path.exists():
            failures.append(f"Missing local file: {reference}")

    required_meta = {"description", "viewport", "theme-color", "twitter:card"}
    missing_meta = required_meta - parser.meta_names
    if missing_meta:
        failures.append(f"Missing metadata: {', '.join(sorted(missing_meta))}")

    required_og = {"og:title", "og:description", "og:image", "og:url"}
    missing_og = required_og - parser.meta_properties
    if missing_og:
        failures.append(f"Missing Open Graph metadata: {', '.join(sorted(missing_og))}")
    if not parser.canonical.startswith("https://"):
        failures.append("Canonical URL must use HTTPS.")
    if "C:\\" in html or "C:/" in html:
        failures.append("Local Windows path detected in the public page.")

    manifest = json.loads((ROOT / "site.webmanifest").read_text(encoding="utf-8"))
    if not manifest.get("name") or not manifest.get("icons"):
        failures.append("Web manifest is incomplete.")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print(f"PASS: {len(parser.headings)} headings, {len(parser.images)} images, {len(parser.links)} links")
    print(f"PASS: {len(set(parser.assets))} referenced asset declarations resolve")
    print("PASS: metadata, canonical URL, manifest, fragments, alt text, and target safety")
    return 0


if __name__ == "__main__":
    sys.exit(main())
