# Guia para Criar um Projeto Streamlit com UV

## 1. Crie o projeto e o ambiente virtual

```bash
uv init meu_streamlit --python 3.12
```

## 2. Entre na pasta do projeto

```bash
cd meu_streamlit
```

## 3. Adicione o Streamlit (e bibliotecas úteis)

```bash
uv add streamlit pandas matplotlib plotly
```

## 4. Exemplo de `main.py`:

```python
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Pokédex Streamlit", layout="wide")

st.title("Pokédex")
st.write(
    "Explore os 150 primeiros pokémons da PokéAPI. Veja imagens, altura e peso de cada um, navegue pela lista e visualize gráficos comparativos!"
)


@st.cache_data
def get_pokemon_details(offset=0, limit=25):
    url = f"https://pokeapi.co/api/v2/pokemon?offset={offset}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    pokemons = data["results"]
    details = []
    for p in pokemons:
        poke_data = requests.get(p["url"]).json()
        details.append(
            {
                "name": poke_data["name"].capitalize(),
                "height": poke_data["height"],
                "weight": poke_data["weight"],
                "image": poke_data["sprites"]["front_default"],
            }
        )
    return pd.DataFrame(details)


# Função para buscar todos os 150 pokémons para os gráficos
@st.cache_data
def get_all_pokemons():
    all_details = []
    for offset in range(0, 150, 25):
        df = get_pokemon_details(offset=offset, limit=25)
        all_details.append(df)
    return pd.concat(all_details, ignore_index=True)


df = get_pokemon_details()


total_pokemons = 150
page_size = 25
num_pages = total_pokemons // page_size
page = st.number_input("Página", min_value=1, max_value=num_pages, value=1, step=1)
offset = (page - 1) * page_size

# Dados para a tabela paginada
df_page = get_pokemon_details(offset=offset, limit=page_size)

# Dados para os gráficos (todos os 150)
df_all = get_all_pokemons()

st.subheader("Lista de Pokémons (paginada)")
for i, row in df_page.iterrows():
    cols = st.columns([1, 2, 2, 2])
    with cols[0]:
        st.image(row["image"], width=60)
    with cols[1]:
        st.write(f"**{row['name']}**")
    with cols[2]:
        st.write(f"Altura: {row['height']} (decímetros)")
    with cols[3]:
        st.write(f"Peso: {row['weight']} (hectogramas)")


# Gráficos comparativos com todos os 150 pokémons
st.subheader("Gráfico de Altura dos 150 Pokémons (decímetros)")
st.bar_chart(df_all.set_index("name")["height"])

st.subheader("Gráfico de Peso dos 150 Pokémons (hectogramas)")
st.bar_chart(df_all.set_index("name")["weight"])
```

## 5. Rodando o app

```bash
uv run python -m streamlit run main.py
```

Acesse: **http://localhost:8501/**
