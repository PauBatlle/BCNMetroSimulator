import numpy as np 

importancia = np.ones(len(G.nodes()))
#ESPANYA
importancia[11] = 4
importancia[55] = 4
#UNIVERSITAT
importancia[14] = 3
importancia[32] = 3
#CATALUNYA
importancia[15] = 5
importancia[60] = 5
#URQUINAONA
importancia[16] = 2
importancia[85] = 2
#ARC DE TRIOMF
importancia[17] = 2
#TETUAN
importancia[34] = 2
#CLOT
importancia[20] = 2
importancia[38] = 2
#LA SAGRERA
importancia[22] = 2
importancia[113] = 2
#SAGRADA FAMILIA
importancia[36] = 3
importancia[110] = 3
#PALAU REIAL
importancia[49] = 3
#MARIA CRISTINA
importancia[50] = 3
#'SANTS ESTACIO'
importancia[53] = 5
importancia[105] = 5
#PARAL*LEL
importancia[30] = 2
importancia[57] = 2
#LICEU
importancia[59] = 3
#'PASSEIG DE GRACIA'
importancia[33] = 4
importancia[61] = 4
importancia[86] = 4
#DIAGONAL
importancia[62] = 3
importancia[108] = 3
#BARCELONETA
importancia[83] = 3
#'CIUTADELLA VILA OLIMPICA'
importancia[82] = 2
#'BOGATELL'
importancia[81] = 2
#'HOSPITAL CLINIC'
importancia[107] = 2
#'HOSPITAL DE SANT PAU GUINARDO'
importancia[91] = 2
#'CORNELLA CENTRE'
importancia[96] = 2
#"VALL D'HEBRON"
importancia[67] = 2
importancia[121] = 2

importancia = 1 + (importancia-1)/1.5

pesos = np.zeros([len(G.nodes()),len(G.nodes())])
distancies = np.zeros([len(G.nodes()),len(G.nodes())])
#agafo el metro per anar una mica lluny
for i in G.nodes():
    for j in G.nodes():
        dist = nx.shortest_path_length(G, i, j)
        pes = 1
        if dist < 2:
            pes = 0
        if dist == 2:
            pes = 0.5
        distancies[i][j] = dist
        pesos[i][j] =  pes

for i,x in enumerate(importancia):
    pesos[i,:] = x * pesos[i,:]
    pesos[:,i] = x * pesos[:,i]
pesos = pesos / pesos.sum()



def font(i,multiplicador, pesos):
    pesos2 = np.ones([len(G.nodes()),len(G.nodes())])
    pesos2[i] = multiplicador * pesos2[i]
    return np.multiply(pesos,pesos2) 

def pou(i,multiplicador, pesos):
    pesos2 = np.ones([len(G.nodes()),len(G.nodes())])
    pesos2[:,i] = multiplicador * pesos2[:,i]
    #print(pesos2[:,i])
    return np.multiply(pesos,pesos2) 

def calcula_persones(lamb, timestep, pesos, fonts, pous):
    pesos2 = lamb * timestep * pesos
    for (i, mult) in fonts:
        pesos2 = font(i,mult, pesos2)
    for (i, mult) in pous:
        pesos2 = pou(i,mult, pesos2)
    pois = np.random.poisson(pesos2)
    return pois
        
calcula_persones(3000,0.1,pesos,[(30, 30)],[]).sum(axis = 1)
    