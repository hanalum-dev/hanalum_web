# hanalum_web

### pre-commit 세팅([참고](https://pre-commit.com/))
```
$ pip install pre-commit
$ pre-commit install
$ pre-commit -V
```

### 도커 세팅
먼저 도커를 설치하세요. [여기서](https://docs.docker.com/get-docker/)

그리고나서, 프로젝트 폴더에서 아래 명령어로 도커 컨테이너 만들고 돌려주세요.
```
docker-compose up -d
```

http://127.0.0.1 로 들어가지는지 확인해보세요


- 했는데 안되는데요..?

이전에 80포트를 쓰는 프로그램이 있어서 그럴 수 있습니다.
docker-compose.yml 에서 80:3000 을 3000:3000 으로 바꾸고 127.0.0.1:3000으로 접속해보세요.


### 여러가지 팁

#### icon을 추가할 때,
https://fontawesome.com/icons?d=gallery 참고

```
{% load fontawesome_5 %}
{% block stylesheet %}
{% fontawesome_5_static %}
{% endblock %}
```

와 같이 코드를 먼저 초기화하고, 

`{% fa5_icon 'pencil-alt' 'fas' %}` 와 같은 형식으로 추가하면 됩니다.
