import geopandas as gpd
import pandas as pd
import pgeocode as pg

# only including zip codes in key that will be placed on map
# this will be taken to be the greatest number of zip codes we could have
shapefile = '/home/jbbutler/chicagos-response-to-the-pandemic/map/Neighborhoods/geo_export_a131bb4a-42f9-4af9-bd33-aedec365203f.shp'
map_zips_gdf = gpd.read_file(shapefile)[["zip"]]


def make_zip_loc_key(map_zips_gdf):

    finder = pg.Nominatim('US')

    map_zips_gdf = gpd.read_file(shapefile)[["zip"]]
    lat_list = []
    lon_list = []
    for i, zip_code in map_zips_gdf.iterrows():
        loc_info = finder.query_postal_code(zip_code.iloc[0])
        lat_list.append(loc_info.latitude)
        lon_list.append(loc_info.longitude)

    map_zips_gdf['latitude'] = lat_list
    map_zips_gdf['longitude'] = lon_list
    map_zips_gdf.rename(columns = {'zip' : 'Zip_Code'}, inplace = True)
    map_zips_gdf.drop_duplicates(subset = ['Zip_Code'], inplace = True)
    map_zips_gdf.reset_index(drop = True, inplace = True)
    map_zips_gdf.to_csv('../csv_files/zip_location_key.csv', index = False)

make_zip_loc_key(map_zips_gdf)
