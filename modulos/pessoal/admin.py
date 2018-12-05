#-*- coding: utf-8 -*-
from django.contrib import admin
from models import Aluno, Professor, Matricula, Duvida, Visita, MotivoCancelamento
from forms import FormAluno

class MotivoAdmin(admin.ModelAdmin):
    #add_form = FormCadastro
    #form = FormCadastro
    list_display = ['motivo', 'dataCadastro']

class AlunoAdmin(admin.ModelAdmin):
    #add_form = FormCadastro
    #form = FormCadastro
    list_display = ['email', 'status', 'nome', 'cpf', 'telefone', 'dataCadastro']

class ProfessorAdmin(admin.ModelAdmin):
    #add_form = FormCadastro
    #form = FormCadastro
    list_display = [ 'email', 'status', 'nome', 'cpf', 'telefone', 'dataCadastro']

class DuvidaAdmin(admin.ModelAdmin):
    #add_form = FormCadastro
    #form = FormCadastro
    list_display = [ 'aluno', 'pergunta', 'resposta', 'dataCadastro']

class MatriculaAdmin(admin.ModelAdmin):
    #add_form = FormCadastro
    #form = FormCadastro
    list_display = ['aluno', 'status', 'numero', 'curso', 'formasDePagamento', 'inicioDoPeriodo', 'terminoDoPeriodo']

class VisitaAdmin(admin.ModelAdmin):
    #add_form = FormCadastro
    #form = FormCadastro
    list_display = ['aluno', 'horario']

admin.site.register(MotivoCancelamento, MotivoAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Duvida, DuvidaAdmin)
admin.site.register(Matricula, MatriculaAdmin)
admin.site.register(Visita, VisitaAdmin)
