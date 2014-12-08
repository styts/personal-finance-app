from .test_labels import file_names, labels
from results import json_ready_chart


def test_json_chart():
    print(json_ready_chart(file_names[0], labels))
