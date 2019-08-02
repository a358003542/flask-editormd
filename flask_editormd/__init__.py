#!/usr/bin/env python
# -*-coding:utf-8-*-


"""Implementation of editor.md the markdown editor for Flask and Flask-WTF."""

__softname__ = 'flask_editormd'
__version__ = '0.0.1'

import json
from jinja2 import Markup
from flask import current_app
from flask import url_for


class _editormd(object):
    """

    """

    def add_editormd_js(self, editormd_id, **kwargs):
        """
        :param editormd_id:
        :param kwargs:
        :return:
        """
        editor_kwargs = {
            'path': "{0}".format(url_for('editormd.static', filename='lib/'))
        }
        editor_kwargs.update(kwargs)

        editor_kwargs_str = json.dumps(editor_kwargs)

        return Markup("""
        <script type="text/javascript">
    $(function () {{
        var editor = editormd("{editormd_id}", {editor_kwargs_str}
        );
    }});
</script>""".format(editormd_id=editormd_id,
                    editor_kwargs_str=editor_kwargs_str))

    def include_editormd(self):
        """

        :return:
        """
        return Markup('''

<script src="https://cdn.bootcss.com/jquery/1.11.3/jquery.min.js"></script>

<link rel="stylesheet"
      href="{editormd_min_css}"/>
<script src="{editormd_min_js}"></script>
            '''.format(
            editormd_min_css=url_for('editormd.static',
                                     filename='css/editormd.min.css'),
            editormd_min_js=url_for('editormd.static',
                                    filename='js/editormd.min.js')
        ))

    def assure_include_jquery(self):
        return Markup('''
            <script src="https://cdn.bootcss.com/jquery/1.11.3/jquery.min.js"></script>
            ''')


from flask import Blueprint


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
