#!/usr/bin/env python3
"""Semantic, fail-closed checks for the temporary MCL v1.x withdrawal state."""

from __future__ import annotations

import hashlib
import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from typing import TypedDict
from urllib.parse import unquote, urljoin, urlparse


ROOT = Path(__file__).resolve().parents[1]
MCL = ROOT / "guidelines" / "mcl" / "index.html"
GUIDELINES = ROOT / "guidelines.html"
TOOLS = ROOT / "tools.html"
SITEMAP = ROOT / "sitemap.xml"
WORKFLOW = ROOT / ".github" / "workflows" / "preflight.yml"
WORKER = ROOT / "_worker.js"
ROUTES = ROOT / "_routes.json"
SITE_SHELL_CSS = ROOT / "assets" / "site-shell.css"
PRINT_CSS = ROOT / "print.css"
COOKIE_BANNER_JS = ROOT / "legal" / "cookie-banner.js"

WITHDRAWAL = "Withdrawn pending controlled update"
PROHIBITION = (
    "Do not use this withdrawn version for treatment selection, prescribing, "
    "commissioning, consent or referral decisions."
)
ARCHIVE_NOTICE = (
    "The previous downloadable DOCX, PDF and visual algorithms have been withdrawn "
    "from active use because they did not form a concordant controlled release family."
)
OLD_CONTENT_IDS = {"summary", "mdt-tools", "visual-support", "firstline", "rr", "commissioning"}
DOWNLOAD_SUFFIXES = (".docx", ".pdf", ".svg", ".excalidraw", ".png")
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
EXPECTED_MCL_INLINE_CSS_SHA256 = "959b1535a2eaa9a8050febfa2624c1fffd13f4b010cf8ba9df8efc1ba76fc971"
EXPECTED_SITE_SHELL_CSS_SHA256 = "044bf57dc0061a953733c3ae80ade81cfaf8aa2635397d8ba3ec4f64d86af8f3"
EXPECTED_PRINT_CSS_SHA256 = "7ff858f2f8bd38af816a139a72f0b2eb29f1c16bf8e9a81bcd9f01998cb5c738"
EXPECTED_COOKIE_BANNER_JS_SHA256 = "9c118967c5f41881b382ba46379521c4bd8d45e2645f3bfcff34e6a64182eafe"
EXPECTED_HUB_STYLESHEET_ATTRIBUTES = (
    {
        "rel": "stylesheet",
        "href": "https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700;800&display=swap",
    },
    {"rel": "stylesheet", "href": "/assets/site-shell.css"},
    {"rel": "stylesheet", "href": "/print.css", "media": "print"},
)
EXPECTED_HUB_SCRIPT_ATTRIBUTES = ({"src": "/legal/cookie-banner.js", "defer": ""},)
EXPECTED_PUBLISHED_GUIDELINES = {
    "/guidelines/anaemia-in-pregnancy",
    "/guidelines/cll",
    "/guidelines/itp",
    "/guidelines/myeloma",
    "/guidelines/vte-cancer",
}
WITHDRAWN_PUBLIC_PATHS = (
    "/guidelines/mcl/guideline.docx",
    "/guidelines/mcl/guideline.pdf",
    "/assets/figures/mcl-access-status-chart.excalidraw",
    "/assets/figures/mcl-access-status-chart.png",
    "/assets/figures/mcl-access-status-chart.svg",
    "/assets/figures/mcl-first-line-algorithm.excalidraw",
    "/assets/figures/mcl-first-line-algorithm.png",
    "/assets/figures/mcl-first-line-algorithm.svg",
    "/assets/figures/mcl-pathway-at-a-glance.excalidraw",
    "/assets/figures/mcl-pathway-at-a-glance.png",
    "/assets/figures/mcl-pathway-at-a-glance.svg",
    "/assets/figures/mcl-visuals.mmd",
    "/assets/pdfs/mcl-access-status-chart.pdf",
    "/assets/pdfs/mcl-first-line-algorithm.pdf",
    "/assets/pdfs/mcl-pathway-at-a-glance.pdf",
)


class ResourceCard(TypedDict):
    href: str
    hidden: bool
    is_card: bool
    published_badge: int


