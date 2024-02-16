from django.shortcuts import render

# Create your views here.

def signup(request):
    # Your view logic here
  #  return HttpResponse('hello')
   return render(request, 'signup.html')
