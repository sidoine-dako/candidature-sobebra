# Libraries importation
import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
from scripts.dataSelector import DataSelector
from scripts.dataCalculator import DataCalculator

# Set up the page
st.set_page_config(page_title="Cartes")

# Page content
st.title("Projet de candidature | Data analyst SOBEBRA")
st.markdown("*Proposé par Sidoine Aude Sèdami DAKO*")

## Data importation
df = pd.read_excel("./data/completeData.xlsx")
shpDep = gpd.read_file("./data/beninCommune.shp")
shpDep = shpDep.loc[:,["geometry","adm2_name"]]

# Sidebar
sdBar = st.sidebar

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