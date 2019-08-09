#!/usr/bin/env python
# -*-coding:utf-8-*-

from wtforms.widgets import HTMLString, TextArea

editormd_pre_html = '<div id="editor1">'
editormd_post_html = '</div>'


class Editormd(TextArea):
    def __call__(self, field, **kwargs):
        html = ''
        class_ = kwargs.pop('class', '').split() + \
                 kwargs.pop('class_', '').split()
        html += editormd_pre_html + super(Editormd, self).__call__(
            field, class_=' '.join(class_), **kwargs) + editormd_post_html
        return HTMLString(html)
