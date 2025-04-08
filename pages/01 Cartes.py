# Libraries importation
import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import folium
import leafmap.foliumap as leafmap
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from utils.dataSelect import DataSelector
from utils.dataCalculate import DataCalculator
from utils.modifyMap import markersMap

# Set up the page
st.set_page_config(page_title="Cartes")

# Page content
st.title("Projet de candidature | Data analyst SOBEBRA")
st.markdown("""*Proposé par Sidoine Aude Sèdami DAKO*\\
    **Important : Les données utilisées pour ce projet ont été générées aléatoirement donc fictives.**
""")
st.markdown("# Cartes")

## Data importation
df = pd.read_excel("./data/completeData.xlsx")
shpDep = gpd.read_file("./data/beninDepartment.shp")
shpDep = shpDep.loc[:,["geometry","adm1_name"]]
shpComm = gpd.read_file("./data/beninCommune.shp")
shpComm = shpComm.loc[:,["geometry","adm2_name"]]

# Sidebar
sdBar = st.sidebar
sdBar.title("Barre latérale")
sdBar.write("""Avec les éléments contenus dans cette barre, vous avez la possibilité de choisir
les segments sur lesquels vous focalisez. Assurez-vous de maintenir choisis quelques éléments pour avoir
des résultats.""")
depLst = sorted(df["Département"].unique()) # List of "Département"
## Départements
with sdBar.expander('Départements'):
    depChoice = st.multiselect("Département",depLst,default=depLst,label_visibility="hidden")
## Communes
tempComm = df.loc[df.loc[:,'Département'].isin(depChoice)]
commLst = sorted(tempComm["Commune"].unique())
del(tempComm)
with sdBar.expander("Communes"):
    commChoice = st.multiselect("Commune",commLst,default=commLst,label_visibility="hidden")
## Types
typeLst = sorted(df["Type"].unique())
with sdBar.expander("Type"):
    typeChoice = st.multiselect("Type",typeLst,default=typeLst,label_visibility="hidden")


# Dropdown list
with st.expander("Description",expanded=True):
        st.markdown("""
            # Description
            *NB: En cliquant sur chacun des titres, vous avez la possibilité d'agrandir les rubans et
            de découvrir les performances.*
            
            Cette page donne un aperçu des performances globales de la SOBEBRA suivant les segments choisis
            au niveau de la barre latérale.
            - Le ratio global indique le nombre de PDVs désservis en moyenne par un dépôt.
            Toutefois, sur la base d'une enquête, on pourrait savoir avec exactitude les PDVs désservis par
            chacun des dépôts et par conséquent déterminer avec exactitude le nombre moyen de PDVs 
            désservis par un dépôt en particulier.
        """)
dataSel = DataSelector(df)
dataSel.extractDepartement(depChoice)
dataSel.extractCommune(commChoice)
dataSel.extractType(typeChoice)
_, colGlobRat = st.columns([7,2])
dataCalc = DataCalculator(dataSel.df)
globRatio = dataCalc.computeRatio()
colGlobRat.metric("Ratio global",value=globRatio,help="Nombre de PDVs désservis par 1 dépôt en moyenne")

## Répartition des dépôts et PDVs
with st.expander("Répartition spatiale des dépôts et PDVs"):
     st.markdown("""La carte ci-dessous est interactive. En cliquant sur un point,
     vous avez la possibilité d'avoir les informations définies telles que le nom, le RCCM,
     le nombre de bouteilles d'eau, de boissons gazeuses, de bières, etc.\\
     En cliquant sur les points aggrégés, vou savez la possibilité de sélectionner chacun des points
     en individuel.
     Les dépôts sont colorés en bleus et les PDVs en rouge.
     """)

     dfDepot, dfPDV = dataSel.separateType()
     m1 = folium.Map(location=[9.223351, 2.262477],zoom_start=6.5)
     clusterDepot = MarkerCluster(name="Dépôts").add_to(m1)
     #fg = folium.FeatureGroup(name="Dépôts")
     markersMap(dfDepot,clusterDepot,"#1A8EFA")
     #m1.add_child(fg)
     clusterPDV = MarkerCluster(name="PDVs").add_to(m1)
     #fg2 = folium.FeatureGroup(name="PDVs")
     markersMap(dfPDV,clusterPDV,"#DB6A39")
     #m1.add_child(fg2)
     folium.map.LayerControl('topleft', collapsed= False).add_to(m1)
     m1.fit_bounds(m1.get_bounds())
     m1_folium = st_folium(m1,height=725)
     #st.write(dfDepot)

## Performances par département
with st.expander("Performances par département"):
    st.markdown("""La carte ci-dessous est interactive. En passant le curseur de la souris,
    vous avez la possibilité de voir les ratios dépôt pour PDV.""")
    st.markdown("**Ratio 1 Dépôt\:PDVs**")
    ratioDep = dataCalc.computeRatio("Département").sort_values(by="Ratio",ascending=False)
    # Create shapefile with ratio
    ratioDepShp = pd.merge(shpDep,ratioDep,how="right",left_on="adm1_name",right_on="Département")
    # initialize the map and store it in a m object
    m = folium.Map(location=[9.223351, 2.262477],zoom_start=6.5)
    #folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(m)

    myscale = (ratioDepShp['Ratio'].quantile((0,0.25,0.5,0.75,1))).tolist()
    folium.Choropleth(
        geo_data=ratioDepShp,
        name='Choropleth',
        data=ratioDepShp,
        columns=['Département','Ratio'],
        key_on="feature.properties.Département",
        fill_color='YlGnBu',
        threshold_scale=myscale,
        fill_opacity=.9,
        line_opacity=0.2,
        legend_name='Ratio Dépôt:PDVs',
        smooth_factor=0
    ).add_to(m)

    style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}
    NIL = folium.features.GeoJson(
        ratioDepShp,
        style_function=style_function, 
        control=False,
        highlight_function=highlight_function, 
        tooltip=folium.features.GeoJsonTooltip(
            fields=['Département','Ratio'],
            aliases=['Département: ','Nbre PDVs par dépôts: '],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
        )
    )
    m.add_child(NIL)
    #m.keep_in_front(NIL)
    folium.LayerControl().add_to(m)
    m.fit_bounds(m.get_bounds())
    st_data = st_folium(m,height=500)
