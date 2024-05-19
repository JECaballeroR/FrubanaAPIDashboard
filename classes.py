from pydantic import BaseModel as BM
from pydantic import  validator, Field
import joblib
import pandas as pd
import pickle
from uuid import UUID

recs=joblib.load('FP_Recs.pkl')
choices=joblib.load('valid_choices.pkl')
opciones =  tuple(choices["data"])


class EntradaModeloFP(BM):
    producto: str
    @validator('producto', allow_reuse=True)
    def is_in_list(cls, value, ):
        if value not in opciones:
            raise ValueError(f"El valor '{value}' no está en la lista de productos")
        return value
    class Config:
        schema_extra = {
            "example":{
                "producto":"Brócoli Estándar Kg"
            }
        }
class EntradaModeloKNN(BM):
    user: UUID = Field( description="A UUID string")

    class Config:
        schema_extra = {
            "example":{
                "user":"c7b460f1-c045-4453-941b-890a6d545a7a"
            }
        }

class ModeloKNNAPI:
    def __init__(self, user):
        self.user = user
    def _cargar_datos(self):

        with open('Recomendaciones_KNNBaseline.pkl', 'rb') as rec_file:
            all_recommendations = pickle.load(rec_file)
        self.modelo = all_recommendations
    def _preprocesar_datos(self):
        return self
    def predecir(self):
        self._cargar_datos()
        self._preprocesar_datos()
        selected_user = self.user
        all_recommendations = self.modelo
        productos_recomendados = []
        if selected_user in all_recommendations['KNNBaseline']:
            recommendations = all_recommendations['KNNBaseline'][selected_user]

            for product, score in recommendations:
                productos_recomendados.append(product)
        return pd.DataFrame(productos_recomendados, columns=["Recomendaciones"]).head(5).to_dict(orient='records')


class  ModeloFPAPI:
    def __init__(self, producto):
        self.producto=producto
    def _cargar_modelo(self):
        self.modelo = recs.copy()
    def _preprocesar_datos(self):
        return self

    def predecir(self ):
        self._cargar_modelo()
        rules = self.modelo
        product= self.producto
        rules_exact_basket = rules[
            rules["antecedents"].apply(lambda x: frozenset([product]) == x)
        ]
        rules_item_in_antecedent = rules[rules["antecedents"].apply(lambda x: product in x)].copy()

        rules_item_in_antecedent["other_antecedents"] = rules_item_in_antecedent[
            "antecedents"
        ].apply(lambda x: frozenset([y for y in x if y != product]))
        rules_item_in_antecedent = rules_item_in_antecedent[
            rules_item_in_antecedent["other_antecedents"].apply(lambda x: len(x) >= 1)
        ]

        return rules_item_in_antecedent.head(5).to_dict(orient='records')


