from django.db import models
from datetime import datetime

class TelaInicialDoAluno(models.Model):
    titulo = models.CharField(max_length=300)
    conteudo = models.TextField(blank = True, null = True)

    class Meta:
        verbose_name = "Tela inicial do aluno"
        verbose_name_plural = "Tela inicial do aluno"

    def __str__(self) :
        return "%s" % self.titulo

    def __unicode__(self) :
        return "%s" % self.titulo
