# #3 Blueprints

Мы можем выносить функциональность в различные модули. В Django это называется applications, во Flask - **blueprints**. Т.е. **blueprint** - блок некоторой изолированной функциональности со своим поведением и шаблонами.

Конструктор blueprint'a имеет вид:
`Blueprint('название', __name__, template_folder='адрес папки с шаблонами')`
В конструктор Blueprint'a нужно передавать **\__name__** - т.к. относительного пути данного файла Flask будет находить шаблоны и другие файлы, необходимые для работы blueprint'a.
`posts\blueprint.py`
```python
from flask import Blueprint

posts = Blueprint('posts', __name__, template_folder='templates')
```

Далее нужно зарегистрировать blueprint в нашем приложении: В `app.py` импортируем объект blueprint'a: `from posts.blueprint import posts`. Далее регистрируем: `app.register_blueprint(posts, url_prefix='/blog')`. `url_prefix` - часть url, которую будет обрабатывать данный blueprint

`app.py`
```python
from flask import Flask
from config import Configuration

from posts.blueprint import posts

app = Flask(__name__)
app.config.from_object(Configuration)

app.register_blueprint(posts, url_prefix='/blog')
```

Определим функцию-обработчик нашего blueprint'a:
`blueprint.py`
```python
from flask import Blueprint, render_template

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/')
def index():
    return render_template('posts/index.html')
```
`@posts.route('/')` - часть url что остается после "отрезания" той, что была определена при регистрации blueprint'a в `app.py`.

Добавим ссылки в базовый шаблон. Для этого используем функцию `url_for('')`, которая в качестве параметра принимает название своей функции обработчика.
Ссылка на главную страницу:
`base.html`
```django
...
    <a class="navbar-brand" href="{{ url_for('index') }}">Flask</a>
...
```

Ссылка на страницу с постами: в `url_for()` сначала идет название Blueprint'a, которое было передано в конструктор, далее через `.` название функции-обработчика из blueprint'a:
`base.html`
```django
...
    <a class="nav-link" href="{{ url_for('posts.index') }}">Blog</a>
...
```
