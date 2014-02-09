#!/usr/bin/python
          # -*- coding: UTF-8 -*-
from django.db import models
from uuid import uuid4


from mptt.models import MPTTModel, TreeForeignKey


class UUIDField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 64)
        kwargs['unique'] = kwargs.get('unique', True)
        kwargs['editable'] = kwargs.get('editable', False)
        kwargs['blank'] = kwargs.get('blank', False)

        super(UUIDField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if add:
            value = str(uuid4())
            setattr(model_instance, self.attname, value)
            return value
        else:
            value = super(UUIDField, self).pre_save(model_instance, add)
            if not value:
                value = str(uuid4())
                setattr(model_instance, self.attname, value)
        return value


# Create your models here.
class TreeItem(models.Model):
    mid = UUIDField(primary_key=True)
    name = models.CharField('Заголовок', db_index=True, max_length=255)
    description = models.TextField('Описание', db_index=True,)


class Structure(models.Model):
    mid = UUIDField(primary_key=True)
    item_id = models.ForeignKey(TreeItem, related_name='used_id')
    item_parent = models.ForeignKey(TreeItem, related_name='used_parent')


class Category(MPTTModel):
    name = models.CharField('Заголовок', db_index=True, max_length=255, unique=False) # Яндекс, зараза, бывает дубли дает
    description = models.TextField('Описание', db_index=True,)
    parent = TreeForeignKey('self', blank=True, null=True, verbose_name="Родитель", related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

