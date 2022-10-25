from tests.conftest import TestClient
from tests.utils import assert_values, generate_random_string


def test_register_success(client: TestClient):
    user_data = {
        "username": generate_random_string(),
        "password": generate_random_string(),
    }

    resp = client.register(**user_data)
    assert resp.status_code == 201
    assert_values(user_data, resp.json(), ["username"])
    assert "password" not in resp.json().keys()


def test_register_fail(client: TestClient):
    user_data = {
        "username": generate_random_string(),
        "password": generate_random_string(),
    }

    resp = client.register(**user_data)
    assert resp.status_code == 201

    resp_2 = client.register(**user_data)
    assert resp_2.status_code == 409


def test_auth_success(client: TestClient):
    user_data = {
        "username": generate_random_string(),
        "password": generate_random_string(),
    }

    client.register(**user_data)
    resp = client.login(**user_data)
    assert resp.status_code == 201


def test_auth_fail(client: TestClient):
    user_data = {
        "username": generate_random_string(),
        "password": generate_random_string(),
    }

    client.register(**user_data)

    wrong_user_data = {
        "username": generate_random_string(),
        "password": generate_random_string(),
    }
    resp = client.login(**wrong_user_data)

    assert resp.status_code == 404


def test_logout_success(authed_client: TestClient):
    resp = authed_client.logout()
    assert resp.status_code == 202


def test_repeated_logout_fail(authed_client: TestClient):
    resp = authed_client.logout()
    assert resp.status_code == 202

    resp_2 = authed_client.logout()
    assert resp_2.status_code == 401
