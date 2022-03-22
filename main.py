from datetime import date
from plots import *
import pandas as pd
import os
import sys, getopt

def get_args(argv):
    """Gather command line arguments to return to main function
    """
    area = ""
    start_date = "1900-01-01"
    end_date = "3000-01-01"
    if len(argv)==0:
        print(f"main.py -a <area> -s <start_date> -e <end_date>\nmain.py -h <for help>")
        sys.exit(2)
    try:
        opts, args = getopt.getopt(argv, "ha:s:e:", ["help", "area=", "start_date=", "end_date="])
    except getopt.GetoptError:
        print(f"main.py -a <area> -s <start_date> -e <end_date>\nmain.py -h <for help>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print(f"\nmain.py -a <area> -s <start_date> -e <end_date>\n")
            sys.exit()
        elif opt in ("-a", "--area"):
            area = arg
        elif opt in ("-s", "--start_date"):
            start_date = arg
        elif opt in ("-e", "--end_date"):
            end_date = arg

    return area, start_date, end_date

def main(argv):
    """Generates a series of charts and graphs to present temperature and humidity data
    """

    FILE_LOCATION = r'C:\Users\havenc\Documents\Environmental\Temp-RH\data\master.xlsx'

    area, start_date, end_date = get_args(argv)

    #TODO ensure that start_date and end_date are valid dates

    # Read the excel file and get a list of all its sheets
    xl = pd.ExcelFile(FILE_LOCATION)
    sheets = xl.sheet_names

    # Ensure the area passed is valid
    if area not in sheets:
        print(f"invalid {area} input, must be a member of:\n" +
        f"{sheets}")

    # Dictionaries to map parameters to strings for file naming
    data_dict = {"TEMP F": "Temp", "RH %": "RH"}

    # Ensure that an images folder exists in the directory
    if not os.path.exists("images"):
        os.mkdir("images")

    # Ensure that folder paths are created to store images in an organized fashion
    area_range = area + "_" + start_date + "_" + end_date
    if not os.path.exists("images\\" + area_range):
        os.mkdir("images\\" + area_range)
    if not os.path.exists("images\\" + area_range + "\\Box"):
        os.mkdir("images\\" + area_range + "\\Box")
    if not os.path.exists("images\\" + area_range + "\\Control"):
        os.mkdir("images\\" + area_range + "\\Control")

    # Create a data frame from the sheet and create/adjust some columns
    print("\nGenerating Dataframe for " + area)
    df = xl.parse(sheet_name=area, index_col=None, header=0)
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['Day'] = df['DATE'].dt.day_name()
    df['Hour'] = [x.hour for x in df['TIME']]
    df['Window'] = ["0-6" if x<6 else "6-18" if x<18 else "18-24" for x in df['Hour']]

    # Filter df to only specified date range
    print("\tFiltering date range...")
    df = df[(df['DATE'] >= start_date) & (df['DATE'] <= end_date)]

    # number of rows in dataframe (number of datapoints)
    data_points = df.shape[0]

    # Create charts from temp and rh columns of the sheet
    for data_name in ["TEMP F", "RH %"]:

        # Create box charts for the different time periods for multiple categories
        print(f"\tCreating {data_dict[data_name]} Box Charts for {area}")
        for category in ["Day", "Hour", "Window"]:
            output_name = f"Images/{area_range}/Box/{area}_{data_dict[data_name]}_{category}_{start_date}_{end_date}-BoxChart"
            CreateBoxChart(df, output_name, data_name, category, area, start_date, end_date)

        # Create control/range charts for different categore/time window combos
        print(f"\tCreating {data_dict[data_name]} Control Charts for {area}")
        for categories,days in [(['DATE'],60), (['DATE', 'Window'],20)]:
            output_name = f"Images/{area_range}/Control/{area}_{data_dict[data_name]}_{', '.join(c for c in categories)}_{start_date}_{end_date}"
            CreateControlRangeCharts(df, output_name, data_name, categories, area, start_date, end_date)

if __name__ == "__main__":
    main(sys.argv[1:])