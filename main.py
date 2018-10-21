
# coding: utf-8

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import itertools
import random
from IPython import embed
from animations import anima


timestep = 5 #Està en segons
capacitat_tren = 500
capacitat_parada = 1000

#elimina to_delete en lista
def elimina(lista, to_delete):
    for k in range(len(to_delete)-1,-1, -1):
        del lista[to_delete[k]]

class linia():    
    def __init__(self, id, nodes, nodesid):
        self.id = id
        self.nodes = nodes
        self.nodesid = nodesid
        
    def nb_nodes(self):
        return len(nodes)
    def add_nodes(self, nodes):
        for node in nodes:
            self.nodes.append(node)


class tren():
    def __init__(self, id, linia, ant, people, velocity, G):
        self.id = id
        self.linia = linia
        self.ant = ant
        if linia.nodesid.index(ant) == 0:
            self.prox = linia.nodesid[1]
        else: self.prox = linia.nodesid[-2]
        self.sentit = linia.nodesid.index(self.prox) - linia.nodesid.index(ant)
        self.people = people
        self.maxtick = np.floor(G.edges[ant, self.prox]['weight']/(velocity*timestep))+1
        self.tick = self.maxtick
        self.v = velocity #en km/s = (km/h)/60
        
    def nb_persones(self):
        return len(self.people)
        
    #avansa el tren i arriba a la nova parada, true
    def avansa(self):
        self.tick -= 1
        if self.tick <= 0: 
            return True
        return False

    #un cop arribat a la parada, decideix la seguent (o mor si fi de trajecte)
    def nou_trajecte(self, G):
        parades = self.linia.nodesid
        posicio = parades.index(self.prox) 
        if (posicio == 0) or (posicio == len(parades) -1):
            return False
        self.ant = self.prox
        self.prox = parades[posicio + self.sentit]
        self.maxtick = np.floor(G.edges[self.ant, self.prox]['weight']/(self.v*timestep))+1
        self.tick = self.maxtick
        return True

    #baixa la gent que ha de baixar (transbord o fi de viatget)
    def descarrega(self, G):
        to_delete = []
        for i, x in enumerate(self.people):
            segueix = x.mou()
            if not segueix: #ha acabat el viatge
                to_delete.append(i)
                continue
                
            if x.trajecte[0] != self.prox: #baixa del tren
                to_delete.append(i)
                G.node[self.ant]['people'][2].append(x)
        elimina (self.people, to_delete)
 
    #carrega la gent del node que va en aquella direcció  
    def carrega(self, G):
        #calcular la max de gen
        max_gent = capacitat_tren - self.nb_persones()
        sen = 0
        if self.sentit == -1: sen = 1
        
        gen_puja = G.node[self.ant]['people'][sen][:max_gent]
        self.people.extend(gen_puja)
        G.node[self.ant]['people'][sen] = G.node[self.ant]['people'][sen][len(gen_puja):]
    


class person():
    def __init__(self, id, inici, destinacio, G):
        self.id = id
        self.pos = inici
        self.trajecte = nx.shortest_path(G, inici, destinacio)[1:]

    #actualitza la seva posicio (per transbords o quan el tren arriba a nova parada)       
    def mou(self):
        self.pos = self.trajecte[0]
        self.trajecte = self.trajecte[1:]
        if not self.trajecte:
            return False
        return True

    #copia la persona en cas de transbord en l'altre parada en la direccio correspondent (o ignore si tranbord => fi de trajecte)
    #just despres el programa principal esborrara els originals (resoltant en moviment o en mort, resp)    
    def transbord(self):
        if len(pers.trajecte) == 1: return
        pers.mou()
        pos = pers.pos
        linia = lineidtoline[idtoname[pos][1]]
        sig = linia.nodesid.index(pers.trajecte[0]) - linia.nodesid.index(pos)
        if sig > 0: 
            G.node[pos]['people'][0].append(pers)
        else: 
            G.node[pos]['people'][1].append(pers)
    
    #per que surtin els noms jeje
    def __repr__(self):
        return "id="+str(self.id)

def sentit(a, b):
    linia = lineidtoline[idtoname[a][1]]
    return linia.nodesid.index(b) - linia.nodesid.index(a)



########
#defineix el graf

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
    pesos_linies = dist_camins3[x]

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
            G.add_edge(cont, cont+1, weight= pesos_linies[j])
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

