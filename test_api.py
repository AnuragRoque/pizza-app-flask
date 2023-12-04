import pytest
import requests

def test_order_more_than_one_quantity():
    # Intentionally ordering more than one quantity
    payload = {
        "pizza_name": "Margherita",
        "quantity": 2
    }

    response = requests.post("http://127.0.0.1:5000/place_order", json=payload)
    # Not Intentionally introducing bug for ordering more than one quantity
    assert response.status_code == 400
    assert 'Bug: Ordering more than one quantity is not allowed.' in response.json().get('error', '')

if __name__ == "__main__":
    pytest.main(["-v", "test_api.py"])
