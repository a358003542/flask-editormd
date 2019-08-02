flask-editormd
===============
Implementation of editor.md the markdown editor for Flask and Flask-WTF.

description
----------------
Please waiting...

It's combined the editor.md version `1.5.0` .


usage
---------
::

    from flask_editormd import Editormd
    editormd = Editormd()
    editormd.init_app(app)


the editormd object is auto inject to the jinja2 template.

::

    <!DOCTYPE html>
    <html>
    <head>

    </head>
    <body>


    <div id="editormd-1">
        <textarea style="display:none;">### 关于 Editor.md

    **Editor.md** 是一款开源的、可嵌入的 Markdown 在线编辑器（组件），基于 CodeMirror、jQuery 和 Marked 构建。
        </textarea>
    </div>


    {{editormd.include_editormd()}}


    {{editormd.add_editormd_js("editormd-1", height="850px")}}


    </body>
    </html>

