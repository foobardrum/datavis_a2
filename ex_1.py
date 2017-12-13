import plotly
import temperature as tp
import terrain as tr
#plotly.tools.set_credentials_file(username='groovyshutter', api_key='V9ITJxS7qvZsXS8P1oTQ')

#P_data = readbin("Pf01.bin")

layout = dict(
    title="Temperatur im Hurrikan 2004",
    font=dict(
        family="Droid Sans, sans-serif",
    ),
    xaxis1=dict(
        title='geographische Breite'
    ),
    yaxis1=dict(
        title='geographische Laenge',
        autorange='reversed'
    ),
    xaxis2=dict(
        title='geographische Breite'
    ),
    yaxis2=dict(
        title='geographische Laenge',
        autorange='reversed'
    ),
)

tp.data['colorbar'].update(
    x=1.1,
    y=0.5,
    len=1,
    lenmode="fractial"
)

fig = plotly.tools.make_subplots(rows=1, cols=2,
                          subplot_titles=('Terrain', 'Hurricane in 1km height'))

fig.append_trace(tr.data, 1, 1)
fig.append_trace(tr.data2, 1, 2)
fig.append_trace(tp.data, 1, 2)

fig['layout'].update(layout)

plotly.offline.plot(fig, filename='base_map.html')
