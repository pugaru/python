from django.shortcuts import render
from src.usuario import Gerencia_permissao
from django.contrib.auth.decorators import login_required, user_passes_test
from SGU.models import Grupos, Usuario, Permissions, Cliente
from catalogo.models import Categoria, Produto
from django.contrib.auth import authenticate
from django.contrib.auth.views import login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from SGU.forms import form_cliente, LoginForm, form_usuario
from django.urls import reverse, reverse_lazy
from src.usuario import Gerencia_usuario, Gerencia_permissao
from django.views.generic import CreateView
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from .forms import contato_forms
from django.views.generic import View, TemplateView, CreateView
from django.contrib import messages

# Create your views here.
def check_estoque(request):
    return 'ESTOQUE' in Gerencia_permissao.Pega_grupo(request)

def check_fluxo(request):
    return 'FLUXO' in Gerencia_permissao.Pega_grupo(request)

def check_pedidos(request):
    return 'PEDIDOS' in Gerencia_permissao.Pega_grupo(request)

def check_empresa(request):
    user = Usuario.objects.get(username=request.username)
    return user.tipo == 'E'

def index(request):
    contexto = {
    'index' : Produto.objects.all()
    }
    
    return render(request, 'index.html',contexto)

def lista_produtos(request):
    contexto = {
        'lista_produtos': Produto.objects.all()
    }
    return render(request, 'lista_produtos.html', contexto)

def loja_categoria(request, slug):
    categoria = Categoria.objects.get(slug=slug)
    contexto = {
        'categoria_corrente': categoria,
        'lista_produtos': Produto.objects.filter(categoria=categoria),
    }
    return render(request, 'categoria.html', contexto)

def loja_produto(request, slug):
    produto = Produto.objects.get(slug=slug)
    contexto = {
        'produto': produto,
    }
    return render(request, 'produto.html', contexto)

def loginEcommerce(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            account = authenticate(username=username, password=password)
            if account is not None:
                login(request, account)
                return HttpResponseRedirect(reverse('index'))
            else:
                form = LoginForm()
                context = {'form':form}
                return render(request, 'login.html', context)
        else:
            form = LoginForm()
            context = {'form':form}
            return render(request, 'login.html', context)
    else:
        form = LoginForm()
        context = {'form':form}
        return render(request, 'login.html', context)

class cadastro_cliente(CreateView):
    form_class = form_cliente
    template_name = 'registro.html'
    success_url = reverse_lazy('index')

registro = cadastro_cliente.as_view() 

def registro(request):    
    if request.method == 'POST':
        form = form_cliente(request.POST)
        if form.is_valid():
            Gerencia_usuario.Cria_cliente(request, form)
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponseRedirect(reverse('registro'))
    else:
        contexto = {
            "form" : form_cliente(),
            "grupos" : Grupos.objects.all(),
        }            
        return render(request, "registro.html", contexto)

def contato(request):
    success = False
    form = contato_forms(request.POST or None)
    if form.is_valid():
        form.send_mail()
        success = True
    else:
        messages.error(request, 'Formulário inválido')
    contexto = {
        'form': form,
        'success': success
    }
    return render(request, 'contato.html', contexto)
    

@login_required(login_url='sgu:login')
@user_passes_test(check_empresa, login_url='sgu:erro_acesso', redirect_field_name=None)
def principal(request):
    return render(request, "principal.html")

@login_required(login_url='sgu:login')
@user_passes_test(check_estoque, login_url='sgu:erro_acesso', redirect_field_name=None)
def estoque(request):
    return render(request, "estoque.html")

@login_required(login_url='sgu:login')
@user_passes_test(check_fluxo, login_url='sgu:erro_acesso', redirect_field_name=None)
def fluxo(request):
    return render(request, "fluxo.html")

@login_required(login_url='sgu:login')
@user_passes_test(check_pedidos, login_url='sgu:erro_acesso', redirect_field_name=None)
def pedidos(request):
    return render(request, "pedidos.html")