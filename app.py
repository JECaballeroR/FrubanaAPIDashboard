import streamlit as st
import pandas as pd
import classes
import requests
import json
import ast
import glob
import pickle
import os
import random
import pandas as pd
import uuid
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="Dashboard Recomendaciones Frubana",
    page_icon="🌟",
    layout="wide",
)
# Estilos CSS personalizados
st.markdown(
    """
    <style>
    
    .sidebar .sidebar-content {
        background-color: #388E3C; /* Fondo de la barra lateral en verde oscuro */
    }
    .stTextInput>div>div>input {
        color: #4CAF50; /* Color de la fuente en verde */
        border: 2px solid #FF9800; /* Borde color naranja */
    }
    .stButton>button {
        background-color: #FF9800; /* Botón color naranja */
        color: white; /* Texto en blanco */
        border-radius: 8px; /* Bordes redondeados */
    }
    .stButton>button:hover {
        background-color: #FFC107; /* Botón color amarillo al pasar el ratón */
        color: black; /* Texto en negro */
    }
    h1 {
        color: #4CAF50; /* Título en verde */
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.sidebar.image("Images/frubana_logo_slogan.png")

st.sidebar.markdown(
    '''
    ### Desarrollado por:
    * Jorge Caballero
    * Jesus Parada
    * Camilo Grande
    * Catalina Garcia
    
    '''
)
@st.cache_data
def cargar_databases():

    ruta_actual = os.getcwd()

    # Buscar todos los archivos .pkl en el directorio actual
    archivos_pkl = glob.glob(os.path.join(ruta_actual, "Datos Frubana/Ventas", "*.pkl"))

    dataframes = []

    # Cargar cada archivo .pkl encontrado
    for archivo in archivos_pkl:
        with open(archivo, "rb") as f:
            df = pickle.load(f)
            dataframes.append(df)

    df_ventas = pd.concat(dataframes)
    df_ventas["cantidad"] = pd.to_numeric(df_ventas["cantidad"])
    df_ventas["precio"] = pd.to_numeric(df_ventas["precio"])
    df_ventas["descuento"] = pd.to_numeric(df_ventas["descuento"])
    df_ventas["product_quantity_x_step_unit"] = pd.to_numeric(
        df_ventas["product_quantity_x_step_unit"]
    )
    # Calcula el precio total
    df_ventas["precio_total"] = (
            df_ventas["precio"] * df_ventas["product_quantity_x_step_unit"]
    )

    return df_ventas

@st.cache_data
def recomendar_por_usuario(_usuario):
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
    }
    request_data = json.dumps(
        {
            "user": str(_usuario)
        }
    ).replace("'", '"')
    url_api = 'http://localhost:8000/recomendar-user'

    return pd.read_json(requests.post(url=url_api, data=request_data, headers=headers).text)



df_ventas = cargar_databases()


st.markdown("# Gráficas de productos relevantes para el usuario")

def graficar_recomendaciones(productos_recomendados):
    df_filtered = df_ventas[df_ventas['producto'].isin(productos_recomendados)]

    # Convertir la columna 'fecha' a tipo datetime si no lo está
    df_filtered['fecha'] = pd.to_datetime(df_filtered['fecha'])

    # Agrupar las ventas por fecha y producto para obtener estadísticas
    df_grouped = df_filtered.groupby(['fecha', 'producto']).agg({
        'cantidad': 'sum',
        'precio': 'mean',
        'precio_total': 'sum',
        'descuento': 'mean',
        'product_quantity_x_step_unit': 'sum'
    }).reset_index()

    # Crear figuras separadas para cantidad vendida, precio, descuento y precio total
    fig_cantidad_vendida = go.Figure()
    fig_precio = go.Figure()
    fig_descuento = go.Figure()
    fig_precio_total = go.Figure()

    # Obtener una paleta de colores automática para los productos
    colors = px.colors.qualitative.Plotly[:len(productos_recomendados)]

    # Agregar trazos para cada producto recomendado en cada figura
    for i, product in enumerate(productos_recomendados):
        product_data = df_grouped[df_grouped['producto'] == product]

        color = colors[i]

        # Trazo para la cantidad vendida
        fig_cantidad_vendida.add_trace(go.Scatter(
            x=product_data['fecha'],
            y=product_data['product_quantity_x_step_unit'],
            mode='lines',
            name=f'{product}',
            line=dict(color=color),

        ))

        # Trazo para el precio
        fig_precio.add_trace(go.Scatter(
            x=product_data['fecha'],
            y=product_data['precio'],
            mode='lines',
            name=f'{product}',
            line=dict(color=color)
        ))

        # Trazo para descuento
        fig_descuento.add_trace(go.Scatter(
            x=product_data['fecha'],
            y=product_data['descuento'],
            mode='lines',
            name=f'{product}',
            line=dict(color=color)
        ))

        # Trazo para precio total
        fig_precio_total.add_trace(go.Scatter(
            x=product_data['fecha'],
            y=product_data['precio_total'],
            mode='lines',
            name=f'{product}',
            line=dict(color=color)
        ))

    # Actualizar el diseño para los ejes y el título en cada figura
    fig_cantidad_vendida.update_layout(
        title='Cantidad Vendida',
        xaxis_title='Fecha',
        yaxis_title='Cantidad Vendida',
        legend=dict(
            orientation='h',  # Orientación horizontal para la leyenda
            yanchor='bottom',  # Anclaje en la parte inferior
            y=1.02,  # Posición vertical fuera del gráfico
            xanchor='right',  # Anclaje a la derecha
            x=1  # Posición horizontal fuera del gráfico
        ),
        hovermode='x unified',
        height=600  # Altura de la figura
    )

    fig_precio.update_layout(
        title='Precio promedio',
        xaxis_title='Fecha',
        yaxis_title='Precio',
        legend=dict(
            orientation='h',  # Orientación horizontal para la leyenda
            yanchor='bottom',  # Anclaje en la parte inferior
            y=1.02,  # Posición vertical fuera del gráfico
            xanchor='right',  # Anclaje a la derecha
            x=1  # Posición horizontal fuera del gráfico
        ),
        hovermode='x unified',
        height=600 ,

    )

    fig_descuento.update_layout(
        title='Descuento promedio',
        xaxis_title='Fecha',
        yaxis_title='Descuento',
        legend=dict(
            orientation='h',  # Orientación horizontal para la leyenda
            yanchor='bottom',  # Anclaje en la parte inferior
            y=1.02,  # Posición vertical fuera del gráfico
            xanchor='right',  # Anclaje a la derecha
            x=1  # Posición horizontal fuera del gráfico
        ),
        hovermode='x unified',
        height=600  # Altura de la figura
    )

    fig_precio_total.update_layout(
        title='Precio total',
        xaxis_title='Fecha',
        yaxis_title='Precio total',
        legend=dict(
            orientation='h',  # Orientación horizontal para la leyenda
            yanchor='bottom',  # Anclaje en la parte inferior
            y=1.02,  # Posición vertical fuera del gráfico
            xanchor='right',  # Anclaje a la derecha
            x=1  # Posición horizontal fuera del gráfico
        ),
        hovermode='x unified',
        height=600  # Altura de la figura
    )

    # Mostrar las figuras por separado
    a, b =st.columns(2)
    a.plotly_chart(fig_cantidad_vendida, use_container_width=True)
    a.plotly_chart(fig_precio, use_container_width=True)
    b.plotly_chart(fig_descuento, use_container_width=True)
    b.plotly_chart(fig_precio_total, use_container_width=True)
# Seleccionar aleatoriamente un usuario de la lista de usuarios únicos


# Inicializar el valor en session_state si no existe
if "selected_user" not in st.session_state:
    st.session_state.selected_user = np.random.choice(df_ventas["customer_id"].unique())

# Función para actualizar el usuario seleccionado
def choose_new_user():
    st.session_state.selected_user = np.random.choice(df_ventas["customer_id"].unique())

# Botón en la barra lateral para elegir un nuevo usuario al azar
if st.sidebar.button("Elegir nuevo usuario al azar"):
    choose_new_user()



st.sidebar.markdown(f"**Usuario Elegido:** {st.session_state.selected_user}")

selected_user = st.session_state.selected_user

productos_recomendados = recomendar_por_usuario(selected_user)


graficar_recomendaciones(list(productos_recomendados['Recomendaciones']))
st.markdown(f"## Basado en las compras de {selected_user}:")

for product in list(productos_recomendados['Recomendaciones']):
    st.write(product)



def eliminar_duplicados(lista):
    return list(dict.fromkeys(lista))
@st.cache_resource
def cargar_opciones():
    opciones = classes.recs
    frozenset_unido = frozenset().union(*opciones['antecedents'])



    return sorted(list(frozenset_unido))


@st.cache_data
def limpiar_prediccion(prediccion):
    if len(prediccion) >0:
        val = (prediccion[['consequents', 'lift']].astype(str).groupby('consequents').sum()
                 .sort_values('lift').reset_index().rename(columns={'consequents':'recomendaciones'}))

        val['recomendaciones'] = val['recomendaciones'].apply(lambda x: ast.literal_eval(x))

        recomendation = sum(val['recomendaciones'], [])
        return eliminar_duplicados(recomendation)
    else:
        return random.sample(['Cebollín Limpio Atado Unidad',
                 'Apio Estándar Atado',
                 'Cebolla Cabezona Blanca Sin Pelar Mixta Desde 1Kg',
                 'Ajo Estandar Kg',
                 'Pimentón Verde Mixto Estándar Desde 1Kg',
                 'Zanahoria Mixta Kg',
                 'Tomate de Árbol Estándar Desde 1Kg',
                 'Cebolla Cabezona Blanca Sin Pelar Mixta Al por mayor',
                 'Papa Blanca Sucia Tamaño Mixto KG',
                 'Papa Blanca Sucia Tamaño Mixto Bulto (48kg)'], 5)



opciones =  cargar_opciones()

@st.cache_data
def recomendar_por_producto(producto):
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
    }
    request_data = json.dumps(
        {
            "producto": producto
        }
    ).replace("'", '"')
    url_api = 'http://localhost:8000/recomendar-fp'

    return pd.read_json(requests.post(url=url_api, data=request_data, headers=headers).text)

producto = st.sidebar.selectbox(label="Elija su producto",options=opciones,index=opciones.index(list(productos_recomendados['Recomendaciones'])[0])  )

if st.sidebar.button("Recomendar"):

    prediccion = recomendar_por_producto(producto)
    st.markdown("## Otros usuarios han comprado: ")
    _ =[st.write(x) for x in limpiar_prediccion(prediccion)]




