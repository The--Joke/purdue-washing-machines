from html.parser import HTMLParser
import requests
from pprint import pprint
import time
import datetime
import csv

mainurl = "http://wpvitassuds01.itap.purdue.edu/washalertweb/washalertweb.aspx?location="
dat = []

#yikes
locations = [["Cary Quad East Laundry","000f2375-7317-4a89-b836-4140dcd49b7c"],
             ["Cary Quad West Laundry","f9db4842-8fae-47d6-8660-645d358ef739"],
             ["Earthart Laundry Room","a0728ede-60be-4155-8ca9-dcde37ad431d"],
             ["Harrison Laundry Room","525ba5bf-7e58-4359-b78f-e8bfb34416cc"],
             ["Hawkins Laundry Room","1733b280-3ea8-4259-be35-d03b6b6d606a"],
             ["Hillenbrand Laundry Room","75896de0-7b2e-4270-bee0-4aefc49b1bd2"],
             ["McCutcheon Laundry Room","27b0544c-8fba-401b-b133-6307cd1fb851"],
             ["Meredith NW Laundry Room","697af07e-a32e-445a-b6ad-4f381458e7b4"],
             ["Meredith SE Laundry Room","3a05822f-c67a-49e9-8105-8255014d491f"],
             ["Own Laundry Room","706682c2-e8f8-4503-8d36-1283cc9bda1e"],
             ["Shreve Laundry Room","f681e273-d865-4274-bf4a-ba9dea2229ce"],
             ["Tarkington Laundry Room","06784d8c-9c16-4d05-9548-0f82dfdcc842"],
             ["Third St. Suites Laundry Room","96ed9941-352d-478f-88c3-1a0320066464"],
             ["Wiley laundry Room","c29eba8b-63d1-4090-bd32-ea85c67f483c"],
             ["Windsor - Duhme Laundry Room","b98170b6-c561-4ea5-8b2d-28ebf4f7cdda"],
             ["Windsor - Warren Laundry Room","da8165d6-7ff9-4311-80c7-2bc3e2da5e5e"]]


class DataScraper(HTMLParser):
    def __init__(self,name):
        self.hallname = name
        self.data = {"Available":0,
            "Ready to start":0,
            "End of cycle":0,
            "In use":0,
            "Payment in progress":0,
            "Almost done":0,
            "Not online":0,
            "Out of order":0}
        self.pull = False

        super().__init__()

    def handle_starttag(self,tag,attrs):
        if tag == "td" and ("class","status") in attrs:
            self.pull = True

    def handle_data(self,data):
        if self.pull:
            self.pull = False
            self.data[data]+=1

def appendRow(row):
    # append row to .csv
    with open("data.csv","a",newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)

def pull():
    global dat
    n=[]

    t = datetime.datetime.now()
    n.append("{0}-{1}-{2} {3}:{4}".format(t.year,t.month,t.day,t.hour,t.minute))

    for i in locations:
        scraper = DataScraper(i[0])

        r = requests.get(mainurl+i[1]);
        scraper.feed(r.text)

        n.append(scraper.data["Available"])

    try:
        # try to empty buffer.
        if dat:
            for i in dat:
                appendRow(i)

            dat = []

        appendRow(n)
    except:
        # add file to buffer when spreadsheet is open so it is written on the next go
        print("File was open when tried to write. Adding line to buffer.")
        dat.append(n)

    print("Hillenbrand currently has", n[6], "washing machines available.")

if __name__ == "__main__":
    while True:
        pull()
        for i in range(3):
            print("Next pull in %d minutes"%((5*3)-(5*i)))
            time.sleep(60*5)
