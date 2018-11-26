from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *
from src.estoque import *
from src.usuario import Gerencia_permissao
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import *

# Create your views here.

def check_estoque(request):
    return 'ESTOQUE' in Gerencia_permissao.Pega_grupo(request)

@login_required(login_url='sgu:login')
@user_passes_test(check_estoque, login_url='sgu:erro_acesso', redirect_field_name=None)
def estoque(request):
    return render(request, "estoque.html")

@login_required(login_url='sgu:login')
@user_passes_test(check_estoque, login_url='sgu:erro_acesso', redirect_field_name=None)
def fornecedores(request):
    contexto = {
        'fornecedores': fornecedor.objects.all(),
    }
    delete = request.POST.get("delete")
    if delete:
        Gerencia_fornecedor.Deleta_fornecedor(delete)
    return render(request, "fornecedor.html", contexto)

@login_required(login_url='sgu:login')
@user_passes_test(check_estoque, login_url='sgu:erro_acesso', redirect_field_name=None)
def cadastro_fornecedor(request):
    if request.method == 'POST':
        form = cadastrar_fornecedor(request.POST)    
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('estoque:fornecedores'))
        else:
            return HttpResponseRedirect(reverse('estoque:cadastro_fornecedor'))
    contexto= {
        'form':cadastrar_fornecedor()
    }
    return render(request, "cadastro_fornecedor.html", contexto)


@login_required(login_url='sgu:login')
@user_passes_test(check_estoque, login_url='sgu:erro_acesso', redirect_field_name=None)
def fornecedor_detalhes(request, slug):
    if request.method == 'POST':
        button = request.POST.get("button")
        Gerencia_fornecedor.Atualiza_fornecedor(request, slug)
        if button == "update_continue":
            return HttpResponseRedirect(reverse('estoque:fornecedor_detalhes', kwargs={'slug':slug}))
        elif button == "update":
            return HttpResponseRedirect(reverse('estoque:fornecedores'))
    else:
        contexto = {
            'fornecedor': fornecedor.objects.get(slug=slug)
        }
    return render(request, 'fornecedor_detalhes.html', contexto)

@login_required(login_url='sgu:login')
@user_passes_test(check_estoque, login_url='sgu:erro_acesso', redirect_field_name=None)
def estoque_produtos(request):
    contexto = {
        'produtos': estoque_produto.objects.all(),
    }
    delete = request.POST.get("delete")
    if delete:
        Gerencia_produto.Deleta_produto(delete)
    return render(request, "estoque_produtos.html", contexto)

@login_required(login_url='sgu:login')
@user_passes_test(check_estoque, login_url='sgu:erro_acesso', redirect_field_name=None)
def cadastro_produto(request):
    if request.method == 'POST':
        form = cadastrar_produto(request.POST, request.FILES)    
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('estoque:estoque_produtos'))
        else:
            return HttpResponseRedirect(reverse('estoque:cadastro_produto'))
    contexto= {
        'form':cadastrar_produto()
    }
    return render(request, "cadastro_produto.html", contexto)

@login_required(login_url='sgu:login')
@user_passes_test(check_estoque, login_url='sgu:erro_acesso', redirect_field_name=None)
def produto_detalhes(request, slug):
    if request.method == 'POST':
        button = request.POST.get("button")
        Gerencia_produto.Atualiza_produto(request, slug)
        if button == "update_continue":
            return HttpResponseRedirect(reverse('estoque:produto_detalhes', kwargs={'slug':slug}))
        elif button == "update":
            return HttpResponseRedirect(reverse('estoque:estoque_produto'))
    else:
        contexto = {
            'produto': estoque_produto.objects.get(slug=slug)
        }
    return render(request, 'estoque_produto_detalhes.html', contexto)


@login_required(login_url='sgu:login')
@user_passes_test(check_estoque, login_url='sgu:erro_acesso', redirect_field_name=None)
def estoque_materia(request):
    contexto = {
        'materia': estoque_materia_prima.objects.all(),
    }
    delete = request.POST.get("delete")
    if delete:
        Gerencia_materia.Deleta_materia(delete)
    return render(request, "estoque_materia.html", contexto)

@login_required(login_url='sgu:login')
@user_passes_test(check_estoque, login_url='sgu:erro_acesso', redirect_field_name=None)
def cadastro_materia(request):
    if request.method == 'POST':
        form = cadastrar_materia(request.POST, request.FILES)    
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('estoque:estoque_materia'))
        else:
            return HttpResponseRedirect(reverse('estoque:cadastro_materia'))
    contexto= {
        'form':cadastrar_materia()
    }
    return render(request, "cadastro_materia.html", contexto)

@login_required(login_url='sgu:login')
@user_passes_test(check_estoque, login_url='sgu:erro_acesso', redirect_field_name=None)
def materia_detalhes(request, slug):
    if request.method == 'POST':
        button = request.POST.get("button")
        Gerencia_materia.Atualiza_materia(request, slug)
        if button == "update_continue":
            return HttpResponseRedirect(reverse('estoque:materia_detalhes', kwargs={'slug':slug}))
        elif button == "update":
            return HttpResponseRedirect(reverse('estoque:estoque_materia'))
    else:
        contexto = {
            'materia': estoque_materia_prima.objects.get(slug=slug)
        }
    return render(request, 'estoque_materia_detalhes.html', contexto)