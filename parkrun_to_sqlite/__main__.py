import argparse
import datetime
import json
import os
import sqlite3
import urllib.request
from html.parser import HTMLParser


class TableHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self.table = []
        self.row = []
        self.td = False

    def handle_starttag(self, tag, attrs):
        if tag == "tbody":
            self.table = []
        elif tag == "tr":
            self.row = []
        elif tag == "td":
            self.td = True

    def handle_endtag(self, tag):
        if tag == "tbody":
            self.tables.append(self.table)
        elif tag == "tr":
            self.table.append(self.row)
        elif tag == "td":
            self.td = False

    def handle_data(self, data):
        if self.td:
            self.row.append(data.strip())


def get_parkruns(req):
    with urllib.request.urlopen(req) as f:
        html = f.read().decode("utf-8")

    parser = TableHTMLParser()
    parser.feed(html)

    return [
        {
            "Event": row[0],
            "Run Date": datetime.datetime.strptime(row[1], "%d/%m/%Y")
            .date()
            .isoformat(),
            "Run Number": int(row[2]),
            "Pos": int(row[3]),
            "Time": f"00:{row[4]}",
            "Age Grade": float(row[5].rstrip("%")),
            "PB?": row[6] == "PB",
        }
        for row in reversed(parser.tables[-1])
    ]


def store_parkruns(runs, database):
    with open(os.path.join(os.path.dirname(__file__), "events.json")) as f:
        features = json.load(f)["events"]["features"]
    conn = sqlite3.connect(database)
    with conn:
        conn.execute("DROP TABLE IF EXISTS runs")
        conn.execute(
            """
            CREATE TABLE runs
            (
                Event     TEXT,
                RunDate   TEXT,
                RunNumber INTEGER,
                Pos       INTEGER,
                Time      TEXT,
                AgeGrade  REAL,
                PB        INTEGER,
                Latitude  REAL,
                Longitude REAL
            )
            """
        )
        for run in runs:
            feature = next(
                feature
                for feature in features
                if feature["properties"]["EventShortName"] == run["Event"]
            )
            conn.execute(
                "INSERT INTO runs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    json.dumps(
                        {
                            "href": "https://www.parkrun.org.uk/"
                            + feature["properties"]["eventname"],
                            "label": run["Event"],
                        }
                    )
                    if feature["properties"]["countrycode"] == 97
                    else run["Event"],
                    run["Run Date"],
                    json.dumps(
                        {
                            "href": (
                                "https://www.parkrun.org.uk/"
                                f"{feature['properties']['eventname']}/results"
                                f"/weeklyresults/?runSeqNumber={run['Run Number']}"
                            ),
                            "label": run["Run Number"],
                        }
                    )
                    if feature["properties"]["countrycode"] == 97
                    else run["Run Number"],
                    run["Pos"],
                    run["Time"],
                    run["Age Grade"],
                    run["PB?"],
                    feature["geometry"]["coordinates"][1],
                    feature["geometry"]["coordinates"][0],
                ),
            )
    conn.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("runner_id")
    parser.add_argument("filename")
    args = parser.parse_args()
    url = (
        "https://www.parkrun.org.uk/results/athleteeventresultshistory/"
        f"?athleteNumber={args.runner_id}&eventNumber=0"
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3)"
        " AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8"
    }
    req = urllib.request.Request(url=url, headers=headers)
    parkruns = get_parkruns(req)
    store_parkruns(parkruns, args.filename)


if __name__ == "__main__":
    main()
