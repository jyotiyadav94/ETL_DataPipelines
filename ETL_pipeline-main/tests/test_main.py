'''
import json
import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestMain(unittest.TestCase):
    """Test case for the main FastAPI application."""
    
    def test_read_main(self):
        """Test reading the main endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the data pipeline!"}

    def test_read_data(self):
        """Test reading the data endpoint."""
        response = client.get("/data")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert len(data) > 0

    def test_get_record_by_city_code(self):
        """Test getting a record by city code."""
        response = client.get("/data/H211")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["cityCode"] == "1"

    def test_get_record_by_city_code_not_found(self):
        """Test getting a record by a city code that doesn't exist."""
        response = client.get("/data/100")
        assert response.status_code == 404
        data = json.loads(response.content)
        assert data["message"] == "Record not found"

if __name__ == '__main__':
    unittest.main()
'''