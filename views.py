# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from django.core.mail import EmailMultiAlternatives, send_mail

from modoz.modulos.institucional.models import TelaInicialDoAluno
from modoz.modulos.pessoal.models import Matricula

from django import forms

def home_view(request):
    cad_usuario = None

    if request.session.get('cad_usuario'):
        cad_usuario = request.session["cad_usuario"]

    telaInicialDoAluno = TelaInicialDoAluno.objects.get(id=1)
    return render_to_response(
        'home.html', locals(), context_instance=RequestContext(request),)

@login_required
def index(request):
    telaInicialDoAluno = TelaInicialDoAluno.objects.get(id=1)
    #matricula = Matricula.objects.get(id=1)
    usuario = request.user
    matricula = Matricula.objects.get(aluno__email__exact=usuario.email)
    return render_to_response('index.html', locals(), context_instance=RequestContext(request),)

def esqueceusuasenha_view(request):
    erro = False

    if request.method == 'POST':
        try:
            cadastro = User.objects.get(username__exact=request.POST['email_contato'])
            nova_senha = random.randint(234567,98765432)
            cadastro.set_password(nova_senha)
            cadastro.save()
            subject, from_email, to = 'MODOZERO - Envio de nova senha', 'informativo@modozero.com.br', cadastro.email
            text_content = """
            Detectamos que voce solicitou uma NOVA SENHA: %s \n
            Por favor altere a senha por uma de sua preferencia.\nEnvio de email automatico, nao responda. """ % (str(nova_senha))
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])

            try:
                msg.send()

            except Exception :
                pass
        except:
            erro = True

    variaveis = RequestContext(request, {"erro":erro})
    return render_to_response('password_reset.html', variaveis)

@login_required
def curso(request):
    telaInicialDoAluno = TelaInicialDoAluno.objects.get(id=1)
    #matricula = Matricula.objects.get(id=1)
    usuario = request.user
    matricula = Matricula.objects.get(aluno__email__exact=usuario.email)
    return render_to_response('curso.html', locals(), context_instance=RequestContext(request),)

@login_required
def aula_view(request,aulaid):
    # checar permissao do aluno para ver essa aula
    usuario = request.user
    matricula = Matricula.objects.get(aluno__email__exact=usuario.email)
    aula = matricula.curso.aulas.get(id=aulaid)
    return render_to_response('aula.html', locals(), context_instance=RequestContext(request),)

def exercicio(request):
    return render_to_response('exercicio.html', locals(), context_instance=RequestContext(request),)
