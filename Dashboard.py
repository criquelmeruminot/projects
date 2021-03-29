# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 23:10:30 2021

@author: Constanza Elizabeth
"""
import random
from math import pi
import numpy as np

import matplotlib.colors as mcolors
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import gridplot
from bokeh.transform import cumsum
from bokeh.models.widgets import Div,DataTable, TableColumn
from bokeh.transform import transform
from bokeh.models import (BasicTicker, ColorBar, ColumnDataSource,
                          LinearColorMapper, PrintfTickFormatter,Legend, LabelSet)
from bokeh.palettes import Set2

class generar_Dash():
    
    def exportar_dash(self,df_lineas_comuna,df_puntos_linea,df_puntos_linea_comuna,df_comunas_linea,df_pivot_table_puntos_comuna):
        output_file('Ventas y Punto de Carga BIP.html')
        #Título
        p0= Div(text="""<h2><b>Ventas y Punto de Carga BIP</b></h2>""",width=600, height=20,sizing_mode='stretch_both')
        
        #Plot 1: Líneas por Comuna
        source = df_lineas_comuna
        p1 = figure(x_range=source['COMUNA'], plot_height=400, title="Cantidad de Líneas por Comuna",
               toolbar_location=None, tools="")
        p1.vbar(x='COMUNA', top='CODIGO', width=0.9, source=source)
        p1.xaxis.major_label_orientation = 1
        p1.yaxis.axis_label = 'Cantidad de Líneas'
        p1.xaxis.axis_label = 'Comuna'
    
        #Plot 2: Puntos por Línea
        source = df_puntos_linea
        p2 = figure(x_range=source['CODIGO'], plot_height=400, title="Puntos de Venta y Carga por Línea")
        p2.line(x='CODIGO', y='NOMBRE FANTASIA', width=0.9,line_color = 'orange',source=source)
        p2.xaxis.major_label_orientation = 1
        p2.yaxis.axis_label = 'Cantidad de Puntos'
        p2.xaxis.axis_label = 'Línea'
        
        #Plot 3: Puntos por Línea y Comuna
        source = ColumnDataSource(df_puntos_linea_comuna.sort_values(by = 'CODIGO'))
        colors = LinearColorMapper(palette= Set2[source.data['NOMBRE FANTASIA'].max()], low=source.data['NOMBRE FANTASIA'].min(), high=source.data['NOMBRE FANTASIA'].max())
        p3 = figure(plot_width=550, plot_height=400, title="Puntos por Línea y Comuna",
                    x_range = df_puntos_linea_comuna['COMUNA'].unique().tolist(), 
                    y_range= df_puntos_linea_comuna['CODIGO'].unique().tolist(), 
                      toolbar_location=None, tools="", x_axis_location="below")
        p3.rect(x="COMUNA", y="CODIGO", width=1, height=1, source=source,
                line_color='black', fill_color=transform('NOMBRE FANTASIA', colors))
        color_bar = ColorBar(color_mapper=colors, location=(0, 0),
                                ticker=BasicTicker())
        p3.add_layout(color_bar, 'right')
        p3.xaxis.major_label_orientation = 1.0
        
        #Plot 4: Comparativo Líneas por Comuna
        
        data = df_comunas_linea
        data['angle'] = data['COMUNA']/data['COMUNA'].sum() * 2*pi
        random.seed(80)
        data['color'] = random.sample([*mcolors.CSS4_COLORS.values()],len(data))
        source = ColumnDataSource(data=data)
    
        p4 = figure(plot_height=430,plot_width=430, title="Comunas por Línea")
        p4.wedge(x=0, y=1, radius=0.6,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white",fill_color='color',legend = 'CODIGO', source=source)
        
        #Tabla1:
        source = ColumnDataSource(df_pivot_table_puntos_comuna.fillna(0))
        columns = [
            TableColumn(field='COMUNA', title='Comuna'),
            TableColumn(field='L1', title='L1'),
            TableColumn(field='L2', title='L2'),
            TableColumn(field='L3', title='L3'),
            TableColumn(field='L4', title='L4'),
            TableColumn(field='L4A', title='L4A'),
            TableColumn(field='L5', title='L5'),
            TableColumn(field='L6', title='L6'),]
        t1 = DataTable(name = 'Tabla Resumen puntos Comuna-Línea',source=source,columns = columns, width=50, height=25,sizing_mode = 'scale_width', fit_columns=True)
        
        #Mapa
        direccion_mapa = './Mapa_Lineas.html'
        map_iframe_text = """<iframe src=" """ + direccion_mapa +"""" height="300" width="400" frameborder="0"></iframe>"""
        map_div = Div(
            text=map_iframe_text,
            height=300, width=400)
        
        #Salida Dashboard
        grid = gridplot([[p0,None],[p1,p2],[p3,p4],[t1,map_div]])
        show(grid)
