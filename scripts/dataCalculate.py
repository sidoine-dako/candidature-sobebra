import pandas as pd
import numpy as np

class DataCalculator:

    def __init__(self,df):
        self.df = df

    def computeRatio(self,level=None):
        """Fonction pour calculer le ratio 1 dépôt pour nbre de PDVs"""
        df = self.df
        if level != None:
            levelLst = sorted(df[level].unique().tolist())
            ratio = list()
            for element in levelLst:
                df2 = df[df[level]==element]
                try:
                    ratio.append(np.round(len(df2[df2["Type"]=="PDV"])/len(df2[df2["Type"]=="Dépôt"]),2))
                except ZeroDivisionError:
                    ratio.append(0)
            dfRatio = pd.DataFrame({level:levelLst,'Ratio':ratio})
            return dfRatio
        else:
            ratio = np.round(len(df[df["Type"]=="PDV"])/len(df[df["Type"]=="Dépôt"]),2)
            return ratio
        
    def aggData(self,level:str):
        df = self.df
        return df.groupby(level).agg('sum')