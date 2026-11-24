# Маршруты API

Все адреса начинаются с `http://127.0.0.1:8000`. Списки выдаются страницами по 5 записей: `count`, `next`, `previous`, `results`. Параметр `page` выбирает страницу. Публичный список и карточка показывают только доступные услуги; сотрудник видит все. Для входа сотрудника в браузере используйте `/api-auth/login/` или админ-панель.

| Метод | Адрес | Доступ |
| --- | --- | --- |
| GET | `/api/categories/`, `/api/categories/{id}/` | все |
| POST | `/api/categories/` | администратор |
| PUT, PATCH, DELETE | `/api/categories/{id}/` | администратор |
| GET | `/api/categories/{id}/services/` | все, доступные услуги категории |
| GET | `/api/services/`, `/api/services/{id}/` | все; в ответе есть `category_name` |
| POST | `/api/services/` | администратор |
| PUT, PATCH, DELETE | `/api/services/{id}/` | администратор |
| POST | `/api/requests/` | все |
| GET | `/api/requests/`, `/api/requests/{id}/` | администратор |
| PUT, PATCH, DELETE | `/api/requests/{id}/` | администратор |
| GET | `/api/statistics/` | администратор |

Фильтры услуг: `category` (числовой ID), `is_available` (`true` или `false`), `min_price`, `max_price`; поиск `search`, сортировка `ordering=price` или `ordering=-price`. Например: `/api/services/?category=1&min_price=1000&max_price=2000&search=английский&ordering=price`. На маршруте услуг категории действуют фильтры категории, доступности и цены. Публичный запрос `is_available=false` возвращает пустой список: недоступные услуги скрыты. Неверные значения фильтров возвращают 400, неверная страница — 404.

Пример создания заявки:

```json
{"service_id": 1, "client_name": "Иван", "phone": "+79001234567", "desired_at": "2030-12-01T12:00:00+03:00"}
```

`status` и `created_at` задаются сервером. Несуществующая или недоступная услуга, пустой телефон и прошедшая дата возвращают 400. Статистика считает все услуги по категориям и заявки со статусом `new`, созданные с начала текущей недели по местному времени (понедельник–воскресенье).

Проверка: `python manage.py test`; сохранённый скриншот списка — `services.png`.