nodesline = [camins3['L1'], camins3['L2'], camins3['L3'], camins3['L4'], camins3['L5']]
namelines = ['L'+str(i) for i in range(1, 6)]

ed = [dist_camins3['L1'], dist_camins3['L2'], dist_camins3['L3'], dist_camins3['L4'], dist_camins3['L5']]

#conté les linies
lines = []
for i, lin in enumerate(namelines):
    lines.append(linia(lin, nodesline[i], [nametoid[j][lin] for j in nodesline[i]]))

lineidtoline = {} 
for ind,lineid in enumerate(namelines):
    lineidtoline[lineid] = lines[ind]
    
for i, lin in enumerate(lines):
    dists = ed[i]
    parid = lin.nodesid
    for j, par in enumerate(parid):
        if not j: continue
        G.add_edge(parid[j-1], par, weight = dists[j-1])
        
N_nodes = len(G)

"""Amunt: Codi_inicialitzacio() """
#print(N_nodes)
###########

#nx.draw(G, with_labels=True)

##########
#Una simulació ha de seguir el següent esquema

##Funcions utilitzades

#genera trens en ambdues direccions a cada crida (mirar condicions etc...)
def genera_trens(time, trains, cont_train, extral4, G):
    print(time)
    segons_entre_trens_l1 = 3*60+20
    segons_entre_trens_l2 = 3*60+15
    segons_entre_trens_l3 = 3*60+21
    segons_entre_trens_l4 = 4*60+3-extral4
    segons_entre_trens_l5 = 2*60+49

    #Divideixo les dades per 3600 per posar-les en km/s
    vel_trens_l1 = 26.5/3600 
    vel_trens_l2 = 27.2/3600
    vel_trens_l3 = 26.5/3600
    vel_trens_l4 = 28.4/3600
    vel_trens_l5 = 26.7/3600

    #l1
    if time == 1 or np.floor((timestep*time)/segons_entre_trens_l1) > np.floor((timestep*(time-1)/segons_entre_trens_l1)):
        train = tren(cont_train, lineidtoline['L1'], 0, [], vel_trens_l1, G)
        trains.append(train)
        train.carrega(G)
        train = tren(cont_train + 1, lineidtoline['L1'], 29, [], vel_trens_l1, G)
        trains.append(train)
        train.carrega(G)
        cont_train = cont_train + 2
    #l2
    if time == 1 or np.floor((timestep*time)/segons_entre_trens_l2) > np.floor((timestep*(time-1)/segons_entre_trens_l2)):
        train = tren(cont_train, lineidtoline['L2'], 30, [], vel_trens_l2, G)
        trains.append(train)
        train.carrega(G)
        train = tren(cont_train + 1, lineidtoline['L2'], 47, [], vel_trens_l2, G)
        trains.append(train)
        train.carrega(G)
        cont_train += 2
    #l3
    if time == 1 or np.floor((timestep*time)/segons_entre_trens_l3) > np.floor((timestep*(time-1)/segons_entre_trens_l3)):
        train = tren(cont_train, lineidtoline['L3'], 48, [], vel_trens_l3, G)
        trains.append(train)
        train.carrega(G)
        train = tren(cont_train + 1, lineidtoline['L3'], 73, [], vel_trens_l3, G)
        trains.append(train)
        train.carrega(G)
        cont_train += 2
    #l4
    if time == 1 or np.floor((timestep*time)/segons_entre_trens_l4) > np.floor((timestep*(time-1)/segons_entre_trens_l4)):
        train = tren(cont_train, lineidtoline['L4'], 74, [], vel_trens_l4, G)
        trains.append(train)
        train.carrega(G)
        train = tren(cont_train + 1, lineidtoline['L4'], 95, [], vel_trens_l4, G)
        trains.append(train)
        train.carrega(G)
        cont_train += 2
    #l5
    if time == 1 or np.floor((timestep*time)/segons_entre_trens_l5) > np.floor((timestep*(time-1)/segons_entre_trens_l5)):
        train = tren(cont_train, lineidtoline['L5'], 96, [], vel_trens_l5, G)
        trains.append(train)
        train.carrega(G)
        train = tren(cont_train + 1, lineidtoline['L5'], 121, [], vel_trens_l5, G)
        trains.append(train)
        train.carrega(G)
        cont_train += 2
    return cont_train

