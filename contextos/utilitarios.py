#-*- coding: utf-8 -*-
from django.conf import settings
import os

from modoz.modulos.pessoal.models import Aluno,Matricula
from modoz.modulos.institucional.models import TelaInicialDoAluno

def utilidades(request):
    site = None
    online = True
    usuario = None
    aluno = None
    telaInicialDoAluno = None
    matriculas = None

    try:
        usuario = request.user
        aluno = Aluno.objects.get(email__exact=usuario.email)
        telaInicialDoAluno = TelaInicialDoAluno.objects.get(id=1)
        matriculas = Matricula.objects.filter(aluno__email__exact=usuario.email)

    except:
        pass

    myhost = os.uname()[1]
    if myhost == 'ghabriel-pc':
        site = 'http://localhost:8000/'
        online = False
    else:
        site = 'devpublicon.kinghost.net/modoz'

    return {'site':site, 'online':online, 'usuario': usuario,
    'aluno': aluno, 'telaInicialDoAluno': telaInicialDoAluno,
     'matriculas': matriculas}
