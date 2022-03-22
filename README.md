
## Table of Contents

- [About the Project](#about-the-project)
- [Running the Script](#running-the-script)
- [Excel Setup](#minimum-excel-setup)
- [Examples](#example-output)
</br></br>

# About the project
Create box, control, and range charts for temperature and relative humidity readings in various functional areas for a specified time range.
</br>

# Running the Script

Creating the venv and install packages only required on initial setup/run.  
**virtual environment will still need to activated each time before running*

Create a virtual environment and activate it (optional):
```sh
$ python -m venv venv
$ venv/Scripts/activate
```
Install the required packages (required):
```sh
$ pip install -r requirements.txt
```
Run the main file:
```sh
$ python main.py -a <area> -s <start_date> -e <end_date>
```
</br>

# Run Parameters

* -h or --help
    * print parameters list out to console.
* -a or --area
    * specify a functional area. Will list valid inputs if provided area is not.
* -s or --start_date
    * start date of date range to use (inclusive range).
* -e or --end_date
    * end date of date range to use (inclusive range).

# Minimum Excel Setup

| DATE       | TIME    | TEMP F | RH % |
| :--        | :--     |  :--:  | :--: |
| 12/29/2020 | 6:00 AM |  71.1  |  39  |
| 12/29/2020 | 6:01 AM |  71.2  |  39  |
| 12/29/2020 | 6:02 AM |   71   |  40  |

</br>

>DATE (excel format: Date): Date of measurement  
>TIME (excel format: Time): Time of measurement  
>TEMP F (excel format: General): Recorded Temperature  
>RH % (excel format: General): Recorded Humidity  
> **column headers must be exact and are case sensitive*  
> **Tab names will be pulled and used to designate functional area, name them accordingly.*

</br>

# Example Output

### Box Chart
<img src="examples/Micro-E-RH-Day-All Data-BoxChart.png">
</br></br>

### Control Charts
<img src="examples/Micro-E-RH-DATE, Window-20 Points-ControlChart.png">
<img src="examples/Micro-E-RH-DATE, Window-20 Points-RangeChart.png">
