# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from django.core.mail import EmailMultiAlternatives, send_mail

from modoz.modulos.institucional.models import TelaInicialDoAluno
from modoz.modulos.pessoal.models import Matricula, Aluno, DesempenhoDoAlunoPorExercicio
from modoz.modulos.educacional.models import Curso, Aula, Exercicio, Alternativa

from django import forms
import datetime

@login_required
def home_view(request):
    cad_usuario = None

    if request.session.get('cad_usuario'):
        cad_usuario = request.session["cad_usuario"]

    telaInicialDoAluno = TelaInicialDoAluno.objects.get(id=1)
    return render_to_response(
        'home.html', locals(), context_instance=RequestContext(request),)

@login_required
def index(request):
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
def curso(request,titulourl):
    cursoSetado = None
    curso = False
    proxAula = False
    aula = False
    aulasHabilitadas = []
    aulasDesabilitadas = []
    aulasAssistidas = []
    if request.session.get('cursoSetado'):
        cursoSetado = request.session["cursoSetado"]

    cursoURL = Curso.objects.get(titulourl=titulourl)
    matriculas = Matricula.objects.filter(aluno__id__exact=request.user.id)

    for matricula in matriculas:
        if (matricula.curso.id == cursoURL.id):
            curso = cursoURL
            matriculaRef = matricula
            break


    for aulaAssistida in matriculaRef.aulasAssistidas.all():
        aulasHabilitadas.append(aulaAssistida.relates_to)
        aulasAssistidas.append(aulaAssistida)

    return render_to_response('curso.html', locals(), context_instance=RequestContext(request),)

@login_required
def cursos(request):
    return render_to_response('cursos.html', locals(), context_instance=RequestContext(request),)

@login_required
def cursosAndamento(request):
    return render_to_response('cursosAndamento.html', locals(), context_instance=RequestContext(request),)

@login_required
def cursosFinalizado(request):
    return render_to_response('cursosFinalizado.html', locals(), context_instance=RequestContext(request),)

@login_required
def aula_view(request,titulourl):
    aula = True
    # checar permissao do aluno para ver essa aula
    aulaURL = Aula.objects.get(titulourl=titulourl)
    aluno = Aluno.objects.get(id__exact=request.user.id)
    matriculas = Matricula.objects.filter(aluno__id__exact=request.user.id)
    exercicios = Exercicio.objects.filter(aula__id__exact=aulaURL.id)
    aulasHabilitadas = []

    for matricula in matriculas:
        for aula in matricula.curso.aulas.all():
            if (aula.id == aulaURL.id):
                aula = aulaURL
                if matricula.aulasAssistidas.all():
                    for aulaAssistida in matricula.aulasAssistidas.all():
                        if aulaAssistida.id == aula.id:
                            aulasHabilitadas.append(aula.relates_to)
                            aula = aulaAssistida
                            break
                else:
                    if matricula.curso.aulaInaugural.id != aula.id:
                        aula = False
                break
            else:
                aula = False

    # except Exception:
    #     aula = False

    return render_to_response('aula.html', locals(), context_instance=RequestContext(request),)

@login_required
def exercicio(request,titulourl):
    cursoSetado = None
    exercicio = None
    aulasHabilitadas = []

    exercicioURL = Exercicio.objects.get(titulourl=titulourl)
    aluno = Aluno.objects.get(id__exact=request.user.id)
    matriculas = Matricula.objects.filter(aluno__id__exact=request.user.id)
    matriculaRef = False
    cursoRef = False
    aulaComeback = False
    exercicioEnviado = False

    try:
        for matricula in matriculas:
            for aula in matricula.curso.aulas.all():
                if exercicioURL.aula.id == aula.id:
                    exercicio = exercicioURL
                    cursoRef = matricula.curso
                    matriculaRef = matricula
                    aulaComeback = aula

    except Exception:
        exercicio = False

    for aula in cursoRef.aulas.all():
        if(matriculaRef.aulasAssistidas.filter(id__exact=aula.id)):
            aulasHabilitadas.append(aula.relates_to)

    if(exercicio):
        exerciciosPorAula = Exercicio.objects.filter(aula__id__exact=aulaComeback.id)

        if request.method == 'POST':
            exercicioEnviado = True
            desempenhoExercicio = DesempenhoDoAlunoPorExercicio.create(aluno, exercicio,  datetime.datetime.now(), 'Andamento', 0)
            desempenhoExercicio.save()
            for item in request.POST.keys():
                if item == 'config' or item == 'token':
                    pass
                else:
                    alternativa = Alternativa.objects.get(id__exact=int(request.POST[item]))
                    desempenhoExercicio.respostas.add(alternativa)

            aluno = Aluno.objects.get(id__exact=request.user.id)

            corretas = 0.0
            totalQuestoes = 0.0
            for questao in desempenhoExercicio.exercicio.questoes.all():
                totalQuestoes +=1
                for marcada in desempenhoExercicio.respostas.all():
                    if(questao.respostaCorreta.id == marcada.id):
                        corretas+=1
                        desempenhoExercicio.questoesAcertadas.add(questao)

            resultado = 0.0

            if(totalQuestoes != 0):
                if(corretas != 0):
                    resultado = float((corretas /totalQuestoes )*100)
            else:
                exercicio = False

            if(exercicio):
                desempenhoExercicio.nota = resultado

                if desempenhoExercicio.exercicio.aprovarCom75:
                    if resultado >= 75:
                        desempenhoExercicio.status = 'Aprovado'
                    else:
                        desempenhoExercicio.status = 'Reprovado'
                else:
                    if corretas != 0:
                        if desempenhoExercicio.exercicio.totalQuestoes:
                            resultado2 = float((desempenhoExercicio.exercicio.totalQuestoes /totalQuestoes )*100)
                            if resultado >= resultado2:
                                desempenhoExercicio.status = 'Aprovado'
                            else:
                                desempenhoExercicio.status = 'Reprovado'
                        else:
                            if resultado >= 75:
                                 desempenhoExercicio.status = 'Aprovado'
                            else:
                                desempenhoExercicio.status = 'Reprovado'

                    else:
                        desempenhoExercicio.status = 'Reprovado'
                        desempenhoExercicio.save()


                if desempenhoExercicio.status =='Aprovado':
                    matriculaRef.aulasAssistidas.add(desempenhoExercicio.exercicio.aula)
                    matriculaRef.exerciciosConcluidos.add(desempenhoExercicio.exercicio)
                    matriculaRef.save()

                desempenhoExercicio.save()

    return render_to_response('exercicio.html', locals(), context_instance=RequestContext(request),)
