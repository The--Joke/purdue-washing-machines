import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime
import csv

DATE = 1
HILLENBRAND = 6
FILE = "data.csv"


def pull_data(x):
    dates = []
    data = []

    # pull data from csv
    with open(FILE,"r",newline="") as f:
        reader = csv.reader(f)
        iterRow = iter(reader)
        next(iterRow)

        for row in iterRow:
            dates.append(row[0])
            data.append(row[HILLENBRAND])

    dates = [datetime.datetime.strptime(x,"%Y-%m-%d %H:%M") for x in dates]

    return (dates,data)

def main():
    (fig,ax) = plt.subplots(1,1)
    p = pull_data(6)

    # Set axis to be hours:minutes
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))

    plt.xticks(rotation=90)

    ax.plot(p[0],p[1])

    fig.show()

if __name__ == "__main__":
    main()
