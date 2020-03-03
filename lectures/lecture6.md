# #6 Добавление поиска. Создание постов через html-форму
## Поиск
---
Добавим форму поиска в базовый шаблон.
`base.html`
```django
<form class="form-inline my-2 my-lg-0" method="GET">
    <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search" name="q" value="{{ request.args.get('q', '') }}">
    <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
</form>
```
`method='GET'` - т.к. выполняется GET-запрос, который вернет посты
`<input ... name="q" value="{{ request.args.get('q', '') }}">` - 
`name="q"` - название поля формы. Из `q` будем считывать данные для поиска постов(q - сокращение от query(запрос))
`value="{{ request.args.get('q', '') }}"`: `request.args` - все параметры, которые мы получаем с get-запросом(не обязательно)
Запрос на поиск будет происходить по основному url с тем отличием, что в строке поиска будет передан параметр `q`:
```
http://127.0.0.1:5000/blog/?q=third
```
Поэтому отредактируем функцию-обработчик главной страницы:
`blueprint.py`
```django
...
@posts.route('/')
def index():
    q = request.args.get('q')
    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q)).all()
    else:
        posts = Post.query.order_by(Post.created.desc())
    return render_template('posts/index.html', posts=posts)
...
```

## Создание постов через html-форму
---
Сначала установим пакет для выстраивания соответствия между классами-моделями и html-формами:
```
$ pip install wtforms
```
Создадим файл `forms.py`, в котором опишем класс формы:
`forms.py`
```python
from wtforms import Form, StringField, TextAreaField


class PostForm(Form):
    title = StringField('Title')
    body = TextAreaField('Body')
```
Здесь `title` и `body` - поля нашей html-формы, типы которых `StringField` и `TextAreaField` соответвенно. В конструктор передаем соответствующие label полей.

Добавим обработчик страницы создания поста.
`blueprint.py`
```python
...
@posts.route('/create', methods=['POST', 'GET'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        try:
            post = Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        except:
            print('Error')
        return redirect(url_for('posts.index'))

    form = PostForm()
    return render_template('posts/create_post.html', form=form)
...
```
`@posts.route(..., methods=['POST', 'GET'])` - функция обрабатывает запросы 'GET' - отрисовка html-формы, 'POST' - создание нового поста.
`request.form['title']` - значение поля 'title' формы(совпадает с полем, что определили в классе). Далее в блоке `try` создаем объект поста и сохраняем его в базу данных. Далее происходит перенаправление на главную страницу в случае `POST` запроса или вывод формы - в случае `GET` запроса.

Добавим html-шаблон, в котором html-форма генерируется на основе класса `PostForm`:
`create_post.html`
```django
...
{% block content %}
    <div class="col-md-6">
        <form action="{{ url_for('posts.create_post') }}" method="POST">
            {% for field in form %}
                <div class="form-group">
                    {{ field.label(class='control-label') }}
                    {{ field(class='form-control') }}
                </div>
            {% endfor %}
            <button type="submit" class="btn btn-success">Create</button>
        </form>
    </div>
{% endblock %}
```
`action="{{ url_for('posts.create_post') }}"`: обработчик формы - вьюха выше(POST запрос)
`{{ field.label(class='control-label') }}` - `class='...'` - добавление bootstrap класса.

