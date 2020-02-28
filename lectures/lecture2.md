# #2 Наследование шаблонов

Для начала создадим базовый шаблон и определим в нем блоки - своеобразные ячейки, в которые мы будем подставлять данные в зависимости от страницы. Для определения блока используется конструкция ниже:
```django
{% block block_name %}
{% endblock %}
```

`base.html`
```django
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>
        {% block title %}
        
        {% endblock %} | Flask app
    </title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">

</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="#">Navbar</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Link</a>
          </li>

          <li class="nav-item">
            <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Disabled</a>
          </li>
        </ul>

        <form class="form-inline my-2 my-lg-0">
          <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
          <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
        </form>
      </div>
    </nav>

    <div class="container">
        <div class="row">
            <h1>
                {% block content_title %}
                
                {% endblock %}
            </h1>
        
            {% block content %}

            {% endblock %}
        </div>
    </div>
</body>
</html>
```

Страницы, переопределяющие базовый шаблон имеют следующий вид:
`index.html`
```django
{% extends 'base.html' %}

{% block title %}
    Index page
{% endblock %}

{% block content_title %}
    Index page
{% endblock %}

{% block content %}
    some content.
{% endblock %}
```

`{% extends 'base.html' %}` - показываем, что текущая страница переопределяет базовый шаблон.
`{% block ...%}` - заполняем блоки, определенные в базовом шаблоне.