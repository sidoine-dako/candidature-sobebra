class DataSelector:
    
    def __init__(self,df):
        self.df = df

    def extractDepartement(self,lst):
        """Fonction permettant d'extraire les départements"""
        df = self.df
        df = df.loc[df.loc[:,'Département'].isin(lst)]
        self.df = df
        return self.df
    
    def extractCommune(self,lst):
        """Fonction permettant d'extraire les communes"""
        df = self.df
        df = df.loc[df.loc[:,'Commune'].isin(lst)]
        self.df = df
        return self.df

    def extractType(self,lst):
        """Fonction permettant de d'extraire les lignes avec le(s) type(s) sélectionné(s)"""
        df = self.df
        df = df.loc[df.loc[:,"Type"].isin(lst)]
        self.df = df
        return self.df