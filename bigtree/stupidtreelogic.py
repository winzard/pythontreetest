#!/usr/bin/python
          # -*- coding: UTF-8 -*-
__author__ = 'winzard'

from _sqlite import OperationalError
import spring_loader as ya_loader
from models import Category
from random import randint



def loadSpring(*args):
    m = Category()
    m.name, m.description = ya_loader.load_single_page()
    print m.name
    return m


def reset(current):
    try:
        new_ = loadSpring()
        new_.save()
        return new_
    except OperationalError:
        print 'База заблокирована'
        return current


def sibling(current):
    try:
        new_ = loadSpring()
        new_.parent = current.parent
        new_.save()
    except OperationalError:
        print 'База заблокирована'
        return current
    return new_


def child(current):
    try:
        new_ = loadSpring()
        new_.parent = current
        new_.save()
    except OperationalError:
        print 'База заблокирована'
        return current
    return new_


def genRandomTree():
    tree_size = 1000 - Category.objects.count()
    if tree_size >0:
        # создаем корневой элемент
        if tree_size == 1000:
            pointer = reset(None)
        else:
            pointer = Category.objects.get(pk=1)  # вообще тупо
        options = { 0: reset,
                    1: sibling,
                    2: child
                    }
        for _ in range(tree_size):
            pointer = options[randint(0, 2)](pointer)
        return tree_size, tree_size, tree_size
    else:
        return "нисколько", "ничего", "ничего"

