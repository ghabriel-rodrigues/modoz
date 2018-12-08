#-*- coding: utf-8 -*-
from django.contrib import admin
from models import Aluno, Professor, Matricula, Duvida, Visita,MotivoCancelamento, DesempenhoDoAlunoPorAula, DesempenhoDoAlunoPorCurso, DesempenhoDoAlunoPorExercicio
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

class DesempenhoDoAlunoPorExercicioAdmin(admin.ModelAdmin):
    #add_form = FormCadastro
    #form = FormCadastro
    list_display = ['aluno', 'status', 'nota', 'exercicio', 'dataCadastro']
    list_filter = ('dataCadastro', 'status', 'nota', 'exercicio', 'aluno')
    search_fields = ['dataCadastro', 'status', 'nota', 'exercicio', 'aluno']

class DesempenhoAlunoPorAulaAdmin(admin.ModelAdmin):
    #add_form = FormCadastro
    #form = FormCadastro
    list_display = [ 'aluno', 'status', 'aula', 'dataCadastro']
    list_filter = ('aluno', 'status', 'aula', 'dataCadastro')
    search_fields = ['aluno', 'status', 'aula', 'dataCadastro']

class DesempenhoDoAlunoPorCursoAdmin(admin.ModelAdmin):
    #add_form = FormCadastro
    #form = FormCadastro
    list_display = [ 'aluno', 'status', 'curso', 'dataCadastro']
    list_filter = ('aluno', 'status', 'curso', 'dataCadastro')
    search_fields = ['aluno', 'status', 'curso', 'dataCadastro']

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
admin.site.register(DesempenhoDoAlunoPorCurso, DesempenhoDoAlunoPorCursoAdmin)
admin.site.register(DesempenhoDoAlunoPorAula, DesempenhoAlunoPorAulaAdmin)
admin.site.register(DesempenhoDoAlunoPorExercicio, DesempenhoDoAlunoPorExercicioAdmin)
