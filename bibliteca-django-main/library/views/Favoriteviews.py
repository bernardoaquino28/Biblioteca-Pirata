from django.shortcuts import render, redirect,reverse, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from ..models import Favorite, Book
from django.contrib.auth import get_user_model
from django.contrib import messages


@login_required
def add_to_favorites(request, book_id):
    """
    Adiciona um livro aos favoritos do usuário.
    """
    book = get_object_or_404(Book, id=book_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)
    if created:
        return JsonResponse({"message": "Livro adicionado aos favoritos com sucesso."}, status=201)
    else:
        return JsonResponse({"message": "Este livro já está na lista de favoritos."}, status=200)


@login_required
def remove_from_favorites(request, book_id):
    """
    Remove um livro dos favoritos do usuário.
    """
    book = get_object_or_404(Book, id=book_id)
    favorite = Favorite.objects.filter(user=request.user, book=book).first()
    if favorite:
        favorite.delete()
        return JsonResponse({"message": "Livro removido dos favoritos com sucesso."}, status=200)
    else:
        return JsonResponse({"message": "Este livro não está nos seus favoritos."}, status=404)


@login_required
def list_favorites(request):
    """
    Lista todos os favoritos do usuário.
    """
    favorites = Favorite.objects.filter(user=request.user).select_related('book')
    favorite_books = [
        {
            "id": fav.book.id,
            "title": fav.book.title,
            "author": fav.book.author,
            "added_at": fav.favorited_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for fav in favorites
    ]
    return JsonResponse({"favorites": favorite_books}, status=200)


@login_required
def toggle_favorite(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    # User = get_user_model()  # Obtem o modelo de usuário configurado
    # user = User.objects.get(pk=request.user.pk)  # Garante que `user` seja uma instância de `User`

    if request.user in book.favorited_by.all():
        favorite = Favorite.objects.filter(user=request.user, book=book).first()
        favorite.delete()
        messages.success(request, 'Livro removido dos favoritos!')
    else:
        favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)

        messages.success(request, 'Livro adicionado aos favoritos!')
    return redirect('book_detail', book_id=book.pk)