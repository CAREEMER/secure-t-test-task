from tests.conftest import TestClient
from tests.utils import assert_values, generate_random_string


def test_create_post_success(authed_client: TestClient):
    post_text = generate_random_string()
    resp = authed_client.create_post(text=post_text)
    assert resp.status_code == 201

    resp_2 = authed_client.get_post(resp.json()["id"])
    assert resp_2.status_code == 200
    assert_values(resp_2.json(), {"text": post_text}, ["text"])


def test_create_post_not_authorized_fail(client: TestClient):
    post_text = generate_random_string()
    resp = client.create_post(text=post_text)
    assert resp.status_code == 403


def test_update_post_success(authed_client: TestClient):
    post_text = generate_random_string()
    resp = authed_client.create_post(text=post_text)
    assert resp.status_code == 201

    new_post_text = generate_random_string()
    resp_2 = authed_client.update_post(resp.json()["id"], text=new_post_text)
    assert resp_2.status_code == 200
    assert resp_2.json()["time_updated"]
    assert_values(resp_2.json(), {"text": new_post_text}, ["text"])


def test_update_post_not_authorized_fail(authed_client: TestClient, client: TestClient):
    post_text = generate_random_string()
    resp = authed_client.create_post(text=post_text)
    assert resp.status_code == 201

    new_post_text = generate_random_string()
    resp_2 = client.update_post(resp.json()["id"], text=new_post_text)
    assert resp_2.status_code == 403


def test_delete_post_success(authed_client: TestClient):
    post_text = generate_random_string()
    resp = authed_client.create_post(text=post_text)
    assert resp.status_code == 201

    resp_2 = authed_client.delete_post(resp.json()["id"])
    assert resp_2.status_code == 202

    resp_3 = authed_client.get_post(resp.json()["id"])
    assert resp_3.status_code == 404


def test_delete_post_not_authorized_fail(authed_client: TestClient, client: TestClient):
    post_text = generate_random_string()
    resp = authed_client.create_post(text=post_text)
    assert resp.status_code == 201

    resp_2 = client.delete_post(resp.json()["id"])
    assert resp_2.status_code == 403
