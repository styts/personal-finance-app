from logic import guess_format, _guess_date_format, read_dicts_from_filename
import pytest

file_names = [
    'csv/bankaustria.csv',
    'csv/raiffeisen.csv'
]


def test_reader():
    assert {'amount': 2,
            'comments': [1, 3],
            'date': 0,
            'date_format': '%d.%m.%Y',
            } == guess_format('csv/bankaustria.csv')
    assert {'amount': 3,
            'comments': [0, 1, 4, 5],
            'date': 2,
            'date_format': '%d.%m.%Y',
            } == guess_format('csv/raiffeisen.csv')


def test_guess_date_format():
    with pytest.raises(ValueError) as e:
        assert _guess_date_format(['01.10-2014'])
    assert "Can not determine date separator" in e.value

    with pytest.raises(ValueError) as e:
        assert _guess_date_format(['010-2014'])
    assert "Cannot determine date format" in e.value

    with pytest.raises(ValueError) as e:
        assert _guess_date_format(['01.10.2014', '30-09-2014']) == "%d.%m.%Y"
    assert "Dates seem to have different separators" in e.value

    assert _guess_date_format(['01.10.2014', '30.09.2014']) == "%d.%m.%Y"
    assert _guess_date_format(['10-01-2014', '09-30-2014']) == "%m-%d-%Y"
    assert _guess_date_format(['10/01/2014', '09/30/2014']) == "%m/%d/%Y"


def test_logic():
    for filename in file_names:
        for d in read_dicts_from_filename(filename):
            print d
        print "============"
