from sciviewer import utils

import numpy as np
import numpy.linalg as la

class Data():
    def __init__(self, adata):
        self.umap = adata.obsm["X_umap"]
        self.gene_names = adata.var.index.tolist()
        
        cell_names = adata.obs.index.tolist()
        self.init_cells(cell_names)

    def init_cells(self, names):
        min1 = self.umap[:,0].min()
        max1 = self.umap[:,0].max()
        min2 = self.umap[:,1].min()
        max2 = self.umap[:,1].max()
        
        self.cells = []
        for i in range(self.umap.shape[0]):
            cell = Cell(names[i], self.umap[i,0], self.umap[i,1])
            cell.normalize(min1, max1, min2, max2)
            self.cells.append(cell)

class Gene():
    def __init__(self, n, i, r, p):
        self.name = n
        self.idx = i
        self.r = r
        self.rabs = abs(r)
        self.p = p

class Cell:
    def __init__(self, c, u1, u2):
        self.code = c
        self.umap1 = u1
        self.umap2 = u2
        self.proj = 0
        self.selected = False
        self.expression = []

    def normalize(self, min1, max1, min2, max2):
        self.umap1 = (self.umap1 - min1) / (max1 - min1)
        self.umap2 = 1 - (self.umap2 - min2) / (max2 - min2)
        
    def project(self, sel):
        if self.selected:
            dirv = np.array([sel.nx1 - sel.nx0, sel.ny1 - sel.ny0])
            celv = np.array([self.umap1 - sel.nx0, self.umap2 - sel.ny0])
            a = utils.angle_between(dirv, celv)
            self.proj = np.cos(a) * la.norm(celv) / la.norm(dirv)