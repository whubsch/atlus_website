from fastapi.testclient import TestClient
import pytest
from app import app

client = TestClient(app)

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


def test_get_main() -> None:
    """Test homepage."""
    response = client.get("/")
    assert response.status_code == 200

@pytest.mark.parametrize("add", test_adds)
def test_post_parse(add: str) -> None:
    """Test single address endpoint."""
    response = client.post("/api/parse/", json={"address": add})
    assert response.status_code == 200


def test_post_batch() -> None:
    """Test batch addresses endpoint."""
    response = client.post("/api/batch/", json=[{"address": each, "@id": oid} for each, oid in enumerate(test_adds)])
    assert response.status_code == 200
    assert response.json() == {}
