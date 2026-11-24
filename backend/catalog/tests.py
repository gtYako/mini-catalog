from datetime import timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase
from .models import Category, Service, ServiceRequest

class CatalogTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Курсы', slug='courses')
        self.items = [Service.objects.create(category=self.category, name=f'Услуга {i}', description='Описание', price=100 + i * 100, duration_minutes=60, is_available=i != 6) for i in range(7)]
        self.url = '/api/services/'
        self.request_data = {'service_id': self.items[0].id, 'client_name': 'Иван', 'phone': '+79001234567', 'desired_at': (timezone.now() + timedelta(days=1)).isoformat()}

    def test_list_only_available(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 6)

    def test_pagination(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.data['results']), 5)
        self.assertIsNotNone(response.data['next'])
        self.assertEqual(len(self.client.get(self.url, {'page': 2}).data['results']), 1)

    def test_sort_by_price(self):
        response = self.client.get(self.url, {'ordering': '-price'})
        prices = [float(x['price']) for x in response.data['results']]
        self.assertEqual(prices, sorted(prices, reverse=True))

    def test_combined_filter(self):
        response = self.client.get(self.url, {'category': self.category.id, 'min_price': 200, 'max_price': 300})
        self.assertEqual(response.data['count'], 2)

    def test_create_request(self):
        self.request_data['status'] = 'done'
        response = self.client.post('/api/requests/', self.request_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['status'], 'new')

    def test_past_date(self):
        self.request_data['desired_at'] = (timezone.now() - timedelta(days=1)).isoformat()
        self.assertEqual(self.client.post('/api/requests/', self.request_data).status_code, 400)

    def test_unavailable_service(self):
        self.request_data['service_id'] = self.items[-1].id
        self.assertEqual(self.client.post('/api/requests/', self.request_data).status_code, 400)

    def test_anonymous_cannot_change_price(self):
        self.assertIn(self.client.patch(f'/api/services/{self.items[0].id}/', {'price': '1.00'}).status_code, (401, 403))
        self.items[0].refresh_from_db()
        self.assertEqual(self.items[0].price, 100)

    def test_invalid_service_and_phone(self):
        self.request_data['service_id'] = 99999
        self.request_data['phone'] = '  '
        response = self.client.post('/api/requests/', self.request_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('service_id', response.data)
        self.assertIn('phone', response.data)

    def test_invalid_filter(self):
        self.assertEqual(self.client.get(self.url, {'min_price': 'abc'}).status_code, 400)
        self.assertEqual(self.client.get(self.url, {'is_available': 'maybe'}).status_code, 400)

    def test_admin_can_edit_and_see_unavailable(self):
        user = get_user_model().objects.create_user(username='manager', password='pass', is_staff=True)
        self.client.force_authenticate(user)
        self.assertEqual(self.client.get(self.url).data['count'], 7)
        self.assertEqual(self.client.patch(f'/api/services/{self.items[0].id}/', {'price': '250.00'}).status_code, 200)
        self.assertEqual(self.client.patch(f'/api/services/{self.items[0].id}/', {'price': '-1'}).status_code, 400)

    def test_category_services_and_details(self):
        self.assertEqual(self.client.get(f'/api/categories/{self.category.id}/services/').data['count'], 6)
        self.assertEqual(self.client.get(f'/api/services/{self.items[0].id}/').data['category_name'], 'Курсы')

    def test_statistics_requires_admin(self):
        self.assertIn(self.client.get('/api/statistics/').status_code, (401, 403))
        user = get_user_model().objects.create_user(username='admin', password='pass', is_staff=True)
        self.client.force_authenticate(user)
        ServiceRequest.objects.create(service=self.items[0], client_name='Иван', phone='123', desired_at=timezone.now() + timedelta(days=1))
        data = self.client.get('/api/statistics/').data
        self.assertEqual(data['services_by_category'][0]['service_count'], 7)
        self.assertEqual(data['new_requests_this_week'], 1)
