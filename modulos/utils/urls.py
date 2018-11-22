#-*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('modoz.modulos.utils.utils',
#    (r'^verificar_cep/(?P<cep>.*)/$', 'pesquisar_cep_view'),
#    (r'^calculo_frete/(?P<servico>.*)/(?P<origem>.*)/(?P<destino>.*)/(?P<peso>.*)/$', 'calcular_frete_view',),
    (r'^cropar_imagem/(?P<imagem_name>.*)/$', 'cropar_imagem_view'),
    (r'^excluir-foto/(?P<caminho_imagem>.*)', 'excluir_foto_ajax'),
    (r'^xls/$', 'xls_view'),
)