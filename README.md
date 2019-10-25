# parkrun-to-sqlite

## Install

```shell
pip install parkrun-to-sqlite
```

## Run

```shell
parkrun-to-sqlite XXXXXXX parkruns.db
```

Replace `XXXXXXX` with your [parkrun ID](https://support.parkrun.com/hc/en-us/articles/200566243-What-is-my-parkrun-ID-number-), excluding the initial 'A'.

The SQLite database produced by this tool is designed to be browsed using [Datasette](https://datasette.readthedocs.io/) ([example](https://datasette.markwoodbridge.com/parkruns/runs)).
