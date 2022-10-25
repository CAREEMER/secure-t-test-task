import random
from typing import Any, Dict
from uuid import uuid4

from tests.conftest import TestClient
from tests.utils import assert_values, generate_random_string


def create_post(authed_client: TestClient) -> str:
    resp = authed_client.create_post(text=generate_random_string())
    assert resp.status_code == 201

    return resp.json()["id"]


def create_comment(authed_client: TestClient, post_id: str) -> str:
    resp = authed_client.create_comment(parent_comment_id=None, post_id=post_id, text=generate_random_string())
    assert resp.status_code == 201

    return resp.json()["id"]


def recursive_create_comment_tree(
    authed_client: TestClient, post_id: str, parent_comment_id: str, depth: int = 5
) -> bool | dict[Any, dict[Any, dict[str, None]] | bool]:
    if depth == 0:
        return True

    comments_count_on_branch = random.randint(1, 1)

    result_map = {}
    for _ in range(comments_count_on_branch):
        resp = authed_client.create_comment(
            parent_comment_id=parent_comment_id, post_id=post_id, text=generate_random_string()
        )
        comment_id = resp.json()["id"]
        res = recursive_create_comment_tree(authed_client, post_id, comment_id, depth - 1)
        result_map[comment_id] = res

    return result_map


def assert_recursive_comment_tree(id_map, response_tree):
    for comment in response_tree:
        assert id_map.get(comment["id"])

        assert_recursive_comment_tree(id_map.get(comment["id"]), comment["children"])


def test_create_comment_success(authed_client: TestClient):
    post_id = create_post(authed_client)

    comment_text = generate_random_string()
    comment_creation_data = {"post_id": post_id, "text": comment_text}
    resp = authed_client.create_comment(parent_comment_id=None, **comment_creation_data)
    assert resp.status_code == 201
    assert_values(resp.json(), comment_creation_data, ["post_id", "text"])


def test_create_child_comment_success(authed_client: TestClient):
    post_id = create_post(authed_client)
    parent_comment_id = create_comment(authed_client, post_id=post_id)

    comment_data = {"text": generate_random_string(), "post_id": post_id}
    resp = authed_client.create_comment(parent_comment_id, **comment_data)
    assert resp.status_code == 201
    assert_values(resp.json(), comment_data, ["text"])


def test_create_child_comment_non_existent_parent_comment_id_fail(authed_client: TestClient):
    post_id = create_post(authed_client)
    _comment_id = create_comment(authed_client, post_id=post_id)

    comment_data = {"text": generate_random_string(), "post_id": post_id}
    random_non_existent_comment_id = str(uuid4())
    resp = authed_client.create_comment(random_non_existent_comment_id, **comment_data)
    assert resp.status_code == 404


def test_create_comment_unauthorized_fail(authed_client: TestClient, client: TestClient):
    post_id = create_post(authed_client)

    comment_text = generate_random_string()
    comment_creation_data = {"post_id": post_id, "text": comment_text}
    resp = client.create_comment(parent_comment_id=None, **comment_creation_data)
    assert resp.status_code == 403


def test_update_comment_success(authed_client: TestClient):
    post_id = create_post(authed_client)
    comment_id = create_comment(authed_client, post_id=post_id)

    comment_data = {"text": generate_random_string()}
    resp = authed_client.update_comment(comment_id, **comment_data)
    assert resp.status_code == 200
    assert_values(resp.json(), comment_data, ["text"])


def test_update_comment_unauthorized_fail(authed_client: TestClient, client: TestClient):
    post_id = create_post(authed_client)
    comment_id = create_comment(authed_client, post_id=post_id)

    resp = client.update_comment(comment_id, text=generate_random_string())
    assert resp.status_code == 403


def test_delete_comment_success(authed_client: TestClient):
    post_id = create_post(authed_client)
    comment_id = create_comment(authed_client, post_id=post_id)

    resp = authed_client.delete_comment(comment_id)
    assert resp.status_code == 202


def test_delete_comment_unathorized_fail(authed_client: TestClient, client: TestClient):
    post_id = create_post(authed_client)
    comment_id = create_comment(authed_client, post_id=post_id)

    resp = client.delete_comment(comment_id)
    assert resp.status_code == 403


def test_list_comments(authed_client: TestClient):
    post_id = create_post(authed_client)
    parent_comment_id = create_comment(authed_client, post_id=post_id)
    comment_tree = {parent_comment_id: recursive_create_comment_tree(authed_client, post_id, parent_comment_id)}

    resp = authed_client.get_comments(post_id)
    assert resp.status_code == 200
    assert_recursive_comment_tree(comment_tree, resp.json())
