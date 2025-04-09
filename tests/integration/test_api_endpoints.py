import os
from fastapi.testclient import TestClient

valid_user = os.getenv("API_USER")
valid_password = os.getenv("API_PASSWORD")

def test_upload_csv_success(client, sample_csv_data, mocker):
    # Acceder a las variables de entorno para el usuario y la contraseña

    mocker.patch("src.api.routes.upload_csv.send_email")
    mocker.patch("src.api.routes.upload_csv.generate_pdf", return_value="dummy_path.pdf")
    mocker.patch("src.api.routes.upload_csv.authenticate", return_value="mock_user")


    response = client.post(
        "/api/upload/usa/atdev",
        files={"file": ("test.csv", sample_csv_data)},
        auth=(valid_user, valid_password)  # Usamos las variables de entorno
    )

    assert response.status_code == 200
    assert "sent" in response.json()
    assert isinstance(response.json()["sent"], list)


def test_upload_csv_unauthorized(client):
    response = client.post("/api/upload/usa/atdev")
    assert response.status_code == 401

def test_invalid_country_code(client):
    response = client.post("/api/upload/invalid/atdev", auth=(valid_user, valid_password))
    assert response.status_code == 422
   