class SemanticHTML(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, bool]] = []
        self.elements: list[tuple[str, dict[str, str], bool]] = []
        self.links: list[tuple[str, bool]] = []
        self.resource_cards: list[ResourceCard] = []
        self._active_anchor: int | None = None
        self.orphan_published_badges = 0
        self.visible_text: list[str] = []
        self.metas: list[dict[str, str]] = []
        self.styles: list[str] = []
        self.json_scripts: list[str] = []
        self._capture_style = False
        self._capture_json = False
        self._buffer: list[str] = []

    @staticmethod
    def _self_hidden(attrs: dict[str, str]) -> bool:
        style = re.sub(r"\s+", "", attrs.get("style", "").casefold())
        return (
            "hidden" in attrs
            or attrs.get("aria-hidden", "").casefold() == "true"
            or "display:none" in style
            or "visibility:hidden" in style
            or "opacity:0" in style
        )

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.casefold()
        attr_map = {key.casefold(): (value or "") for key, value in attrs}
        hidden = (self.stack[-1][1] if self.stack else False) or tag == "template" or self._self_hidden(attr_map)
        if tag not in VOID_TAGS:
            self.stack.append((tag, hidden))
        self.elements.append((tag, attr_map, hidden))
        if tag == "meta":
            self.metas.append(attr_map)
        if tag == "a":
            self.links.append((attr_map.get("href", ""), hidden))
            self.resource_cards.append(
                {
                    "href": attr_map.get("href", ""),
                    "hidden": hidden,
                    "is_card": "card" in attr_map.get("class", "").split(),
                    "published_badge": 0,
                }
            )
            self._active_anchor = len(self.resource_cards) - 1
        if tag == "span" and not hidden and "badge-live" in attr_map.get("class", "").split():
            if self._active_anchor is not None and self.resource_cards[self._active_anchor]["is_card"]:
                self.resource_cards[self._active_anchor]["published_badge"] += 1
            else:
                self.orphan_published_badges += 1
        if tag == "style":
            self._capture_style = True
            self._buffer = []
        if tag == "script" and attr_map.get("type", "").casefold() == "application/ld+json":
            self._capture_json = True
            self._buffer = []

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag.casefold() not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() == "style" and self._capture_style:
            self.styles.append("".join(self._buffer))
            self._capture_style = False
            self._buffer = []
        elif tag.casefold() == "script" and self._capture_json:
            self.json_scripts.append("".join(self._buffer))
            self._capture_json = False
            self._buffer = []
        tag = tag.casefold()
        if tag == "a":
            self._active_anchor = None
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data: str) -> None:
        if self._capture_style or self._capture_json:
            self._buffer.append(data)
        elif not (self.stack[-1][1] if self.stack else False):
            self.visible_text.append(data)


def parse_html(text: str) -> SemanticHTML:
    parser = SemanticHTML()
    parser.feed(text)
    parser.close()
    return parser


