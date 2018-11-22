#-*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
import os
import sys
import urllib2

try:
    import Image
except ImportError:
    try:
        #from modoz.modulos.PIL import Image
        pass
    except ImportError:
        raise ImportError((u"Crop não conseguiu importar a biblioteca de imagem do Python (Python Imaging Library)."))

from modoz.modulos import xlrd
import csv

def xls_view(request):
    livro = xlrd.open_workbook("/home/silvio/teste.xls")
    sheet = livro.sheet_by_index(0)
    nome = []
  #  for coluna in range(sheet.ncols):
  #      nome.append(sheet.cell_value(0, coluna))
    writer = csv.writer(open("/home/silvio/teste_converter.csv", "wb"))
    for linha in range(2, sheet.nrows):
        writer.writerow(unicode(sheet.row_values(linha)).encode('utf-8'))
    variaveis = RequestContext(request, {"colunas": nome, "linha": sheet.row_values(1)})
    return render_to_response("xls_teste.html", variaveis)


#View normalmente usada no response_add e response_change do ModelAdmin para cropar imagem.
def cropar_imagem_view(request, imagem_name, post_redirect = "../", largura = None, altura = None, proporcao = None, POST_DATA = False):
    if imagem_name:
        imagem_src = "%s/%s" % (settings.MEDIA_URL, imagem_name)
        imagem_root = "%s/%s" % (settings.MEDIA_ROOT, imagem_name)
        if request.method == "POST" and POST_DATA == False:
            dimensao_crop = (int(request.POST['x']), int(request.POST['y']), int(request.POST['x2']), int(request.POST['y2']))
            imagem = Image.open(imagem_root)
            imagem_crop = imagem.crop(dimensao_crop)
            imagem_crop.save(imagem_root, imagem.format, quality = 95)
            redirecionar = request.POST['redirect']
            path_redirect = redirecionar[0:redirecionar.rfind("/", 0, -1)]
            request.session['obj_crop'].criar_miniaturas()
            request.session['obj_crop'] = None
            return HttpResponseRedirect(path_redirect)
        variaveis = RequestContext(request, {'imagem_name': imagem_name, 'imagem_src': imagem_src, 'post_redirect': request.path, "largura": largura, "altura":altura, "proporcao": proporcao})
        return render_to_response('utils/crop_padrao.html', variaveis)
    else:
        return HttpResponseRedirect("../")

#Função para criação de miniaturas, substitui a thumbnails do modulo Imagem da PIL por ser mais flexivel
def criar_miniatura(caminho_imagem, dimencoes, thumbnail_path, proporcional, forcar = False):
        foto = Image.open(caminho_imagem)
        foto.load()
        largura, altura = dimencoes
        largura_original, altura_original = foto.size
        thumbnail_path = thumbnail_path
        if proporcional :
            nova_largura = (largura_original * altura) / altura_original
            nova_altura = (altura_original * largura) / largura_original
            dimencoes = (largura, nova_altura)
            thumb = foto.resize(dimencoes, Image.ANTIALIAS)
        else:
            if forcar:
                thumb = foto.resize(dimencoes, Image.ANTIALIAS)
            else:
                if largura_original < altura_original:
                    nova_altura = (largura * altura_original) / largura_original
                    nova_largura = altura
                elif altura_original < largura_original:
                    nova_largura = largura
                    nova_altura = (altura * largura_original) / largura
                else:
                    nova_largura = largura
                    nova_altura = altura
              #  if nova_altura < altura:
              #      nova_largura = altura
              #      nova_altura = (altura * largura_original) / largura_original
                dimencoes = (nova_largura, nova_altura)
                thumb = foto.resize(dimencoes, Image.ANTIALIAS)
                thumb = thumb.crop((((nova_largura - largura) / 2), ((nova_altura - altura) / 2), (((nova_largura - largura) / 2) + largura), (((nova_altura - altura) / 2) + altura)))
        thumb.save(thumbnail_path, foto.format, quality = 95)

def excluir_foto_ajax(request, caminho_imagem):
    caminho_imagem = caminho_imagem.replace(settings.MEDIA_URL, settings.MEDIA_ROOT)
    os.unlink(caminho_imagem)
    return HttpResponse("nada")

#View usada pelo Plugin TinyMCE para upload e inserção de foto no texto
def handler_upload_foto(arquivo):
    nome_arquivo = arquivo.name
    diretorio_destino = "%s/img/plugin_tiny_foto/fotos/" % settings.MEDIA_ROOT
    extensao = nome_arquivo[nome_arquivo.rfind("."):]
    nome_arquivo = nome_arquivo[:nome_arquivo.rfind(".")]
    while True:
        if not os.path.exists(diretorio_destino + nome_arquivo + extensao):
            break
        nome_arquivo += "_"
    arquivo_destino = open(diretorio_destino + nome_arquivo + extensao, "wb+")
    for chunk in arquivo.chunks():
        arquivo_destino.write(chunk)
    arquivo_destino.close()
    return diretorio_destino + nome_arquivo + extensao


#Faz uma requisição ao ceplivre para consutar um cep.
#def pesquisar_cep_view(request, cep):
    #url = "http://ceplivre.pc2consultoria.com/index.php?module=cep&cep=%s&formato=xml" % cep
    #pagina = urllib2.urlopen(url)
    #dom = minidom.parse(pagina)
    #xml = dom.firstChild
    #ceplivre = xml.childNodes[1]
    #tags = {}
    #for tag in ceplivre.childNodes:
            #if tag.nodeType == tag.ELEMENT_NODE:
                #if tag.firstChild:
                    #tags[tag.tagName] = tag.firstChild.data
    #variaveis = RequestContext(request, tags)
    #return render_to_response("detalhe_cep.html", variaveis)

##Consome o webservice dos correios para calculo de frete
##Codigo de serviços
##41106 - PAC
##40010 - SEDEX
##40215 - SEDEX 10
##40290 - SEDEX HOJE
##81019 - e-SEDEX
##44105 - MALOTE
#def calcular_frete_view(request, servico, origem, destino, peso):
    #url = "http://www.correios.com.br/encomendas/precos/calculo.cfm?resposta=xml&servico=%s&cepOrigem=%s&cepDestino=%s&peso=%s" % (
        #servico, origem, destino, peso)
    #pagina = urllib2.urlopen(url)
    #tags = {}
    #try:
        #dom = minidom.parse(pagina)
        #xml = dom.firstChild
        #dados_postais = xml.childNodes[3]
        #for tag in dados_postais.childNodes:
            #if tag.nodeType == tag.ELEMENT_NODE:
                #if tag.firstChild:
                    #tags[tag.tagName] = tag.firstChild.data
        #erro = xml.childNodes[5]
        #for tag in erro.childNodes:
            #if tag.nodeType == tag.ELEMENT_NODE:
                #if tag.firstChild:
                    #tags[tag.tagName] = tag.firstChild.data
    #except ExpatError:
        #pass
    #variaveis = RequestContext(request, tags)
    #return render_to_response("calculo_frete.html", variaveis)
