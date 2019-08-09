#!/usr/bin/env python
# -*-coding:utf-8-*-


from wtforms.fields import TextAreaField

from .widgets import Editormd


class EditormdField(TextAreaField):
    widget = Editormd()
