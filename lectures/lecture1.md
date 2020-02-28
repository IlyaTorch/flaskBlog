# #1 Создание приложения. Обработка запросов. HTML шаблоны

## Создание приложения
---
`app.py` - основной файл приложения.

`app.py`
```python
from flask import Flask
from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)
```

`app = Flask(__name__)` - отталкиваясь от имени этого файла(его пути) Flask будет искать другие файлы: шаблоны, css, js и др. файлы.
`from config import Configuration` - импортируем класс конфигурации, чтобы использовать его.
`app.config.from_object(Configuration)` - заполняем словарь `config` настроек приложения нашим классом настроек `Configuration`.

Файл `config.py` содержит класс `Configuration`, который описывает настройки приложения:

`config.py`

```python
class Configuration(object):
    DEBUG = True
```


`main.py` - точка входа в приложение(запуска приложения).

`main.py`
```python
from app import app
import view

if __name__ == '__main__':
    app.run()
```
---
**Flask** реализует паттерн **MVC**:
* **Model** - раздел кода, отвечающий за описание моделей(данных, хранящихся в бд)
* **View** - код, отвечающий за отображение пользователю данных
* **Controller** - отвечает за получение запроса от пользователя, обработку этого запроса, перенаправление на страницу с ответом после выполнения запроса.

В терминологии **Flask**/**Django**:
* View - templates
* Controller - view

## Обработка запросов и HTML шаблоны
`view.py`

```python
from app import app
from flask import render_template


@app.route('/')
@app.route('blog')
def index():
    name = 'Ilya'
    return render_template('index.html', n=name)
```

`@app.route('/')`: внутри Flask есть словарь вида `{'url': 'view.index'}`, где ключ `url` - путь, по которому пользователь обращается к нашему ресурсу. В данном примере это `'/'`. А значение по этому ключу - функция, которая должна обрабатывать запрос по данному адресу. Здесь это `index`.
Одна функция-вьюха может обрабатывать запрос по нескольким путям.

Обычно функции-обработчики генерируют html-шаблоны. Они хранятся в папке `templates`. Чтобы вернуть пользователю html-документ используется функция `render_template`: `return render_template('index.html', n=name)`, которая может принимать данные, которые будут подставляться в html-шаблон.

`index.html`
```django
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>Hello {{ n }}</h1>
</body>
</html>
```

