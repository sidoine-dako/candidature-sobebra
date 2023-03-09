# Libraries importation
import streamlit as st
import pandas as pd
import numpy as np
from scripts.dataSelector import DataSelector
from scripts.dataCalculator import DataCalculator

# Set up the page
st.set_page_config(page_title="Tableaux")

# Page content
st.title("Projet de candidature | Data analyst SOBEBRA")
st.markdown("""*Proposé par Sidoine Aude Sèdami DAKO*\\
    *Date de début du projet: Lundi 06 Mars 2023*\\
    **Important : Les données utilisées pour ce projet ont été générées aléatoirement donc fictives.**
""")
st.markdown("# Tableaux")

## Data importation
df = pd.read_excel("./data/completeData.xlsx")

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
dataCalc = DataCalculator(dataSel.df)
_, colGlobRat = st.columns([7,2])
globRatio = dataCalc.computeRatio()
colGlobRat.metric("Ratio global",value=globRatio,help="Nombre de PDVs désservis par 1 dépôt en moyenne")

## Performances par département
with st.expander("Performances par département"):
    st.markdown("**Ratio 1 Dépôt\:PDVs**")
    st.write(dataCalc.computeRatio("Département").sort_values(by="Ratio",ascending=False))
    st.markdown("**Performances agrégées par département**")
    dfDep = dataCalc.aggData("Commune")
    dfDep.drop(columns=["Latitude","Longitude"],inplace=True)
    st.write(dfDep.sort_values(by="Total"))

## Performances par commune
with st.expander("Performances par commune"):
    st.markdown("**Ratio 1 Dépôt\:PDVs**")
    st.write(dataCalc.computeRatio("Commune").sort_values(by="Ratio",ascending=False))
    st.markdown("**Performances agrégées par commune**")
    dfComm = dataCalc.aggData("Commune")
    dfComm.drop(columns=["Latitude","Longitude"],inplace=True)
    st.write(dfComm.sort_values(by="Total"))

dfDepot, dfPDV = dataSel.separateType()

## Performances des dépôts
with st.expander("Performances des dépôts"):
     st.markdown("""
        Cette section présente dans un tableau les performances de chaque dépôt. En cliquant
        sur l'en-tête d'une colonne, celle-ci est ordonnée par ordre croissant ou décroissant.
     """)
     dfDepot.drop(columns=["Longitude","Latitude","Type"],inplace=True)
     st.write(dfDepot.sort_values(by="Total",ascending=False))

## Performances des PDVs
with st.expander("Performances des PDVs"):
     st.markdown("""
        Cette section présente dans un tableau les performances de chaque PDV. En cliquant
        sur l'en-tête d'une colonne, celle-ci est ordonnée par ordre croissant ou décroissant.
     """)
     dfPDV.drop(columns=["Longitude","Latitude","Type"],inplace=True)
     st.write(dfPDV.sort_values(by="Total",ascending=False))