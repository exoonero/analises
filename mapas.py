import geopandas as gpd
import matplotlib.pyplot as plt
import pathlib
import enrich_data
import pandas as pd

PATH = (".")

map_al = gpd.read_file('./dados/AL_Municipios_2022/AL_Municipios_2022.shp')
map_al = map_al.rename(columns ={'CD_MUN': 'cod_mun'})
#print(map_al.head(5))

df = enrich_data.get_data(".")
new_df_2021 = df[df['ano'] == 2021]
#print(new_df_2021.head(5))

#### CHECAR SE todos os municípios tem uma atribuição. - Mapa com furos..

### Merge enrich_data no shapefile
map_enrich = pd.merge(map_al, new_df_2021, on='cod_mun')
print(map_enrich.dtypes)

fig, ax = plt.subplots(figsize=(10, 6))
map_enrich.plot(column='pop_estim', cmap='viridis', linewidth=0.8, ax=ax, edgecolor='0.8', legend = True)

sizes = map_enrich['num_nomeacoes']
map_enrich.geometry.centroid.plot(ax=ax, marker='o', color='red', markersize=sizes, alpha=0.7)

ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
plt.show()