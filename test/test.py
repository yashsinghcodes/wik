#!/usr/bin/env python3
import re
import unittest
from io import StringIO
from unittest.mock import patch

from wik import info


class FakeResp:
    def __init__(self, text, url="https://en.wikipedia.org/wiki/Test", status_code=200):
        self.text = text
        self.url = url
        self.status_code = status_code


class FetchTest(unittest.TestCase):
    def setUp(self):
        info.set_cache_enabled(False)

    def _clean(self, text):
        ansi_escape = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")
        cleaned = ansi_escape.sub("", text)
        return re.sub(r"\n+", "\n", cleaned).strip()

    @patch("sys.stdout", new_callable=StringIO)
    @patch("requests.get")
    def test_getSummary(self, mock_get, mock_stdout):
        html = """
        <html><body>
        <div class="mw-parser-output">
          <p>First paragraph.</p>
          <p>Second paragraph.</p>
          <p>Third paragraph.</p>
        </div>
        </body></html>
        """
        mock_get.return_value = FakeResp(html)

        info.getSummary("KISS_principle")
        output = self._clean(mock_stdout.getvalue())

        self.assertIn("NAME", output)
        self.assertIn("SUMMARY", output)
        self.assertIn("First paragraph.", output)
        self.assertIn("Second paragraph.", output)
        self.assertIn("Third paragraph.", output)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("requests.get")
    def test_getInfo_with_headings(self, mock_get, mock_stdout):
        html = """
        <html><body>
        <div class="mw-parser-output">
          <p>This is an accepted version of this page</p>
          <p>Intro paragraph.</p>
          <h2><span class="mw-headline">Origin</span></h2>
          <p>Origin paragraph.</p>
          <h3><span class="mw-headline">Variants</span></h3>
          <p>Variants paragraph.</p>
        </div>
        </body></html>
        """
        mock_get.return_value = FakeResp(html)

        info.getInfo("Linux")
        output = self._clean(mock_stdout.getvalue())

        self.assertIn("NAME", output)
        self.assertIn("SOURCE", output)
        self.assertIn("ORIGIN", output)
        self.assertIn("VARIANTS", output)
        self.assertIn("Intro paragraph.", output)
        self.assertIn("Origin paragraph.", output)
        self.assertIn("Variants paragraph.", output)
        self.assertNotIn("accepted version", output.lower())

    @patch("sys.stdout", new_callable=StringIO)
    @patch("requests.get")
    def test_searchInfo_results(self, mock_get, mock_stdout):
        html = """
        <html><body>
        <a data-serp-pos="0" title="Linux"></a>
        <a data-serp-pos="1" title="Linux kernel"></a>
        </body></html>
        """
        mock_get.return_value = FakeResp(html, url="https://en.wikipedia.org/w/index.php?search=Linux")

        info.searchInfo("Linux")
        output = self._clean(mock_stdout.getvalue())

        self.assertIn("SEARCH RESULTS", output)
        self.assertIn("Linux", output)
        self.assertIn("Linux kernel", output)

if __name__ == '__main__':
    unittest.main()