#genera una person random
def genera_rndpersona(cont_pers, G):
    #def __init__(self, id, inici, destinacio, G):
    posis = random.sample(set(G.nodes()), 2)
    pers = person(cont_pers, posis[0], posis[1], G)
    next_pos = pers.trajecte[0]
    if idtoname[pers.pos][0] == idtoname[next_pos][0]:
        coloco = 2
    elif sentit(pers.pos, next_pos) == 1:
        coloco = 0
    else: coloco = 1
    G.node[pers.pos]['people'][coloco].append(pers)

#genera persones seguint uns criteris
def genera_persones(time, cont_pers, G):
    if time == 1:
        for i in range(40):
            genera_rndpersona(cont_pers, G)
            cont_pers += 1
    else:
        for i in range(40):
            genera_rndpersona(cont_pers, G)
            cont_pers += 1
    return cont_pers

def genera_paco(time, G):
    if time != 1: return
    Paco = person('Paco', 0, 90, G)
    G.node[Paco.pos]['people'][0].append(Paco)
#############################################################################

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
#agafo el metro per anar una mica lluny
for i in G.nodes():
    for j in G.nodes():
        dist = nx.shortest_path_length(G, i, j)
        pes = 1
        if dist < 2:
            pes = 0
        if dist == 2:
            pes = 0.5
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

def genera_persones_poisson(cont_pers,pois, G):
    for i in range(len(pois)):
        for j in range(len(pois)):
            if pois[i][j] == 0: continue
            for k in range(pois[i][j]):
                pers = person(cont_pers,i,j,G)
                next_pos = pers.trajecte[0]
                if idtoname[pers.pos][0] == idtoname[next_pos][0]:
                    coloco = 2
                elif sentit(pers.pos, next_pos) == 1:
                    coloco = 0
                else: coloco = 1
                G.node[pers.pos]['people'][coloco].append(pers)
                cont_pers += 1
    return cont_pers
    


#############################################################################
#embed()
trains = []
cont_train = 0
cont_pers = 0
N_steps = 1000
full_data_trains = []
full_data_nodes = []
for time in range (1, N_steps):
    to_delete = []
    #def calcula_persones(lamb, timestep, pesos, fonts, pous):
    fonts = []
    if time > N_steps/4:
        fonts = [(80,10),(81,10),(79,10)]
    pois = calcula_persones(20,timestep,pesos,fonts,[])
    cont_pers = genera_persones_poisson(cont_pers,pois, G)
    #cont_pers = genera_persones(time, cont_pers, G)
    extral4 = 0
    if time > N_steps/2:
        extral4 = 2
    cont_train = genera_trens(time, trains, cont_train,extral4 ,G)
    """ El que ve aquí sota no es toca """
    for n, train in enumerate(trains):
        #if true has arribat a la parada seguent
        arribat = train.avansa()
        if arribat:
            #if false, hem de matar el tren
            segueix = train.nou_trajecte(G)
            if not segueix: to_delete.append(n) 
            train.descarrega(G)
            train.carrega(G)
        """print("tren: ", train.id, "linia:",train.linia.id, "sentit", train.sentit, "parada ant:", 
              train.ant, "parada prox:",train.prox, "maxtick:",train.maxtick, "tick:", train.tick, 
              "persones", train.nb_persones())"""
    elimina(trains, to_delete)

    trains_to_plot = []
    for train in trains:
        trains_to_plot.append([G.node[train.ant]['pos'], G.node[train.prox]['pos'], train.nb_persones()/capacitat_tren, 1 - train.tick/train.maxtick])
    full_data_trains.append(trains_to_plot)
    #transbord

    nodes_to_plot = []
    for i, x in enumerate(G.nodes()):
        
        persones_amoure = G.node[x]['people'][2]
        for pers in persones_amoure:
            pers.transbord()
        G.node[x]['people'][2] = []
        gent_andana_pos = len(G.node[x]['people'][0])
        gent_andana_neg = len(G.node[x]['people'][1])
        ocupa = min((gent_andana_pos+gent_andana_neg)/capacitat_parada, 1)
        if gent_andana_pos > capacitat_parada or gent_andana_neg > capacitat_parada:
            pass
        nodes_to_plot.append([i, ocupa])

    full_data_nodes.append(nodes_to_plot)

#embed()
anima(full_data_nodes, full_data_trains, nametoid)    
########

