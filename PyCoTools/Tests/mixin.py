# -*- coding: utf-8 -*-
"""
Copyright (c) 2010-2014 Benjamin Peterson

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

This file was downloaded from https://github.com/yupeng0921/pymixin.
"""
import sys
import types

__all__ = ['mixin', 'Mixin', 'InstantiationMixinError', 'InvalidMixinError', 'InheritMixinError']

# class_types and add_metaclass were copied from six

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    class_types = type,
else:
    class_types = (type, types.ClassType)

def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper

class InstantiationMixinError(Exception):
    pass

class InvalidMixinError(Exception):
    pass

class InheritMixinError(Exception):
    pass

def mixin_new(cls, *args, **kwargs):
    raise InstantiationMixinError(cls)

MIXIN_CLASS = None
class MixinMeta(type):
    def __new__(cls, clsname, bases, dct):
        valid_mixin = False
        if MIXIN_CLASS == None and clsname == 'Mixin' and bases == (object,):
            valid_mixin = True
        elif bases == (MIXIN_CLASS,):
            valid_mixin = True
        elif '__mixin__' in dct:
            dct.pop('__mixin__')
            valid_mixin = True
        if not valid_mixin:
            raise InheritMixinError(clsname)
        dct['__new__'] = mixin_new
        return super(MixinMeta, cls).__new__(cls, clsname, bases, dct)

@add_metaclass(MixinMeta)
class Mixin(object): pass

MIXIN_CLASS = Mixin

def copy_cls_vars(cls):
    cls_vars = cls.__dict__.copy()
    slots = cls_vars.get('__slots__')
    if slots is not None:
        if isinstance(slots, str):
            slots = [slots]
        for slots_var in slots:
            cls_vars.pop(slots_var)
    cls_vars.pop('__dict__', None)
    cls_vars.pop('__weakref__', None)
    return cls_vars

def copy_mixin(cls):
    cls_vars = copy_cls_vars(cls)
    cls_vars.pop('__new__')
    cls_bases = list(cls.__bases__)
    if Mixin in cls_bases:
        cls_bases.remove(Mixin)
        cls_bases.append(object)
    return type(cls.__name__, tuple(cls_bases), cls_vars)

def mixin(*clses):
    copied_clses = []
    for cls in clses:
        if type(cls) != MixinMeta:
            raise InvalidMixinError(cls)
        copied_cls = copy_mixin(cls)
        copied_clses.append(copied_cls)
    def generate_mixin(orig_cls):
        orig_vars = copy_cls_vars(orig_cls)
        orig_bases = list(orig_cls.__bases__)
        orig_type = type(orig_cls)
        if orig_type == MixinMeta:
            orig_vars['__mixin__'] = True
            if Mixin in orig_bases:
                orig_bases.remove(Mixin)
        return orig_type(orig_cls.__name__,
                         tuple(copied_clses) + tuple(orig_bases),
                         orig_vars)
    return generate_mixin