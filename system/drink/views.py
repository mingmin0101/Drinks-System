from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from drink.models import Customer,Ingredient


def add_member(request):
    if ('customer_name' in request.GET and request.GET['customer_name']) and ('phone' in request.GET and request.GET['phone']) and ('gender' in request.GET and request.GET['gender']) :
        name = request.GET['customer_name']
        phone = request.GET['phone']
        gender = request.GET['gender']
        Customer.objects.create(name=name, customer_phone=phone, gender=gender, points=0)
    return render_to_response('add_member.html',locals())



def order(request):
    
    return HttpResponse('成功撰寫視圖函式')

def check_ingredientl(request):
    i_list=list(Ingredient.objects.all())

    low_lev_i=[]
    low_lev_processed_i=[]
    low_lev_unprocessed_i=[]

    for i in i_list:
        if i.amount<10:
            low_lev_i.append([i.ingredient_name,i.is_processed,i.amount])
            if i.is_processed:
                low_lev_processed_i.append([i.ingredient_name,i.is_processed,i.amount])
            else:
                low_lev_unprocessed_i.append([i.ingredient_name,i.is_processed,i.amount])

    return HttpResponse(low_lev_i)

def analyze_c_info(request):
    c_list=list(Customer.objects.all())
    return HttpResponse("test")

