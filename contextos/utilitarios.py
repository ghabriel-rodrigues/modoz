#-*- coding: utf-8 -*-
from django.conf import settings
import os

def utilidades(request):
    site = None
    online = True
    usuario = None
    try:
        usuario = request.user
    except:
        pass

    myhost = os.uname()[1]
    if myhost == 'ghabriel-pc':
        site = 'http://localhost:8000/'
        online = False
    else:
        site = 'devpublicon.kinghost.net/modoz'

    return {'site':site, 'online':online, 'usuario': usuario}
