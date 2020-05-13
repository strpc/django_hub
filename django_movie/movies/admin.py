from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import (Category,
                     Genre,
                     Movie,
                     MovieShots,
                     Actor,
                     Rating,
                     RatingStar,
                     Reviews
                     )
class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


class ReviewsInline(admin.StackedInline):
    """Отзывы на странице фильма"""
    model = Reviews
    extra = 1


class MovieShotsInline(admin.StackedInline):
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.image.url} height='110'")

    get_image.short_description = 'Изображение'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display =('id', 'name', 'url',)
    list_display_links = ('name', 'url', 'id')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year')
    search_fields =('title', 'category__name',)
    inlines = [MovieShotsInline, ReviewsInline]
    save_on_top = True
    save_as = True
    list_editable = ('draft',)
    actions = ['publish', 'unpublish']
    # fields = (('actors', 'directors', 'genres'), )
    readonly_fields = ('get_image',)
    form = MovieAdminForm
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline'),)
        }),
        (None, {
            'fields': (('description', ('poster', 'get_image')))
        }),
        (None, {
            'fields': (('year', 'world_premiere', 'country'),)
        }),
        ('Actors', {
            'classes': ('collapse',),
            'fields': (('actors', 'directors', 'genres', 'category'),)
        }),
        (None, {
            'fields': (('budget', 'fees_in_usa', 'fees_in_world'),)
        }),
        ('Options', {
            'fields': (('url', 'draft'),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.poster.url} height='110'")
    get_image.short_description = 'Постер'

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f"{row_update} записей было обновлено"
        self.message_user(request, f"{message_bit}")
    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f"{row_update} записей было обновлено"
        self.message_user(request, f"{message_bit}")
    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change',)


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    list_display_links = ('name', 'email', 'id')
    readonly_fields = ('name', 'email')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ('name', 'url')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.image.url} height='40'")

    get_image.short_description = 'Изображение'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ('star', 'ip')


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры к фильму"""
    list_display = ('title', 'movie', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.image.url} height='40'")

    get_image.short_description = 'Изображение'


admin.site.register(RatingStar)

admin.site.site_title = 'MovieHub'
admin.site.site_header = 'MovieHub'