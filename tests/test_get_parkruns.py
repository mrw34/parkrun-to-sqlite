import unittest
import urllib

from parkrun_to_sqlite.__main__ import get_parkruns


class TestCase(unittest.TestCase):
    def test_get_parkruns(self):
        req = urllib.request.Request(url="file:tests/athleteeventresultshistory.html")
        run = get_parkruns(req)[0]
        self.assertEqual("Tooting Common", run["Event"])
