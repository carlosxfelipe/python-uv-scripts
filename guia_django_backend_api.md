# Guia Completo para Criar um Backend Django com UV (API REST)

Este guia cria um **backend Django moderno** usando [uv](https://github.com/astral-sh/uv) como gerenciador de ambiente e pacotes.  
Focado em uso como **API REST**, ideal para frontends React, Vue, mobile, etc.

---

## 1. Crie o projeto e o ambiente virtual

(O comando cria a pasta do projeto, inicializa o ambiente e configura o Python automaticamente)

```bash
uv init meu_projeto --python 3.12
```

---

## 2. Entre na pasta do projeto

```bash
cd meu_projeto
```

---

## 3. Instale o Django e pacotes essenciais

```bash
uv add django djangorestframework django-cors-headers drf-spectacular
```

> Esses pacotes permitem criar uma API com Django REST Framework, habilitar CORS e gerar documentação Swagger automática.

---

## 4. Crie a estrutura do projeto Django

(O ponto final `.` indica que o projeto será criado **na pasta atual**)

```bash
uv run django-admin startproject config .
```

---

## 5. Configure o `settings.py`

Abra `config/settings.py` e adicione/edite conforme abaixo:

```python
INSTALLED_APPS = [
    ...,
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    *MIDDLEWARE,
]

# CORS - permitir o frontend (React, etc.)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

# Configurações DRF
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

# Outras configurações usuais
ALLOWED_HOSTS = ["*"]
```

---

## 6. Crie uma aplicação de API

```bash
uv run python manage.py startapp api
```

Em `config/settings.py`, adicione:

```python
INSTALLED_APPS += ["api"]
```

---

## 7. Crie o modelo, serializer e viewset

**api/models.py**

```python
from django.db import models

class Item(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome
```

**api/serializers.py**

```python
from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"
```

**api/views.py**

```python
from rest_framework import viewsets
from .models import Item
from .serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
```

---

## 8. Configure as rotas da API

**config/urls.py**

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from api.views import ItemViewSet

router = DefaultRouter()
router.register(r"items", ItemViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
```

---

## 9. Migre e rode o servidor

```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py runserver
```

Acesse:

- API CRUD: [http://localhost:8000/api/items/](http://localhost:8000/api/items/)
- Documentação Swagger: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)

---

## 10. (Opcional) JWT Auth

Para autenticação via tokens JWT:

```bash
uv add djangorestframework-simplejwt
```

Em `settings.py`:

```python
REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = [
    "rest_framework_simplejwt.authentication.JWTAuthentication",
]
```

E adicione as rotas:

```python
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns += [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
```

---

## 11. (Opcional) Servir o frontend React

Caso queira servir o build do React dentro do Django:

```bash
uv add whitenoise
```

E copie o `build/` do React para dentro de `static/` ou `templates/`.

---

## 12. Produção

- Configure `DEBUG = False`
- Defina `ALLOWED_HOSTS` corretamente
- Use `gunicorn` ou `uvicorn` para servir o app
  ```bash
  uv add gunicorn
  uv run gunicorn config.wsgi:application
  ```
- Configure Nginx / proxy reverso
- Use `.env` para segredos (SECRET_KEY, banco de dados, etc.)

---

## Pronto!

Seu **backend Django + DRF + Swagger** está pronto para integrar com React, Flutter, ou qualquer frontend que consuma APIs REST.

---

### Recursos recomendados

- [Django REST Framework](https://www.django-rest-framework.org/)
- [drf-spectacular (Swagger para Django)](https://drf-spectacular.readthedocs.io/)
- [django-cors-headers](https://github.com/adamchainz/django-cors-headers)
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)
