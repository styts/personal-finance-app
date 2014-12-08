from datetime import datetime
from reader import read_dicts_from_filename


def json_ready_chart(filename, labels):
    data = {
        "labels": [],
        "datasets": [],
    }
    for month_tuple, sum_labels, _ in read_dicts_from_filename(filename, labels):
        # create chart label, e.g. "December 2014"
        data['labels'].append("{} {}".format(datetime(month_tuple[0], month_tuple[1], 1).strftime("%B"), month_tuple[0]))
        for label, amounts in sum_labels.iteritems():
            # insert ds if it's not present
            is_present = False
            for ds in data['datasets']:
                if ds['label'] == label:
                    is_present = True
                    break
            if not is_present:
                data['datasets'].append({
                    "label": label,
                    "data": [],
                    "fillColor": "rgba(220,220,220,0.2)",
                    "strokeColor": "rgba(220,220,220,1)",
                    "pointColor": "rgba(220,220,220,1)",
                    "pointStrokeColor": "#fff",
                    "pointHighlightFill": "#fff",
                    "pointHighlightStroke": "rgba(220,220,220,1)",
                })

            # update dataset by label
            for ds in data['datasets']:
                if ds['label'] == label:
                    ds['data'].append(str(abs(sum(amounts))))
    return data
