"""Test the Atlus API."""

import pytest
from fastapi.testclient import TestClient

from .app import VERSION, app

client = TestClient(app=app, root_path="")

test_adds: list[str] = [
    "946 West Mitchell Hammock Road Suite 1220, Suite 1220",
    "123 Main St, Springfield, IL 62701",
    "1500 Pennsylvania Ave NW, Washington, DC 20220, United States",
    "456 Elm Ave, Anytown, NY 12345",
    "789 Oak Dr, Smallville California, 98765",
    "101 W. Pine St Bigtown Texas 54321",
    "234 Cedar Hwy Suite 2, W. Des Moines, IA",
    "345 MAPLE RD, COUNTRYSIDE, PA 24680-0198",
    "678 MLK Blvd, Suburbia, Ohio 97531",
    "890 St Mary St, Metropolis, GA 86420",
    "111 N.E. Cherry St, Villageton, Michigan 36912",
    "222 NW Pineapple Ave, Beachville, SC 75309",
    "333 Orange Blvd, Riverside Arizona 80203",
    "444 Grape St SE, Hilltop, NV 46895 Unit B",
    "158 S. Thomas Court, Marietta, GA 30008",
    "666 BANANA AVE LAKESIDE NEW MEXICO 36921",
    "777 Strawberry Street, Mountainview, OR 25874",
]

test_phones = [
    "+1 (909) 2988892",
    "17379089203",
    "1.223.394.3983",
    "282-203-2988",
    "1 902 989 2837",
    "9389209876",
]

test_hours = [
    "Mo-Fr 08:00-12:00,13:00-17:30",
    "Monday to Friday 9am-5pm, Saturday 9am-12pm",
    "Closed",
    "24 hours",
    "Mon-Sun 9-5",
    "Weekdays 8am-6pm",
]

test_times = [
    "Mo-Fr 15:00,18:00,19:00,23:00; Sa 15:00; Su 10:30,23:00",
    "Monday to Friday 3pm and 6pm",
]


def test_get_version() -> None:
    """Test version endpoint."""
    response = client.get("/meta")
    assert response.json()["version"] == VERSION


def test_get_main() -> None:
    """Test homepage."""
    response = client.get("/meta")
    assert response.status_code == 200


@pytest.mark.parametrize("add", test_adds)
def test_post_add_parse(add: str) -> None:
    """Test single address endpoint."""
    response = client.post("/address/parse/", json={"address": add})
    assert response.status_code == 200


def test_post_add_batch() -> None:
    """Test batch addresses endpoint."""
    response = client.post(
        "/address/batch/",
        json=[{"address": each, "@id": oid} for oid, each in enumerate(test_adds)],
    )

    assert response.status_code == 200


def test_post_add_parse_error_preserves_id() -> None:
    """An unparseable address should keep the caller-supplied @id, not default to 0."""
    response = client.post("/address/parse/", json={"address": "asdkfj", "@id": 42})
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["@id"] == 42


@pytest.mark.parametrize("phone", test_phones)
def test_post_phone_parse(phone: str) -> None:
    """Test single phone endpoint."""
    response = client.post("/phone/parse/", json={"phone": phone})
    assert response.status_code == 200


def test_post_phone_parse_error_preserves_id() -> None:
    """An unparseable phone should keep the caller-supplied @id, not default to 0."""
    response = client.post("/phone/parse/", json={"phone": "not-a-phone", "@id": 42})
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["@id"] == 42


def test_post_phone_batch() -> None:
    """Test batch phones endpoint."""
    response = client.post(
        "/phone/batch/",
        json=[{"phone": each, "@id": oid} for oid, each in enumerate(test_phones)],
    )

    assert response.status_code == 200


@pytest.mark.parametrize("hours", test_hours)
def test_post_hours_parse(hours: str) -> None:
    """Test single hours endpoint."""
    response = client.post("/hours/parse/", json={"hours": hours})
    assert response.status_code == 200


def test_post_hours_batch() -> None:
    """Test batch hours endpoint."""
    response = client.post(
        "/hours/batch/",
        json=[{"hours": each, "@id": oid} for oid, each in enumerate(test_hours)],
    )

    assert response.status_code == 200


def test_post_hours_parse_unparseable_includes_reason() -> None:
    """Unparseable hours should surface the underlying reason, not a generic message."""
    response = client.post("/hours/parse/", json={"hours": "asdkfj asdkfj"})
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["error"] != "Unparseable"
    assert "rule" in data["error"].lower()


def test_post_hours_parse_empty_string_error() -> None:
    """An empty hours string should report why it failed."""
    response = client.post("/hours/parse/", json={"hours": ""})
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["error"] == "Empty opening hours string."


def test_post_hours_parse_error_preserves_id() -> None:
    """An error result should keep the caller-supplied @id, not default to 0."""
    response = client.post("/hours/parse/", json={"hours": "", "@id": 42})
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["@id"] == 42


def test_post_hours_batch_error_preserves_id() -> None:
    """Errors within a batch should keep each item's own @id."""
    response = client.post(
        "/hours/batch/",
        json=[{"hours": "", "@id": 7}, {"hours": test_hours[0], "@id": 8}],
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data[0]["@id"] == 7
    assert data[1]["@id"] == 8


@pytest.mark.parametrize("times", test_times)
def test_post_times_parse(times: str) -> None:
    """Test single times endpoint."""
    response = client.post("/times/parse/", json={"times": times})
    assert response.status_code == 200


def test_post_times_batch() -> None:
    """Test batch times endpoint."""
    response = client.post(
        "/times/batch/",
        json=[{"times": each, "@id": oid} for oid, each in enumerate(test_times)],
    )

    assert response.status_code == 200


def test_post_times_parse_empty_string_error() -> None:
    """An empty times string should report why it failed."""
    response = client.post("/times/parse/", json={"times": ""})
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["error"] == "Empty collection/service times string."


def test_post_times_parse_error_preserves_id() -> None:
    """An error result should keep the caller-supplied @id, not default to 0."""
    response = client.post("/times/parse/", json={"times": "", "@id": 42})
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["@id"] == 42


def test_post_times_batch_error_preserves_id() -> None:
    """Errors within a batch should keep each item's own @id."""
    response = client.post(
        "/times/batch/",
        json=[{"times": "", "@id": 7}, {"times": test_times[0], "@id": 8}],
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data[0]["@id"] == 7
    assert data[1]["@id"] == 8
