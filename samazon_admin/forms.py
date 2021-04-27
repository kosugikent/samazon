from django import forms

from core.models import Category, MajorCategory, Product


class MajorCategoryCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = MajorCategory
        fields = '__all__'


class CategoryCreateUpdateForm(forms.ModelForm):
    major_category = forms.ModelChoiceField(queryset=MajorCategory.objects.all())

    class Meta:
        model = Category
        fields = '__all__'


class ProductCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = {'': '---------'}
        for category in Category.objects.all():
            categories.setdefault(category.major_category.name, [])
            categories[category.major_category.name].append([category.id, category.name])
        self.fields['category'].choices = categories.items()
