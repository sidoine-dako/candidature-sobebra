import folium

def markersMap(df,map,color):
    for i in range(0,len(df)):
        html=f"""
            <h2> {df.iloc[i]['Nom']}</h2>
            <h4> RCCM: </h4>
            {df.iloc[i]['RCCM']}
            <h4> Type: </h4>
            {df.iloc[i]['Type']}
            <h4> Bouteilles total: </h4>
            {df.iloc[i]['Total']}
            <h4> Bouteilles d'eau: </h4>
            {df.iloc[i]['#Eau']}
            <h4> Bouteilles de boisson gazeuse: </h4>
            {df.iloc[i]['#Boisson gazeuse']}
            <h4> Bouteilles de bière: </h4>
            {df.iloc[i]['#Biere']}
            <h4> Bouteilles de panaché: </h4>
            {df.iloc[i]['#Panache']}
            """
        iframe = folium.IFrame(html=html, width=230, height=230)
        popup = folium.Popup(iframe, max_width=2650)
        folium.CircleMarker(
            location=[df.iloc[i]['Latitude'],df.iloc[i]['Longitude']],popup=popup,
            #fill_color="#FFCA03",
            color=color, opacity=.5, fill_opacity=.5, fill=True
        ).add_to(map)