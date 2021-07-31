import numpy as np
import pandas as pd
import math

from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import ToktokTokenizer
import re 

import warnings
warnings.filterwarnings("ignore")

import joblib 

from google_play_scraper import app, Sort, reviews, reviews_all

import uvicorn
from fastapi import FastAPI 


app = FastAPI(
    title="Claro App Reviews Sentiment Model API",
    description="Esta es una API que hace uso de NPL para analizar los comentarios de la aplicacion de Claro en la Google Store",
    version="0.1",
)

#Carga de los modelos

with open("Models/sentiment_model.pkl", "rb") as f:
    sentiment_classifier = joblib.load(f)

with open("Models/calification_model.pkl", "rb") as f:
    calification_classifier = joblib.load(f)


nltk.download('stopwords')


def limpiado_de_texto(texto, remove_stop_words=True, stemming_words=True):
    
    # Eliminamos los caracteres especiales
    texto = re.sub(r'\W', ' ', str(texto))
    # Eliminado las palabras que tengo un solo caracter
    texto = re.sub(r'\s+[a-zA-Z]\s+', ' ', texto)
    # Sustituir los espacios en blanco en uno solo
    texto = re.sub(r'\s+', ' ', texto, flags=re.I)
    # remover numeros
    texto = re.sub(r'\b\d+(?:\.\d+)?\s+', '', texto) 
    # Convertimos textos a minusculas
    texto = texto.lower()
    
    # Tokenizado
    tokenizer = ToktokTokenizer() 
    tokens = tokenizer.tokenize(texto)
    
    # Eliminacion de stopwords
    stop_words =  stopwords.words('spanish')
    if remove_stop_words:
        tokens = [w for w in tokens if not w in stop_words]

    # Stemming
    stemmer = SnowballStemmer("spanish") 
    if stemming_words:
        tokens = [stemmer.stem(token) for token in tokens]
    
    text = " ".join(tokens)
 
    return(text)



@app.get("/consulta_de_los_n_comentarios_y_su_sentimiento")
def predict_n_reviews_sentiments(n: int):

    if n > 200:
        n = 200
    elif n < 1:
        n = 1

    rvws, token = reviews(
        'com.clarocolombia.miclaro', 
        lang='es',            
        country='us',         
        sort=Sort.NEWEST,     
        filter_score_with=None,  
        count=n             
    )

    result = []
   
    for rvw in rvws:

        cleaned_review = limpiado_de_texto(rvw['content'])
    
        sentiment_prediction = sentiment_classifier.predict([cleaned_review])
        sentiment_output = int(sentiment_prediction[0])
        sentiment_probas = sentiment_classifier.predict_proba([cleaned_review])[0]

        sentiment_output_probability = {"Negativo": sentiment_probas[0], 
                                        "Neutro": sentiment_probas[1], 
                                        "Positivo": sentiment_probas[2]}

        sentiments = {-1: "Negativo", 0: "Neutro", 1: "Positivo"}

        prediction = {"Comentario": rvw['content'],
                    "Sentimiento": sentiments[sentiment_output], 
                    "Probabilidades de la prediccion de Sentimiento": sentiment_output_probability}

        result.append(prediction)



    return result



@app.get("/sentimiento_y_calificacion_de_un_comentario")
def predict_sentiment_and_qualification(comentario: str):

    cleaned_review = limpiado_de_texto(comentario)
    
    sentiment_prediction = sentiment_classifier.predict([cleaned_review])
    sentiment_output = int(sentiment_prediction[0])
    sentiment_probas = sentiment_classifier.predict_proba([cleaned_review])[0]

    sentiment_output_probability = {"Negativo": sentiment_probas[0], 
                                    "Neutro": sentiment_probas[1], 
                                    "Positivo": sentiment_probas[2]}

    qualification_prediction = calification_classifier.predict([cleaned_review])
    qualification_output = int(qualification_prediction[0])
    qualification_probas = calification_classifier.predict_proba([cleaned_review])[0]

    qualification_output_probability = {"1": qualification_probas[0], 
                                        "2": qualification_probas[1], 
                                        "3": qualification_probas[2],
                                        "4": qualification_probas[3],
                                        "5": qualification_probas[4]}

    sentiments = {-1: "Negativo", 0: "Neutro", 1: "Positivo"}

    result = {"Sentimiento": sentiments[sentiment_output], 
            "Probabilidades de la prediccion de Sentimiento": sentiment_output_probability,
            "Calificacion": qualification_output,
            "Probabilidades de la prediccion de Calificacion": qualification_output_probability
            }

    return result

