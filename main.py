import argparse

from stripe_xero_csv import get_transactions, write_csv_file


if __name__ == "__main__":
    """Get Stripe transactions on CLI args"""

    # create CLI args
    parser = argparse.ArgumentParser()

    # API key
    parser.add_argument(
        '-k',
        '--api-key',
        help='Stripe API key',
        required=True
    )

    parser.add_argument(
        '-c',
        '--currency',
        default='USD',
        help='Currency'
    )

    parser.add_argument(
        '-s',
        '--start',
        help='Transaction start date'
    )
    parser.add_argument(
        '-e',
        '--end',
        help='Transaction end date'

    )
    parser.add_argument(
        '-o',
        '--output',
        help='Output file name'
    )

    # parse arguments
    args = parser.parse_args()

    # retrieve Stripe transactions
    transactions = get_transactions(
        stripe_api_key=args.api_key,
        currency=args.currency,
        start=args.start,
        end=args.end
    )

    # write to .csv file
    write_csv_file(
        file=args.output,
        transactions=transactions
    )
