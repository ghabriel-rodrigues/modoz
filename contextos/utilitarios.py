#-*- coding: utf-8 -*-
from django.conf import settings
import os

def utilidades(request):
    site = None

    myhost = os.uname()[1]
    if myhost == 'ghabriel-pc':
        site = 'http://localhost:8000/'
    else:
        site = 'devpublicon.kinghost.net/modoz'

    return {'site':site}
