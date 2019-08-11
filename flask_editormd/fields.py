#!/usr/bin/env python
# -*-coding:utf-8-*-


from wtforms.fields import TextAreaField

from .widgets import Editormd
from . import default_editor_id


class EditormdField(TextAreaField):
    def __init__(self, editor_id=default_editor_id, **kwargs):
        super(EditormdField, self).__init__(**kwargs)
        self.editor_id = editor_id

    widget = Editormd()
