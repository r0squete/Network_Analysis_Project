#!/usr/bin/env python
# coding: utf-8

#librerias necesarias
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt 
import networkx.algorithms.community as nxcom


#importando bd
bd=pd.read_csv('/home/aleida/Documentos/Posgrado_Redes/repo/bd.csv')



#print(bd.shape)
#bd.head()

#info sobre la categoria de los ingredientes
info_ingredients=pd.read_csv('/home/aleida/Documentos/Posgrado_Redes/repo/ingr_info.tsv',sep='\t',usecols=['ingredient name','category'],index_col='ingredient name')


#info_ingredients.head()


# print(info_ingredients.shape)
#info_ingredients.loc['mackerel']['category']


#info_ingredients["category"].value_counts()


#lista de ingredientes
ingredients=bd.columns.values[1:]


#ingredients

color_values = {
    'plant derivative':'palegreen',
    'plant':'greenyellow',
    'fruit':'orange',
    'vegetable':'green',
    'herb':'gold',
    'flower':'pink',
    'meat':'red',
    'fish/seafood':'steelblue',
    'spice':'brown',
    'alcoholic beverage':'goldenrod',
    'cereal/crop':'tan',
    'dairy':'white',
    'nut/seed/pulse':'coral',
    'animal product':'navajowhite'
}


#Construyendo grafo
G1 = nx.Graph()
for i in ingredients:
    G1.add_node(i, weight=(bd[i].values == True).sum(), category=info_ingredients.loc[i,'category'],color=color_values[info_ingredients.loc[i,'category']])


"""nx.draw(G1, with_labels=True,node_color=nx.get_node_attributes(G1, "color").values())
plt.show()"""


#Matriz para los pesos
matriz_i=pd.DataFrame(0,index=ingredients, columns=ingredients)


#matriz_i



for row in range(len(bd)):
    receta=bd.iloc[row][1:][bd.iloc[row][1:]==1]
    for i in range(len(receta.index)):
        k=receta.index[i]
        matriz_i.loc[k][k]+=1
        for j in range(i+1,len(receta.index)):
            l=receta.index[j]
            matriz_i.loc[k][l]+=1
            matriz_i.loc[l][k]+=1


#matriz_i


#Añadiendo aristas con sus pesos
weights1={}
for i in range(len(ingredients)):
    k=ingredients[i]
    for j in range(i+1,len(ingredients)):
        l=ingredients[j]
        if matriz_i.loc[k][j]!=0:
            G1.add_edge(k,l,weight=matriz_i.loc[k][j])
            weights1[(k,l)]=matriz_i.loc[k][j]
            weights1[(l,k)]=matriz_i.loc[k][j]



#Salvando grafo
nx.write_graphml(G1,'/home/aleida/Documentos/Posgrado_Redes/repo/ingredients_graph.graphml')


#weights1

#Funcion para extraer backbone
def extract_backbone(G,weights,alpha):
    keep_graph=nx.Graph()
    for n in G:
        k_n=len(G[n])
        if k_n>1:
            sum_w=sum(weights[n,nj] for nj in G[n])
            for nj in G[n]:
                pij=1.0*weights[n,nj]/sum_w
                if (1-pij)**(k_n-1)<alpha:
                    keep_graph.add_edge(n,nj,weight=matriz_i.loc[n][nj])
                    if keep_graph.nodes()[n]=={}:
                        keep_graph.nodes()[n]['color']=G.nodes()[n]['color']
                        keep_graph.nodes()[n]['category']=G.nodes()[n]['category']
                        keep_graph.nodes()[n]['weight']=G.nodes()[n]['weight']
    return keep_graph

G3 = extract_backbone(G1,weights1,0.04)


#Grafo principal
nx.write_graphml(G3,'/home/aleida/Documentos/Posgrado_Redes/repo/backbone.graphml')



"""nx.draw(G3, with_labels=True, node_color=nx.get_node_attributes(G3, "color").values())
plt.show()"""





