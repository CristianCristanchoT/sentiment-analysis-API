# Sentiment analysis API
## Claro App (Google Play Store)

La presente es una API la cual es capaz de analizar los sentimiento de los comentarios hechos en la Google Play Store sobre la App de Claro.

## Características

- Permite obtener y analizar los últimos comentarios posteados para la aplicación.
- Estima el sentimiento de cada uno de los comentarios.
- Permite estimar el sentimiento y predecir la calificación de cualquier comentario dado a la API.

## Uso
### Obtención de los últimos **n** comentarios mas recientes de la app y obtención de su sentimiento

El endpoint  **/consulta_de_los_n_comentarios_y_su_sentimiento** permite obtener un numero n de los últimos comentarios hechos a la aplicación (n puede estar entre 1 y 200 comentarios solicitados) y obtener el sentimiento de cada uno de estos comentarios.


| Parámetro | Función |
| ------ | ------ |
| n | Indica la cantidad de comentarios a importar desde la Play Store (mínimo 1, máximo 200) |

#### [Ejemplo:](https://sentiment-analysis-api-claro.herokuapp.com/docs#/default/predict_n_reviews_sentiments_consulta_de_los_n_comentarios_y_su_sentimiento_get)

Solicitud:
```url
https://sentiment-analysis-api-claro.herokuapp.com/consulta_de_los_n_comentarios_y_su_sentimiento?n=2
```

Respuesta:
```json
[{
    "Comentario":"Buen servicio y la atención domiciliaria fue muy oportuna.Muchas gracias .",
    "Sentimiento":"Positivo",
    "Probabilidades de la prediccion de Sentimiento":
        {"Negativo":0.041559579123194884,
        "Neutro":0.012581511473484653,
        "Positivo":0.9458589094033188}
},
{
    "Comentario":"buena aplicación excelente",
    "Sentimiento":"Positivo",
    "Probabilidades de la prediccion de Sentimiento":
        {"Negativo":0.002143731259394213,
        "Neutro":0.0011111493265661635,
        "Positivo":0.9967451194140401}}]
```

### Estimación del sentimiento y predicción de la calificación dado un comentario

El endpoint  **/sentimiento_y_calificacion_de_un_comentario** permite obtener el sentimiento y la predicción  dada un comentario dado como parámetro de entrada..


| Parámetro | Función |
| ------ | ------ |
| comentario | Comentario a analizar |

#### [Ejemplo:](https://sentiment-analysis-api-claro.herokuapp.com/docs#/default/predict_sentiment_and_qualification_sentimiento_y_calificacion_de_un_comentario_get)

Solicitud:
```url
https://sentiment-analysis-api-claro.herokuapp.com/sentimiento_y_calificacion_de_un_comentario?comentario=La%20aplicacion%20presenta%20deficiencias%20a%20la%20hora%20de%20funcionar
```

Respuesta:
```json
{
    "Sentimiento":"Negativo",
    "Probabilidades de la prediccion de Sentimiento":
        {"Negativo":0.8175027502832946,
        "Neutro":0.03879126644864383,
        "Positivo":0.14370598326806172},
    "Calificacion":1,
    "Probabilidades de la prediccion de Calificacion":
        {"1":0.7825737131841086,
        "2":0.06009932071896851,
        "3":0.049403137132370226,
        "4":0.04429830033792553,
        "5":0.0636255286266267}
}
```

# [Mas Información y pruebas con la API ](https://sentiment-analysis-api-claro.herokuapp.com/docs)

## https://sentiment-analysis-api-claro.herokuapp.com/docs
