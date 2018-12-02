#-*- coding: utf-8 -*-
import urllib , random

from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from modoz.modulos.pessoal.forms import FormAluno,FormAlterarDados,FormCancelarMatricula,FormDuvidas
from modoz.modulos.pessoal.models import Aluno, Matricula
from modoz.modulos.institucional.models import TelaInicialDoAluno

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/modoz/')

def aluno_view(request):
    cad_usuario = None

    username = ""
    password = ""

    if request.session.get('cad_usuario'):
        cad_usuario = request.session["cad_usuario"]

    form = FormAluno()

    if request.method == 'POST':
        form = FormAluno(request.POST, request.FILES)
        if form.is_valid():
            aluno = Aluno()
            novo_usuario = form.save(commit=False)

            if request.POST['nome']:
                aluno.nome = request.POST['nome']
                novo_usuario.first_name = request.POST['nome']

            if request.POST['email']:
                try:
                    novo_usuario.username = request.POST['email']
                    novo_usuario.email = request.POST['email']
                    pessoal.email = request.POST['email']
                except:
                    pass

            novo_usuario = form.save()

            if request.POST['endereco']:
                aluno.endereco = request.POST['endereco']

            if request.POST['telefone']:
                aluno.telefone = request.POST['telefone']

            aluno.cpf = request.POST['cpf']

            if request.POST['sexo']:
                aluno.sexo = request.POST['sexo']
            try:
                aluno.opt = request.POST['opt']
            except:
                pass

            aluno.usuario = novo_usuario
            aluno.save()

            subject, from_email, to = 'MODOZERO - Cadastro realizado pelo site', 'modoz@modoz.com.br', aluno.email
            bcc = "ghabriel.rodrigues.araujo@gmail.com"

            msg = EmailMultiAlternatives(subject, "Cadastro realizado.", from_email, [to])
            html_content = '<a href="http://www.modoz.com.br/modoz/"><img src="http://www.modoz.com.br/modoz/media/img/pessoal.jpg" alt="Obrigado por se cadastrar no site" /></a>'
            msg.attach_alternative(html_content, "text/html")

            try:
                msg.send()
                enviado = True

            except Exception :
                enviado = False


            username = aluno.usuario.username
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            user.backend = 'django.contrib.auth.backends.ModelBackend'

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('http://www.modoz.com.br/modoz/')

                else:
                    conta_desabilitada = True
                    variaveis = RequestContext(request, {"conta_desabilitada":conta_desabilitada,"form":form, "cad_usuario":cad_usuario,
                                                         "username":username,"password":password})
                    return render_to_response('aluno.html', variaveis)

            variaveis = RequestContext(request, {"form":form, "cad_usuario":cad_usuario, "username":username,"password":password})
            return HttpResponseRedirect('http://www.modoz.com.br/modoz/')


    variaveis = RequestContext(request, {"form":form, "cad_usuario":cad_usuario, "username":username,"password":password})
    return render_to_response('aluno.html', variaveis)

@login_required
def alterardados_view(request):
    cad_usuario = None

    if request.session.get('cad_usuario'):
        cad_usuario = request.session["cad_usuario"]

    usuario = request.user
    aluno = Aluno.objects.get(email__exact=usuario.email)
    matricula = Matricula.objects.get(aluno__email__exact=usuario.email)
    telaInicialDoAluno = TelaInicialDoAluno.objects.get(id=1)


    enviado = False
    form = FormAlterarDados()

    if request.method == 'POST':
        form = FormAlterarDados(request.POST)
        if form.is_valid():
            usuario = User.objects.get(id__exact=request.user.id)
            usuario.set_password(request.POST['password'])

            if request.POST['nome'] != "":
                aluno.nome = request.POST['nome']
                usuario.first_name = request.POST['nome']

            usuario.save()

            aluno.nome = request.POST['nome']
            aluno.email = request.POST['email']
            aluno.endereco = request.POST['endereco']
            aluno.telefone = request.POST['telefone']
            aluno.cpf = request.POST['cpf']
            aluno.nascimento = request.POST['nascimento']
            aluno.sexo = request.POST['sexo']
            try:
                pessoal.opt = request.POST['opt']
            except:
                pass
            aluno.save()
            enviado = True

    variaveis = RequestContext(request, locals())
    return render_to_response('alterar_dados.html', variaveis)

@login_required
def cancelar_matricula_view(request):
    cad_usuario = None

    if request.session.get('cad_usuario'):
        cad_usuario = request.session["cad_usuario"]

    usuario = request.user
    aluno = Aluno.objects.get(email__exact=usuario.email)
    matricula = Matricula.objects.get(aluno__email__exact=usuario.email)
    telaInicialDoAluno = TelaInicialDoAluno.objects.get(id=1)

    enviado = False
    form = FormCancelarMatricula()

    if request.method == 'POST':
        form = FormCancelarMatricula(request.POST)
        if form.is_valid():
            usuario = User.objects.get(id__exact=request.user.id)
            usuario.set_password(request.POST['password'])

            if request.POST['nome'] != "":
                aluno.nome = request.POST['nome']
                usuario.first_name = request.POST['nome']

            usuario.save()

            aluno.nome = request.POST['nome']
            aluno.email = request.POST['email']
            aluno.telefone = request.POST['telefone']
            aluno.sexo = request.POST['sexo']
            try:
                pessoal.opt = request.POST['opt']
            except:
                pass
            aluno.save()
            enviado = True

    variaveis = RequestContext(request, locals())
    return render_to_response('cancelar_matricula.html', variaveis)


def duvidas_view(request):
    cad_usuario = None
    form = FormDuvidas()

    usuario = request.user
    aluno = Aluno.objects.get(email__exact=usuario.email)
    matricula = Matricula.objects.get(aluno__email__exact=usuario.email)
    telaInicialDoAluno = TelaInicialDoAluno.objects.get(id=1)


    if request.session.get('cad_usuario'):
        cad_usuario = request.session["cad_usuario"]


    if request.method == 'POST':
        form = FormDuvidas(request.POST)
        form.save(commit=False)

        # ///enviar email

    return render_to_response('duvidas.html',locals(),context_instance=RequestContext(request),)


def esqueceusuasenha_view(request):
    erro = False

    if request.method == 'POST':
        try:
            aluno = User.objects.get(username__exact=request.POST['email_contato'])
            nova_senha = random.randint(234567,98765432)
            aluno.set_password(nova_senha)
            aluno.save()
            subject, from_email, to = 'MODOZERO - Envio de nova senha', 'informativo@modoz.com.br', aluno.email
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
