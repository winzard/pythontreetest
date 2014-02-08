#!/usr/bin/python
          # -*- coding: UTF-8 -*-
# Create your views here.
from _sqlite import OperationalError
import spring_loader as ya_loader
from models import TreeItem, Structure

from multiprocessing import Pool
from random import randint




def loadSpring(*args):
    try:
        m = TreeItem()
        m.name, m.description = ya_loader.load_single_page()
        m.save()
    except OperationalError:
        print 'База заблокирована'
    print m.name


def loadMultiSprings(amount):
    #pool = Pool()
    #result = [pool.apply_async(loadSpring, [t,]) for t in xrange(amount)]
    for t in xrange(amount):
        loadSpring(t,)
    return amount


def reset(current, add):
    new_ = Structure()
    new_.item_id = add
    new_.item_parent = add
    new_.save()
    return new_


def sibling(current, add):
    new_ = Structure()
    new_.item_id = add
    new_.item_parent = current.item_parent
    new_.save()
    return new_


def child(current, add):
    new_ = Structure()
    new_.item_id = add
    new_.item_parent = current.item_id
    new_.save()
    return new_


def genRandomTree():
    tree_size = 1000 - TreeItem.objects.count()
    loaded = 0
    if tree_size > 0:
        loaded = loadMultiSprings(tree_size)
    leaves = Structure.objects.all()
    # только те элементы, которые еще не в дереве
    filtered = [leaf.item_id for leaf in leaves]
    elements = TreeItem.objects.all()

    inserted = len(elements) - len(leaves)
    if inserted >0:
        # создаем корневой элемент
        if len(leaves) == 0:
            root = Structure()
            root.item_id = elements[0]
            root.item_parent = elements[0]
            root.save()
            pointer = root
        else:
            pointer = leaves[0]
        options = { 0: reset,
                    1: sibling,
                    2: child
                    }
        for s in elements[1:]:
            if s not in filtered:
                pointer = options[randint(0,2)](pointer, s)

    return tree_size, loaded, inserted
