#-*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from modoz.modulos.grappelli.sites import GrappelliSite
admin.site = GrappelliSite()
admin.autodiscover()

admin.site.groups = {
    0: {
        'title': u'Pessoal', # optional
        'name': u'Pessoal',
        'apps': ['pessoal'],
        'classes': ['collapse-closed'], # optional
        'show_apps': True, # optional
    } ,
    1: {
        'title': u'Educacional', # optional
        'name': u'Educacional',
        'apps': ['educacional'],
        'classes': ['collapse-closed'], # optional
        'show_apps': True, # optional
    } ,
    2: {
        'title': u'Institucional', # optional
        'name': u'Institucional',
        'apps': ['institucional'],
        'classes': ['collapse-closed'], # optional
        'show_apps': True, # optional
    } ,
    3: {
        'title': u'Usuários e Grupos de Acesso', # optional
        'name': u'Usuários e Grupos de Acesso',
        'apps': ['auth'],
        'classes': ['collapse-closed'], # optional
        'show_apps': True, # optional
    },
    4: {
        'title': u'Sites', # optional
        'name': u'Sites',
        'apps': ['sites'],
        'classes': ['collapse-closed'], # optional
        'show_apps': False, # optional
    }
}

admin.site.collections = {
    0: {
        'title': 'User Admin',
        'groups': [0,1]
    },
}

urlpatterns = patterns('',
#configs
    #mapeamento dos arquivos estaticos
    (r'^media/(.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),

    #mapeamento do pacote admin
    (r'^admin/(.*)', admin.site.root),

    #funcionais
    (r'^grappelli/', include('modoz.modulos.grappelli.urls')),
    (r'^utils/', include('modoz.modulos.utils.urls')),

    (r'^modoz/aula/(?P<aulaid>[\w_-]+)/$', 'modoz.views.aula_view'),

    #home
    (r'^modoz/curso', 'modoz.views.curso'),

    #exercicio
    (r'^modoz/exercicio', 'modoz.views.exercicio'),

    #cadastro
    (r'^modoz/aluno/', 'modoz.modulos.pessoal.views.aluno_view'),
    (r'^modoz/alterar_dados/', 'modoz.modulos.pessoal.views.alterardados_view',{}, 'alterar_dados'),
    (r'^modoz/login/$', 'django.contrib.auth.views.login',{}, 'entrar'),
    (r'^modoz/logout/$', 'django.contrib.auth.views.logout',{'template_name': 'logout_simples.html'}, 'sair'),
    (r'^modoz/esqueceu_sua_senha/$', 'modoz.modulos.pessoal.views.esqueceusuasenha_view'),


    #home
    (r'^modoz/', 'modoz.views.index'),

    # url(r'^(?P<ofertaslug>[\w_-]+)/$', 'oferta_view', name='oferta'),



)
