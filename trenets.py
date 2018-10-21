
from matplotlib.patches import Rectangle
from matplotlib import cm
import numpy as np
cm_vv = lambda x: cm.gist_rainbow(-0.48*x + 0.48)


def donam_el_tren(x, y, frac_ocup, frac_trajecte, l_q = 10):
    x1,y1 = x 
    x2,y2 = y
    abs_vec = l2distance(x1, y1, x2, y2)
    angle = np.arctan2(y2-y1,x2-x1)
    v_direccio = np.array([x2-x1, y2-y1])/abs_vec
    v_perpendicular = np.array([y1-y2, x2-x1])/abs_vec
    xcent = frac_trajecte*x2 + (1-frac_trajecte)*x1
    ycent = frac_trajecte*y2 + (1-frac_trajecte)*y1
    baix_esq = np.array([xcent, ycent]) -(l_q/2)*v_direccio-(l_q/2)*v_perpendicular
    rect = Rectangle(baix_esq, l_q, l_q, 360*angle/(2*np.pi), fc=cm_vv(frac_ocup))
    return rect



def l2distance(x1, y1, x2, y2):
    return np.linalg.norm([x1-x2, y1-y2])

