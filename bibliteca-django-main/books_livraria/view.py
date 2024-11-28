from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
def custom_view(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')  # Redireciona para a página de login
    return redirect('/library')  # Substitua pelo template correto

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Salva o novo usuário no banco de dados
            return redirect('login')  # Redireciona para a página de login
    else:
        form = UserCreationForm()  # Exibe o formulário vazio
    return render(request, 'registration/signup.html', {'form': form})