#!/usr/bin/env python
# -*-coding:utf-8-*-


"""Implementation of editor.md the markdown editor for Flask and Flask-WTF."""

__softname__ = 'flask_editormd'
__version__ = '0.0.3'

import json
from jinja2 import Markup
from flask import current_app
from flask import url_for
from flask import Blueprint
from wtforms.validators import ValidationError
from queue import Queue

editormd_object_name = 'editor'


class _editormd(object):
    """
    """
    viewer_count = 0  # 默认计数器 防止重名现象
    editor_count = 0
    q_editormd_name = Queue()  # 编辑器的名字队列

    def create_default_viewer_name(self):
        """
        创建下一个默认的名字
        :return:
        """
        if self.viewer_count > 100000:  #
            self.viewer_count = 0

        self.viewer_count += 1
        return 'editormd-viewer-{0}'.format(self.viewer_count)

    def put_editormd_name(self):
        self.editor_count += 1
        name = 'editormd-{0}'.format(self.editor_count)
        self.q_editormd_name.put(name)
        return name

    def get_editormd_name(self):
        self.editor_count -= 1
        name = self.q_editormd_name.get()
        return name

    def add_editormd_js(self, editormd_id_name=None, **kwargs):
        """
        一般只有一个编辑器 多个应该也是支持的
        :return:
        """
        if editormd_id_name is None:
            editormd_id_name = self.get_editormd_name()
        else:
            if editormd_id_name == 'editor':
                raise ValidationError('editormd_id_name can not set to editor')

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

    def add_editormd_previewer(self, md_content, editormd_id_name=None,
                               **kwargs):
        """
        :return:
        """
        if editormd_id_name is None:
            editormd_id_name = self.create_default_viewer_name()
        else:
            if editormd_id_name == 'editor':
                raise ValidationError('editormd_id_name can not set to editor')

        editor_kwargs = {}
        editor_kwargs.update(kwargs)

        editor_kwargs_str = json.dumps(editor_kwargs)

        return Markup("""
        <div id="{editormd_id_name}">
            <textarea style="display:none;">{md_content}</textarea>
        </div>
        
        <script type="text/javascript">
        function whenAvailable(name, callback) {{
            var interval = 10; // ms
            window.setTimeout(function () {{
                if (window[name]) {{
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
        whenAvailable("editormd", func);
    </script>""".format(
            editor_kwargs_str=editor_kwargs_str,
            editormd_id_name=editormd_id_name,
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
