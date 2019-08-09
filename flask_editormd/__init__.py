#!/usr/bin/env python
# -*-coding:utf-8-*-


"""Implementation of editor.md the markdown editor for Flask."""

__softname__ = 'flask_editormd'
__version__ = '0.0.2'

import json
from jinja2 import Markup
from flask import current_app
from flask import url_for
from flask import Blueprint
from wtforms.validators import ValidationError

editormd_object_name = 'editor'
editormd_previewer_object_name = 'editor_previewer'


class _editormd(object):
    """
    """
    editormd_id_name = None

    def add_editormd_js(self, editormd_id_name=None, **kwargs):
        """
        :return:
        """
        if editormd_id_name is None:
            self.editormd_id_name = editormd_id_name = 'editor1'
        else:
            if editormd_id_name == 'editor':
                raise ValidationError('editormd_id_name can not set to editor')
            else:
                self.editormd_id_name = editormd_id_name

        editor_kwargs = {
            'path': "{0}".format(url_for('editormd.static', filename='lib/'))
        }
        editor_kwargs.update(kwargs)

        editor_kwargs_str = json.dumps(editor_kwargs)

        return Markup("""<script type="text/javascript">
        $(function () {{
            var {editormd_object_name} = editormd("{editormd_id_name}", {editor_kwargs_str}
            );
            window["{editormd_object_name}"] = {editormd_object_name};
        }});
    </script>""".format(
            editor_kwargs_str=editor_kwargs_str,
            editormd_object_name=editormd_object_name,
            editormd_id_name=self.editormd_id_name
        ))

    def add_editormd_preview_js(self, editormd_id_name=None, **kwargs):
        """
        :return:
        """
        if editormd_id_name is None:
            self.editormd_id_name = editormd_id_name = 'editor1'
        else:
            if editormd_id_name == 'editor':
                raise ('editormd_id_name can not set to editor')
            else:
                self.editormd_id_name = editormd_id_name

        editor_kwargs = {}
        editor_kwargs.update(kwargs)

        editor_kwargs_str = json.dumps(editor_kwargs)

        return Markup("""<script type="text/javascript">
        $(function () {{
            var {editormd_previewer_object_name} = editormd.markdownToHTML("{editormd_id_name}", {editor_kwargs_str}
            );
            window["{editormd_previewer_object_name}"] = {editormd_previewer_object_name};
        }});
    </script>""".format(
            editor_kwargs_str=editor_kwargs_str,
            editormd_previewer_object_name=editormd_previewer_object_name,
            editormd_id_name=self.editormd_id_name
        ))


class Editormd(object):
    """
    from flask_editormd import Editormd
    editormd = Editormd()
    editormd.init_app(app)
    """

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        blueprint = Blueprint(
            'editormd',
            __name__,
            template_folder='templates',
            static_folder='static',
            static_url_path=app.static_url_path + '/editormd', )

        app.register_blueprint(blueprint)

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['editormd'] = _editormd()
        app.context_processor(self.context_processor)

    @staticmethod
    def context_processor():  # 向模板上下文注入变量
        return {'editormd': current_app.extensions['editormd']}
