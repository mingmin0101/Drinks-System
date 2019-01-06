from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from drink.models import Customer,Ingredient,Order, Order_has_product, Product   
import datetime


def main_page(request):

    return render_to_response('main_page.html')

def add_member(request):
    if ('customer_name' in request.GET and request.GET['customer_name']) and ('phone' in request.GET and request.GET['phone']) and ('gender' in request.GET and request.GET['gender']) :
        name = request.GET['customer_name']
        phone = request.GET['phone']
        gender = request.GET['gender']
        Customer.objects.create(name=name, customer_phone=phone, gender=gender, points=0)
    return render_to_response('add_member.html',locals())

def order(request):
    #order_has_product_set = Order_has_product.objects.get(order=Order.objects.get(id=1))
    if('convert' in request.GET and request.GET['convert']
        and 'drink' in request.GET
        and 'size' in request.GET
        and 'sugar' in request.GET
        and 'ice' in request.GET
        and 'num_of_drink' in request.GET):
        drink = request.GET['drink']
        size = request.GET['size']
        sugar = request.GET['sugar']
        ice = request.GET['ice']
        order_num = request.GET['num_of_drink']



    if('createOrder' in request.GET and request.GET['createOrder']
        and 'drink' in request.GET
        and 'size' in request.GET
        and 'sugar' in request.GET
        and 'ice' in request.GET
        and 'num_of_drink' in request.GET):
        noMember = Customer.objects.get(name='noMember')
        orderCreate_date = datetime.datetime.now()
        orderCreate = Order(date=orderCreate_date , total_price=0, customer=noMember)
        orderCreate.save()
        orderid = Order.objects.get(date=orderCreate_date).id
        ordernum = {'num':orderid }

        size = request.GET['size']
        sugar = request.GET['sugar']
        ice = request.GET['ice']
        order_num = request.GET['num_of_drink']
        order = Order.objects.get(id=orderid)
        product = Product.objects.get(product_name=request.GET['drink'])
            
        order_has_product_set = Order_has_product.objects.get(order=Order.objects.get(id=orderid))
        Order_has_product.objects.create(cup_size=size, ice_level=ice, sugar_level=sugar, product=product, order=order)
    

    return render_to_response('order.html', locals())


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

