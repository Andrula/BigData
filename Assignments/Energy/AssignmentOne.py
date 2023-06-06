import aiohttp
import asyncio
import requests
from time import sleep
import csv
import os.path


async def getData():

    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.energidataservice.dk/dataset/ElectricityProdex5MinRealtime?limit=2') as response:
            result = await response.json()
            records = result.get('records', [])
            return records                    

oldDict = []

def storeData(filename, dictList):
    """
    Store a list of dicts as CSV file
    filename: Name of file to store data in 
    """
    global oldDict
    
    if not oldDict == dictList:
        fileExist = os.path.exists(filename)

        with open(filename, 'a', newline='') as f:  
            w = csv.DictWriter(f, dictList[0].keys()) 
            if not fileExist: w.writeheader()
            w.writerows(dictList)
        sleep(1)
    oldDict = dictList



async def main():
    try:
        while True:
            data = await getData()
            storeData("Data/EnergyDataPer5Min.csv", data)
            await asyncio.sleep(300)  # Sleep for 5 minutes before fetching data again
    except Exception as ex:
        print(f"An exception has occoured!: {ex}")

if __name__ == "__main__":
    asyncio.run(main())
