from django.db import models


NULLABLE = {'blank': True, "null": True}


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='наименование товара')
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', **NULLABLE)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    price = models.IntegerField()
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}\n(цена за кг: {self.price})\n{self.description}\n{self.photo}'

    class Meta:
        verbose_name = 'товар'  # Настройка для наименования одного объекта
        verbose_name_plural = 'товары'  # Настройка для наименования набора объектов
        ordering = ('name',)

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='наименование категории')
    description = models.TextField(blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'  # Настройка для наименования одного объекта
        verbose_name_plural = 'категории'  # Настройка для наименования набора объектов


class Blog(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название блога')
    slug = models.SlugField(max_length=255, unique=True, null=False, verbose_name='URL')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', **NULLABLE, verbose_name='Превью')
    time_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True)
    count_view = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Блог'  # Настройка для наименования одного объекта
        verbose_name_plural = 'Блоги'  # Настройка для наименования набора объектов
        ordering = ('name', 'time_create')