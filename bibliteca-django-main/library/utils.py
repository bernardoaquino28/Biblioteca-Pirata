import requests
from django.core.files.base import ContentFile

def salvar_thumbnail(livro, url_thumbnail):
    """
    Faz o download da imagem da URL fornecida e a salva no campo thumbnail do modelo Livro.
    
    :param livro: Instância do modelo Book
    :param url_thumbnail: URL da miniatura a ser baixada
    """
    try:
        response = requests.get(url_thumbnail)
        if response.status_code == 200:
            livro.thumbnail.save(
                f"{livro.title.replace(' ', '_')}_thumbnail.jpg",  # Nome do arquivo
                ContentFile(response.content),  # Conteúdo da imagem
                save=True  # Salva no modelo
            )
    except Exception as e:
        print(f"Erro ao salvar a miniatura: {e}")
