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
    proxAula = False
    if request.session.get('cursoSetado'):
        cursoSetado = request.session["cursoSetado"]

    curso = Curso.objects.get(titulourl=titulourl)
    matriculas = Matricula.objects.filter(aluno__id__exact=request.user.id)

    for matricula in matriculas:
        for aula in matricula.curso.aulas.all():
            try:
                aulaAssistida = matricula.aulasAssistidas.get(id__exact=aula.id)
                proxAula = True
            except:
                pass

    return render_to_response('curso.html', locals(), context_instance=RequestContext(request),)


@login_required
def cursos(request):
    return render_to_response('cursos.html', locals(), context_instance=RequestContext(request),)

@login_required
def aula_view(request,titulourl):
    aula = True
    # checar permissao do aluno para ver essa aula
    aulaURL = Aula.objects.get(titulourl=titulourl)
    aluno = Aluno.objects.get(id__exact=request.user.id)
    matriculas = Matricula.objects.filter(aluno__id__exact=request.user.id)

    for matricula in matriculas:
        for aula in matricula.curso.aulas.all():
            if (aula.id == aulaURL.id):
                aula = aulaURL
                try:
                    aula = matricula.aulasAssistidas.filter(id__exact=aula.id).exists()
                    proxAula = aula.relates_to
                except:
                    pass
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
    aulas = []

    exercicioURL = Exercicio.objects.get(titulourl=titulourl)
    aluno = Aluno.objects.get(id__exact=request.user.id)
    matriculas = Matricula.objects.filter(aluno__id__exact=request.user.id)
    matriculaRef = None

    try:
        for matricula in matriculas:
            for aula in matricula.curso.aulas.all():
                for exercicio in aula.exercicios.all():
                    if exercicio.id == exercicioURL.id:
                        aulas.append(aula)
                        exercicio = exercicioURL
                        cursoRef = matricula.curso
                        matriculaRef = matricula
    except Exception:
        exercicio = False

    if(exercicio):
        if request.session.get('cursoSetado'):
            cursoSetado = request.session["cursoSetado"]
        else:
            cursoSetado = cursoRef
            request.session["cursoSetado"] = cursoSetado

        if request.method == 'POST':
            desempenhoExercicio = DesempenhoDoAlunoPorExercicio.create(aluno, exercicio,  datetime.datetime.now(), 'Andamento', 0)
            desempenhoExercicio.save()
            for item in request.POST.keys():
                if item == 'config' or item == 'token':
                    pass
                else:
                    alternativa = Alternativa.objects.get(id__exact=int(request.POST[item]))
                    desempenhoExercicio.respostas.add(alternativa)

            aluno = Aluno.objects.get(id__exact=request.user.id)

            corretas = 0
            totalQuestoes = 0
            for questao in desempenhoExercicio.exercicio.questoes.all():
                totalQuestoes +=1
                for marcada in desempenhoExercicio.respostas.all():
                    if(questao.respostaCorreta.id == marcada.id):
                        corretas+=1
                        desempenhoExercicio.questoesAcertadas.add(questao)

            resultado = 0

            if(totalQuestoes != 0):
                if(corretas != 0):
                    resultado = (corretas / totalQuestoes) * 100
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
                            if resultado >= desempenhoExercicio.exercicio.totalQuestoes*100:
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

                desempenhoExercicio.save()
                desempenhos = DesempenhoDoAlunoPorExercicio.objects.filter(aluno__id__exact=request.user.id).exclude(status__exact='Reprovado').filter(exercicio__id=exercicio.id)
                checarFimDeAula(matriculaRef, desempenhos)

    return render_to_response('exercicio.html', locals(), context_instance=RequestContext(request),)

def checarFimDeAula(matricula, desempenhos):
    countExerciciosFeitos = 0
    for aula in matricula.curso.aulas.all():
        totalExercicios = aula.exercicios.count()
        for exercicio in aula.exercicios.all():
            for desempenho in desempenhos:
                if desempenho.exercicio.id == exercicio.id and desempenho.status=='Aprovado':
                    countExerciciosFeitos +=1

        if countExerciciosFeitos == totalExercicios:
            matricula.aulasAssistidas.add(aula)
            matricula.save()
            break
