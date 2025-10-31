# Guia para Criar um Projeto Django com UV

### 1. Crie o projeto e o ambiente virtual

(O comando cria a pasta do projeto, inicializa o ambiente e configura o
Python automaticamente)

``` bash
uv init meu_projeto --python 3.12
```

### 2. Entre na pasta do projeto

``` bash
cd meu_projeto
```

### 3. Instale o Django no projeto

(O pacote será registrado no `pyproject.toml`)

``` bash
uv add django
```

### 4. Crie a estrutura do projeto Django

(O ponto final `.` indica que o projeto será criado **na pasta atual**)

``` bash
uv run django-admin startproject config .
```

### 5. Aplique as migrações iniciais

*(opcional, mas recomendável)*

``` bash
uv run python manage.py migrate
```

### 6. Inicie o servidor de desenvolvimento

``` bash
uv run python manage.py runserver
```

### 7. Acesse o site no navegador

Abra o navegador e vá para:\
**http://localhost:8000/**
