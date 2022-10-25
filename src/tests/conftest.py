from enum import Enum

import pytest
import requests

from core.config import app_config
from tests.utils import generate_random_string

scheme = "http" if app_config.ENV == "local" else "https"
APP_URL = f"{scheme}://{app_config.HOST}:{app_config.PORT}"


class UrlEndpoints(str, Enum):
    register = APP_URL + "/api/v1/auth/register/"
    login = APP_URL + "/api/v1/auth/login/"
    logout = APP_URL + "/api/v1/auth/logout/"
    post = APP_URL + "/api/v1/post/"
    comment = APP_URL + "/api/v1/comment/"


class BaseMixin:
    @property
    def headers(self):
        return {"Authorization": f"Token {self.auth_token}"} if getattr(self, "auth_token", None) else None


class TestClientAuthMixin(BaseMixin):
    def register(self, username: str, password: str):
        return requests.post(UrlEndpoints.register.value, json={"username": username, "password": password})

    def login(self, username: str, password: str):
        resp = requests.post(UrlEndpoints.login.value, json={"username": username, "password": password})

        if resp.ok:
            self.auth_token = resp.json()["key"]
        return resp

    def logout(self):
        return requests.post(UrlEndpoints.logout.value, headers=self.headers)


class TestClientPostCRUDMixin(BaseMixin):
    def create_post(self, **post_data):
        return requests.post(UrlEndpoints.post.value, json=post_data, headers=self.headers)

    def get_post(self, post_id: str):
        return requests.get(UrlEndpoints.post.value + f"{post_id}/")

    def update_post(self, post_id: str, **post_data):
        return requests.patch(UrlEndpoints.post.value + f"{post_id}/", json=post_data, headers=self.headers)

    def delete_post(self, post_id: str):
        return requests.delete(UrlEndpoints.post.value + f"{post_id}/", headers=self.headers)


class TestClientCommentCRUDMixin(BaseMixin):
    def create_comment(self, parent_comment_id: str | None = None, **comment_data):
        url = UrlEndpoints.comment.value
        if parent_comment_id:
            url += f"?parent_comment_id={parent_comment_id}"
        return requests.post(url, json=comment_data, headers=self.headers)

    def get_comments(self, post_id: str):
        return requests.get(UrlEndpoints.comment.value + f"?post_id={post_id}")

    def update_comment(self, comment_id: str, **comment_data):
        return requests.patch(UrlEndpoints.comment.value + f"{comment_id}/", json=comment_data, headers=self.headers)

    def delete_comment(self, comment_id: str):
        return requests.delete(UrlEndpoints.comment.value + f"{comment_id}/", headers=self.headers)


class TestClient(TestClientAuthMixin, TestClientPostCRUDMixin, TestClientCommentCRUDMixin):
    pass


@pytest.fixture()
def client():
    client = TestClient()
    return client


@pytest.fixture(autouse=True)
def authed_client():
    authed_client = TestClient()

    register_data = {"username": generate_random_string(), "password": generate_random_string()}
    authed_client.register(**register_data)
    authed_client.login(**register_data)

    return authed_client
