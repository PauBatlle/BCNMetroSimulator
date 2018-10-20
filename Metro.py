
# coding: utf-8

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import itertools
import random


timestep = 1
capacitat_tren = 30
capacitat_parada = 50 

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
        self.maxtick = np.floor(G.edges[ant, self.prox]['weight']/(velocity*timestep))
        self.tick = self.maxtick
        self.v = velocity
        
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
        self.maxtick = np.floor(G.edges[self.ant, self.prox]['weight']/(self.v*timestep))
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

#bastant explicit, torna +1, -1
def sentit(a, b):
    linia = lineidtoline[idtoname[a][1]]
    return linia.nodesid.index(b) - linia.nodesid.index(a)

#genera trens en ambdues direccions a cada crida (mirar condicions etc...)
def genera_trens(time, trains, cont_train):
    #l1
    if time%3 == 1:
        train = tren(cont_train, lineidtoline['l1'], 0, [], 1, G)
        trains.append(train)
        train.carrega(G)
        train = tren(cont_train + 1, lineidtoline['l1'], 5, [], 1, G)
        trains.append(train)
        train.carrega(G)
        cont_train = cont_train + 2
    #l2
    if time%4 == 1: 
        train = tren(cont_train, lineidtoline['l2'], 3, [], 1, G)
        trains.append(train)
        train.carrega(G)
        train = tren(cont_train + 1, lineidtoline['l2'], 10, [], 1, G)
        trains.append(train)
        train.carrega(G)
        cont_train += 2
    #l3
    if time%3 == 1: 
        train = tren(cont_train, lineidtoline['l3'], 8, [], 1, G)
        trains.append(train)
        train.carrega(G)
        train = tren(cont_train + 1, lineidtoline['l3'], 11, [], 1, G)
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
        for i in range(100):
            genera_rndpersona(cont_pers, G)
            cont_pers += 1
    else:
        for i in range(100):
            genera_rndpersona(cont_pers, G)
            cont_pers += 1
    return cont_pers

########
#defineix el graf

####  DATA A FICAR
#DATA: Noms, pos, lines
df = pd.DataFrame([['A', [0, 0], ['l1']], ['B', [0, 1], ['l1']], ['C', [1, 0], ['l1', 'l2', 'l3']], 
                   ['D', [1, 1], ['l1']], ['E', [2, 4], ['l2']], ['F', [3, 3], ['l2']], ['G', [3, 3], ['l3']], 
                   ['H', [3, 3], ['l3']], ['I', [3, 3], ['l2','l3']]],columns=['name', 'pos', 'linia'])

#matriu de lines amb parades en ordre canonic MELCHORRA
nodesline = [['A', 'B', 'C', 'D'], ['C', 'E', 'F', 'I'], ['G','C', 'H', 'I']]

#list amb noms de les lines
namelines = ['l'+str(i) for i in range(1, 4)]

#ditancies entre parades adjacents en cada line
ed = [[2, 3, 2],[3, 2, 4], [2, 2, 4]]

#### FI DATA A FICAR
#print(df)

#input: [name][line], output: id
nametoid= {}

#input: id, output: [name, line]
idtoname = []
G = nx.Graph()
cont = 0
for n, row in df.iterrows():
    name = row['name']
    nametoid[name]= {}
    for lin in row['linia']:
        nametoid[name][lin]= cont
        idtoname.append([name, lin])
        G.add_node(cont, name= name, pos=row['pos'], linia= lin, people = [[], [], []])
        cont += 1
    x=list(nametoid[name].values())
    for pair in list(itertools.combinations(x, 2)):
        G.add_edge(pair[0], pair[1], weight= 0.0001)


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
###########

#nx.draw(G, with_labels=True)

##########
#Iteracions

trains = []
cont_train = 0
cont_pers = 0
for time in range (1, 12):
    to_delete = []
    #def __init__(self, linia, ant, prox, people, velocity, G)
    cont_pers = genera_persones(time, cont_pers, G)
    cont_train = genera_trens(time, trains, cont_train)
    print("iteracio: ", time)
    for n, train in enumerate(trains):
        #if true has arribat a la parada seguent
        arribat = train.avansa()
        if arribat:
            #if false, hem de matar el tren
            segueix = train.nou_trajecte(G)
            if not segueix: to_delete.append(n)
            
            train.descarrega(G)
            train.carrega(G)
        print("tren: ", train.id, "linia:",train.linia.id, "sentit", train.sentit, "parada ant:", 
              train.ant, "parada prox:",train.prox, "maxtick:",train.maxtick, "tick:", train.tick, 
              "persones", train.nb_persones())
    elimina(trains, to_delete)
    
    #transbord
    for x in G.nodes():
        persones_amoure = G.node[x]['people'][2]
        for pers in persones_amoure:
            pers.transbord()
        G.node[x]['people'][2] = []
        gent_andana_pos = len(G.node[x]['people'][0])
        gent_andana_neg = len(G.node[x]['people'][1])
        print('Gent a la parada '+ str(G.node[x]['name'])+ ' linia '+str(G.node[x]['linia'])+':', 
              gent_andana_pos+gent_andana_neg)
        if gent_andana_pos > capacitat_parada or gent_andana_neg > capacitat_parada:
            print("Warning: Parada " + str(G.node[x]['name'])+ ' linia '+str(G.node[x]['linia']) +
                  " està col·lapsada")
    
    print(" ")
########

