import allure
import requests
import jsonschema
import pytest
from .schemas.store_schema import INVENTORY_SCHEMA, ORDER_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")
class TestStore:
    @allure.step("Размещение заказа")
    def test_add_order(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }
        with allure.step("Отправка запроса на размещение заказа"):
            response = requests.post(url=f'{BASE_URL}/store/order', json=payload)
            response_json = response.json()
        with allure.step("Проверка статуса ответа и валидации JSON-схемы"):
            assert response.status_code == 200, "Статус код не совпадает"
            jsonschema.validate(response_json, ORDER_SCHEMA)
            assert response_json["id"] == payload["id"]
            assert response_json["petId"] == payload["petId"]
            assert response_json["quantity"] == payload["quantity"]
            assert response_json["status"] == payload["status"]
            assert response_json["complete"] == payload["complete"]
    @allure.title("Получение информации о заказе по ID")
    def test_get_order(self, create_order):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_order["id"]
        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(url=f'{BASE_URL}/store/order/{pet_id}')
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Статус код не совпадает"
            assert response.json()["id"] == create_order["id"]
            assert response.json()["petId"] == create_order["petId"]
            assert response.json()["quantity"] == create_order["quantity"]
            assert response.json()["status"] == create_order["status"]
            assert response.json()["complete"] == create_order["complete"]

    @allure.title("Удаление заказа по ID")
    def test_delete_order(self, create_order):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_order["id"]
        with allure.step('Отправка запроса на удаление заказа по ID'):
            response = requests.delete(url=f'{BASE_URL}/store/order/{pet_id}')
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, "Статус код не совпадает"
        with allure.step('Отправка запроса на проверку получения информации по удаленному заказу'):
            response = requests.get(url=f'{BASE_URL}/store/order/{pet_id}')
            assert response.status_code
            assert response.text == 'Order not found'


    @allure.title("Попытка получить информацию о несуществующем заказе ")
    def test_get_nonexistent_order(self):
        with allure.step("Отправка запроса на получиние информации о несуществующем заказе "):
            response = requests.get(url=f'{BASE_URL}/store/order/9999')
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404
            assert response.text == 'Order not found'

    @allure.title("Получение инвентаря магазина")
    def test_get_inventory(self):
        with allure.step("Отправка запроса на получиние информации о несуществующем заказе "):
            response = requests.get(url=f'{BASE_URL}/store/inventory')
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200
            jsonschema.validate(response.json(), INVENTORY_SCHEMA)






