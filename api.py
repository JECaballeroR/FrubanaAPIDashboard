from fastapi import FastAPI
from classes import ModeloFPAPI, EntradaModeloFP,  EntradaModeloKNN, ModeloKNNAPI


app = FastAPI(title='API Frubana', version="0.42.69")
"""Esta es una API que recomienda productos según un producto u otros usuarios"""

@app.post("/recomendar-fp", tags=["Recomendación"])
async def recomendar_fp_growth(entrada: EntradaModeloFP):
    """Endpoint para recomendar basado en los productos"""
    modelo=ModeloFPAPI(producto=entrada.producto)
    return modelo.predecir()

@app.post("/recomendar-user", tags=["Recomendación"])
async def recomendar_user(entrada: EntradaModeloKNN):
    """Endpoint para recomendar basado en el user"""
    modelo=ModeloKNNAPI(user=entrada.user)
    return modelo.predecir()
