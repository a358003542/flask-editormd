# flask-editormd
Implementation of editor.md the markdown editor for Flask and Flask-WTF.


## description
It's combined the editor.md version `1.5.0` .


## usage

```
from flask_editormd import Editormd
editormd = Editormd()
editormd.init_app(app)
```

the editormd object is auto inject to the jinja2 template.

### Editor
```jinja2
{% extends "editormd/editor.html" %}
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

{{ editormd.add_editormd(autoHeight=True)}}

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
{% extends "editormd/preview.html" %}

{% block content -%}

{{ editormd.add_editormd_previewer(cotnent) }}

{%- endblock content %}

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