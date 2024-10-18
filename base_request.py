import requests
import pprint


class BaseRequest:
    def __init__(self, base_url):
        self.base_url = base_url

    def _request(self, url, request_type, data=None, expected_error=False):
        stop_flag = False
        while not stop_flag:
            if request_type == 'GET':
                response = requests.get(url)
            elif request_type == 'POST':
                response = requests.post(url, data=data)
            else:
                response = requests.delete(url)

            if not expected_error and response.status_code == 200:
                stop_flag = True
            elif expected_error:
                stop_flag = True

        pprint.pprint(f'{request_type} example')
        pprint.pprint(response.url)
        pprint.pprint(response.status_code)
        pprint.pprint(response.reason)
        pprint.pprint(response.text)
        pprint.pprint(response.json())
        pprint.pprint('**********')
        return response

    def get(self, endpoint, endpoint_id=None, expected_error=False):
        url = f'{self.base_url}/{endpoint}'
        if endpoint_id:
            url += f'/{endpoint_id}'
        response = self._request(url, 'GET', expected_error=expected_error)
        return response.json()

    def post(self, endpoint, endpoint_id=None, body=None):
        url = f'{self.base_url}/{endpoint}'
        if endpoint_id:
            url += f'/{endpoint_id}'
        response = self._request(url, 'POST', data=body)
        return response.json()

    def delete(self, endpoint, endpoint_id):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'DELETE')
        return response.json()


class UserAPI(BaseRequest):
    def create_user(self, user_data):
        """Создание нового пользователя"""
        return self.post('user', body=user_data)

    def get_user(self, username):
        """Получение информации о пользователе"""
        return self.get('user', username)

    def update_user(self, username, user_data):
        """Обновление данных пользователя"""
        return self.post(f'user/{username}', body=user_data)

    def delete_user(self, username):
        """Удаление пользователя"""
        return self.delete('user', username)


class StoreAPI(BaseRequest):
    def create_order(self, order_data):
        """Создание нового заказа"""
        return self.post('store/order', body=order_data)

    def get_order(self, order_id):
        """Получение информации о заказе"""
        return self.get('store/order', order_id)

    def delete_order(self, order_id):
        """Удаление заказа"""
        return self.delete('store/order', order_id)

    def get_inventory(self):
        """Получение инвентаря"""
        return self.get('store/inventory')


if __name__ == "__main__":
    BASE_URL = 'https://petstore.swagger.io/v2'

    user_api = UserAPI(BASE_URL)

    user_data = {
        "id": 1,
        "username": "johndoe",
        "firstName": "John",
        "lastName": "Doe",
        "email": "johndoe@example.com",
        "password": "password123",
        "phone": "1234567890",
        "userStatus": 1
    }

    print("Создание пользователя...")
    user_api.create_user(user_data)

    print("Получение информации о пользователе...")
    user_info = user_api.get_user("johndoe")
    pprint.pprint(user_info)

    print("Обновление данных пользователя...")
    user_data["firstName"] = "Jonathan"
    user_api.update_user("johndoe", user_data)

    print("Удаление пользователя...")
    user_api.delete_user("johndoe")

    store_api = StoreAPI(BASE_URL)

    order_data = {
        "id": 1,
        "petId": 10,
        "quantity": 2,
        "shipDate": "2024-10-14T00:00:00.000Z",
        "status": "placed",
        "complete": True
    }

    print("Создание заказа...")
    store_api.create_order(order_data)

    print("Получение информации о заказе...")
    order_info = store_api.get_order(1)
    pprint.pprint(order_info)

    print("Удаление заказа...")
    store_api.delete_order(1)

    print("Получение инвентаря...")
    inventory = store_api.get_inventory()
    pprint.pprint(inventory)
