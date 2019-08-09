#!/usr/bin/env python
# -*-coding:utf-8-*-


"""Implementation of editor.md the markdown editor for Flask and Flask-WTF."""

__softname__ = 'flask_editormd'
__version__ = '0.0.4'

import json
from jinja2 import Markup
from flask import current_app
from flask import url_for
from flask import Blueprint
from wtforms.validators import ValidationError

editormd_object_name = 'editor'
editormd_id_name = 'editor1'


class _editormd(object):
    """
    """
    viewer_count = 0  # 默认计数器 防止重名现象

    def create_default_viewer_name(self):
        """
        创建下一个默认的名字
        :return:
        """
        if self.viewer_count > 100000:  #
            self.viewer_count = 0

        self.viewer_count += 1
        return 'editormd-viewer-{0}'.format(self.viewer_count)

    def add_editormd(self, **kwargs):
        """
        一般只有一个编辑器 多个应该也是支持的
        :return:
        """
        global editormd_id_name

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
            editormd_id_name=editormd_id_name
        ))

    def add_editormd_previewer(self, md_content, editormd_previewer_id=None,
                               **kwargs):
        """
        :return:
        """
        if editormd_previewer_id is None:
            editormd_previewer_id = self.create_default_viewer_name()
        else:
            if editormd_previewer_id == 'editor':
                raise ValidationError('editormd_id_name can not set to editor')

        editor_kwargs = {}
        editor_kwargs.update(kwargs)

        editor_kwargs_str = json.dumps(editor_kwargs)

        return Markup("""
        <div id="{editormd_id_name}">
            <textarea style="display:none;">{md_content}</textarea>
        </div>
        
        <script type="text/javascript">
        function whenAllAvailable(names, callback) {{
            var interval = 30; // ms
            window.setTimeout(function () {{
                if (names.every(function(name) {{ return window[name] }}) ) {{
                    callback();
                }} else {{
                    window.setTimeout(arguments.callee, interval);
                }}
            }}, interval);
        }};
        var func = function () {{
            var editormd_previewer = editormd.markdownToHTML("{editormd_id_name}", {editor_kwargs_str}
            );
        }};
        whenAllAvailable(["editormd","marked"], func);
    </script>""".format(
            editor_kwargs_str=editor_kwargs_str,
            editormd_id_name=editormd_previewer_id,
            md_content=md_content
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
