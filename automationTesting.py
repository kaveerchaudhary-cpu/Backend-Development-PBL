import json
from urllib import request
from urllib.error import HTTPError

BASE_URL = "http://localhost:8000"


class Response:
    def __init__(self, status_code, body):
        self.status_code = status_code
        self._body = body

    def json(self):
        return json.loads(self._body) if self._body else None


def http_request(method, path, data=None):
    body = json.dumps(data).encode("utf-8") if data is not None else None

    req = request.Request(
        f"{BASE_URL}{path}",
        data=body,
        method=method,
        headers={"Content-Type": "application/json"} if body else {},
    )

    try:
        with request.urlopen(req) as response:
            return Response(
                response.status,
                response.read().decode("utf-8")
            )
    except HTTPError as error:
        return Response(
            error.code,
            error.read().decode("utf-8")
        )


def test_home():
    response = http_request("GET", "/")
    assert response.status_code == 200
    print("PASS: Home route")


def test_health():
    response = http_request("GET", "/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("PASS: Health route")


def test_create_todo():
    data = {
        "title": "Automation Test Todo",
        "completed": False
    }

    response = http_request("POST", "/todos", data)

    assert response.status_code == 200
    assert response.json()["title"] == "Automation Test Todo"

    print("PASS: Create Todo")


def test_get_todos():
    response = http_request("GET", "/todos")

    assert response.status_code == 200

    print("PASS: Get all Todos")


def test_get_todo():
    response = http_request("GET", "/todos/0")

    assert response.status_code == 200

    print("PASS: Get Todo by ID")


def test_update_todo():
    data = {
        "title": "Updated Automation Todo",
        "completed": True
    }

    response = http_request("PUT", "/todos/0", data)

    assert response.status_code == 200
    assert response.json()["completed"] is True

    print("PASS: Update Todo")


def test_delete_todo():
    response = http_request("DELETE", "/todos/0")

    assert response.status_code == 200

    print("PASS: Delete Todo")


if __name__ == "__main__":
    print("\nStarting API Automation Tests...\n")

    test_home()
    test_health()
    test_create_todo()
    test_get_todos()
    test_get_todo()
    test_update_todo()
    test_delete_todo()

    print("\nALL TESTS PASSED!")