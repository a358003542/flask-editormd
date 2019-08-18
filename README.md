# flask-editormd
Implementation of editor.md the markdown editor for Flask and Flask-WTF.


## description
It's combined the [editor.md](https://github.com/pandao/editor.md) version `1.5.0` .



## usage

```
from flask_editormd import Editormd
editormd = Editormd()
editormd.init_app(app)
```

the editormd object is auto inject to the jinja2 template.

### Editor
```jinja2
{% extends "bootstrap/base.html" %}
{% import "bootstrap/wtf.html" as wtf %}

{% block content -%}

<form method="POST">
    {{ form.hidden_tag() }}

    {{ form.body() }}

    {{ wtf.form_field(form.submit) }}
</form>

{%- endblock content %}


{% block scripts %}
{{ super() }}

{{ editormd.add_editormd_resource(autoLoadModules=False) }}
{{ editormd.add_editormd(autoHeight=True, autoLoadModules=False)}}

{%- endblock scripts %}
```

```python
from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_editormd import Editormd
from flask_bootstrap import Bootstrap
from flask_editormd.fields import EditormdField
from wtforms.fields import SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
editormd = Editormd(app)
Bootstrap(app)

class EditormdForm(FlaskForm):
    body = EditormdField()
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = EditormdForm()
    if form.validate_on_submit():
        text = form.body.data
        print(text)

    return render_template('index.html', form=form)
```


### Preview
```jinja2
{% extends "bootstrap/base.html" %}

{% block content -%}

{{ editormd.add_editormd_previewer(content) }}


{%- endblock content %}


{% block scripts %}
{{ super() }}
{{ editormd.add_editormd_previewer_resource() }}

{%- endblock scripts %}

```

```python
from flask import Flask, render_template
from flask_editormd import Editormd
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
editormd = Editormd(app)
Bootstrap(app)

@app.route('/preview', methods=['GET', 'POST'])
def preview():
    content = """
    ###科学公式 TeX(KaTeX)
                    
$$E=mc^2$$

行内的公式$$E=mc^2$$行内的公式，行内的$$E=mc^2$$公式。

$$\(\sqrt{3x-1}+(1+x)^2\)$$
                    
$$\sin(\alpha)^{\theta}=\sum_{i=0}^{n}(x^i + \cos(f))$$

$$X^2 > Y$$

#####上标和下标

上标：X&lt;sup&gt;2&lt;/sup&gt;

下标：O&lt;sub&gt;2&lt;/sub&gt;
"""
    return render_template('preview.html', content=content)
```


## API
可以配置flask下这些配置，默认都为 `True` ，即启用cdn资源。
- CODEMIRROR_CSS_CDN
- CODEMIRROR_JS_CDN
- MARKED_JS_CDN
- PRETTIFY_JS_CDN

### add_editormd和add_editormd_resource
针对editormd的某个编辑器的配置接口，editormd文档描述的那些参数都可以传递过去：
```jinja2
    {{ editormd.add_editormd_resource(autoLoadModules=False) }}

    {{ editormd.add_editormd(toolbarIcons=["undo", "redo", "|", "bold", "del", "italic","quote", "|", "list-ul", "list-ol", "hr", "|", "link","reference-link","image","|","code-block", "table","html-entities","|", "goto-line", "watch", "unwatch","preview","fullscreen", "help"], autoHeight=True, appendMarkdown="\n\n\n\n\n",autoLoadModules=False, autoLoadPlugins=True) }}
```

- autoLoadModules 默认 `True` 自动加载本地editormd的模块，如果设置为False，那么记得 `add_editormd_resource` 也要设置 `autoLoadModules=False` 好加载额外需要的本地模块资源，

- autoLoadPlugins 默认为 `False`，你可能并不需要加载插件资源，比如editormd的simple模式，如果需要加载插件那么将其设置为 `True` 。

### add_editormd_previewer 和 add_editormd_previewer_resource
针对editormd的markdown文件预览接口，具体使用很简单，除了 `add_editormd_previewer` 将markdown content 传递进去即可，并不其他参数。

可以在jinja2上执行多次 `add_editormd_previewer` 添加多个文章预览。
```jinja2
{{ editormd.add_editormd_previewer(post.body) }}

{{ editormd.add_editormd_previewer_resource() }}

```