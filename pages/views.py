from django.shortcuts import render, HttpResponse
def index(request):
    return render(request,'pages/index.html')

def aboutus(request):
    # name = "John"
    student = {1:"john", 2:"jane", 3:"blake", 4:"kristen"}
    results = {
        1 : {"name" :"john", "cgpa":[9.2,9.8,9.1,9.7]},
        2 : {"name" :"sara", "cgpa":[9.5,8.6,9.4,9.0]},
        3 : {"name" :"sam", "cgpa":[9.3,9.1,9.8,9.2]},
        4 : {"name" :"kristen", "cgpa":[9.9,9.0,9.1,9.6]},
        4 : {"name" :"niya", "cgpa":[9.9,9.0,9.1,9.6]},
    }
    context={
        "name":"Sam",
        "age":20,
        "num1":12,
        "num2":10,
        "nums":[1,2,3,4,5],
        "students" :student,
        "results":results
    }
    return render(request,"pages/about.html", context)

# always key should be the variba