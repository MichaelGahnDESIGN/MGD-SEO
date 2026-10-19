"""Extrahiert nur SEO-relevante Metadaten; führt kein HTML oder JavaScript aus."""
from html.parser import HTMLParser
from urllib.parse import urljoin

class PageParser(HTMLParser):
    def __init__(self, url):
        super().__init__(convert_charrefs=True)
        self.url = url
        self.titles, self.descriptions, self.canonicals = [], [], []
        self.robots, self.links, self.headings, self.jsonld = [], [], [], []
        self.images_missing_alt = 0
        self.images = 0
        self.lang = ""
        self._capture = None
        self._text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang", "") or ""
        if tag in ("title", "h1") or (tag == "script" and (attrs.get("type") or "").lower() == "application/ld+json"):
            self._capture, self._text = tag, []
        if tag == "meta":
            name = (attrs.get("name") or "").lower()
            value = attrs.get("content") or ""
            if name == "description":
                self.descriptions.append(value.strip())
            if name in ("robots", "googlebot"):
                self.robots.append(value.lower())
        if tag == "link" and "canonical" in (attrs.get("rel") or "").lower().split():
            self.canonicals.append(urljoin(self.url, attrs.get("href") or ""))
        if tag == "a" and attrs.get("href"):
            self.links.append(urljoin(self.url, attrs["href"]))
        if tag == "img":
            self.images += 1
            if "alt" not in attrs:
                self.images_missing_alt += 1

    def handle_data(self, data):
        if self._capture:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag == self._capture:
            value = "".join(self._text)
            if tag != "script":
                value = " ".join(value.split())
            target = {"title": self.titles, "h1": self.headings, "script": self.jsonld}[tag]
            target.append(value)
            self._capture, self._text = None, []

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