def normalise_path(href: str, base: str) -> str:
    path = unquote(urlparse(urljoin(base, href)).path)
    if path.endswith("/index.html"):
        path = path[: -len("index.html")]
    return path.rstrip("/") or "/"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate(mcl: str, guidelines: str, tools: str, sitemap: str, workflow: str, worker: str, routes: str, site_css: str, print_css: str, cookie_js: str) -> None:
    mcl_doc = parse_html(mcl)
    guidelines_doc = parse_html(guidelines)
    tools_doc = parse_html(tools)
    require(hashlib.sha256(site_css.encode()).hexdigest() == EXPECTED_SITE_SHELL_CSS_SHA256, "Linked site stylesheet integrity check failed")
    require(hashlib.sha256(print_css.encode()).hexdigest() == EXPECTED_PRINT_CSS_SHA256, "Linked print stylesheet integrity check failed")
    require(hashlib.sha256(cookie_js.encode()).hexdigest() == EXPECTED_COOKIE_BANNER_JS_SHA256, "Linked cookie script integrity check failed")

    robots = [meta.get("content", "") for meta in mcl_doc.metas if meta.get("name", "").casefold() == "robots"]
    require(len(robots) == 1, "MCL page must contain exactly one robots meta element")
    robots_tokens = {token.strip().casefold() for token in robots[0].split(",")}
    require(robots_tokens == {"noindex", "nofollow", "noarchive"}, "MCL robots metadata is not fail-closed")

    bodies = [attrs for tag, attrs, _ in mcl_doc.elements if tag == "body"]
    require(len(bodies) == 1 and "contained" in bodies[0].get("class", "").split(), "MCL body is not in containment mode")
    archives = [hidden for tag, attrs, hidden in mcl_doc.elements if tag == "template" and attrs.get("id") == "withdrawn-mcl-v1-archive"]
    require(archives == [True], "Legacy MCL markup is not isolated in a non-rendering template")
    for public_path in WITHDRAWN_PUBLIC_PATHS:
        require(not (ROOT / public_path.lstrip("/")).exists(), f"Withdrawn MCL file remains publicly deployable: {public_path}")

    json_objects = [json.loads(raw) for raw in mcl_doc.json_scripts]
    require(bool(json_objects), "MCL page has no JSON-LD withdrawal record")
    require(all(obj.get("@type") != "MedicalGuideline" for obj in json_objects if isinstance(obj, dict)), "MCL JSON-LD still identifies a MedicalGuideline")
    require(any(obj.get("@type") == "WebPage" and "withdrawn" in str(obj.get("reviewStatus", "")).casefold() for obj in json_objects if isinstance(obj, dict)), "MCL JSON-LD does not record withdrawal")

    containment = [attrs for tag, attrs, hidden in mcl_doc.elements if tag == "main" and attrs.get("id") == "main-content" and not hidden]
    require(len(containment) == 1, "The withdrawal notice is absent or hidden")
    containment_style = re.sub(r"\s+", "", containment[0].get("style", "").casefold())
    require(
        all(rule in containment_style for rule in ("display:block!important", "visibility:visible!important", "opacity:1!important")),
        "The withdrawal notice lacks its inline fail-closed visibility guard",
    )
    alerts = [attrs for tag, attrs, hidden in mcl_doc.elements if tag == "div" and attrs.get("role", "").casefold() == "alert" and not hidden]
    require(len(alerts) == 1, "The withdrawal alert is absent or hidden")
    alert_style = re.sub(r"\s+", "", alerts[0].get("style", "").casefold())
    require(
        all(rule in alert_style for rule in ("display:block!important", "visibility:visible!important", "opacity:1!important")),
        "The withdrawal alert lacks its inline fail-closed visibility guard",
    )
    visible = " ".join(" ".join(mcl_doc.visible_text).split())
    require(WITHDRAWAL.casefold() in visible.casefold(), "Visible withdrawal status is missing")
    require(PROHIBITION.casefold() in visible.casefold(), "Visible clinical-use prohibition is missing")
    require(ARCHIVE_NOTICE.casefold() in visible.casefold(), "Visible archive/download notice is missing")
    visible_casefold = visible.casefold()
    prohibited_publication_claims = (
        "this guideline remains published",
        "published for clinical",
        "published educational guideline",
        "guideline is published",
        "status: published",
    )
    require(not any(claim in visible_casefold for claim in prohibited_publication_claims), "Visible MCL page still claims an active published state")

    for tag, attrs, hidden in mcl_doc.elements:
        if attrs.get("id") in OLD_CONTENT_IDS:
            require(hidden, f"Legacy MCL content is visible: #{attrs['id']}")

    for href, hidden in mcl_doc.links:
        if hidden:
            continue
        path = normalise_path(href, "https://mohsinhaemacademy.com/guidelines/mcl/")
        require(not path.casefold().endswith(DOWNLOAD_SUFFIXES), f"Visible MCL download remains exposed: {href}")

    css = "\n".join(mcl_doc.styles)
    require(hashlib.sha256(css.encode()).hexdigest() == EXPECTED_MCL_INLINE_CSS_SHA256, "MCL containment CSS integrity check failed")
    compact_css = re.sub(r"\s+", "", css.casefold())
    require(re.search(r"\.contained\[hidden\]\{[^}]*display:none!important", compact_css) is not None, "Containment CSS does not force hidden legacy content off")
    for selector, declarations in re.findall(r"([^{}]+)\{([^{}]*)\}", compact_css):
        important_hiding = (
            "display:none!important" in declarations
            or "visibility:hidden!important" in declarations
            or "opacity:0!important" in declarations
        )
        if important_hiding:
            require(selector == ".contained[hidden]" and "display:none!important" in declarations, f"CSS can hide the withdrawal notice: {selector}")
        ordinary_hiding = "display:none" in declarations or "visibility:hidden" in declarations or "opacity:0" in declarations
        notice_selector_tokens = ("#main-content", ".containment-notice", ".containment-card", "[role=alert]", "[role=\"alert\"]", "containment-title", "main", ".contained")
        if ordinary_hiding and selector != ".contained[hidden]":
            require(not any(token in selector for token in notice_selector_tokens), f"CSS can hide the withdrawal notice: {selector}")
        if "!important" in declarations and re.search(r"display:(?!none)[^;]+!important", declarations):
            require(not any(token in selector for token in ("[hidden]", ".layout", ".hero", ".anchor-nav-wrap", ".governance-footer")), f"CSS can force legacy content visible: {selector}")
        if "containment" in selector:
            require("display:none" not in declarations and "visibility:hidden" not in declarations and "opacity:0" not in declarations, "CSS hides the containment notice")

    for document, base, surface in (
        (guidelines_doc, "https://mohsinhaemacademy.com/guidelines", "guidelines hub"),
        (tools_doc, "https://mohsinhaemacademy.com/tools", "tools hub"),
    ):
        for href, hidden in document.links:
            if not hidden:
                require(normalise_path(href, base) != "/guidelines/mcl", f"{surface} links to withdrawn MCL content: {href}")

    guideline_descriptions = [meta.get("content", "") for meta in guidelines_doc.metas if meta.get("name", "").casefold() == "description" or meta.get("property", "").casefold() == "og:description"]
    require(bool(guideline_descriptions), "Guidelines hub descriptions are missing")
    require(all("mantle cell lymphoma" not in value.casefold() for value in guideline_descriptions), "Guidelines hub metadata still describes MCL as published")
    guidelines_visible = " ".join(" ".join(guidelines_doc.visible_text).split()).casefold()
    require("mantle cell lymphoma" in guidelines_visible and "withdrawn pending controlled update" in guidelines_visible, "Guidelines hub does not show the MCL withdrawal state")

    for document, base, surface in (
        (guidelines_doc, "https://mohsinhaemacademy.com/guidelines", "Guidelines hub"),
        (tools_doc, "https://mohsinhaemacademy.com/tools", "Tools hub"),
    ):
        stylesheet_attributes = tuple(
            attrs
            for tag, attrs, hidden in document.elements
            if tag == "link" and not hidden and "stylesheet" in attrs.get("rel", "").casefold().split()
        )
        require(stylesheet_attributes == EXPECTED_HUB_STYLESHEET_ATTRIBUTES, f"{surface} linked stylesheet attributes, sequence or multiplicity are not controlled")
        require(not document.styles, f"{surface} contains an unapproved inline stylesheet")
        script_attributes = tuple(attrs for tag, attrs, hidden in document.elements if tag == "script" and not hidden)
        require(script_attributes == EXPECTED_HUB_SCRIPT_ATTRIBUTES, f"{surface} script attributes or multiplicity are not controlled")
        require(
            not any(attribute.startswith("on") for _, attrs, _ in document.elements for attribute in attrs),
            f"{surface} contains an event-handler attribute",
        )
        require(document.orphan_published_badges == 0, f"{surface} contains a published badge outside a resource card")
        for card in document.resource_cards:
            if not card["hidden"] and card["is_card"]:
                require(card["published_badge"] <= 1, f"{surface} contains duplicate published badges in one resource card")
        published_paths = [
            normalise_path(str(card["href"]), base)
            for card in document.resource_cards
            if not card["hidden"] and card["is_card"] and card["published_badge"] == 1
        ]
        require(len(published_paths) == len(set(published_paths)), f"{surface} contains duplicate published resource cards")
        require(all(path.startswith("/guidelines/") and path != "/guidelines/mcl" for path in published_paths), f"{surface} contains an invalid published resource card")
        require(set(published_paths) == EXPECTED_PUBLISHED_GUIDELINES, f"{surface} published resource set does not match the controlled library")
        published_badges = len(published_paths)
        surface_visible = " ".join(" ".join(document.visible_text).split()).casefold()
        require(
            f"{published_badges} published guidance resources" in surface_visible,
            f"{surface} published-resource count does not match its published cards",
        )

    root = ET.fromstring(sitemap)
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1] == "loc" and element.text:
            require(normalise_path(element.text, "https://mohsinhaemacademy.com/") != "/guidelines/mcl", "Sitemap still exposes withdrawn MCL content")

    active_workflow = "\n".join(line.split("#", 1)[0].rstrip() for line in workflow.splitlines() if not line.lstrip().startswith("#"))
    require(re.search(r"^\s*run:\s*python(?:3)?\s+scripts/validate_mcl_containment\.py\s*$", active_workflow, re.MULTILINE) is not None, "CI does not invoke the MCL containment validator as an active command")
    active_worker = re.sub(r"/\*.*?\*/", "", worker, flags=re.DOTALL)
    active_worker = "\n".join(line.split("//", 1)[0] for line in active_worker.splitlines() if not line.lstrip().startswith("//"))
    blocked_files_match = re.search(r"const\s+BLOCKED_FILES\s*=\s*new\s+Set\s*\(\s*\[(.*?)\]\s*\)", active_worker, re.DOTALL)
    if blocked_files_match is None:
        raise AssertionError("Worker BLOCKED_FILES declaration is missing")
    blocked_files = set(re.findall(r'["\']([^"\']+)["\']', blocked_files_match.group(1)))
    require(set(WITHDRAWN_PUBLIC_PATHS).issubset(blocked_files), "Worker does not fail closed for every withdrawn MCL file")

    routes_config = json.loads(routes)
    require(isinstance(routes_config, dict), "Cloudflare routes configuration must be an object")
    require(set(routes_config) == {"version", "include", "exclude"}, "Cloudflare routes configuration has an unexpected schema")
    require(routes_config["version"] == 1, "Cloudflare routes configuration version must be 1")
    require(isinstance(routes_config["include"], list) and all(isinstance(path, str) for path in routes_config["include"]), "Cloudflare include routes must be strings")
    require(routes_config["exclude"] == [], "Cloudflare routes must not bypass the containment worker")
    require(set(WITHDRAWN_PUBLIC_PATHS).issubset(set(routes_config["include"])), "Cloudflare routes bypass the worker for withdrawn MCL files")


