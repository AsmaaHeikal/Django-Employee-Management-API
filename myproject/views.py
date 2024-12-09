import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

FILE_PATH = os.path.join(os.path.dirname(__file__), '../employees.json')

def read_json():
    with open(FILE_PATH, 'r') as file:
        return json.load(file)

def write_json(data):
    with open(FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)

def get_all_employees(request):
    data = read_json()
    return JsonResponse({"employees": data})

@csrf_exempt
def add_employee(request):
    if request.method == "POST":
        new_employee = json.loads(request.body)
        data = read_json()
        data.append(new_employee)
        write_json(data)
        return JsonResponse({"message": "Employee added successfully!"})
    return JsonResponse({"error": "Only POST requests allowed"}, status=400)

def search_employee(request):
    search_term = request.GET.get("term")
    data = read_json()
    search_results = [
        emp for emp in data
        if str(emp.get("EmployeeID")) == search_term or emp.get("Designation") == search_term
    ]
    return JsonResponse({"results": search_results})
