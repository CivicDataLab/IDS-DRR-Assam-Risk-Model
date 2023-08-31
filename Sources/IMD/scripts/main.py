import imdlib as imd
import os

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))

DATA_FOLDER = os.path.abspath(CURRENT_FOLDER + '/../' + 'data')

TIFF_DATA_FOLDER = os.path.join(DATA_FOLDER, 'rain', 'tiff')

def download_data(year: int):
    """
    Downloads the data year wise data in the DATA_FOLDER
    The year wise data has datapoint for all days of all months
    """
    imd.get_data(
        var_type='rain',
        start_yr=year,
        end_yr=year,
        fn_format='yearwise',
        file_dir=DATA_FOLDER
    )

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

    # Convert and save data as tiff format in data folder
    os.makedirs(TIFF_DATA_FOLDER, exist_ok=True)

    data.to_geotiff(
        '{}.tif'.format(year),
        TIFF_DATA_FOLDER
    )

if __name__ == '__main__':
    # Takes year as an input from the cli
    # year = input('Please enter a year: ')

    # Year defined in the script
    year = 2019

    download_data(year)
    parse_and_format_data(year)