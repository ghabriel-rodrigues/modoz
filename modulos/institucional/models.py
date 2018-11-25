from django.db import models
from datetime import datetime

class TelaInicialDoAluno(models.Model):
    titulo = models.CharField(max_length=300)
    urlYoutube = models.CharField(u"Url do video", max_length=150, blank=True, null=True,help_text = u"Insira a URL do video da home.")
    conteudo = models.TextField(u"Texto do video da home",blank = True, null = True)
    textoPirataria = models.TextField(u"Texto sobre pirataria",blank = True, null = True)


    class Meta:
        verbose_name = "Tela inicial do aluno"
        verbose_name_plural = "Tela inicial do aluno"

    def __str__(self) :
        return "%s" % self.titulo

    def __unicode__(self) :
        return "%s" % self.titulo
