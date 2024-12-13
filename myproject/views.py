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


def get_min(employees):
    # Initialize the minimum employee and score
    minimum = None
    min_score = float('inf')  # Start with a very high value for the score

    # Iterate through all employees
    for emp in employees:
        langs = emp["KnownLanguages"]
        for lang in langs:
            # Check if the language is "Java"
            if lang["LanguageName"] == "Java":
                # If the current score is lower than min_score, update minimum and min_score
                if lang["ScoreOutof100"] < min_score:
                    minimum = emp
                    min_score = lang["ScoreOutof100"]

    return minimum


def sort_acs(employees):
    result = []
    while len(employees) != 0:
        minimum = get_min(employees)
        result.append(minimum)
        employees.remove(minimum)
    return result

@csrf_exempt
def retrieve_employees(request):
    data = read_json()
    results = []
    for emp in data:
        langs = emp.get("KnownLanguages")
        for lang in langs:
            if lang.get("LanguageName") == "Java" and lang.get("ScoreOutof100") > 50:
                results.append(emp)

    x = sort_acs(results)
    return JsonResponse({"results": x})

@csrf_exempt
def delete_employee(request):
    if request.method == "POST":
        employee_to_delete = json.loads(request.body)
        employee_id = employee_to_delete.get("EmployeeID")

        if not employee_id:
            return JsonResponse({"error": "EmployeeID is required"}, status=400)

        data = read_json()
        employee_found = False

        for emp in data:
            if emp.get("EmployeeID") == employee_id:
                data.remove(emp)
                employee_found = True
                break

        if not employee_found:
            return JsonResponse({"error": "Employee not found"}, status=400)

        write_json(data)
        return JsonResponse({"message": "Employee deleted successfully!"})

    return JsonResponse({"error": "Only POST requests allowed"}, status=400)

@csrf_exempt
def update_employee(request):
    if request.method == "POST":
        employee_to_update = json.loads(request.body)
        employee_id = employee_to_update.get("EmployeeID")
        employee_designation = employee_to_update.get("Designation")

        if not employee_id:
            return JsonResponse({"error": "EmployeeID is required"}, status=400)
        if not employee_designation:
            return JsonResponse({"error": "Employee Designation is required"}, status=400)

        data = read_json()
        employee_found = False
        for emp in data:
             if emp.get("EmployeeID") == employee_id:
                 emp["Designation"] = employee_designation
                 employee_found = True
                 break
        if not employee_found:
            return JsonResponse({"error": "Employee not found"}, status=400)

        write_json(data)
        return JsonResponse({"message": f"Employee {employee_id} updated successfully!"})

    return JsonResponse({"error": "Only POST requests allowed"}, status=400)



