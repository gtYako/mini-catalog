from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Category, Service, ServiceRequest

class CatalogAPITests(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Языки', slug='languages')
        
        self.service1 = Service.objects.create(
            category=self.category, name='Английский', description='Описание 1',
            price=1000, duration_minutes=60, is_available=True
        )
        self.service2 = Service.objects.create(
            category=self.category, name='Немецкий', description='Описание 2',
            price=2000, duration_minutes=60, is_available=True
        )
        self.service_unavailable = Service.objects.create(
            category=self.category, name='Недоступная', description='Описание 3',
            price=3000, duration_minutes=60, is_available=False
        )
        
        self.list_url = '/api/services/'
        self.request_url = '/api/requests/' 

    def test_services_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_pagination(self):
        for i in range(6):
            Service.objects.create(
                category=self.category, name=f'Услуга {i}', description='...',
                price=100, duration_minutes=60, is_available=True
            )
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertIsNotNone(response.data['next'])

    def test_sorting(self):
        response = self.client.get(f'{self.list_url}?ordering=-price')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['price'], '2000.00')

    def test_filter(self):
        response = self.client.get(f'{self.list_url}?min_price=1500&max_price=2500')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Немецкий')

    def test_create_valid_request(self):
        data = {
            'service': self.service1.id,  # <--- ТЕПЕРЬ 'service'
            'client_name': 'Иван',
            'phone': '+79000000000',
            'desired_at': (timezone.now() + timedelta(days=1)).isoformat()
        }
        response = self.client.post(self.request_url, data, format='json')
        
        if response.status_code != 201:
            print(f"\nОШИБКА ВАЛИДАЦИИ: {response.data}\n")
            
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'new')

    def test_create_request_past_date(self):
        data = {
            'service': self.service1.id,
            'client_name': 'Иван',
            'phone': '+79000000000',
            'desired_at': (timezone.now() - timedelta(days=1)).isoformat()
        }
        response = self.client.post(self.request_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('desired_at', response.data)

    def test_create_request_unavailable_service(self):
        data = {
            'service': self.service_unavailable.id, 
            'client_name': 'Иван',
            'phone': '+79000000000',
            'desired_at': (timezone.now() + timedelta(days=1)).isoformat()
        }
        response = self.client.post(self.request_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('service', response.data) # Теперь ошибка будет тут

    def test_anonymous_cannot_change_price(self):
        url = f'{self.list_url}{self.service1.id}/'
        response = self.client.patch(url, {'price': 5000}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)