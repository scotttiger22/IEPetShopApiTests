import allure
import requests
import jsonschema
import pytest
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = 'http://5.181.109.28:9090/api/v3'


@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_non_pet(self):
        with allure.step("Отправка запроса на удаление несущетсвующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка статуса ответа"):
            assert response.text == "Pet deleted", "Текст ответа не совпал с ожидаемым"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несущетсвующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put(f'{BASE_URL}/pet', json=payload)

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step('Проверка статуса ответа'):
            assert response.text == "Pet not found", "Текст ответа не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexistent_pet(self):
        with allure.step("Отправка запроса на получиние информации о несуществующем питомце"):
            response = requests.get(url=f'{BASE_URL}/pet/9999')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step('Проверка статуса ответа'):
            assert response.text == "Pet not found", "Текст ответа не совпал с ожидаемым"

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }

        with allure.step("Отправка запроса на добавление питомца"):
            response = requests.post(url=f'{BASE_URL}/pet', json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидации JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "name питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status питомца не совпадает с ожидаемым"

    @allure.title("Добавление нового питомца c полными данными")
    def test_add_pet_fulldata(self):
        with allure.step("Подготовка данных для создания питомца c полными данными"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {"id": 1, "name": "Dogs"},
                "photoUrls": ["string"],
                "tags": [{"id": 0, "name": "string"}],
                "status": "available"
            }
        with allure.step("Отправка запроса на добавление питомца c полными данными"):
            response = requests.post(url=f'{BASE_URL}/pet', json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидации JSON-схемы"):
            assert response.status_code == 200, "Статус код не совпадает"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "name питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status питомца не совпадает с ожидаемым"
            assert response_json['photoUrls'] == payload['photoUrls'], "photoUrls питомца не совпадает с ожидаемым"
            assert response_json['category'] == payload['category'], "category питомца не совпадает с ожидаемым"
            assert response_json['tags'] == payload['tags'], "tags питомца не совпадает с ожидаемым"

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]
        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(url=f'{BASE_URL}/pet/{pet_id}')
        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200, "Статус код не совпадает"
            assert response.json()['id'] == pet_id

    @allure.title("Обновение информации о питомце по ID")
    def test_put_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet['id']

        with allure.step("Отправка запроса на обновление информации о питомце по ID"):
            payload = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }
            response = requests.put(f'{BASE_URL}/pet', json=payload)

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200, "Статус код не совпадает"
            assert response.json()['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response.json()['name'] == payload['name'], "name питомца не совпадает с ожидаемым"
            assert response.json()['status'] == payload['status'], "status питомца не совпадает с ожидаемым"

    @allure.title("Удаление питомца по ID")
    def test_delete_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet['id']

        with allure.step("Удаление питомца по ID"):
            response = requests.delete(url=f'{BASE_URL}/pet/{pet_id}')

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Статус код не совпадает"

        with allure.step("Проверка статуса ответа удаленного питомца"):
            response = requests.get(url=f'{BASE_URL}/{pet_id}')
            assert response.status_code == 404, "Статус код не совпадает"

    @allure.title("Получение списка питомцев по статусу")
    @pytest.mark.parametrize(
        "status, expectd_status_code",
        [
            ("available", 200),
            ("pending", 200),
            ("sold", 200),
            ("", 400),
            (12132136151, 400)
        ]
    )
    def test_get_pets_by_status(self, status, expectd_status_code):
        with allure.step(f"Отправка запроса на получение списка питомцев по статусу {status}"):
            response = requests.get(url=f'{BASE_URL}/pet/findByStatus', params={"status": status})

        with allure.step("Проверка статуса ответа и формата данных"):
            assert response.status_code == expectd_status_code, "Статус код не совпадает"
            if response.status_code == 200:
                assert isinstance(response.json(), list), "Формат данных не совпадает"
                assert response.json()[0]["status"] == status, "status питомца не совпадает с ожидаемым"
                assert response.json()[-1]["status"] == status, "status питомца не совпадает с ожидаемым"
            else:
                assert isinstance(response.json(), dict), "Формат данных не совпадает"
