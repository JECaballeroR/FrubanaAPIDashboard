# FrubanaAPIDashboard

## Descripción General
La aplicación **FrubanaAPIDashboard** es un dashboard interactivo que se conecta con una API para recomendar productos basados en el usuario y en otros productos. La API está construida utilizando FastAPI, mientras que el dashboard está desarrollado con Streamlit.

## Requisitos base
- Python 3.7+
- pip

## Instalación

1. **Clonar el repositorio:**
```sh
   git clone https://github.com/yourusername/FrubanaAPIDashboard.git
   cd FrubanaAPIDashboard
 ```


2. **Instalar las dependencias:**
 ```sh
pip install -r requirements.txt
cd FrubanaAPIDashboard 

 ```
# Ejecución
## Iniciar la API

 ```sh
uvicorn api:app --reload


 ```

* api.py contiene la implementación de la API.
* La API se ejecutará en http://127.0.0.1:8000.

## Iniciar el Dashboard
Para iniciar la aplicación Streamlit, utiliza el siguiente comando:


 ```sh
streamlit run app.py


 ```


* app.py contiene la implementación del dashboard.
* El dashboard se ejecutará en http://localhost:8501.


## Archivos Principales
* api.py: Contiene la implementación de la API utilizando FastAPI.
* app.py: Contiene la implementación del dashboard utilizando Streamlit.
* api_starter.py: Archivo auxiliar para iniciar la API.
* classes.py: Define las clases y modelos utilizados en la aplicación.
* requirements.txt: Lista de dependencias necesarias para la aplicación.
* Recomendaciones_KNNBaseline.pkl: Modelo de recomendaciones preentrenado.
* valid_choices.pkl: Archivo que contiene opciones válidas para la API.


