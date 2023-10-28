from django import forms
from django.core.exceptions import ValidationError

from main.models import Product, Version

class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
class ProductForm(StyleFormMixin, forms.ModelForm):
    bad_words = ("казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар")


    def clean_name(self):
        name = str(self.cleaned_data['name'])
        for word in self.bad_words:
            if word in name:
                raise forms.ValidationError('Невозможно создать продукт с таким наименованием')
        return name

    def clean_description(self):
        description = str(self.cleaned_data['description'])
        for word in self.bad_words:
            if word in description:
                raise forms.ValidationError('Невозможно создать продукт с таким описанием')
        return description

    class Meta:
        model = Product
        fields = ["name", "price", "category", "description", "photo", "is_published"]


class VersionForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Version
        fields = ["name_version", "number_version"]