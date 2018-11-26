"""NGKS_Shop path Configuration

The `pathpatterns` list routes paths to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/paths/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a path to pathpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a path to pathpatterns:  path('', Home.as_view(), name='home')
Including another pathconf
    1. Import the include() function: from django.paths import include, path
    2. Add a path to pathpatterns:  path('blog/', include('blog.paths'))
"""
from django.conf.urls import url, include
from core.views import *
from django.contrib.auth.views import logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete

from django.conf import settings
from django.views.static import serve

from catalogo import views as views_catalogo
from checkout import views as views_checkout

urlpatterns = [
    #ecommerce
    url(r'^$', index, name='index'),
    url(r'^lista_produtos/', lista_produtos, name='lista_produtos'),
    url(r'^categoria/(?P<slug>.*)/$', loja_categoria, name='loja_categoria'),
    url(r'^produtos/(?P<slug>.*)/$', loja_produto, name='loja_produto'),
    url(r'^registro/', registro, name='registro'),
    url(r'^login/$', loginEcommerce, name='loginEcommerce'),
    url(r'^logout/$', logout, {'next_page': 'index'} ,name='logout'),
    url(r'^contato/$', contato,name='contato'),
    url(r'^checkout/', include(('checkout.urls', 'checkout'), namespace='checkout')),
    url(r'^password_reset/$', password_reset, {'subject_template_name': 'password_reset_subject.txt'}, name='password_reset'),
    url(r'^password_reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', password_reset_complete, name='password_reset_complete'),
    url(r'^paypal/', include(('paypal.standard.ipn.urls', 'paypal'), namespace='paypal')),
    #administrativo
    url(r'^principal/$', principal, name='principal'),
    url(r'^sgu/', include(('SGU.urls', 'sgu'), namespace='sgu')),
    url(r'^estoque/', include(('estoque.urls', 'estoque'), namespace='estoque')),
    url(r'^fluxo/$', fluxo, name='fluxo'),
    url(r'^pedidos/$', pedidos, name='pedidos'),
    url(r'^catalogo/', include(('catalogo.urls', 'catalogo'), namespace='catalogo')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
