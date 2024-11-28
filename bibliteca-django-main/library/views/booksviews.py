from django.shortcuts import render, redirect,reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from ..models import Book,Category, Tag
from ..forms import BookForm
import requests
from django.core.files.base import ContentFile
from notifications.signals import notify
from notifications.models import Notification
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def dashboard(request):
    """Dashboard para exibir livros do usuário e notificações."""
    books = Book.objects.filter(added_by=request.user,status='pending')
    soliciaçoesLivros = Book.objects.filter(status='pending')
    acervos = Book.objects.filter(status='approved')[:5]
    notifications = request.user.notifications.unread() if hasattr(request.user, 'notifications') else []
    search_query = request.GET.get('q', '')  # Busca por título
    if search_query:
        books = books.filter(title__icontains=search_query)
    return render(request, 'library/dashboard.html', {
        'books': books,
        'notifications': notifications,
        'search_query': search_query,
        'acervos':acervos,
        'soliciaçoesLivros':soliciaçoesLivros
    })
@login_required
def add_book(request):
    """Adiciona um novo livro manualmente."""
    if request.method == 'POST':
        
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.added_by = request.user
            # book.id_google = request.user
            book.save()
            # Envia notificação para o usuário que adicionou o livro
            notify.send(
                    request.user,
                    recipient=request.user,
                    verb='Livro adicionado.',
                    description=f'Seu livro "{book.title}" foi adicionado e está aguardando processamento.'
                )
            return redirect('dashboard')
    else:
        form = BookForm()
    return render(request, 'library/add_book.html', {'form': form})

@login_required
def edit_book(request, pk):
    """Permite que o usuário edite um livro que ele adicionou."""
    # Recupera o livro ou retorna 404 se não for encontrado ou não pertencer ao usuário
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        # Cria o formulário com os dados enviados e associa o objeto existente
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()  # Salva as alterações no banco de dados
            messages.success(request, 'Livro atualizado com sucesso!')
            return redirect('dashboard')  # Redireciona para o painel do usuário
        else:
            messages.error(request, 'Erro ao atualizar o livro. Verifique os dados.')
    else:
        # Cria o formulário preenchido com os dados do livro
        form = BookForm(instance=book)

    return render(request, 'library/edit_book.html', {'form': form, 'book': book})

@login_required
def delete_book(request, pk):
    """Deleta um livro adicionado pelo usuário."""
    book = get_object_or_404(Book, pk=pk, added_by=request.user)
    if request.method == 'POST':
        book.delete()
        return redirect('dashboard')
    return render(request, 'library/delete_book.html', {'book': book})

@staff_member_required
def approve_book(request, pk):
    """Aprova um livro pendente."""
    book = get_object_or_404(Book, pk=pk, status='pending')

    if  not (book.pdf and  book.thumbnail):
        form = BookForm( instance=book)
        
        messages.error(request, 'Erro ao aprovar o livro.Não tem capa ou não tem pdf.')
        return render(request, 'library/edit_book.html', { 'form': form,'book': book})

        
    Notification.objects.filter(
        recipient=book.added_by,  # Ou o usuário associado ao livro
        verb='Livro adicionado.',
        description__icontains=book.title  # Critério para identificar a notificação
    ).delete()
    book.status = 'approved'
    book.save()
    notify.send(
            request.user,
            recipient=book.added_by,  # Ou outro destinatário, se necessário
            verb='Livro aprovado.',
            description=f'Seu livro "{book.title}" foi aprovado e salvo no sistema.'
        )

    return redirect('dashboard')

@staff_member_required
def reject_book(request, pk):
    """Rejeita um livro pendente."""
    book = get_object_or_404(Book, pk=pk, status='pending')

    
        
    Notification.objects.filter(
        recipient=request.user,  # Ou o usuário associado ao livro
        verb='Livro adicionado.',
        description__icontains=book.title  # Critério para identificar a notificação
    ).delete()
    book.status = 'rejetado'
    book.save()
    notify.send(
            request.user,
            recipient=book.added_by,  # Ou outro destinatário, se necessário
            verb='Livro rejetado.',
            description=f'Seu livro "{book.title}" foi rejetado do sistema. pois esta faltando alguma coisa'
        )

    return redirect('dashboard')


GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"
@login_required
def search_google_books(request):
    query = request.GET.get('q', '')  # Termo de busca
    lang = request.GET.get('lang', 'pt')  # Idioma padrão
    max_results = int(request.GET.get('maxResults', 10))  # Máximo de resultados
    start_index = int(request.GET.get('startIndex', 0))  # Posição inicial para paginação
    books = []
    total_items = 0

    # Calcula os índices de paginação
    next_index = start_index + max_results
    prev_index = start_index - max_results if start_index - max_results >= 0 else 0

    if query:
        try:
            response = requests.get(
                GOOGLE_BOOKS_API_URL,
                params={
                    'q': query,
                    'langRestrict': lang,
                    'maxResults': max_results,
                    'startIndex': start_index,
                    'printType': 'books',
                    'orderBy': 'relevance',
                    'key': 'AIzaSyBD9TMu8GI2Ywpva7vXhgIv9boT9CNeXDQ',  # Substitua pela sua chave da API
                },
                timeout=10  # Timeout de 10 segundos
            )
            response.raise_for_status()  # Lança exceção para status HTTP >= 400
            data = response.json()

            total_items = data.get('totalItems', 0)  # Total de itens disponíveis
            if 'items' in data:
                books = [
                    {
                        'title': item['volumeInfo'].get('title', 'Título não disponível'),
                        'authors': ', '.join(item['volumeInfo'].get('authors', ['Autor desconhecido'])),
                        'thumbnail': item['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),
                        'description': item['volumeInfo'].get('description', 'Descrição não disponível'),
                        'publisher': item['volumeInfo'].get('publisher', 'Editora desconhecida'),
                        'publishedDate': item['volumeInfo'].get('publishedDate', 'Data não disponível'),
                        'external_link': item['selfLink'],
                        'id_google': item['id'],
                    }
                    for item in data['items']
                ]
        except requests.exceptions.RequestException as e:
            print(f"Erro ao consultar a API do Google Books: {e}")
            return HttpResponse("Erro ao consultar a API do Google Books", status=500)

    return render(request, 'library/search_google_books.html', {
        'books': books,
        'query': query,
        'lang': lang,
        'max_results': max_results,
        'start_index': start_index,
        'total_items': total_items,
        'next_index': next_index,
        'prev_index': prev_index,
    })

@login_required
def add_book_to_db(request):
    """Adiciona um livro da busca externa para o banco de dados."""
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publisher = request.POST.get('publisher')
        thumbnail_url = request.POST.get('thumbnail')
        description = request.POST.get('description')
        id_google = request.POST.get('id_google')
        book = Book.objects.create(
            title=title,publisher=publisher, author=author, description=description, added_by=request.user,id_google=id_google
        )
        if thumbnail_url:
            response = requests.get(thumbnail_url)
            if response.status_code == 200:
                book.thumbnail.save(
                    f"{title.replace(' ', '_')}.jpg",
                    ContentFile(response.content),
                    save=True
                )
        
        notify.send(
                request.user,
                recipient=request.user,
                verb='Livro adicionado.',
                description=f'Seu livro "{book.title}" foi adicionado e está aguardando processamento.',
                data=f'key={book.id}'
            )
        return redirect('dashboard')
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)

@login_required
def marca_notfy(request):
    Notification.objects.mark_all_as_read(recipient=request.user)
    return redirect(reverse('dashboard'))


GOOGLE_BOOKS_API_URL_d = "https://www.googleapis.com/books/v1/volumes"
API_KEY = "AIzaSyBD9TMu8GI2Ywpva7vXhgIv9boT9CNeXDQ"

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'library/book_detail.html', {'book': book})

@login_required
def allacervo(request):
    """Dashboard para exibir livros aprovados com funcionalidade de busca aprimorada."""
    # Inicializar a lista de livros aprovados
    acervos = Book.objects.filter(status='approved')

    # Capturar valores da busca
    search_query = request.GET.get('q', '').strip()
    selected_category = request.GET.get('category', '')
    selected_tag = request.GET.get('tag', '')

    # Filtros por título, autor ou descrição
    if search_query:
        acervos = acervos.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Filtro por categoria, se selecionada
    if selected_category:
        acervos = acervos.filter(categories__id=selected_category)
    
    # Filtro por tag, se selecionada
    if selected_tag:
        acervos = acervos.filter(tags__id=selected_tag)

    # Ordenação por título
    acervos = acervos.order_by('title')

    # Paginação (10 itens por página)
    paginator = Paginator(acervos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Obter categorias e tags para o filtro
    categories = Category.objects.all()
    tags = Tag.objects.all()

    # Contexto para o template
    context = {
        'acervos': page_obj,  # Livros paginados
        'search_query': search_query,  # Valor da busca
        'selected_category': selected_category,  # Categoria selecionada
        'selected_tag': selected_tag,  # Tag selecionada
        'categories': categories,  # Todas as categorias
        'tags': tags,  # Todas as tags
    }

    return render(request, 'library/allcervo.html', context)