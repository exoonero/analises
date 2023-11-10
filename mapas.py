import geopandas as gpd
import matplotlib.pyplot as plt
import pathlib
import enrich_data

PATH = (".")

map_al = gpd.read_file('./dados/AL_Municipios_2022/AL_Municipios_2022.shp')
print(map_al.head())

df = enrich_data.get_data(".")
new_df_2021 = df[df['ano'] == 2021]

