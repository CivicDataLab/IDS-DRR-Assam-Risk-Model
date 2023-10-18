import os
import pandas as pd
import geopandas as gpd
from rasterio.crs import CRS
from geopandas import GeoDataFrame
from shapely.geometry import Point
import time


CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))

DATA_FOLDER = os.path.abspath(CURRENT_FOLDER + '/data')


ASSAM_REVENUE_CIRCLE_FILE = os.getcwd() + '/Maps/Assam_Revenue_Circles/assam_revenue_circle_nov2022.geojson'

def main():
    mission_antyodaya_df = pd.read_excel(
        DATA_FOLDER + '/MissionAntyodaya2020_Assam.xlsx'
    )

    mission_antyodaya_geometry = [
        Point(xy) for xy in zip(
            mission_antyodaya_df.village_longitude,
            mission_antyodaya_df.village_latitude
        )
    ]

    gdf_points = GeoDataFrame(mission_antyodaya_df, geometry=mission_antyodaya_geometry)
    gdf_polygons = GeoDataFrame.from_file(ASSAM_REVENUE_CIRCLE_FILE)
    
    sindex = gdf_polygons.sindex
    point_in_polygon = []

    for i, point in gdf_points.iterrows():
        possible_matches_index = list(sindex.intersection(point.geometry.bounds))
        possible_matches = gdf_polygons.iloc[possible_matches_index]
        precise_matches = possible_matches[possible_matches.contains(point.geometry)]

        del(point['geometry'])
        if not precise_matches.empty:
            point['revenue_circle'] = precise_matches.revenue_cr.iloc[0]
        else:
            point['revenue_circle'] = '-'
        point_in_polygon.append(point)

    pd.DataFrame(point_in_polygon).to_excel(
        DATA_FOLDER + '/antyodaya_village_dataset_with_revenue_circle.xlsx'
    )

if __name__ == "__main__":
    main()