#!/usr/bin/env python
# coding: utf-8

# importando librerias necesarias
import pandas as pd
import numpy as np
import scipy as sp


#leyendo la bd
recipes=pd.read_csv('/home/aleida/Documentos/Posgrado_Redes/repo/recipes.csv')


#recipes.head()
#recipes.shape

# cuantas recetas hay por pais
#recipes["country"].value_counts()


# poniendo en minuscula todo en la columna "country"
recipes["country"] = recipes["country"].str.lower()


# esto es para homogenizar el pais
recipes.loc[recipes["country"] == "austria", "country"] = "austrian"
recipes.loc[recipes["country"] == "belgium", "country"] = "belgian"
recipes.loc[recipes["country"] == "china", "country"] = "chinese"
recipes.loc[recipes["country"] == "canada", "country"] = "canadian"
recipes.loc[recipes["country"] == "netherlands", "country"] = "dutch"
recipes.loc[recipes["country"] == "france", "country"] = "french"
recipes.loc[recipes["country"] == "germany", "country"] = "german"
recipes.loc[recipes["country"] == "india", "country"] = "indian"
recipes.loc[recipes["country"] == "indonesia", "country"] = "indonesian"
recipes.loc[recipes["country"] == "iran", "country"] = "iranian"
recipes.loc[recipes["country"] == "italy", "country"] = "italian"
recipes.loc[recipes["country"] == "japan", "country"] = "japanese"
recipes.loc[recipes["country"] == "israel", "country"] = "israeli"
recipes.loc[recipes["country"] == "korea", "country"] = "korean"
recipes.loc[recipes["country"] == "lebanon", "country"] = "lebanese"
recipes.loc[recipes["country"] == "malaysia", "country"] = "malaysian"
recipes.loc[recipes["country"] == "mexico", "country"] = "mexican"
recipes.loc[recipes["country"] == "pakistan", "country"] = "pakistani"
recipes.loc[recipes["country"] == "philippines", "country"] = "philippine"
recipes.loc[recipes["country"] == "scandinavia", "country"] = "scandinavian"
recipes.loc[recipes["country"] == "spain", "country"] = "spanish_portuguese"
recipes.loc[recipes["country"] == "portugal", "country"] = "spanish_portuguese"
recipes.loc[recipes["country"] == "switzerland", "country"] = "swiss"
recipes.loc[recipes["country"] == "thailand", "country"] = "thai"
recipes.loc[recipes["country"] == "turkey", "country"] = "turkish"
recipes.loc[recipes["country"] == "vietnam", "country"] = "vietnamese"
recipes.loc[recipes["country"] == "uk-and-ireland", "country"] = "uk-and-irish"
recipes.loc[recipes["country"] == "irish", "country"] = "uk-and-irish"

#recipes["country"].value_counts()



recipes = recipes.replace(to_replace="Yes", value=1)
recipes = recipes.replace(to_replace="No", value=0)


#recipes


recipes.to_csv("/home/aleida/Documentos/Posgrado_Redes/repo/bd.csv",index=False)



