import sys
import numpy as np
import numpy.linalg as la

def angle_between(v1, v2):
    cosang = np.dot(v1, v2)
    sinang = la.norm(np.cross(v1, v2))
    return np.arctan2(sinang, cosang)

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