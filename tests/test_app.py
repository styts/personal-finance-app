from flask import url_for


def test_app(client):
    # we can access the root view
    assert client.get(url_for('root')).status_code == 200
