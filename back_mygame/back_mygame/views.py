from django.http.response import HttpResponse

#functions
def home_view(request):
    return HttpResponse("Home Page")


pages = {
    'forgot':'Forgot Page',
    'index':'Index Page',
    'register':'Register Page',
}

def pages_view(request,page):
    return HttpResponse(pages[page])

def add_view(request, num1, num2):
    # domain.com/num1/num2 --> num1+num2
    add_result = num1 + num2
    result= f"{num1}+{num2} = {add_result}"
    return HttpResponse(str(result))