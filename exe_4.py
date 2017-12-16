#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 15:49:17 2017

@author: cynthiaaludogbu
"""
from bokeh.plotting import figure, output_file, show
from bokeh.models import LinearColorMapper, BasicTicker, ColorBar, Arrow, VeeHead
import numpy as np
import pandas as pd 
from pandas.plotting import scatter_matrix
# obtaining the data
files=['TCf01', 'TCf02', 'TCf03', 'TCf04', 'TCf05', 'Uf01', 'Vf01','Wf01', 'Pf01', 'PRECIPf01']
# files += ['Uf37','Vf37', 'Wf37'] # debug
colors3 = {'TCf01':'blue', 'TCf02':'red', 'TCf03':'green', 'TCf04':'pink', 'TCf05':'purple'}
data = {}
for f in files:
    t = np.fromfile('data/%s.bin' % f, dtype='>f4')
    t[t >= 1e35] = np.nan
    data[f] = t

def get_xy(data,z):
    outcome = np.zeros((500,500),dtype='float')
    for x in range(500):
        for y in range(500):
            outcome[x,y] = data[x+500*y+250000*z]
    return outcome

def get_z(data,x,y):
    return np.array([data[x+500*y+250000*z] for z in range(100)], dtype='float')

#task 2
heights=np.linspace(0.035, 19.835, num=100)

p2=figure(title='Temperature @ (200,250), hour 1', x_axis_label='height (km)', y_axis_label='temperature (degree C)')
p2.line(x=heights, y=get_z(data['TCf01'],200,250))
output_file('task2.html')
show(p2)

#task 3
p3=figure(title='hour lines', x_axis_label='height (km)', y_axis_label='temperature (degree C)')

baseline=np.zeros(100, dtype='float')
for f in files:
    if f.startswith('TC'):
        baseline = baseline + get_z(data[f],200,250)
        p3.line(x=heights, y=baseline, legend=f, color=colors3[f])
output_file('task3.html')
show(p3)
    
#task 4
image = get_xy(data['TCf01'], 5) # 5=1km altitude

color_mapper = LinearColorMapper(palette="Viridis256", low=np.nanmin(image), high=np.nanmax(image), nan_color='white')
plot = figure(title='Temperature @ 1km, hour 1', x_axis_label='Longitude', y_axis_label='Latitude', x_range=(0,500), y_range=(0,500), toolbar_location=None)
plot.image(image=[np.flipud( image ) ], color_mapper=color_mapper,
           dh=[500], dw=[500], x=[0], y=[0])
color_bar = ColorBar(title='T [ºC]', color_mapper=color_mapper, ticker=BasicTicker(),
                     label_standoff=12, border_line_color=None, location=(0,0))
plot.add_layout(color_bar, 'left')
output_file('task4.html')
show(plot)

##task 5
U=get_xy(data['Uf01'], 5)
V=get_xy(data['Vf01'], 5)
W=get_xy(data['Wf01'], 5) 
#U=get_xy(data['Uf37'], 50) # reproduce plot in assignment
#V=get_xy(data['Vf37'], 50)
#W=get_xy(data['Wf37'], 50)

x_start = np.zeros(100, dtype='float')
y_start = x_start.copy()
x_end = x_start.copy()
y_end = x_start.copy()
speed = x_start.copy()
i = -1
for x in range(0, 500, 50):
    for y in range(0,500, 50):
        i += 1
        x_start[i] = x
        y_start[i] = y
        u = U[y,x]
        v = V[y,x]
        w = W[y,x]
        if np.isnan(u):
            continue
        speed[i] = (u**2 + v**2 + w**2)**0.5
        speed_xy = (u**2 + v**2)**0.5

        factor = 0 if speed[i] == 0 else speed[i] / speed_xy
        x_end[i] = x + u * factor
        y_end[i] = y - v * factor

plot = figure(title='Wind speed @ 1km, hour 1', x_axis_label='Longitude', y_axis_label='Latitude', x_range=(0,500), y_range=(500,0), toolbar_location=None)

color_mapper = LinearColorMapper(palette="Viridis256", low=np.nanmin(speed), high=np.nanmax(speed), nan_color='black')
ci = (256*(speed - color_mapper.low)/(1e-5+color_mapper.high-color_mapper.low)).astype('int')
col = [color_mapper.palette[i] for i in ci]

for i in range(len(x_start)):
    plot.add_layout(Arrow(end=VeeHead(size=5), x_start=x_start[i], y_start=y_start[i], x_end=x_end[i], y_end=y_end[i], line_color=col[i]))

plot.circle(x=x_start, y=y_start, color=col ,size=8)
plot.x(x=x_end, y=y_end)
color_bar = ColorBar(title='speed', color_mapper=color_mapper, ticker=BasicTicker(),
                     label_standoff=12, border_line_color=None, location=(0,0))
plot.add_layout(color_bar, 'left')
output_file('task5.html')
show(plot)

variables=['TCf01', 'Pf01', 'PRECIPf01']
Loc = [ [250,200,5], [300,300,5], [200,100,5], [400,400,5] ]
sc_data = [ list(get_z(data[v],x,y)[z] for v in variables) for (x,y,z) in Loc]
pd_data = pd.DataFrame(sc_data, columns=['Temp', 'Pressure', 'Precip'])
scatter_matrix(pd_data)
