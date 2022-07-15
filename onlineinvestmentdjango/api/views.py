from telnetlib import STATUS
from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import threading
import pymongo

# MONGO_URI = "mongodb+srv://musthafa:khSsPbdN8CKFjJA2@cluster0.dgrnriw.mongodb.net/?retryWrites=true&w=majority"
# client = pymongo.MongoClient("mongodb+srv://musthafa:khSsPbdN8CKFjJA2@cluster0.dgrnriw.mongodb.net/?retryWrites=true&w=majority")
# db=client['onlineinvestment']
# land_values = db['LandValues']
# print(land_values)


# Create your views here.
def initialise_mongodb():
    MONGO_URI = "mongodb+srv://musthafa:khSsPbdN8CKFjJA2@cluster0.dgrnriw.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(MONGO_URI, connect=False)
    db=client['onlineinvestment']
    land_values = db['LandValues']
    return db, land_values


def retrieve_land_values(request):
    db, land_values = initialise_mongodb()
    land_data = land_values.find()
    land_data_array = []
    for item in land_data:
        land_data_array.append(item)
    return HttpResponse(land_data_array)

def multithreading_calculate_land_values(request):
    # MONGO_URI = "mongodb+srv://musthafa:khSsPbdN8CKFjJA2@cluster0.dgrnriw.mongodb.net/?retryWrites=true&w=majority"
    # client = pymongo.MongoClient(MONGO_URI, connect=False)
    # db=client['onlineinvestment']
    # land_values = db['LandValues']
    t = threading.Thread(target=calculate_land_values)
    t.start()
    t.join()
    return HttpResponse(status=200)

def calculate_land_values():
    # MONGO_URI = "mongodb+srv://musthafa:khSsPbdN8CKFjJA2@cluster0.dgrnriw.mongodb.net/?retryWrites=true&w=majority"
    # client = pymongo.MongoClient(MONGO_URI, connect=False)
    # db=client['onlineinvestment']
    # land_values = db['LandValues']
    # land_values.drop()
    # land_values = db['LandValues']
    db, land_values = initialise_mongodb()
    land_values.drop()
    land_values = db['LandValues']
    list = []
    pages = 400
    for i in range(pages):
        current_page_number = i+1
        print(current_page_number)
        URL = "https://ikman.lk/en/ads/sri-lanka/land?sort=date&order=desc&buy_now=0&urgent=0&page=" + str(current_page_number)
        r = requests.get(URL)
        # print(r.content)
        # If this line causes an error, run 'pip install html5lib' or install html5lib
        soup = BeautifulSoup(r.content, 'html5lib')
        perch_value_divs = soup.find_all('div', class_= 'price--3SnqI color--t0tGX')
        perch_location_divs = soup.find_all('div', class_= 'description--2-ez3')

        # print(soup.prettify())
        # print(perch_location_divs)
        # print(len(perch_value_divs))
        max_value_per_perch = 50000000
        for i in range(len(perch_value_divs)):
            perch_value_string = perch_value_divs[i].span.text
            # print(perch_value_string)
            perch_location_string = perch_location_divs[i].text.split()[0].replace(',', '')
            perch_value = int(perch_value_string.split()[1].replace(',', ''))
            ad_cost_type = perch_value_string.split() ##could be the total cost or value per perch

            ##Reject total cost ads. Only accept adds which indicate the price per perch
            if (ad_cost_type[2] == "per" and ad_cost_type[3] == "perch" and perch_value < max_value_per_perch):
                ##check if current land name exist in list
                land_exist = False
                land_index = None
                for j in range(len(list)):
                    if perch_location_string == list[j][0]:
                        land_exist = True
                        land_index = j
                        break ##break for efficiency
            
                if land_exist:
                    list[land_index][1].append(perch_value)
                else: ##Create new tuple
                    new_land = (perch_location_string, [perch_value])
                    list.append(new_land)
            # print(perch_location_string, ": ", perch_value)
    

    average_land_values = []
    ##Calculate average of the land values
    for i in range(len(list)):
        average_land_price = sum(list[i][1])/len(list[i][1])
        # average_land_values.append((list[i][0], average_land_price))
        average_land_values.append((list[i][0], int(round(average_land_price, -2))))


    print(len(average_land_values))
    for item in average_land_values:
        print(item)
        land_data = {"landName": str(item[0]), "averageLandCost":item[1]}
        land_values.insert_one(land_data)



    