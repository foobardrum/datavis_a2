import globals as g
import plotly.graph_objs as go

temperature = []
for i in range(len(g.TC_data)/(g.YDIM*g.ZDIM)):
    row = []
    for j in range(len(g.TC_data)/(g.XDIM*g.ZDIM)):
        if g.TC_data[g.idx(j,i,g.TC_height)] > 1.0e30:
            row.append(None)
        else:
            row.append(g.TC_data[g.idx(j,i,g.TC_height)])
    temperature.append(row)
print "temperature built"

data = go.Contour(
    name= "Temperatur",
    z=temperature,
    contours=dict(coloring='fill',size=2,showlabels=True),
    connectgaps= False,
    x=range(500),
    x0=0,
    y=range(500),
    y0=0,
    xaxis="x2",
    yaxis="y2",
    showscale=True,
    colorscale='Magma',
    colorbar=dict(
        title="Temperatur auf 1 km Hoehe",
        titleside='right',
        ticks='outside'
    )
)
