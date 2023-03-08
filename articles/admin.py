from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        """
        Валидация полей формы разделов для статьи
        Один из разделов обязательно должен быть главным
        Проверка на отсутствие двух главных разделов
        """
        count = 0
        for form in self.forms:
            print(form.cleaned_data)
            print(form.cleaned_data['is_main'])
            if form.cleaned_data['is_main']:
                count += 1
        if count == 0:
            raise ValidationError('Укажите основной раздел')
        elif count > 1:
            raise ValidationError('Основным может быть только один раздел')
        return super().clean()  # вызываем базовый код переопределяемого метода


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'published_at', 'image']
    list_filter = ['title']
    inlines = [ScopeInline, ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']





