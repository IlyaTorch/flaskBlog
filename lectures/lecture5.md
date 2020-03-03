# #5 Миграции. Теги. Связь Many To Many
## Миграции
---
**Миграция** - "обновление" структуры базы данных(синхронизация базы даных и моделей. Нужно для того, чтобы при изменинии моделей не вносить соответствующие изменения в бд вручную, а делать это автоматически). Для этого нужно установить модули `flask-migrate` и `flask-script`.
```
$ pip install flask-migrate
$ pip install flask-script
```

Создаем объект миграции, менеджера и добавляем команду менеджера `db`:
`app.py`
```python
...
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
```

Фиксируем первоначальное состояние приложения и базы данных, после чего можно добавлять новые модели, редактировать старые и т.д.
```
$ python manage.py db init
```
`db` - команда, которую зарегестрировали выше.

## Теги
Добавляем модель `Tag`:
`models.py`
```python
...
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100))

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return'<Tag id: {}, name: {}>'.format(self.id, self.name)
```
Далее в консоли выполняем следующую команду:
```
$ python manage.py db migrate
```
`migrate` создает файл миграций, но в бд никаких изменений пока не произошло.
Применим созданные миграции:
```
$ python manage.py db upgrade
```
Теперь в бд появилась новая таблица.

Для **сохранения в бд нескольких обектов** используется метод:
```
db.session.add_all([p1, p2])
```

## Связь Many To Many
---
Наши посты и теги будут реализовывать связь Many To Many. При реализации такой связи в базе данных создается одна дополнительная таблица. Ее вид будет примерно следующим:
post id| tag id
------ | ------
   1   |   1   
   1   |   2 
   1   |   2
 ...   |  ...

Создадим такую таблицу:
`models.py`
```python
...
post_tags = db.Table('post_tags',
                     db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                     db.Column('tag_id'), db.Integer, db.ForeignKey('tag.id')
                     )
...
```
* `post_tags` - название таблицы
* `db.Column()` - колонка в таблице
* `post_id` - название колонки,
* `db.Integer` - тип значений этой колонки
* `db.ForeignKey('post.id')`- чужой ключ, и в кавычках путь к этому ключу

 Теперь установим отношение между нашими моделями. Это делайтся путем создания дополнительного свойства в модели `Post`(или `Tag`)
 `models.py`
 ```python
 class Post(db.Model):
    ...
    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='dynamic'))
```
* `'Tag'` - класс, с которым создаем отношение
* `secondary=post_tags` - название общей таблицы
* `backref=db.backref('posts')` - соответствующее свойство, которое появится у тегов
* `db.backref(lazy='dynamic')` - свойство `posts` будет представлять собой не обычный список, а объект `BaseQuery`, который имеет дополнительные свойства и генерируется "налету".

Применяем миграции:
```
$ python manage.py db migrate
$ python manage.py db upgrade
```

Добавим на страницу отдельного поста отображение тегов, связанных с этим постом: Во вьюхе поста в шаблон будем дополнителльно передавать `tags`:
`blueprint.py`
```
...
@posts.route('/post/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first()
    tags = post.tags
    return render_template('posts/post_detail.html', post=post, tags=tags)
```

`post_detail.html`
```django
...
<div class="tags">
    Tags:
        {% for tag in tags %}
             <a href="{{ url_for('posts.tag_detail', slug=tag.slug) }}">{{ tag.name }}</a>
        {% endfor %}
    </div>
...
```
Аналогично создадим страницы для отдельных тегов, на которых будут отображаться посты, связанные с этим тегом(все как и с постами, за исключением того инициализации списка постов `posts`):
```
posts = tag.posts.all()
```
Здесь вызываем метод `all()` т.к. `tag.posts` - `BaseQuery`, из которого методом `all()` получаем список.

