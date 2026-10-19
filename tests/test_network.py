"""Netzwerkgrenzen mit Attrappen; keine Live-Angriffstests."""
import socket
import unittest
from unittest.mock import patch
from mgd_seo.network import Fetcher, FetchError, Response, normalize_url, public_addresses

class NetworkTests(unittest.TestCase):
    def test_normalize_and_fragment(self):
        self.assertEqual(normalize_url("https://EXAMPLE.org:443/a#x"), "https://example.org/a")

    def test_reject_credentials_scheme_port_controls(self):
        for url in ("file:///etc/passwd", "https://user:secret@example.org/", "http://example.org:8080/", "https://example.org/\nX:x", "https://example.org\\@evil.org/"):
            with self.subTest(url=url), self.assertRaises(FetchError):
                normalize_url(url)

    def test_private_dns_addresses_blocked(self):
        for ip in ("127.0.0.1", "10.0.0.1", "169.254.169.254", "::1", "fc00::1", "0.0.0.0"):
            with self.subTest(ip=ip), patch("socket.getaddrinfo", return_value=[(2,1,6,"",(ip,80))]), self.assertRaises(FetchError):
                public_addresses("fixture.invalid", 80)

    def test_mixed_dns_blocked(self):
        with patch("socket.getaddrinfo", return_value=[(2,1,6,"",("1.1.1.1",80)), (2,1,6,"",("127.0.0.1",80))]), self.assertRaises(FetchError):
            public_addresses("fixture.invalid",80)

    def test_public_dns(self):
        with patch("socket.getaddrinfo", return_value=[(2,1,6,"",("1.1.1.1",443))]):
            self.assertEqual(public_addresses("fixture.invalid",443), ["1.1.1.1"])

    def test_redirect_cross_origin_before_fetch(self):
        fetcher = Fetcher(delay=0)
        with patch.object(fetcher,"_once",return_value=Response("https://example.org/",302,{"location":"https://other.example/"},b"")) as once:
            with self.assertRaises(FetchError):
                fetcher.fetch("https://example.org/",allowed_origin="https://example.org")
            self.assertEqual(once.call_count,1)

    def test_robots_redirect_before_fetch(self):
        fetcher = Fetcher(delay=0)
        with patch.object(fetcher,"_once",return_value=Response("https://example.org/",302,{"location":"/private"},b"")) as once:
            with self.assertRaises(FetchError):
                fetcher.fetch("https://example.org/",permitted=lambda url: not url.endswith("private"))
            self.assertEqual(once.call_count,1)

    def test_redirect_loop_limit(self):
        fetcher=Fetcher(delay=0)
        with patch.object(fetcher,"_once",return_value=Response("https://example.org/",302,{"location":"/"},b"")) as once:
            with self.assertRaises(FetchError):
                fetcher.fetch("https://example.org/")
            self.assertEqual(once.call_count,6)

    def test_http_connects_to_checked_ip(self):
        class Reply:
            status=200
            def getheaders(self): return [("Content-Type","text/html")]
            def read1(self,n): return b""
        with patch("mgd_seo.network.public_addresses",return_value=["1.1.1.1"]), patch("socket.create_connection") as connect, patch("http.client.HTTPConnection") as connection:
            connection.return_value.getresponse.return_value=Reply()
            Fetcher(delay=0)._once("http://example.org/")
            self.assertEqual(connect.call_args.args[0], ("1.1.1.1",80))
            connection.return_value.request.assert_called_once()

    def test_https_checks_original_hostname(self):
        class Reply:
            status=200
            def getheaders(self): return []
            def read1(self,n): return b""
        with patch("mgd_seo.network.public_addresses",return_value=["1.1.1.1"]), patch("socket.create_connection") as connect, patch("ssl.create_default_context") as context, patch("http.client.HTTPConnection") as connection:
            connection.return_value.getresponse.return_value=Reply()
            Fetcher(delay=0)._once("https://example.org/")
            context.return_value.wrap_socket.assert_called_once_with(connect.return_value,server_hostname="example.org")

    def test_budget_prevents_connection(self):
        with patch("mgd_seo.network.public_addresses",return_value=["1.1.1.1"]), patch("socket.create_connection") as connect:
            with self.assertRaises(FetchError):
                Fetcher(max_requests=0,delay=0)._once("http://example.org/")
            connect.assert_not_called()

    def test_response_size_limit(self):
        class Reply:
            status=200
            def getheaders(self): return []
            def read1(self,n): return b"x" * n
        with patch("mgd_seo.network.public_addresses",return_value=["1.1.1.1"]), patch("socket.create_connection"), patch("http.client.HTTPConnection") as connection:
            connection.return_value.getresponse.return_value=Reply()
            with self.assertRaises(FetchError):
                Fetcher(delay=0,max_bytes=10)._once("http://example.org/")

    def test_compressed_response_rejected(self):
        class Reply:
            status=200
            def getheaders(self): return [("Content-Encoding","gzip")]
        with patch("mgd_seo.network.public_addresses",return_value=["1.1.1.1"]), patch("socket.create_connection"), patch("http.client.HTTPConnection") as connection:
            connection.return_value.getresponse.return_value=Reply()
            with self.assertRaises(FetchError):
                Fetcher(delay=0)._once("http://example.org/")

if __name__ == "__main__":
    unittest.main()
