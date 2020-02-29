# #4 Создание моделей
**Модель** - python-класс, который представляет таблицу в базе данных.

Установим `flask-sqlalchemy` и `mysql-connector`, который будет транслировать наш код на python в sql-запросы.
```
$ pip install flask-sqlalchemy
$ pip install mysql-connector
```

Подключение базы данных к flask-приложению:

`config.py`
```python
class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:1@localhost/test1'
```

`SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:1@localhost/test1'`:
`mysql` - база дынных.
`mysqlconnector` - драйвер базы данных.
`root` - имя пользователя базы данных.
`1` - пароль пользователя базы данных.
`localhost` - адрес веб сервера.
`test1` - название базы данных.

Создаем экземпляр класса `SQLAlchemy` в `app.py`. `SQLAlchemy` - ORM система. ORM предоставляет возможность описывать таблицы базы данных в виде python классов.
`db = SQLAlchemy(app)`

Теперь создадим класс-модель, который будет отвечать за хранение объектов в базе данных(в нашем случае - посты).

`models.py`
```python
from app import db
from datetime import datetime
import re


def slugify(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return '<Post id: {}, title: {}>'.format(self.id, self.title)

```

```python
def slugify(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s)
```

`pattern = r'[^\w+]'`:
* `r''` - для интерпритации строки "как есть"
* `^` - инвертирование
* `/w` - любые буквы и цифры
* `+` - неограниченное количество

`re.sub(pattern, '-', s)`: 
* `sup()` - функция, которая заменяет символы, содержащиеся в `pattern`
* `-` - то, на что заменяем
* `s` - строка, в которой будем заменять

Функция `__repr__` отвечает за текстовое представление класса в консоли.


Далее в python-консоли создадим таблицу для класса `Post` в базе данных:
```python
>>> from app import db
>>> db.create_all()
Создадим объект модели Post:
>>> from models import Post
>>> p = Post(title='first post', body='first post body')
>>> P
<Post id: None, title: first post>
Сохраним объект в бд:
!!!
>>> db.session.rollback()
>>> db.session.add(p)
>>> db.session.commit()
Теперь у нашего поста появился id
>>> p
<Post id: 1, title: first post>
Все посты, сохраненные в базе даныых:
>>> posts = Post.query.all()
Поиск конкретного поста:
>>> p2 = Post.query.filter(Post.title.contains('second')).all()
>>> p2
[<Post id: 2, title: Second post>]
или, когда указываем целиком заголовок:
>>> p3 = Post.query.filter(Post.title=='!').all()
>>> p3
[]
```
При поиске вместо `all()` можно использовать `first()`. `all()` возвращает список. `first()` - первый элемент списка.

Добавим вывод всех постов на главную страницу.
`blueprint.py`
```python
@posts.route('/')
def index():
    posts = Post.query.all()
    return render_template('posts/index.html', posts=posts)
```
т.к. получается круговое импортирование, перенесем регистрацию blueprint'a в `main.py`.

Добавим ссылки на страницы отдельных постов:

`posts/index.html`
```django
{% for post in posts  %}
    <p>
        <a href="{{ url_for('posts.post_detail', slug=post.slug) }}">
            {{ post.title }}
        </a>
    </p>
{% endfor %}
```
`url_for('posts.post_detail', slug=post.slug)` - генерация адреса, запрос по которому обрабатывает функция `post_detail`, которая в качестве идентификатора объекта принимает `slug`(вернет что-то наподобие `localhost:5000/blog/<slug>`);
здесь `posts.post_detail`:
`blueprint.py`
```python
...
@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first()
    return render_template('posts/post_detail.html', post=post)
...
```
При переходе по адресу `localhost:5000/blog/<slug>` декоратор `@posts.route('/<slug>')` передает `slug` дальше в функцию `post_detail()`, где происходит выбор поста, передача его в шаблон и генерация html-документа.
