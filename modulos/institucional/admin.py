from django.contrib import admin
from models import TelaInicialDoAluno
from django.contrib.admin.options import ModelAdmin

class TelaInicialDoAlunoAdm(ModelAdmin):
    list_display = ('titulo',)

admin.site.register(TelaInicialDoAluno,TelaInicialDoAlunoAdm)
