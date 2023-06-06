import requests
import csv
import os.path
from time import sleep

def GetData():
    response = requests.get(
        url='https://api.energidataservice.dk/dataset/ElectricityProdex5MinRealtime?offset=0&start=2020-01-01T00:00&sort=Minutes5UTC%20DESC&timezone=dk'
    )
    result = response.json()
    records = result.get('records', [])
    return records
                                           
def storeData(filename, dictList):
    """
    Store a list of dicts as a CSV file
    filename: Name of the file to store data in 
    """
    file_exists = os.path.exists(filename)

    with open(filename, 'w', newline='') as f:  
        writer = csv.DictWriter(f, fieldnames=dictList[0].keys()) 
        writer.writeheader()
        writer.writerows(dictList)

    if file_exists:
        print(f"File '{filename}' already exists and has been overwritten.")
    else:
        print(f"New file '{filename}' has been created.")


def main():
    data = GetData()
    storeData('Data/GetDataFrom2020ToNow.csv', data)

if __name__ == "__main__":
    main()
