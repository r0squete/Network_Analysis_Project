#!/usr/bin/env python
# coding: utf-8



#importando librerias
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt 
from community import community_louvain

#leyendo backbone del grafo
G3=nx.read_graphml('/home/aleida/Documentos/Posgrado_Redes/repo/new_backbone.graphml')


#Detectando comunidades
comunidades=nx.community.louvain_communities(G3, weight='weight', resolution=1.5,seed=3)


#comunidades
#len(comunidades)

comunidades_map={}
for i in range(len(comunidades)):
    comunidades_map.update(dict.fromkeys(comunidades[i],i))
#comunidades_map

#cargando bd
bd=pd.read_csv('/home/aleida/Documentos/Posgrado_Redes/repo/bd_new.csv',index_col='country')


#bd


#df para la info de la frecuencia de los ingredientes por paises
new_df=pd.DataFrame(data=0,index=bd.index.unique(),columns=bd.columns)


#new_df


for i in bd.columns:
    distribucion=bd[i].groupby("country").sum()
    for index in distribucion.index:
        new_df.loc[index][i]=distribucion[index]        


#new_df

tabla_resumen=pd.DataFrame(columns=['ingredient','comunidad','pais','category'])


#df resumen sobre info de las comunidades
for k in range(len(comunidades)):
    for ingredient in comunidades[k]:
        pais=new_df.index[0]
        x=new_df.loc[pais][ingredient]
        for i in new_df.index[1:]:
                if x<new_df.loc[i][ingredient]:
                    pais=i
                    x=new_df.loc[i][ingredient]
        tabla_resumen = tabla_resumen.append({'ingredient': ingredient,
                                              'comunidad': k,
                                              'pais': pais,
                                              'category': G3.nodes[ingredient]['category']}, ignore_index=True)
             

#tabla_resumen

#df resumen sobre la representacion de cada pais en las comunidades
tabla_resumen2=pd.DataFrame(columns=['comunidad','pais','aporte relativo'])


for i in range(len(comunidades)):
    df=tabla_resumen[tabla_resumen['comunidad'] == i]
    for k in df['pais'].value_counts().index:
        tabla_resumen2 = tabla_resumen2.append({'comunidad': i,
                                                'pais': k,
                                                'aporte relativo': df['pais'].value_counts(normalize=True)[k]}, ignore_index=True)


#tabla_resumen2


#df resumen sobre la representacion de cada categoria en las comunidades
tabla_resumen3=pd.DataFrame(columns=['comunidad','category','aporte'])


for i in range(len(comunidades)):
    df=tabla_resumen[tabla_resumen['comunidad'] == i]
    for k in df['category'].value_counts().index:
        tabla_resumen3 = tabla_resumen3.append({'comunidad': i,
                                                'category': k,
                                                'aporte': df['category'].value_counts(normalize=True)[k]}, ignore_index=True)


#tabla_resumen3


datos = open('/home/aleida/Documentos/Posgrado_Redes/repo/communities_stat_new.txt', 'wt')

for i in range(len(comunidades)):
    datos.write('\n')
    datos.write(".........comunidad.........."+str(i))
    datos.write('\n')
    datos.write(str(tabla_resumen2[tabla_resumen2['comunidad']==i].iloc[0:3]))
    datos.write('\n')
    datos.write(str(tabla_resumen3[tabla_resumen3['comunidad']==i].iloc[0:3])) 
    
datos.close()


import matplotlib.colors as mcolors
paleta=list(mcolors.TABLEAU_COLORS.values())
paleta.append("darkslateblue")
color_pallet=paleta

color_nodos=[]
for node in G3:
    color_nodos.append(color_pallet[comunidades_map[node]])


"""nx.draw(G3,node_color=color_nodos, with_labels=True)
plt.show()


#Pintando el grafo con colores segun las comunidades y peso
weights = [a[2]["weight"] for a in G3.edges(data=True)]
weights = [(a-min(weights))/(max(weights)-min(weights))*100 for a in weights]


# Definir la posición de los nodos utilizando un layout
pos = nx.spring_layout(G3)

# Representar nodos y ejes
fig, ax = plt.subplots(figsize=(15,10))
nx.draw_networkx_nodes(
    G3,
    pos = pos,
    node_size=600,
    ax = ax,
    node_color=color_nodos,
)
nx.draw_networkx_edges(
    G3,
    pos = pos,
    edgelist = G3.edges,
    width = weights,
    alpha=0.3,
    ax = ax
)
nx.draw_networkx_labels(
    G3,
    pos = pos,
    horizontalalignment='right',
    verticalalignment='center',
    font_size = 8
)
("")


H = G3.subgraph(comunidades[2])


#Pintando algunas comunidades
# Definir la posición de los nodos utilizando un layout
pos = nx.random_layout(H)

# Representar nodos y ejes
fig, ax = plt.subplots(figsize=(15,10))
nx.draw_networkx_nodes(
    H,
    pos = pos,
    node_size=600,
    ax = ax,
    node_color=list(nx.get_node_attributes(H, "color").values()),
)
nx.draw_networkx_edges(
    H,
    pos = pos,
    edgelist = H.edges,
    width = weights,
    alpha=0.3,
    ax = ax
)
nx.draw_networkx_labels(
    H,
    pos = pos,
    horizontalalignment='right',
    verticalalignment='center',
    font_size = 8
)
("")"""

G6=nx.Graph()


k=0
for node in G3:
    G6.add_node(node,weight=nx.get_node_attributes(G3,'weight')[node],category=nx.get_node_attributes(G3,'category')[node],color=color_nodos[k])
    k+=1


for edge in G3.edges():
    G6.add_edge(edge[0],edge[1],weight=G3.get_edge_data(edge[0],edge[1])["weight"])


nx.write_graphml(G6,'/home/aleida/Documentos/Posgrado_Redes/repo/new_communities_graph.graphml')



central = open("/home/aleida/Documentos/Posgrado_Redes/repo/new_central.txt", "w")
for j, com in enumerate(comunidades):
    H = G3.subgraph(com)
    degree=nx.degree_centrality(H)
    betweennes=nx.betweenness_centrality(H)
    sor1 = sorted(degree.items(), key=lambda i: i[1], reverse=True)
    sor2 = sorted(betweennes.items(), key=lambda i: i[1], reverse=True)
    degree_com=0
    for z in sor1:
        degree_com+=z[1]
    degree_com=degree_com/len(sor1)
    betwennes_com=0
    for z in sor2:
        betwennes_com+=z[1]
    betwennes_com=betwennes_com/len(sor1)
    central.write(f"degree\n")
    for i in sor1[:3]:
        central.write(f"{j}: {i[0]}={i[1]}\n")
    central.write(f"degree_community....{degree_com}\n")
    central.write(f"beetwennes\n")
    for i in sor2[:3]:
        central.write(f"{j}: {i[0]}={i[1]}\n")
    central.write(f"beetwennes_community....{betwennes_com}\n")
central.close()



