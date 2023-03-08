class DataSelector:
    
    def __init__(self,df):
        self.df = df

    def extractDepartement(self,lst):
        """Fonction permettant d'extraire les départements"""
        df = df.loc[df.loc[:,'Département'].isin(lst)]
        self.df = df
        return self.df
    
    def extractCommune(self,lst):
        """Fonction permettant d'extraire les communes"""
        df = df.loc[df.loc[:,'Commune'].isin(lst)]
        self.df = df
        return self.df