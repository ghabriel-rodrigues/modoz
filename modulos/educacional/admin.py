#-*- coding: utf-8 -*-
from django.contrib import admin
from models import Questao, Tema, Alternativa, Exercicio, Aula, Curso

class TemaAdmin(admin.ModelAdmin):
    list_display = ['id','titulo','dataCadastro']
    list_filter = ('titulo','dataCadastro')
    search_fields = ['titulo','dataCadastro']
    prepopulated_fields = {'titulourl':('titulo',)}

class AlternativaAdmin(admin.ModelAdmin):
    list_display = ['id','enunciadoAbreviado','dataCadastro']

class QuestaoAdmin(admin.ModelAdmin):
    list_display = ['id','perguntaAbreviada','dataCadastro']

class ExercicioAdmin(admin.ModelAdmin):
    list_display = ['id','titulo','aprovarCom75','dataCadastro']
    list_filter = ('titulo','dataCadastro')
    search_fields = ['titulo','dataCadastro']
    prepopulated_fields = {'titulourl':('titulo',)}

class AulaAdmin(admin.ModelAdmin):
    list_display = ['id','tema','titulo','dataCadastro']
    list_filter = ('titulo','dataCadastro')
    search_fields = ['titulo','dataCadastro']
    prepopulated_fields = {'titulourl':('titulo',)}

class CursoAdmin(admin.ModelAdmin):
    list_display = ['id','tema','titulo','dataCadastro']
    list_filter = ('titulo','dataCadastro')
    search_fields = ['titulo','dataCadastro']
    prepopulated_fields = {'titulourl':('titulo',)}

admin.site.register(Tema, TemaAdmin)
admin.site.register(Alternativa, AlternativaAdmin)
admin.site.register(Questao, QuestaoAdmin)
admin.site.register(Exercicio, ExercicioAdmin)
admin.site.register(Aula, AulaAdmin)
admin.site.register(Curso, CursoAdmin)
