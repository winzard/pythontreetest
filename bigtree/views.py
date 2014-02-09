#!/usr/bin/python
          # -*- coding: UTF-8 -*-
# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
import stupidtreelogic as usual
from models import Category
import datetime
from django.core.cache import cache


# views

class Cache:
    cachetime = ''

def index(request):
    template = loader.get_template('bigtree/index.html')
    context = RequestContext(request, {'links': {
        'generate': 'Вырастить дерево',
        'forest': 'Вырастить лес',
        'display': 'Посмотреть на дерево',
        'manage': 'Собрать урожай',
        'clear': 'Порубать всё'
        },
    }
    )
    return HttpResponse(template.render(context))


def generate(request):
    template = loader.get_template('bigtree/generate.html')
    amount, loaded, inserted, time = usual.genRandomTree()
    context = RequestContext(request, {
        'success': True,
        'amount': amount,
        'loaded': loaded,
        'inserted': inserted,
        'time': time,
    })
    return HttpResponse(template.render(context))

def forest(request):
    template = loader.get_template('bigtree/generate.html')
    amount, loaded, inserted, time = usual.genMultiTree()
    context = RequestContext(request, {
        'success': True,
        'amount': amount,
        'loaded': loaded,
        'inserted': inserted,
        'time': time,
    })
    return HttpResponse(template.render(context))

def display(request):
    template = loader.get_template('bigtree/treeview.html')
    context = RequestContext(request, {
        'success': True,
    })
    return HttpResponse(template.render(context))


from django.db import connection
from django.db import transaction


def clear(request):
    #Category.objects.all().delete() не так всё просто. SQLite3 не может больше 999 элементов

    cursor = connection.cursor()
    cursor.execute("DELETE from bigtree_category")
    transaction.commit_unless_managed()
    html = "<html><body>Деревья удалены</body></html>"
    return HttpResponse(html)


def make_changes(post):
    if post.__contains__('save'):
        #save changes
        cat_id = post.get('cat_id', None)
        name = post.get('name', '')
        description = post.get('description', '')
        if cat_id is not None:
            c = Category.objects.get(pk=int(cat_id))
            if c is not None:
                c.name = name
                c.description = description
                # тут бы и parent поменять, но не буду, это лучше через GUI делать
                c.save()

                return cat_id, str(datetime.datetime.now())
    elif post.__contains__('delete'):
        cat_id = post.get('cat_id', None)
        if cat_id is not None:
            c = Category.objects.get(pk=int(cat_id))
            if c is not None:
                c.delete()

                return '', str(datetime.datetime.now())
    elif post.__contains__('add'):
        # добавляем на текущий уровень
        cat_id = post.get('cat_id', None)
        if cat_id is not None and len(cat_id) > 0:
            c = Category.objects.get(pk=int(cat_id))
            if c is not None:
                new_ = usual.child(c)

                return str(new_.id), str(datetime.datetime.now())
        else:
            new_ = usual.reset(None, usual.loadSpring())

            return str(new_.id), str(datetime.datetime.now())
    return None


def manage(request, *args):
    template = loader.get_template('bigtree/manage.html')
    cachetime = cache.get('cachetime', '') # вообще эти данные можно писать в базу или файл и читать оттуда, но так проще
    name = ''
    description = ''
    if len(args) > 0:
        cat_id = args[0]
    else:
        cat_id = ''
    if len(request.POST) > 0:
        cat_id, cachetime = make_changes(request.POST)
        cache.set('cachetime', cachetime)
    if len(cat_id) > 0:
        c = Category.objects.get(pk=int(cat_id))
        if c is not None:
            name = c.name
            description = c.description

    context = RequestContext(request, {
        'success': True,
        'cat_id': cat_id,
        'name': name,
        'description': description,
        'time': str(datetime.datetime.now()),
        'cachetime': cachetime

    })
    return HttpResponse(template.render(context))


def element(request):
    template = loader.get_template('bigtree/element.html')
    context = RequestContext(request, {
        'success': True,
    })
    return HttpResponse(template.render(context))

