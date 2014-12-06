from logic import guess_format


def test_reader():
    assert {'amount': 2, 'comment': [1, 3], 'date': 0} == \
        guess_format('csv/bankaustria.csv')
    assert {'amount': 3, 'comment': [0, 1, 4, 5], 'date': 2} == \
        guess_format('csv/raiffeisen.csv')