def self_test(payload: dict[str, str]) -> None:
    mutations = [
        ("MedicalGuideline JSON-LD", "mcl", '"@type": "WebPage"', '"@type": "MedicalGuideline"'),
        ("visible PDF", "mcl", "</main>", '<a href="guideline.pdf">Download PDF</a></main>'),
        ("CSS reveal", "mcl", "</style>", ".contained .layout{display:block!important}</style>"),
        ("CSS-hide notice by ID", "mcl", "</style>", "#main-content{display:none!important}</style>"),
        ("CSS-hide alert by role", "mcl", "</style>", '[role="alert"]{display:none}</style>'),
        ("hidden notice", "mcl", '<main class="containment-notice" id="main-content" style="display: block !important; visibility: visible !important; opacity: 1 !important;">', '<main class="containment-notice" id="main-content" hidden style="display: block !important; visibility: visible !important; opacity: 1 !important;">'),
        ("missing main inline visibility guard", "mcl", '<main class="containment-notice" id="main-content" style="display: block !important; visibility: visible !important; opacity: 1 !important;">', '<main class="containment-notice" id="main-content">'),
        ("missing alert inline visibility guard", "mcl", '<div class="containment-card" role="alert" aria-labelledby="containment-title" style="display: block !important; visibility: visible !important; opacity: 1 !important;">', '<div class="containment-card" role="alert" aria-labelledby="containment-title">'),
        ("alternate-quote hub link", "guidelines", "</main>", "<a href='/guidelines/mcl/'>MCL</a></main>"),
        ("relative tools link", "tools", "</main>", "<a href='guidelines/mcl'>MCL</a></main>"),
        ("incorrect tools published count", "tools", "<strong>5</strong><span>published guidance resources</span>", "<strong>6</strong><span>published guidance resources</span>"),
        ("orphan published badge", "tools", "</main>", '<span class="badge badge-live">Published</span></main>'),
        ("hidden published badge", "tools", '<span class="badge badge-live">Published</span>', '<span class="badge badge-live" style="opacity: 0">Published</span>'),
        ("stylesheet-hidden badges", "tools", "</head>", "<style>.badge-live{display:none}</style></head>"),
        ("duplicate badge in card", "tools", '<span class="badge badge-live">Published</span>', '<span class="badge badge-live">Published</span><span class="badge badge-live">Published</span>'),
        ("sitemap no-slash URL", "sitemap", "</urlset>", "<url><loc>https://mohsinhaemacademy.com/guidelines/mcl</loc></url></urlset>"),
        ("published clinical claim", "mcl", "</main>", "<p>This guideline remains published for clinical decision support.</p></main>"),
        ("rendered legacy archive", "mcl", '<template id="withdrawn-mcl-v1-archive">', '<div id="withdrawn-mcl-v1-archive">'),
        ("commented CI decoy", "workflow", "run: python scripts/validate_mcl_containment.py", "run: echo ok # python scripts/validate_mcl_containment.py"),
        ("missing worker block", "worker", '  "/guidelines/mcl/guideline.pdf",\n', ""),
        ("commented worker decoy", "worker", '  "/guidelines/mcl/guideline.docx",', '  /* "/guidelines/mcl/guideline.docx", */'),
        ("missing Cloudflare worker route", "routes", '    "/guidelines/mcl/guideline.pdf",\n', ""),
        ("linked site stylesheet badge hide", "site_css", ":focus-visible {", ".badge-live { opacity: 0 !important; }\n\n:focus-visible {"),
        ("linked print stylesheet badge hide", "print_css", "@media print {", "@media print {\n  .badge-live { display: none !important; }"),
        ("duplicate Google font stylesheet", "guidelines", '  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700;800&display=swap">', '  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700;800&display=swap">\n  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700;800&display=swap">'),
        ("duplicate site stylesheet", "guidelines", '  <link rel="stylesheet" href="/assets/site-shell.css">', '  <link rel="stylesheet" href="/assets/site-shell.css">\n  <link rel="stylesheet" href="/assets/site-shell.css">'),
        ("duplicate print stylesheet", "guidelines", '  <link rel="stylesheet" href="/print.css" media="print">', '  <link rel="stylesheet" href="/print.css" media="print">\n  <link rel="stylesheet" href="/print.css" media="print">'),
        ("Guidelines stylesheet event handler", "guidelines", '<link rel="stylesheet" href="/assets/site-shell.css">', '<link rel="stylesheet" href="/assets/site-shell.css" onload="document.body.hidden=true">'),
        ("Tools stylesheet event handler", "tools", '<link rel="stylesheet" href="/assets/site-shell.css">', '<link rel="stylesheet" href="/assets/site-shell.css" onload="document.body.hidden=true">'),
        ("disabled stylesheet", "tools", '<link rel="stylesheet" href="/print.css" media="print">', '<link rel="stylesheet" href="/print.css" media="print" disabled>'),
        ("unexpected stylesheet attribute", "tools", '<link rel="stylesheet" href="/assets/site-shell.css">', '<link rel="stylesheet" href="/assets/site-shell.css" data-containment="bypass">'),
        ("inline script badge hide", "tools", "</body>", "<script>document.querySelectorAll('.badge-live').forEach(e => e.hidden=true)</script>\n</body>"),
        ("linked script badge hide", "cookie_js", "(function () {", "(function () {\n  document.querySelectorAll('.badge-live').forEach(function (e) { e.hidden = true; });"),
        ("card event handler", "guidelines", '<a class="card card-red" href="/guidelines/cll/">', '<a class="card card-red" href="/guidelines/cll/" onmouseover="this.hidden=true">'),
    ]
    for name, key, old, new in mutations:
        mutated = payload.copy()
        require(old in mutated[key], f"Self-test fixture anchor missing: {name}")
        mutated[key] = mutated[key].replace(old, new, 1)
        try:
            validate(**mutated)
        except (AssertionError, ET.ParseError, json.JSONDecodeError):
            continue
        raise AssertionError(f"Containment validator failed open for fixture: {name}")


def main() -> None:
    payload = {
        "mcl": MCL.read_text(encoding="utf-8"),
        "guidelines": GUIDELINES.read_text(encoding="utf-8"),
        "tools": TOOLS.read_text(encoding="utf-8"),
        "sitemap": SITEMAP.read_text(encoding="utf-8"),
        "workflow": WORKFLOW.read_text(encoding="utf-8"),
        "worker": WORKER.read_text(encoding="utf-8"),
        "routes": ROUTES.read_text(encoding="utf-8"),
        "site_css": SITE_SHELL_CSS.read_text(encoding="utf-8"),
        "print_css": PRINT_CSS.read_text(encoding="utf-8"),
        "cookie_js": COOKIE_BANNER_JS.read_text(encoding="utf-8"),
    }
    validate(**payload)
    self_test(payload)
    print("MCL containment validation: PASS")


if __name__ == "__main__":
    main()
