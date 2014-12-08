from __future__ import print_function
from reader import read_dicts_from_filename

file_names = [
    'csv/bankaustria.csv',
    'csv/raiffeisen.csv'
]

labels = {
    'Groceries': ['SPAR DANKT', 'HOFER DANKT', 'BILLA DANKT'],
}


def test_logic():
    for filename in file_names:
        for month_tuple, sum_labels, dict_iter in read_dicts_from_filename(filename, labels):
            # print("----", month_tuple)
            for l, amts in sum_labels.iteritems():
                print("in month {} you spent {} on {} ({})".format(month_tuple, sum(amts), l, len(amts)))
            for d in dict_iter:
                print(d)
            pass
        print("\n============================================")
