from django.contrib import admin
from .models import Book, Category, Tag,  Collection, PurchaseLocation, Favorite

# Configuração personalizada para o modelo Book
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'status', 'is_published', 'added_by', 'created_at')
    list_filter = ('status', 'is_published', 'categories', 'tags')
    search_fields = ('title', 'author', 'publisher', 'id_google')
    autocomplete_fields = ('categories', 'tags', 'purchase_locations')
    raw_id_fields = ('added_by',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ("Basic Information", {
            "fields": ('title', 'author', 'description', 'id_google', 'publisher', 'published_date', 'cover', 'thumbnail', 'pdf')
        }),
        ("Status and Publication", {
            "fields": ('status', 'is_published', 'rejection_reason')
        }),
        ("Relations", {
            "fields": ('categories', 'tags', 'purchase_locations')
        }),
        ("Metadata", {
            "fields": ('added_by', 'created_at', 'updated_at')
        }),
    )


# Configuração personalizada para o modelo Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


# Configuração personalizada para o modelo Tag
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)



# Configuração personalizada para o modelo Collection
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by')
    search_fields = ('name',)
    autocomplete_fields = ('books',)
    raw_id_fields = ('created_by',)


# Configuração personalizada para o modelo PurchaseLocation
@admin.register(PurchaseLocation)
class PurchaseLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'address')
    search_fields = ('name', 'url')


# Configuração personalizada para o modelo Favorite
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'favorited_at')
    search_fields = ('user__username', 'book__title')
    raw_id_fields = ('user', 'book')
    readonly_fields = ('favorited_at',)
