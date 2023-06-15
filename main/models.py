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
        return f'{self.name} {self.price}'

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