# hanalum_web

### 기초 세팅 및 pre-commit 세팅
```
$ python -m venv venv
$ .\venv\bin\activate

$ pip install -r reqirements.txt
$ pre-commit install
$ pre-commit -V

$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```


### icon을 추가할 때,
https://fontawesome.com/icons?d=gallery 참고

```
{% load fontawesome_5 %}
{% block stylesheet %}
{% fontawesome_5_static %}
{% endblock %}
```

와 같이 코드를 먼저 초기화하고, 

`{% fa5_icon 'pencil-alt' 'fas' %}` 와 같은 형식으로 추가하면 됨.