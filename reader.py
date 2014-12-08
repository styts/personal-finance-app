import csv
import dateutil.parser
import logging
from datetime import datetime
import re
from decimal import Decimal
from itertools import groupby
from collections import defaultdict


potential_formats = [
    "%d.%m.%Y",
    "%m.%d.%Y",
    "%Y.%m.%d",
]


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


def get_rows(csv_filename, max_lines=None):
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
            if max_lines and reader.line_num > max_lines:
                break
    return rows


def _determine_separator(date_list):
    # determine separator
    all_potential_seps = []
    for d in date_list:
        potential_seps = set(re.findall('[^\d]', d))
        if len(potential_seps) != 1:
            raise ValueError('Can not determine date separator')
        sep = potential_seps.pop()
        all_potential_seps.append(sep)
    if len(set(all_potential_seps)) != 1:
        raise ValueError('Dates seem to have different separators')
    return sep


def _guess_date_format(date_list):
    sep = _determine_separator(date_list)

    for f in potential_formats:
        good_candidate = True
        # update separator
        if sep != '.':
            f = f.replace('.', sep)

        # make sure _all_ dates can be parsed with this format
        for d in date_list:
            try:
                datetime.strptime(d, f)
            except:
                good_candidate = False
                break
        if good_candidate:
            return f
    raise ValueError('Cannot determine date format')


def guess_format(csv_filename):
    frmt = {}

    rows = get_rows(csv_filename, max_lines=10)

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
    frmt['comments'] = cols_comment

    # date format
    frmt['date_format'] = _guess_date_format(z_rows[frmt['date']])

    return frmt


def assign_labels(labels, d):
    for label, label_markers in labels.iteritems():
        for m in label_markers:
            if m in d['comments']:
                d['labels'].append(label)
    return d


def _dict_from_format_and_line(line, fmt):
    date_origin = line[fmt['date']]
    dat = datetime.strptime(date_origin, fmt['date_format']).date()
    return {
        'amount': Decimal(line[fmt['amount']]),
        'date': dat,
        'comments': " ".join(line[n] for n in fmt['comments']),
        'labels': [],
    }


def sum_labels(labels, dict_iter):
    results = defaultdict(list)

    pass
    for d in dict_iter:
        if not len(d['labels']):
            continue
        print d
        for l in labels:
            results[l].append(d['amount'])

    return results


def group_by_month(iter_, labels):
    for month_tuple, dict_iter in groupby(iter_, key=lambda d: (d['date'].year, d['date'].month)):
        yield (month_tuple, sum_labels(labels, dict_iter), dict_iter)


def read_dicts_from_filename(filename, labels):
    fmt = guess_format(filename)
    results = []
    for line in get_rows(filename):
        d = _dict_from_format_and_line(line, fmt)
        d = assign_labels(labels, d)
        results.append(d)
    results = sorted(results, key=lambda x: x['date'])
    return group_by_month(results, labels)
