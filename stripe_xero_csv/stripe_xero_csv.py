from datetime import date, datetime
import os
import csv
from collections import namedtuple
from decimal import Decimal

import dateparser
import stripe

Transactions = namedtuple('stripe_transactions', 'start end currency results')
TWO_PLACES = Decimal('0.01')


def get_transactions(stripe_api_key=None, currency='USD', start=None, end=None):
    """Get a list of Stripe transactions"""

    # set the time to 0:00
    min_time = {'hour': 0,
                'minute': 0,
                'second': 0,
                'microsecond': 0}

    # set default dates
    now = datetime.today()
    start_of_month = now.replace(day=1, **min_time)

    # create start and end date - default to start of month -> now
    start = dateparser.parse(start) if start else start_of_month
    end = dateparser.parse(end) if end else now

    # attach Stripe API key
    stripe.api_key = stripe_api_key

    # call Stripe, and get transactions
    results = stripe.BalanceTransaction.list(
        currency=currency,
        created={
            'gte': int(start.timestamp()),
            'lte': int(end.timestamp()),
        }
    )

    # return start, end and results
    return Transactions(
        start=start,
        end=end,
        currency=currency,
        results=results
    )


def write_csv_file(file=None, transactions: Transactions=None):
    """Write results file to .csv"""

    # set default file name
    start_formatted = transactions.start.strftime('%Y_%m_%d')
    end_formatted = transactions.end.strftime('%Y_%m_%d')
    file = file or f"output/{transactions.currency}-{start_formatted}-{end_formatted}.csv"

    # create dir if it doesn't already exist
    dirname = os.path.dirname(file)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname)

    # open the file as writable
    with open(file, 'w', newline='') as csvfile:

        # create CSV writer, with column names
        writer = csv.DictWriter(
            csvfile,
            fieldnames=[
                '*Date',
                '*Amount',
                'Description',
                'Reference',
            ]
        )

        # write first row
        writer.writeheader()

        # cycle through transactions
        for transaction in transactions.results.auto_paging_iter():

            # Xero format for dates
            created = date.fromtimestamp(transaction['created']).strftime('%d/%m/%y')

            # transaction amount
            transaction_amount = Decimal(transaction['amount'] / 100).quantize(TWO_PLACES)

            # write row
            writer.writerow({
                '*Date': created,
                '*Amount': transaction_amount,
                'Description': transaction['description'],
                'Reference': transaction['id'],
            })

            # cycle through fees and create separate rows
            for fee in transaction.fee_details:

                # fee amount
                fee_amount = -Decimal(fee['amount'] / 100).quantize(TWO_PLACES)

                writer.writerow({
                    '*Date': created,  # same date
                    '*Amount': fee_amount,
                    'Description': fee['description'],
                    'Reference': transaction['id'],  # same id
                })

    # done!
    print(f"written to {file}")
