#!/usr/bin/python
          # -*- coding: UTF-8 -*-
__author__ = 'winzard'


from django.contrib import admin
from bigtree.models import TreeItem
from bigtree.models import Structure
from bigtree.models import Category
from mptt.admin import MPTTModelAdmin


admin.site.register(TreeItem)
admin.site.register(Structure)

class CustomMPTTModelAdmin(MPTTModelAdmin):
    list_display = ['name']
    mptt_level_indent = 20
    mptt_indent_field = "name"
admin.site.register(Category, CustomMPTTModelAdmin)