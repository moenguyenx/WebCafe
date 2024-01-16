import pytest
from cafe.routes import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


def test_order_get(client):
    response = client.get('/order/table/1')
    assert response.status_code == 200


def test_order_post(client):
    data = {
        'order':
            [
                {'_id': '657919b4e4fb7c8534cc9ba9', 'quantity': 2, 'note': 'iced'},
                {'_id': '65805ce202f3e0db3e2dc369', 'quantity': 1, 'note': 'iced'}
            ]
    }
    response = client.post('/order/table/1', json=data)
    assert response.status_code == 200
    assert b'Successfully placed your order' in response.data


def test_login_get(client):
    response = client.get('/')
    assert response.status_code == 200


def test_login_post(client):
    admin_data = {'username': 'admin', 'password': 'admin'}
    staff_data = {'username': 'staff', 'password': '123123'}
    wrong_data = {'username': 'abc', 'password': '123'}
    staff_response = client.post('/', data=staff_data)
    admin_response = client.post('/', data=admin_data)
    wrong_response = client.post('/', data=wrong_data)
    assert admin_response.status_code == 302  # Check if it redirects after login
    assert staff_response.status_code == 302  # Check if it redirects after login
    assert wrong_response.status_code == 302


def test_staff_dashboard_get(client):
    response = client.get('/staff/dashboard')
    assert response.status_code == 200


def test_staff_dashboard_patch(client):
    data = {'_id': '65805e5002f3e0db3e2dc36a'}
    response = client.patch('/staff/dashboard', json=data)
    assert response.status_code == 200
    assert b'Successfully updated the database' in response.data


def test_staff_finished_orders(client):
    response = client.get('/staff/finished-orders')
    assert response.status_code == 200


def test_staff_products(client):
    response = client.get('/staff/products')
    assert response.status_code == 200


def test_admin_dashboard(client):
    response = client.get('/admin/dashboard')
    assert response.status_code == 200


def test_admin_orders(client):
    response = client.get('/admin/orders')
    assert response.status_code == 200


def test_admin_products(client):
    route = '/admin/products'
    true_post_data = {'name': 'Bac Xiu', 'price': 35000, 'img_src': 'test.com'}
    false_post_data = {'name': 'Latte', 'price': 50000, 'img_src': 'test.com'}
    patch_response = client.patch(route, json={'_id': '657919b4e4fb7c8534cc9bb0', 'new_price': 45000})
    true_post_response = client.post(route, data=true_post_data)
    false_post_response = client.post(route, data=false_post_data)
    get_response = client.get(route)
    delete_response = client.delete(route, json={'_id': '657919b4e4fb7c8534cc9baa'})
    assert get_response.status_code == 200
    assert true_post_response.status_code == 200
    assert false_post_response.status_code == 400
    assert patch_response.status_code == 200
    assert delete_response.status_code == 200
    assert b'Successfully added new product' in true_post_response.data
    assert b'Drink already existed' in false_post_response.data
    assert b'Successfully updated price' in patch_response.data
    assert b'Successfully deleted item' in delete_response.data


def test_register(client):
    true_response = client.post('/create_user', data={'username': 'bartender', 'password': '123'})
    false_response = client.post('/create_user', data={'username': 'admin', 'password': 'admin'})
    assert true_response.status_code == 201
    assert false_response.status_code == 400
    assert b'User created successfully.' in true_response.data
    assert b'Username already exists.' in false_response.data


if __name__ == '__main__':
    pytest.main()
