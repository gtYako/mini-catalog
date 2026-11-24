from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from catalog.models import Category, Service, ServiceRequest

class Command(BaseCommand):
    help = 'Добавить учебные данные в пустую базу'
    def handle(self, *args, **options):
        if Category.objects.exists() or Service.objects.exists() or ServiceRequest.objects.exists():
            self.stdout.write('База уже содержит данные. Загрузка отменена.')
            return
        groups = [
            ('Языки', 'languages', ['Английский для начинающих', 'Разговорный английский', 'Немецкий язык', 'Подготовка к экзамену']),
            ('Компьютеры', 'computers', ['Основы компьютера', 'Текстовый редактор', 'Электронные таблицы', 'Основы программирования']),
            ('Творчество', 'creative', ['Рисование', 'Фотография', 'Графический дизайн', 'Рукоделие']),
            ('Профессия', 'career', ['Подготовка резюме', 'Собеседование', 'Выбор профессии']),
        ]
        services = []
        for group, slug, names in groups:
            category = Category.objects.create(name=group, slug=slug)
            for name in names:
                i = len(services)
                services.append(Service.objects.create(category=category, name=name, description='Учебная услуга: ' + name, price=1000 + i * 150, duration_minutes=60 + (i % 3) * 30, is_available=i != 14))
        for i in range(8):
            ServiceRequest.objects.create(service=services[i], client_name=f'Клиент {i + 1}', phone=f'+790000000{i:02}', desired_at=timezone.now() + timedelta(days=i + 1))
        self.stdout.write(self.style.SUCCESS('Добавлены 4 категории, 15 услуг и 8 заявок.'))
