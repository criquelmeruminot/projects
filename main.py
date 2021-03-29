# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 23:16:03 2021

@author: Constanza Elizabeth
"""
from Modelo.Folium import generar_Mapa
from Modelo.Dashboard import generar_Dash
import pandas as pd


if __name__ == "__main__":
    ##Carga del Archivo
    puntos_carga =  pd.read_excel("Puntos_Carga_Venta_BIP.xlsx",sheet_name = "Abiertos")
    
    ##Generar DF
    #Líneas por Comuna
    df_lineas_comuna = puntos_carga.pivot_table(index = 'COMUNA',values = 'CODIGO',
                                                aggfunc = pd.Series.nunique).reset_index(drop = False)
    #Comunas por Línea
    df_comunas_linea = puntos_carga.pivot_table(index = 'CODIGO',values = 'COMUNA',
                                                aggfunc = pd.Series.nunique).reset_index(drop = False)

    #Puntos por Línea
    df_puntos_linea = puntos_carga.pivot_table(index = 'CODIGO',values = 'NOMBRE FANTASIA',
                                               aggfunc = "count").reset_index(drop = False)
    #Puntos por Comuna
    df_puntos_linea_comuna = puntos_carga.pivot_table(index = ['COMUNA','CODIGO'],values = 'NOMBRE FANTASIA',
                                                aggfunc = "count").reset_index(drop = False)

    #Puntos por Comuna
    df_pivot_table_puntos_comuna = puntos_carga.pivot_table(index = ['COMUNA'],values = 'NOMBRE FANTASIA',columns = 'CODIGO',
                                                aggfunc = "count").reset_index(drop = False)
    
    ##Creación Mapa HTML
    generar_maps = generar_Mapa()
    generar_maps.exportar_mapa(puntos_carga,df_comunas_linea)

    ##Creación Dashboard
    generar_dash = generar_Dash()
    generar_dash.exportar_dash(df_lineas_comuna,df_puntos_linea,df_puntos_linea_comuna,df_comunas_linea,df_pivot_table_puntos_comuna)





