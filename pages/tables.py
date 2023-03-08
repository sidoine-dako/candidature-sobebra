# Libraries importation
import streamlit as st
import pandas as pd
import scripts

# Set up the page
st.set_page_config(page_title="Tableaux")

# Page content
st.title("Projet de candidature | Data analyst SOBEBRA")
st.markdown("*Proposé par Sidoine Aude Sèdami DAKO*")

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
with sdBar.expander("Communes"):
    commChoice = st.multiselect("Commune",commLst,default=commLst,label_visibility="hidden")
## Types
typeLst = sorted(df["Type"].unique())
with sdBar.expander("Type"):
    typeChoice = st.multiselect("Type",typeLst,default=typeLst,label_visibility="hidden")



# Dropdown list
st.markdown("""
    # Description
    Cette feuille vous donne un aperçu des performances globales de la SOBEBRA suivant les segments choisis
    dans 
""")
st.write(tempComm)