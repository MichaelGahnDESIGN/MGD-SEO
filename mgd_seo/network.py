"""Begrenzte öffentliche Abrufe; keine Proxys, Cookies oder Anmeldedaten.

DNS wird vor jeder Verbindung geprüft. Die Verbindung nutzt genau eine der
geprüften IP-Adressen; TLS prüft weiterhin Zertifikat und ursprünglichen Host.
Dadurch führt eine zweite DNS-Auflösung nicht zu einem ungeprüften Ziel.
Dies ist keine vollständige Isolation: untrusted Browser brauchen eigene Sandboxen.
"""
import http.client
import ipaddress
import socket
import ssl
import time
from dataclasses import dataclass
from urllib.parse import urljoin, urlsplit, urlunsplit

AGENT = "MGD-SEO/0.1.0"

class FetchError(ValueError):
    """Ein Abruf wurde begrenzt, abgelehnt oder ist fehlgeschlagen."""


def normalize_url(url):
    """Nur öffentliche Web-URL-Syntax zulassen; Fragmente gehören nicht zum Abruf."""
    try:
        if any(ord(char) <= 32 or ord(char) == 127 for char in url):
            raise ValueError("Steuer- oder Leerzeichen in URL")
        parts = urlsplit(url)
        if parts.scheme not in ("http", "https") or not parts.hostname:
            raise ValueError("Nur vollständige HTTP/HTTPS-URLs zulässig")
        if parts.username is not None or parts.password is not None:
            raise ValueError("Anmeldedaten in URLs sind nicht zulässig")
        port = parts.port
        expected = 443 if parts.scheme == "https" else 80
        if port is not None and port != expected:
            raise ValueError("Nur Standardports 80/443 zulässig")
        host = parts.hostname.rstrip(".").encode("idna").decode("ascii").lower()
        if not host or "%" in host or "\\" in url:
            raise ValueError("Ungültiger Host")
        hostpart = "[" + host + "]" if ":" in host else host
        return urlunsplit((parts.scheme, hostpart, parts.path or "/", parts.query, ""))
    except (ValueError, UnicodeError) as exc:
        raise FetchError(str(exc)) from exc


def public_addresses(host, port):
    """Alle DNS-Antworten müssen öffentlich sein; gemischte Antworten ablehnen."""
    try:
        records = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    except OSError as exc:
        raise FetchError("DNS-Auflösung fehlgeschlagen") from exc
    addresses = sorted({record[4][0] for record in records})
    if not addresses or any(not ipaddress.ip_address(ip).is_global for ip in addresses):
        raise FetchError("Privates, lokales oder reserviertes Netzwerkziel gesperrt")
    return addresses


def origin(url):
    p = urlsplit(normalize_url(url))
    return p.scheme + "://" + p.netloc


@dataclass
class Response:
    url: str
    status: int
    headers: dict
    body: bytes

    def text(self):
        # Explizite Kodierung beachten; unbekannte Kodierungen fallen auf UTF-8 zurück.
        import re
        match = re.search(r"charset=[\"']?([^;\s\"']+)", self.headers.get("content-type", ""), re.I)
        try:
            return self.body.decode(match.group(1) if match else "utf-8", errors="replace")
        except LookupError:
            return self.body.decode("utf-8", errors="replace")


class Fetcher:
    """Gesamtbudget, Zeitabstand und Antwortgröße gelten für alle Abrufe zusammen."""
    def __init__(self, timeout=10, max_bytes=2_000_000, max_requests=80,
                 max_seconds=120, delay=0.5):
        self.timeout, self.max_bytes = timeout, max_bytes
        self.max_requests, self.delay = max_requests, delay
        self.deadline = time.monotonic() + max_seconds
        self.requests = 0
        self.last_request = 0

    def fetch(self, url, allowed_origin=None, permitted=None):
        current = normalize_url(url)
        for _ in range(6):
            if allowed_origin and origin(current) != allowed_origin:
                raise FetchError("Weiterleitung verlässt den freigegebenen Ursprung")
            if permitted and not permitted(current):
                raise FetchError("URL durch robots.txt gesperrt")
            response = self._once(current)
            if response.status not in (301, 302, 303, 307, 308):
                return response
            location = response.headers.get("location")
            if not location:
                raise FetchError("Weiterleitung ohne Ziel")
            current = normalize_url(urljoin(current, location))
        raise FetchError("Weiterleitungslimit überschritten")

    def _once(self, url):
        p = urlsplit(url)
        port = 443 if p.scheme == "https" else 80
        addresses = public_addresses(p.hostname, port)
        remaining = self.deadline - time.monotonic()
        pause = max(0, self.delay - (time.monotonic() - self.last_request))
        if self.requests >= self.max_requests or remaining <= pause:
            raise FetchError("Gesamtbudget überschritten")
        time.sleep(pause)
        timeout = min(self.timeout, self.deadline - time.monotonic())
        connection = http.client.HTTPConnection(p.hostname, port, timeout=timeout)
        sock = None
        try:
            sock = socket.create_connection((addresses[0], port), timeout=timeout)
            if p.scheme == "https":
                sock = ssl.create_default_context().wrap_socket(sock, server_hostname=p.hostname)
            connection.sock = sock
            self.requests += 1
            self.last_request = time.monotonic()
            path = p.path + (("?" + p.query) if p.query else "")
            connection.request("GET", path, headers={
                "User-Agent": AGENT, "Accept": "text/html,application/xhtml+xml,text/plain,application/xml;q=0.9",
                "Accept-Encoding": "identity", "Connection": "close"})
            response = connection.getresponse()
            headers = {}
            for key, value in response.getheaders():
                key = key.lower()
                headers[key] = headers[key] + ", " + value if key in headers else value
            if headers.get("content-encoding", "identity").lower() not in ("", "identity"):
                raise FetchError("Komprimierte Antwort wird in 0.1.0 nicht verarbeitet")
            chunks, length = [], 0
            while True:
                remaining = self.deadline - time.monotonic()
                if remaining <= 0:
                    raise FetchError("Zeitbudget überschritten")
                sock.settimeout(min(self.timeout, remaining))
                chunk = response.read1(min(65536, self.max_bytes + 1 - length))
                if not chunk:
                    break
                chunks.append(chunk)
                length += len(chunk)
                if length > self.max_bytes:
                    raise FetchError("Antwort überschreitet das Größenlimit")
            return Response(url, response.status, headers, b"".join(chunks))
        except (OSError, http.client.HTTPException, UnicodeError) as exc:
            raise FetchError("HTTP/TLS-Abruf fehlgeschlagen: " + type(exc).__name__) from exc
        finally:
            connection.close()
            if sock is not None:
                sock.close()
