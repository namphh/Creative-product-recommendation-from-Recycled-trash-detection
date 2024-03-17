import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("C:/Users/GF63/Downloads/gdcs-bb5d6-firebase-adminsdk-pzrwf-3feb968280.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def export_firestore_data_to_json(collection_name, output_file):
    collection_ref = db.collection(collection_name)
    docs = collection_ref.get()
    
    data = []
    for doc in docs:
        doc_data = doc.to_dict()
        if '\ufeffProduct_ID' in doc_data:
            doc_data['Product_ID'] = doc_data.pop('\ufeffProduct_ID')
        data.append(doc_data)
        print(data)
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

collection_name = "Product"
output_file = "Product.json"

export_firestore_data_to_json(collection_name, output_file)
