import os
import calendar
import rasterio
import rasterstats
import pandas as pd
import imdlib as imd
import geopandas as gpd

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))

DATA_FOLDER = os.path.abspath(CURRENT_FOLDER + '/../' + 'data')

TIFF_DATA_FOLDER = os.path.join(DATA_FOLDER, 'rain', 'tiff')

ASSAM_REVENUE_CIRCLE_GDF = gpd.read_file(
    os.getcwd() + '/Maps/Assam_Revenue_Circles/assam_revenue_circle_nov2022.shp'
)

def download_data(year: int):
    """
    Download year wise data in the DATA_FOLDER
    The year wise data has datapoint for all days of all months
    """
    imd.get_data(
        var_type='rain',
        start_yr=year,
        end_yr=year,
        fn_format='yearwise',
        file_dir=DATA_FOLDER
    )

    return

def parse_and_format_data(year: int):
    """
    Parses the year wise data in the DATA_FOLDER and formats to required type
    """
    data = imd.open_data(
        var_type='rain',
        start_yr=year,
        end_yr=year,
        fn_format='yearwise',
        file_dir=DATA_FOLDER
    )

    dataset = data.get_xarray()

    # Remove NaN values
    dataset = dataset.where(dataset['rain'] != -999.)

    # Group the dataset by month
    dataset = dataset.groupby(
        'time.month'
    )

    # Make sure TIFF_DATA_FOLDER exists
    os.makedirs(TIFF_DATA_FOLDER, exist_ok=True)

    # For each month in the dataset, save the average rain in tif format
    for el in dataset:
        el[1]['rain'].mean('time').rio.to_raster(
            TIFF_DATA_FOLDER + '/{}-{}.tif'.format(
                year,
                calendar.month_abbr[el[1]['time.month'].to_dict()['data'][0]]
            )
        )

    # Save yearwise file as geotiff, this is used in getting crs
    data.to_geotiff(
        '{}.tif'.format(year),
        TIFF_DATA_FOLDER
    )

    return

def retrieve_assam_revenue_circle_data(year: int):
    """
    Retrives assam revenue circle data from the year wise .tif file
    """
    coordinate_reference_system_used = rasterio.open(
        os.path.join(TIFF_DATA_FOLDER, '{}.tif'.format(
            str(year)
        ))
    ).crs
    
    for month in range(1,13):
        raster = rasterio.open(
            os.path.join(TIFF_DATA_FOLDER, '{}-{}.tif'.format(
                str(year),
                calendar.month_abbr[month]
            ))
        )

        raster_array = raster.read(1)

        mean_dicts = rasterstats.zonal_stats(
            ASSAM_REVENUE_CIRCLE_GDF.to_crs(coordinate_reference_system_used),
            raster_array,
            affine=raster.transform,
            stats= ['count'],
            nodata=raster.nodata,
            geojson_out = True
        )

        dfs = []
        
        for rc in mean_dicts:
            dfs.append(pd.DataFrame([rc['properties']]))

        zonal_stats_df = pd.concat(dfs).reset_index(drop=True)

        print(zonal_stats_df)

    return


if __name__ == '__main__':
    
    # Takes year as an input from the cli
    # years = input('Please enter the years (comman separated): ').split(',')

    # Year defined in the script
    years = [2018]

    for year in years:
        year = int(year)

        # download_data(year)
        # parse_and_format_data(year)
        retrieve_assam_revenue_circle_data(year)
