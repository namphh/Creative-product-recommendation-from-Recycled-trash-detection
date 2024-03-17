import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import csv

cred = credentials.Certificate("C:/Users/GF63/Downloads/gdcs-bb5d6-firebase-adminsdk-pzrwf-3feb968280.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def store_csv_data_to_firestore(csv_file_path, collection_name):
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            document_data = {}
            for key, value in row.items():
                # if key == 'Tool_ID' or key == 'Product_ID' :
                #     value = int(value)
                document_data[key] = value
            db.collection(collection_name).add(document_data)


csv_file_path = "Product.csv"
collection_name = "Product"

store_csv_data_to_firestore(csv_file_path, collection_name)
