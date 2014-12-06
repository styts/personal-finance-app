import csv
import dateutil.parser
import logging
from decimal import Decimal


def _is_amount(s):
    s = s.replace(',', '.')
    s = s.replace(' ', '')
    try:
        Decimal(s)
        return True
    except Exception, e:
        logging.debug(e)
        return False


def _is_date(s):
    try:
        dateutil.parser.parse(s)
        return True
    except Exception, e:
        logging.debug(e)
        return False


def guess_format(csv_filename):
    frmt = {}
    with open(csv_filename, 'rU') as csvfile:
        sample = csvfile.read(2048)
        # guess delimeter
        dialect = csv.Sniffer().sniff(sample)
        has_header = csv.Sniffer().has_header(sample)

        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)

        if has_header:  # skip first header row
            reader.next()

        rows = []
        for row in reader:
            rows.append(row)
            if reader.line_num > 10:
                break

        z_rows = zip(*rows)
        for i, column_i_data in enumerate(z_rows):
            if all(map(_is_date, column_i_data)):
                frmt['date'] = i
            elif all(map(_is_amount, column_i_data)):
                frmt['amount'] = i

        if len(frmt.keys()) != 2:
            raise ValueError('CSV must contain a date and amount columns')

        # the remaining columns are comments
        cols_comment = range(len(z_rows))
        map(cols_comment.remove, frmt.values())
        frmt['comment'] = cols_comment
    return frmt
