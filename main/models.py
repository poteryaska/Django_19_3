from django.db import models
from django.template.defaultfilters import slugify as d_slugify
from config import settings


def slugify(words: str) -> str:
    """
    Slugify for russian language.
    """
    alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z',
                'и': 'i',
                'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
                'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e',
                'ю': 'yu',
                'я': 'ya'}

    return d_slugify(''.join(alphabet.get(w, w) for w in words.lower()))

NULLABLE = {'blank': True, "null": True}


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='наименование товара')
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', **NULLABLE)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    price = models.IntegerField()
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE)
    is_published = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.name}\n(цена за кг: {self.price})\n{self.description}\n{self.photo}'

    class Meta:
        verbose_name = 'товар'  # Настройка для наименования одного объекта
        verbose_name_plural = 'товары'  # Настройка для наименования набора объектов
        ordering = ('name',)
        permissions = [('publish_status', 'Can publish'),
                       ('change_description', 'change description'),
                       ('change_category', 'change category')
                       ]


    # выбор последней версии продукта
    @property
    def active_version(self):
        return self.version_set.last()

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='наименование категории')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Блог'  # Настройка для наименования одного объекта
        verbose_name_plural = 'Блоги'  # Настройка для наименования набора объектов
        ordering = ('name', 'time_create')

class Version(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    number_version = models.IntegerField()
    name_version = models.CharField(max_length=100, verbose_name="Название версии")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"

    def __str__(self):
        return f"{self.name_version} | Номер версии: {self.number_version}"