


import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib.collections as collections
from IPython.display import HTML
import matplotlib.patches as patches
"""
fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)
"""
from matplotlib import cm
cm_vv = lambda x: cm.gist_rainbow(-0.48*x + 0.48)
"""
ax = plt.axes(xlim=(0, 10), ylim=(0, 10))
patch = plt.Rectangle((1, 1), 0.25, 0.25, fc='y')
patch2 = plt.scatter((1,9),(1,9))
line = plt.Line2D((1,9),(1,9), lw=4.5)
plt.gca().add_line(line)


def init():
    patch.xy = (1, 1)
    patch.angle = 45
    ax.add_patch(patch)
    return patch,

def animate(i):
    patch.xy = (1+0.1*i, 1+0.1*i)
    patch.angle = 45
    return patch,

anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=100, 
                               interval=20,
                               blit=True)

"""
#plt.show()


def l2distance(x1, y1, x2, y2):
    return np.linalg.norm([x1-x2, y1-y2])

def on_esta_el_tren(x1, y1, x2, y2, frac_ocup, frac_trajecte, l_q = 50):
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')
    #frac_ocup es un real entre zero i u
    #frac_trajecte es un real entre zero i u
    abs_vec = l2distance(x1, y1, x2, y2)
    angle = np.arctan2(y2-y1,x2-x1)
    v_direccio = np.array([x2-x1, y2-y1])/abs_vec
    v_perpendicular = np.array([y1-y2, x2-x1])/abs_vec
    #plt.scatter((x1,x2),(y1,y2))
    #line = plt.Line2D((x1, x2), (y1, y2), lw=2.5)
    #plt.gca().add_line(line)
    xcent = frac_trajecte*x2 + (1-frac_trajecte)*x1
    ycent = frac_trajecte*y2 + (1-frac_trajecte)*y1
    baix_esq = np.array([xcent, ycent]) -(l_q/2)*v_direccio-(l_q/2)*v_perpendicular
    print(xcent, ycent, baix_esq)
    print(v_direccio, v_perpendicular)
    rect = patches.Rectangle(baix_esq, l_q, l_q, 360*angle/(2*np.pi), fc=cm_vv(frac_ocup))
    ax1.add_line(plt.Line2D((x1,x2), (y1,y2)))
    rect=collections.PatchCollection([rect], match_original = True, zorder=10)
    ax1.add_collection(rect)
    plt.xlim([x1,x2])
    plt.ylim([y1,y2])
    plt.show()

on_esta_el_tren(2,2, 4,3, 0, 0.5)
from IPython import embed

#embed()