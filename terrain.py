import globals as g
import plotly.graph_objs as go

landscape = []
for i in range(len(g.height_data)/g.YDIM):
    row = []
    for j in range(len(g.height_data)/g.XDIM):
        row.append(g.height_data[j+(500*i)])
    landscape.append(row)
print "landscape built"


data = go.Contour(
    name= "Terrain",
    z= landscape,
    x= range(500),
    y= range(500),
    xaxis="x1",
    yaxis="y1",
    colorscale='Earth',
    showscale= False,
    contours= dict(
    coloring='heatmap'
)
)
data2 = go.Contour(
    name= "Terrain",
    z= landscape,
    x= range(500),
    y= range(500),
    xaxis="x2",
    yaxis="y2",
    colorscale='Earth',
    contours= dict(
    coloring='heatmap'
)
)