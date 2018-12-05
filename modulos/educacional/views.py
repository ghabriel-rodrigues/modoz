@login_required
def exercicio(request,titulourl):
    exercicio = Exercicio.objects.get(titulourl=titulourl)
    return render_to_response('exercicio.html', locals(), context_instance=RequestContext(request),)
