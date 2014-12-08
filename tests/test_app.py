from flask import url_for


def test_app(client):
    # we can access the root view
    response = client.get(url_for('root'))
    assert response.status_code == 200

    # it contains a file submission form
    assert '<input type="file">' in response.get_data()


def test_results(client):
    # we can access the root view
    response = client.get(url_for('results'))
    assert response.status_code == 200

    # it contains a file submission form
    assert 'myChart' in response.get_data()
