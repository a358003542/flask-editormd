#!/usr/bin/env python
# -*-coding:utf-8-*-


"""Implementation of editor.md the markdown editor for Flask and Flask-WTF."""

__softname__ = 'flask_editormd'
__version__ = '0.0.6'

import logging
import json
from jinja2 import Markup
from flask import current_app
from flask import url_for
from flask import Blueprint
from wtforms.validators import ValidationError

logger = logging.getLogger(__name__)

CODEMIRROR_VERSION = '5.0.0'
CDN_PREFIX = 'cdn.bootcss.com'
MARKED_VERSION = '0.3.3'
PRETTIFY_VERSION = '188.0.0'

editormd_object_name = 'editor'
default_editor_id = 'editor1'

from flask_bootstrap import WebCDN, StaticCDN

local = StaticCDN('editormd.static')


def get_local_resource(filename):
    return local.get_resource_url(filename)


def create_webcdn(rep_name, version):
    return WebCDN(
        '//{cdn_prefix}/{rep_name}/{version}/'.format(
            cdn_prefix=CDN_PREFIX,
            rep_name=rep_name,
            version=version
        ))


codemirror_webcdn = create_webcdn('codemirror', CODEMIRROR_VERSION)
marked_webcdn = create_webcdn('marked', MARKED_VERSION)
prettify_webcdn = create_webcdn('prettify', PRETTIFY_VERSION)


def get_cdn_resource(cdn, filename, local_filename=None, condition_name=None):
    """
    可在app上配置 condition_name True 则选择cdn False 则选择local 不配置默认选择cdn
    :param condition_name:
    """
    if condition_name is None:
        choose_cdn = True
    else:
        choose_cdn = current_app.config.get(condition_name, True)

    if choose_cdn:
        return cdn.get_resource_url(filename)
    else:
        assert local_filename is not None
        return local.get_resource_url(local_filename)


upload_flag = False


def upload_url_info():
    """
    需要在flask框架下调用
    :return:
    """
    global upload_flag
    if upload_flag:
        return

    global editormd_css_url
    global editormd_js_url
    global editormd_preview_css_url
    global codemirror_css_url
    global codemirror_js_url
    global codemirror_addons_js_url
    global codemirror_modes_js_url
    global marked_js_url
    global prettify_js_url

    editormd_css_url = get_local_resource('css/editormd.min.css')
    editormd_js_url = get_local_resource('js/editormd.min.js')
    editormd_preview_css_url = get_local_resource(
        'css/editormd.preview.min.css')

    codemirror_css_url = get_cdn_resource(codemirror_webcdn,
                                          filename='codemirror.min.css',
                                          local_filename='lib/codemirror/codemirror.min.css',
                                          condition_name='CODEMIRROR_CSS_CDN')
    codemirror_js_url = get_cdn_resource(codemirror_webcdn,
                                         filename='codemirror.min.js',
                                         local_filename='lib/codemirror/codemirror.min.js',
                                         condition_name='CODEMIRROR_JS_CDN')
    codemirror_addons_js_url = get_local_resource(
        'lib/codemirror/addons.min.js')
    codemirror_modes_js_url = get_local_resource('lib/codemirror/modes.min.js')

    marked_js_url = get_cdn_resource(marked_webcdn,
                                     filename='marked.min.js',
                                     local_filename='lib/marked.min.js',
                                     condition_name='MARKED_JS_CDN')
    prettify_js_url = get_cdn_resource(prettify_webcdn,
                                       filename='prettify.min.js',
                                       local_filename='lib/prettify.min.js',
                                       condition_name='PRETTIFY_JS_CDN')

    upload_flag = True


