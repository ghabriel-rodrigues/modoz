#-*- coding: utf-8 -*-
from django.forms import ModelForm
from models import Questao, Alternativa

class FormQuestao(ModelForm):
    class Meta:
        model = Questao
        exclude = ("data")

class FormAlternativa(ModelForm):
    class Meta:
        model = Alternativa
        exclude = ("data")
