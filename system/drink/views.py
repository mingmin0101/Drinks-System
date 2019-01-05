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

def list_ingredient(request):
        pi_list=list(Ingredient.objects.all().filter(is_processed=False))
        i_list=list(Ingredient.objects.all().filter(is_processed=True))
        level=10
        return render(request,'manager_check_i.html',locals())
        
def level_setup(request):
    #單期訂購模型
    
    #再訂購點訂購法
    default_LT=4
    default_d=2
    default_sigma=0.1
    default_accepted_risk=1.5

    LT=default_LT
    d=default_d
    sigma=default_sigma
    accepted_risk=default_accepted_risk

    ROP=d * LT + (100-accepted_risk)/100*sigma*LT**0.5

    #數量折扣模型

    Q=10 #訂購數量
    H=5  #每單位持有成本
    D=1  #需求
    P=3  #單位價格

    holding_cost = (Q/2)*H
    order_cost = D/Q
    purchase_cost = P*D

    total_cost = holding_cost + order_cost + purchase_cost

    return render(request,'level_setup.html',locals())

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

