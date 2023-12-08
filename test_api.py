import requests
import pytest

def test_end_to_end_order_delivery_flow():
    # Step 1: User places an order
    payload = {
        "pizza_name": "Margherita",
        "quantity": 2
    }
    response = requests.post("http://127.0.0.1:5000/place_order", json=payload)

    # Check if the order placement was successful
    assert response.status_code == 200
    order_id = response.json().get('order_id')
    assert order_id is not None, "Failed to obtain order ID after placing the order"

    # Step 2: User checks order status while order is pending
    response = requests.get(f"http://127.0.0.1:5000/order_status/{order_id}")

    # Check if the order status is pending
    assert response.status_code == 200
    assert response.json().get('order_status') == 'pending'

    # Step 3: Delivery person updates order status to "delivered" after food is delivered
    response = requests.put(f"http://127.0.0.1:5000/update_delivery_status/{order_id}")

    # Check if the order status was updated successfully
    assert response.status_code == 200
    assert response.json().get('message') == 'Order status updated successfully'

    # Step 4: User checks order status again and sees the status as "delivered"
    response = requests.get(f"http://127.0.0.1:5000/order_status/{order_id}")

    # Check if the order status is now "delivered"
    assert response.status_code == 200
    assert response.json().get('order_status') == 'delivered'

if __name__ == "__main__":
    pytest.main(["-v", "test_api.py"])
