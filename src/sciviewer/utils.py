import sys
import numpy as np
import numpy.linalg as la

def angle_between(v1, v2):
    cosang = np.dot(v1, v2)
    sinang = la.norm(np.cross(v1, v2))
    return np.arctan2(sinang, cosang)

# Using the ray tracing method discussed here:
# https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python
def point_inside_polygon(x, y, poly):
    n = len(poly)
    inside = False

    p1x, p1y = poly[0]
    for i in range(n+1):
        p2x, p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

def is_mac():
    return sys.platform == 'darwin'

def in_notebook():
    try:
        from IPython import get_ipython
        if 'IPKernelApp' not in get_ipython().config:  # pragma: no cover
            return False
    except ImportError:
        return False
    except AttributeError:
        return False
    return True

def get_cell_width():
    # https://stackoverflow.com/questions/64391373/how-do-i-find-the-width-of-an-ipython-cell
    # https://medium.com/@tomgrek/reactive-python-javascript-communication-in-jupyter-notebook-e2a879e25906
    # https://jakevdp.github.io/blog/2013/06/01/ipython-notebook-javascript-python-communication/
    # https://jupyter-notebook.readthedocs.io/en/stable/comms.html    
    # https://github.com/jupyterlab/jupyterlab/issues/5660
    # https://github.com/jupyter/notebook/issues/6394
    if in_notebook():
        from IPython.core.display import Javascript
        # js = "IPython.notebook.kernel.execute("cell_width="+($( ".cell").width()))"
        js = "alert('Hello, world!')"
        Javascript(js)
        return 1
    return -1    