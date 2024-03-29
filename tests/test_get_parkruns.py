import unittest
import urllib

from parkrun_to_sqlite.__main__ import get_parkruns


class TestCase(unittest.TestCase):
    def test_get_parkruns(self):
        req = urllib.request.Request(url="file:tests/results.html")
        runs = get_parkruns(req)
        self.assertEqual(60, len(runs))
        self.assertEqual("Tooting Common", runs[0]["Event"])
