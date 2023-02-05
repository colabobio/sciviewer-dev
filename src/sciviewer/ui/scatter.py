from sciviewer.ui.widget import Widget
from sciviewer.utils import point_inside_polygon

class Scatter(Widget):
    def setup(self):
        self.cell_size = 3 * self.intf.scale_factor
        self.padding = 10 * self.intf.scale_factor
        self.spacing = 2 * self.intf.scale_factor
        self.edge_weight = 1 * self.intf.scale_factor

    def draw(self):
        p = self.intf.sketch
        self.draw_cells(p)
        self.draw_edges(p)

    def draw_cells(self, p):
        p.rect_mode(p.CENTER)
        p.no_stroke()
        ps = self.padding + self.spacing
        for cell in p.data.cells:
            x = p.remap(cell.umap1, 0, 1, ps, self.width - ps)
            y = p.remap(cell.umap2, 0, 1, ps, self.height - ps)
            if cell.is_selected:
                p.fill(230, 20, 20, 100)
            else:                
                p.fill(0, 100)
            p.rect(x, y, self.cell_size, self.cell_size)

    def draw_edges(self, p):
        p.rect_mode(p.CORNER)
        p.stroke(150)
        p.stroke_weight(self.edge_weight)
        p.no_fill()
        p.rect(self.padding, self.padding, self.width - 2 * self.padding, self.height - 2 * self.padding)

    def clear_selection(self):
        p = self.intf.sketch
        for cell in p.data.cells:
            cell.is_selected = False

    def select_cells(self, sel_area):
        p = self.intf.sketch
        ps = self.padding + self.spacing
        for cell in p.data.cells:
            x = p.remap(cell.umap1, 0, 1, ps, self.width - ps)
            y = p.remap(cell.umap2, 0, 1, ps, self.height - ps)
            cell.is_selected = point_inside_polygon(x, y, sel_area)