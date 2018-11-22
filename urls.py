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

    #home
    (r'^$', 'modoz.views.index'),

    #home
    (r'^curso', 'modoz.views.curso'),

    #exercicio
    (r'^exercicio', 'modoz.views.exercicio'),


)
