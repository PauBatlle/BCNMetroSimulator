
import pandas as pd
import networkx as nx 
import numpy as np 
import itertools
import matplotlib.pyplot as plt

def get_barcelona():

    df2 = pd.read_csv('metrolines.csv', sep = ',')

    text_file2 = open("camins.txt", "r")
    text = text_file2.read()
    text = text.split('\n')
    camins = [x.split(';') for x in text]
    text_file2.close()


    text_file2 = open("dist_camins.txt", "r")
    text = text_file2.read()
    text = text.split('\n')
    dist_camins = [x.split(';') for x in text]
    text_file2.close()

    parades = pd.read_csv('parades2.csv', sep = ',')
    parades2 = parades[['name', 'line']]


    def arregla(x):
        x= x.replace('[','')
        x= x.replace(']','')
        x= x.replace('[','')
        x= x.replace("'",'')
        x = x.split(',')
        return x

    parades2['line'] = parades2['line'].apply(lambda x: arregla(x))

    camins2 = [[x[0], x[1].split(',')] for x in camins]
    dist_camins2 = [[x[0], x[1].split(',')] for x in dist_camins]
    camins3 = {}
    dist_camins3 = {}
    for i,x in enumerate(camins2):
        camins3[x[0]] = x[1]
        dist_camins3[dist_camins2[i][0]] = [float(y) for y in dist_camins2[i][1]]

    indexs = ['L1','L2','L3','L4','L5']
    G = nx.Graph()
    cont = 0
    nametoid= {}
    idtoname = []
    for i,x in enumerate(indexs):
        coordenades = df2.iloc[:,2*i:2*i+2]
        estacions = camins3[x]
        pesos = dist_camins3[x]

        for j, name in enumerate(estacions):
            idtoname = idtoname + [[name,x]]
            if name not in nametoid.keys():
                nametoid[name] = {}
                nametoid[name][x]= cont
            else:
                nametoid[name][x] = cont
            coord = coordenades.iloc[j].values.tolist()
            coord[1] = 1400 - coord[1]
            G.add_node(cont, name= name, pos=coord, linia= x, people = [[], [], []])
            if j != len(estacions)-1:
                G.add_edge(cont, cont+1, weight= pesos[j])
            cont = cont + 1


    for i, row in parades2.iterrows():
        lines = row['line']
        parada = row['name']
        for j, lin in enumerate(lines):
            if lin in indexs:
                x=list(nametoid[parada].values())
                for pair in list(itertools.combinations(x, 2)):
                    G.add_edge(pair[0], pair[1], weight= 0.0001)
                break
    return G


if __name__ == '__main__':
    G = get_barcelona()
    posvect = []
    for x in G.nodes():
        posvect = posvect + [G.node[x]['pos']]
    nx.draw_networkx_nodes(G,posvect, node_size = 1, with_labels = True)
    plt.show()
