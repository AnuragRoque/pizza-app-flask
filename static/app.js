function placeOrder() {
    var name = document.getElementById('name').value;
    var phone = document.getElementById('phone').value;
    var address = document.getElementById('address').value;
    var pizzaName = document.getElementById('pizzaName').value;
    var quantity = document.getElementById('quantity').value;

    fetch('/place_order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: name,
            phone: phone,
            address: address,
            pizza_name: pizzaName,
            quantity: quantity,
        }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message + '\nOrder ID: ' + data.order_id);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function checkOrderStatus() {
    var orderId = document.getElementById('orderId').value;

    fetch('/order_status/' + orderId, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        alert('Order Status: ' + data.order_status);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function updateDeliveryStatus() {
    var updateOrderId = document.getElementById('updateOrderId').value;

    fetch('/update_delivery_status/' + updateOrderId, {
        method: 'PUT',
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

