#!/usr/bin/python
          # -*- coding: UTF-8 -*-
__author__ = 'winzard'

from _sqlite import OperationalError
import spring_loader as ya_loader
from models import Category
from random import randint
import datetime


def loadSpring(*args):
    m = Category()
    m.name, m.description = ya_loader.load_single_page()
    return m


def reset(current, element):
    try:
        element.save()
        return element
    except OperationalError:
        print 'База заблокирована'
        return current


def sibling(current, element):
    try:
        element.parent = current.parent
        element.save()
    except OperationalError:
        print 'База заблокирована'
        return current
    return element


def child(current, element):
    try:
        element.parent = current
        element.save()
    except OperationalError:
        print 'База заблокирована'
        return current
    return element


def genRandomTree():
    tree_size = 1000 - Category.objects.count()
    if tree_size > 0:
        # создаем корневой элемент
        if tree_size == 1000:
            pointer = reset(None, loadSpring())
        else:
            pointer = Category.objects.get(pk=1)  # вообще тупо
        options = { 0: reset,
                    1: sibling,
                    2: child
                    }
        begin = datetime.datetime.now()
        for _ in range(tree_size):
            pointer = options[randint(0, 2)](pointer, loadSpring())
        end = datetime.datetime.now()
        return tree_size, tree_size, tree_size, (end - begin).seconds
    else:
        return "нисколько", "ничего", "ничего"

from multiprocessing import Pool


def loadMultiSprings(amount):
    pool = Pool()
    result = [pool.apply_async(loadSpring, [t, ]) for t in xrange(amount)]
    return result


def genMultiTree():
    tree_size = 1000 - Category.objects.count()
    if tree_size > 0:
        # создаем корневой элемент
        if tree_size == 1000:
            pointer = reset(None, loadSpring())
        else:
            pointer = Category.objects.get(pk=1)  # вообще тупо
        options = { 0: reset,
                    1: sibling,
                    2: child
                    }
        begin = datetime.datetime.now()
        li = loadMultiSprings(tree_size)
        for m in li:
            pointer = options[randint(0, 2)](pointer, m.get())
        end = datetime.datetime.now()
        return tree_size, tree_size, tree_size, (end - begin).seconds
    else:
        return "нисколько", "ничего", "ничего"
