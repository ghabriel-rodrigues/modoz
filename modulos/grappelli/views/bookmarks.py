# -*- coding: utf-8 -*-

# imports
import urllib

# django imports
from django.shortcuts import HttpResponse, render_to_response
from django.http import HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import ugettext as _

# grappelli imports
from modulos.grappelli.models.bookmarks import Bookmark, BookmarkItem
from modulos.grappelli.settings import ADMIN_TITLE, ADMIN_URL


def add_bookmark(request):
    """
    Add Site to Bookmarks.
    """
    
    if request.method == 'POST':
        if request.POST.get('path') and request.POST.get('title'):
            next = urllib.unquote(request.POST.get('path'))
            try:
                bookmark = Bookmark.objects.get(user=request.user)
            except Bookmark.DoesNotExist:
                bookmark = Bookmark(user=request.user)
                bookmark.save()
            try:
                bookmarkitem = BookmarkItem.objects.get(bookmark=bookmark, link=urllib.unquote(request.POST.get('path')))
                msg = ['error', 'A pagina já esta cadastrada como Atalho.']
            except BookmarkItem.DoesNotExist:
                try:
                    bookmarkitem = BookmarkItem(bookmark=bookmark, title=request.POST.get('title'), link=urllib.unquote(request.POST.get('path')))
                    bookmarkitem.save()
                    msg = ['success', 'A pagina foi adicionada aos Atalhos.']
                except:
                    msg = ['error', 'A pagina não pode ser adicionada aos Atalhos']
        else:
            msg = ['error', 'A pagina não pode ser adicionada aos Atalhos']
            next = request.POST.get('path')
    else:
        msg = ['error', 'A pagina não pode ser adicionada aos Atalhos']
        next = ADMIN_URL
    
    # MESSAGE & REDIRECT
    if not request.session.get('grappelli'):
        request.session['grappelli'] = {}
    request.session['grappelli']['message'] = msg
    request.session.modified = True
    return HttpResponseRedirect(next)
add_bookmark = staff_member_required(add_bookmark)


def remove_bookmark(request):
    """
    Remove Site from Bookmarks.
    """
    
    if request.GET:
        if request.GET.get('path'):
            next = urllib.unquote(request.GET.get('path'))
            try:
                bookmarkitem = BookmarkItem.objects.get(bookmark__user=request.user, link=urllib.unquote(request.GET.get('path')))
                bookmarkitem.delete()
                msg = ['success', 'A pagina foi removida dos Atalhos']
            except BookmarkItem.DoesNotExist:
                msg = ['error', 'A pagina não pode ser removida dos Atalhos']
        else:
            msg = ['error', 'A pagina não pode ser removida dos Atalhos']
            next = ADMIN_URL
    else:
        msg = ['error', 'A pagina não pode ser removida dos Atalhos']
    
    # MESSAGE & REDIRECT
    if not request.session.get('grappelli'):
        request.session['grappelli'] = {}
    request.session['grappelli']['message'] = msg
    request.session.modified = True
    return HttpResponseRedirect(next)
remove_bookmark = staff_member_required(remove_bookmark)


def get_bookmark(request):
    """
    Get Bookmarks for the currently logged-in User (AJAX request).
    """
    
    if request.method == 'GET':
        if request.GET.get('path'):
            object_list = BookmarkItem.objects.filter(bookmark__user=request.user).order_by('order')
            #print urllib.unquote(request.GET.get('path'))
            try:
                bookmark = Bookmark.objects.get(user=request.user)
            except Bookmark.DoesNotExist:
                bookmark = Bookmark(user=request.user)
                bookmark.save()
            try:
                BookmarkItem.objects.get(bookmark__user=request.user, link=urllib.unquote(request.GET.get('path')))
                is_bookmark = True
            except BookmarkItem.DoesNotExist:
                is_bookmark = False
        else:
            object_list = ""
            is_bookmark = ""
    else:
        object_list = ""
        is_bookmark = ""
    
    return render_to_response('admin/includes_grappelli/bookmarks.html', {
        'object_list': object_list,
        'bookmark': bookmark,
        'is_bookmark': is_bookmark,
        'admin_title': ADMIN_TITLE,
        'path': request.GET.get('path', ''),
    })
get_bookmark = staff_member_required(get_bookmark)

