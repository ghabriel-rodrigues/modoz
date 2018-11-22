# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from django.core.mail import EmailMultiAlternatives, send_mail

from modoz.modulos.institucional.models import TelaInicialDoAluno

from django import forms

def home_view(request):
    cad_usuario = None

    if request.session.get('cad_usuario'):
        cad_usuario = request.session["cad_usuario"]

    telaInicialDoAluno = TelaInicialDoAluno.objects.get(id=1)
    return render_to_response(
        'home.html', locals(), context_instance=RequestContext(request),)

def index(request):
    return render_to_response('base.html', locals(), context_instance=RequestContext(request),)

def curso(request):
    return render_to_response('curso.html', locals(), context_instance=RequestContext(request),)

def exercicio(request):
    return render_to_response('exercicio.html', locals(), context_instance=RequestContext(request),)
