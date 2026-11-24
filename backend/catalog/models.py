from django.core.validators import MinValueValidator
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='services')
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    duration_minutes = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ServiceRequest(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'Новая'
        IN_PROGRESS = 'in_progress', 'В работе'
        DONE = 'done', 'Завершена'
        CANCELLED = 'cancelled', 'Отменена'

    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='requests')
    client_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    desired_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client_name}: {self.service}'
