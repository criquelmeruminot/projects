# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 23:08:41 2021

@author: Constanza Elizabeth
"""
import folium
from folium.plugins import MarkerCluster
import webbrowser
import matplotlib.colors as mcolors
import random
from folium import LayerControl

class generar_Mapa():
    
    def exportar_mapa(self,puntos_carga,df_comunas_linea):
        random.seed(80)
        df_comunas_linea['color'] = random.sample([*mcolors.CSS4_COLORS.values()],len(df_comunas_linea))

        mapa_general = folium.Map(location=(puntos_carga.iloc[0,9],puntos_carga.iloc[0,8]),zoom_start=10)
        for i,j in df_comunas_linea.iterrows():
            linea = j['CODIGO']
            color = j['color']
            puntos_solo_linea = puntos_carga[puntos_carga['CODIGO'] == linea]
            grupo_linea = folium.FeatureGroup(name=linea)
            lista_coordenadas = []
            for index,row in puntos_solo_linea.iterrows():
                coordenada = (row['LATITUD'],row['LONGITUD'])
                lista_coordenadas.append(coordenada)
                folium.CircleMarker(location = coordenada, radius=5 ,popup=None, weight=1,color=color,fill_color=color).add_to(grupo_linea)
            folium.PolyLine(lista_coordenadas,color=color,weight=3,opacity=0.8).add_to(grupo_linea)
            grupo_linea.add_to(mapa_general)
    
        LayerControl().add_to(mapa_general)
        mapa_general.fit_bounds(mapa_general.get_bounds())
        mapa_general.save( 'Mapa_Lineas.html')