class _editormd(object):
    """
    """
    viewer_count = 0  # 默认计数器 防止重名现象

    def create_default_viewer_id(self):
        """
        创建viewer下一个默认的名字
        :return:
        """
        if self.viewer_count > 100000:
            self.viewer_count = 0

        self.viewer_count += 1
        return 'editormd-viewer-{0}'.format(self.viewer_count)

    def add_editormd_resource(self, autoLoadModules=True,
                            previewCodeHighlight=True, flowchart=False,
                            tex=False):
        """
        one page add one function
        :return:
        """
        upload_url_info()

        if autoLoadModules:
            origin_markup = Markup("""
                 <link rel="stylesheet" href="{editormd_css_url}"/>
                 <script src="{editormd_js_url}"></script>
                 """.format(
                editormd_css_url=editormd_css_url,
                editormd_js_url=editormd_js_url,

            ))
            return origin_markup

        origin_markup = Markup("""
             <link rel="stylesheet" href="{editormd_css_url}"/>
            <link rel="stylesheet" href="{codemirror_css_url}"/>
             
             <script src="{editormd_js_url}"></script>
            <script src="{codemirror_js_url}"></script>
            <script src="{codemirror_addons_js_url}"></script>
            <script src="{codemirror_modes_js_url}"></script>
                            <script src="{marked_js_url}"></script>
             """.format(
            editormd_css_url=editormd_css_url,
            editormd_js_url=editormd_js_url,
            codemirror_css_url=codemirror_css_url,
            codemirror_js_url=codemirror_js_url,
            codemirror_addons_js_url=codemirror_addons_js_url,
            codemirror_modes_js_url=codemirror_modes_js_url,
            marked_js_url=marked_js_url
        ))

        if previewCodeHighlight:
            origin_markup += Markup("""
            <script src="{prettify_js_url}"></script>
            """.format(
                prettify_js_url=prettify_js_url
            ))

        if flowchart:
            logger.warning('not implement')

        if tex:
            logger.warning('not implement')

        return origin_markup

    def add_editormd(self, editor_id=default_editor_id, **kwargs):
        """
        you can add more than one editor
        可能执行多次 添加多个编辑器
        :return:
        """
        autoLoadModules = kwargs.get('autoLoadModules', True)
        editor_kwargs = {}

        if autoLoadModules:
            editor_kwargs['path'] = "{0}".format(
                url_for('editormd.static', filename='lib/'))

        editor_kwargs.update(kwargs)

        editor_kwargs_str = json.dumps(editor_kwargs)

        origin_markup = Markup("""
        <script type="text/javascript">
        $(function () {{
            var {editormd_object_name} = editormd("{editor_id}", {editor_kwargs_str}
            );
            window["{editormd_object_name}"] = {editormd_object_name};
        }});
    </script>""".format(
            editor_kwargs_str=editor_kwargs_str,
            editormd_object_name=editormd_object_name,
            editor_id=editor_id,
            editormd_css_url=get_local_resource('css/editormd.min.css'),
            editormd_js_url=get_local_resource('js/editormd.min.js')
        ))

        return origin_markup

    def add_editormd_previewer_resource(self):
        """
        one page add one function
        一个页面添加一个即可
        :return:
        """
        upload_url_info()

        origin_markup = Markup("""
        <link rel="stylesheet" href="{editormd_preview_css_url}"/>
        <script src="{editormd_js_url}"></script>
        <script src="{marked_js_url}"></script>             
        <script src="{prettify_js_url}"></script>
             """.format(
            editormd_preview_css_url=editormd_preview_css_url,
            editormd_js_url=editormd_js_url,
            marked_js_url=marked_js_url,
            prettify_js_url=prettify_js_url
        ))
        return origin_markup

    def add_editormd_previewer(self, md_content, previewer_id=None,
                      **kwargs):
        """
        you may add more than one editormd previewer
        可添加多个previewer
        :return:
        """
        if previewer_id is None:
            previewer_id = self.create_default_viewer_id()
        else:
            if previewer_id == 'editor':
                raise ValidationError('editormd_id_name can not set to editor')

        editor_kwargs = {}
        editor_kwargs.update(kwargs)

        editor_kwargs_str = json.dumps(editor_kwargs)

        return Markup("""
        <div id="{previewer_id}">
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
            var editormd_previewer = editormd.markdownToHTML("{previewer_id}", {editor_kwargs_str}
            );
        }};
        whenAllAvailable(["editormd","marked", "prettyPrint"], func);
    </script>""".format(
            editor_kwargs_str=editor_kwargs_str,
            previewer_id=previewer_id,
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
        app.config.setdefault('CODEMIRROR_CSS_CDN', True)
        app.config.setdefault('CODEMIRROR_JS_CDN', True)
        app.config.setdefault('MARKED_JS_CDN', True)
        app.config.setdefault('PRETTIFY_JS_CDN', True)

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
