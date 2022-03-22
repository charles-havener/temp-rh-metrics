from plots import *
import pandas as pd
import os
import sys, getopt

def get_args(argv):
    area = ""
    start_date = "1/1/1900"
    end_date = "1/1/3000"
    if len(argv)==0:
        print(f"main.py -a <area> -s <start_date> -e <end_date>\nmain.py -h <for help>")
        sys.exit(2)
    try:
        opts, args = getopt.getopt(argv, "ha:s:e:", ["area=", "start_date=", "end_date="])
    except getopt.GetoptError:
        print(f"main.py -a <area> -s <start_date> -e <end_date>\nmain.py -h <for help>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(f"main.py -a <area> -s <start_date> -e <end_date>\n" +
                  f"e\n" +
                  f"e")
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

    area, start_date, end_date = get_args(argv)
    print(f"Creating charts for {area} for dates in range [{start_date} - {end_date}]")



def _main():
    """Generates a series of charts and graphs to represent temperature and humidity data
    """

    FILE_LOCATION = r'C:\Users\havenc\Documents\Environmental\Temp-RH\data\master.xlsx'

    # Ensure that an images exists in the directory
    if not os.path.exists("images"):
        os.mkdir("images")

    # Read the excel file and get a list of all its sheets
    xl = pd.ExcelFile(FILE_LOCATION)
    sheets = xl.sheet_names
    print(sheets)

    # Dictionaries to map parameters to strings for file naming
    data_dict = {"TEMP F": "Temp", "RH %": "RH"}
    day_dict = {0: "All Data", 7: "7 Points", 20: "20 Points", 30: "30 Points", 60: "60 Points"}

    '''
    # Loop through each tab to create charts for each functional area
    for group in sheets:

        # Ensure that folder paths are created to store images in an organized fashion
        if not os.path.exists("images\\" + group):
            os.mkdir("images\\" + group)
        if not os.path.exists("images\\" + group + "\\Box"):
            os.mkdir("images\\" + group + "\\Box")
        if not os.path.exists("images\\" + group + "\\Control"):
            os.mkdir("images\\" + group + "\\Control")

        # Create a data frame from the sheet and create/adjust some columns
        print("\nGenerating Dataframe for " + group)
        df = xl.parse(sheet_name=group, index_col=None, header=0)
        df['DATE'] = pd.to_datetime(df['DATE'])
        df['Day'] = df['DATE'].dt.day_name()
        df['Hour'] = [x.hour for x in df['TIME']]
        df['Window'] = ["0-6" if x<6 else "6-18" if x<18 else "18-24" for x in df['Hour']]

        # Create charts from temp and rh columns of the sheet
        for data_name in ["TEMP F", "RH %"]:

            # Create box charts for the different time periods for multiple categories
            print(f"\tCreating {data_dict[data_name]} Box Charts for {group}")
            for category in ["Day", "Hour", "Window"]:
                for days in [0,7,30]:
                    output_name = f"Images/{group}/Box/{group}-{data_dict[data_name]}-{category}-{day_dict[days]}-BoxChart"
                    CreateBoxChart(df, output_name, data_name, category, days)

            # Create control/range charts for different categore/time window combos
            print(f"\tCreating {data_dict[data_name]} Control Charts for {group}")
            for categories,days in [(['DATE'],60), (['DATE', 'Window'],20)]:
                output_name = f"Images/{group}/Control/{group}-{data_dict[data_name]}-{', '.join(c for c in categories)}-{day_dict[days]}"
                CreateControlRangeCharts(df, output_name, data_name, categories, days)
    '''

if __name__ == "__main__":
    main(sys.argv[1:])