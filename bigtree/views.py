#!/usr/bin/python
          # -*- coding: UTF-8 -*-
# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
import stupidtreelogic as usual
from models import Category
import datetime


# views


def index(request):
    template = loader.get_template('bigtree/index.html')
    context = RequestContext(request, {'links': {
        'generate': 'Вырастить дерево',
        'display': 'Посмотреть на дерево',
        'manage': 'Собрать урожай',
        },
    }
    )
    return HttpResponse(template.render(context))


def generate(request):
    template = loader.get_template('bigtree/generate.html')
    amount, loaded, inserted = usual.genRandomTree()
    context = RequestContext(request, {
        'success': True,
        'amount': amount,
        'loaded': loaded,
        'inserted': inserted,
    })
    return HttpResponse(template.render(context))

def display(request):
    template = loader.get_template('bigtree/treeview.html')
    context = RequestContext(request, {
        'success': True,
    })
    return HttpResponse(template.render(context))


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

                return cat_id
    elif post.__contains__('delete'):
        cat_id = post.get('cat_id', None)
        if cat_id is not None:
            c = Category.objects.get(pk=int(cat_id))
            if c is not None:
                c.delete()

                return ''
    elif post.__contains__('add'):
        # добавляем на текущий уровень
        cat_id = post.get('cat_id', None)
        if cat_id is not None and len(cat_id) > 0:
            c = Category.objects.get(pk=int(cat_id))
            if c is not None:
                new_ = usual.child(c)

                return str(new_.id)
        else:
            new_ = usual.reset(None)

            return str(new_.id)
    return None


def manage(request, *args):
    template = loader.get_template('bigtree/manage.html')
    name = ''
    description = ''
    if len(args) > 0:
        cat_id = args[0]
    else:
        cat_id = ''
    if len(request.POST) > 0:
        cat_id = make_changes(request.POST)
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

    })
    return HttpResponse(template.render(context))

def element(request):
    template = loader.get_template('bigtree/element.html')
    context = RequestContext(request, {
        'success': True,
    })
    return HttpResponse(template.render(context))

