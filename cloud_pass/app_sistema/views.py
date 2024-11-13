from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Credential
from django.contrib.auth.decorators import login_required  # Importando corretamente
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.views.decorators.cache import never_cache


def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Faz o login do usuário
            return redirect('home')  # Redirecione para a página inicial após o login
        else:
            return render(request, 'index.html', {'error': 'Usuário ou senha inválidos.'})

    return render(request, 'index.html')

@never_cache
@login_required
def home(request):
    return render(request, 'home.html')

@never_cache
@login_required
def register_password(request):
    if request.method == 'POST':
        system = request.POST['system']
        module = request.POST['module']
        login = request.POST['login']
        password = request.POST['password']  # senha fornecida pelo usuário

        # Cria a instância da credencial com a senha crua (será criptografada no model)
        Credential.objects.create(
            user=request.user,
            system=system,
            module=module,
            login=login,
            encrypted_password=password  # Aqui estamos passando a senha, o model lida com a criptografia
        )
        
        return redirect('home')  # Redireciona para a página inicial após o cadastro
    
    return render(request, 'register_password.html')

@never_cache
@login_required
def list_credentials(request):
    # Busca todas as credenciais do usuário logado
    credentials = Credential.objects.filter(user=request.user)
    
    # Descriptografa as senhas antes de passar para o template
    for credential in credentials:
        credential.decrypted_password = credential.get_decrypted_password()
    
    return render(request, 'list_credentials.html', {'credentials': credentials})

# Usando a LogoutView padrão
class CustomLogoutView(LogoutView):
    def get_next_page(self):
        messages.success(self.request, "Você foi desconectado com sucesso.")
        return '/'  # Redireciona para a página de índice após o logout
    
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('index')  # Se não estiver autenticado, redireciona para a página inicial
        return super().dispatch(request, *args, **kwargs)
