import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.animation
import matplotlib.collections as collections
import numpy as np
from creagraf import get_barcelona
from IPython import embed
from trenets import donam_el_tren
from matplotlib import cm
from adjustText import adjust_text
"""
Codi de colors 
0 --> Verd
1 --> Vermell
"""


def anima(full_data_nodes, full_data_trains, nametoid):

    Niter = len(full_data_nodes)
    cm_vv = lambda x: cm.gist_rainbow(-0.48*x + 0.48)

    # Create Graph
    G = get_barcelona()

    pos = {i: G.node[i]['pos'] for i in range(len(G))}
    linia = 1

    def update(num):
        ax.clear()
        nodes_this_step = full_data_nodes[num]
        trains_this_step = full_data_trains[num]
        dibuixa_xarxa()
        #print(nodes_this_step)
        #print(nodes_this_step)
        #nx.draw_networkx_nodes(G,pos,node_color=nodes_this_step,node_size=5, cmap = cm_vv) #Falta posar color segons ocupació
        nx.draw_networkx_nodes(G,pos,node_color=[cm_vv(nodes_this_step[i][1])[:4] for i in range(len(nodes_this_step))],node_size=50) #Falta posar color segons ocupació

        #Per a cada tren necessito: nd
        # [x_0, y_0, x_desti, y_desti, ocupacio sobre 1, fraccio_viatge]
        trens = [donam_el_tren(*i) for i in trains_this_step]
        #trens = None
        Trenets = collections.PatchCollection(trens, match_original = True, zorder=10)
        ax.add_collection(Trenets)
        #new_colors_edges= [cm_vv(np.random.random()) for _ in range(12)]
        #new_colors_nodes = [cm_vv(1) for _ in range(8)]

        # Scale plot ax
        """
        ax.set_title("Frame %d"%(num+1), fontweight="bold")
        ax.set_xticks([])
        ax.set_yticks([])
        plt.axis('equal')
        plt.title(str(num) + " segons")
        """
        plt.title(str(num))

    fig, ax = plt.subplots(figsize=(40,20))

    magic_numbers = [-1,29,47,73,95,121]
    color = {1: 'red', 2: 'purple', 3: 'green', 4: 'yellow', 5: 'blue'}

    def dibuixa_xarxa():
        for i in range(1,6):
            nx.draw_networkx_edges(G,pos, edgelist = [(k, k+1) for k in range(magic_numbers[i-1]+1, magic_numbers[i])], width=5.0,edge_color=color[i], alpha = 0.2)

        for i in nametoid.keys():
            idd = list(nametoid[i].values())[0]
            gj = G.node[idd]
            plt.text(gj['pos'][0]+10, gj['pos'][1]+10, gj['name'][:8]+("" if len(gj['name']) <= 8 else "."), fontsize = 5, rotation = 10)

    dibuixa_xarxa()
    nx.draw_networkx_nodes(G,pos,node_color=cm_vv(0),node_size=50)
    #embed()
    anim = matplotlib.animation.FuncAnimation(fig, update, frames=Niter, interval = 1)
    #Writer = matplotlib.animation.writers['ffmpeg']
    #writer = Writer(fps=60, metadata=dict(artist='Me'), bitrate=1800)
    #anim.save('Resultat1.mp4', writer = writer)
    plt.show()