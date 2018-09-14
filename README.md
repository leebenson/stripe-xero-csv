# Stripe -> Xero-compatible `.csv`

Python CLI for dumping Stripe transactions to a `.csv` file that's compatible with [Xero](https://xero.com) bank statement imports.

## Features

- Handles multiple currencies (just pass a `--currency` flag)
- Parses plain English/multi-lingual transaction dates using [dateparser](https://pypi.org/project/dateparser/)
- Adds Stripe fees as separate rows, for easier accounting
- Outputs to a `.csv` file that can be uploaded immediately into Xero

## Requirements

- Python 3 (tested on 3.7)

## Installation

Install packages:

```bash
pip install -r requirements.txt
```

## Usage

This is intended as a CLI tool rather than a library.

`cd` into the cloned folder and run from the command line:

```bash
python3 main.py --api-key="YOUR_STRIPE_API_HERE" --start="Jan 1" --currency="GBP"
```

By default, a `.csv` file will be generated in the the `output` folder of the current directory.

## CLI options

- 
- `--currency` - 3 letter currency code (defaults to `USD`)
- `--start` - Start date (defaults to start of the current month)
- `--end` - End date (defaults to now)
- `-o` or `--output` - Override default output file name

Dates will be parsed using [dateparser](https://pypi.org/project/dateparser/)

## LICENSE

[MIT](LICENSE)