from django.urls import path
from library import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-book/', views.add_book, name='add_book'),
    path('edit-book/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete-book/<int:pk>/', views.delete_book, name='delete_book'),
    path('search-google-books/', views.search_google_books, name='search_google_books'),
    path('add-book-to-db/', views.add_book_to_db, name='add_book_to_db'),
    path('approve-book/<int:pk>/', views.approve_book, name='approve_book'),
    path('reject-book/<int:pk>/', views.reject_book, name='reject_book'),
    path('book-detail/<str:book_id>/', views.book_detail, name='book_detail'),
    path('ver-no-google-books/<str:book_id>/', views.book_detail, name='ver_no_google_books'),
    path('marca_notfy',views.marca_notfy,name='marca_notfy'),
    path('allacervo',views.allacervo,name='allacervo')
]


urlpatterns += [
    
    # Category URLs
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),

    # Tag URLs
    path('tags/', views.TagListView.as_view(), name='tag-list'),
    path('tags/<int:pk>/', views.TagDetailView.as_view(), name='tag-detail'),


    # Collection URLs
    path('collections/', views.CollectionListView.as_view(), name='collection-list'),
    path('collections/<int:pk>/', views.CollectionDetailView.as_view(), name='collection-detail'),

    # Purchase Location URLs
    path('locations/', views.PurchaseLocationListView.as_view(), name='purchase-location-list'),
    path('locations/<int:pk>/', views.PurchaseLocationDetailView.as_view(), name='purchase-location-detail'),

    # Favorite URLs
    path('favorites/add/<int:book_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:book_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('favorites/', views.list_favorites, name='list_favorites'),]
