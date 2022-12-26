# PythonCLI

## Installation

Run setup

- virtual environment is optional but recommended.

```bash
# pip
python -m venv venv
. venv/bin/activate
pip install -e .

# poetry
poetry install
```

Checking if it works

```bash
# If installed with pip
pcli-test

# Using poetry
poetry run pcli-test
```

## Archive view

Find media in an archive file and view it.

Example:

```bash
pcli-archive-view -p "~/Downloads/Google Photos" -s LS --view
```

## Dedupe Lines

A simple script to remove duplicate lines from a file without sorting the file.

Alternative was to sort and output unique lines, but when I used this to sort a lastpass export csv file
the file format was not supported for import again.

```
sort file.txt | uniq > sorted.file.txt
```
