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

    # minimum = employees[0][KnownLanguages]
    # for emp in employees:
    #     langs = emp[5]
    #     for lang in langs:
    #         if lang.get("LanguageName") == "Java" and minimum.get("LanguageName") == "Java":
    #             if lang.get("ScoreOutof100") < minimum.get("ScoreOutof100"):
    #                 minimum = lang
    #
    # return minimum


def sort_acs(employees):
    result = []
    while len(employees) != 0:
        minimum = get_min(employees)
        result.append(minimum)
        employees.remove(minimum)
    return result


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
