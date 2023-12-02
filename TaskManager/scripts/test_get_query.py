import requests
url = "http://127.0.0.1:5000/get_data"
data = {
    "year": 2023,
    "function_update": "update_teachers_table",
    "data": {'name' : ['Titar Pidoras', 'Artemchuk Eblan']},
    "delete": False
}

response = requests.post(url, json=data)
print(response.status_code, response.text)