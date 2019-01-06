from django.shortcuts import render, render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from drink.models import Customer,Ingredient,Order, Order_has_product, Product,ROP_Parameters
from scipy import stats
import datetime

DEFAULT_LT=4
DEFAULT_D=2
DEFAULT_SIGMA=0.1
DEFAULT_ACCEPTED_RISK=1.5

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
        return render(request,'manager_check_i.html',locals())

def getROP(LT,d,sigma,accepted_risk):
    #再訂購點訂購法
    ROP=d * LT + stats.norm.ppf((100-accepted_risk)/100)*sigma*LT**0.5
    return ROP

def level_setup(request):
    i_para_list=list(ROP_Parameters.objects.all())
    ROP_list=[]
    #再訂購點訂購法

    for i in i_para_list:
        ingredient_name=0
        green_tea_LT = 0
        green_tea_d = 0
        green_tea_sigma = 0
        green_tea_accepted_risk = 0

        if(green_tea_LT in request.GET and green_tea_d in request.GET and green_tea_sigma in request.GET and green_tea_accepted_risk in request.GET):
            LT = float(request.GET['LT'])
            d=float(request.GET['d'])
            sigma=float(request.GET['sigma'])
            accepted_risk=float(request.GET['a_risk'])

            i.LT=LT
            i.d=d
            i.sigma=sigma
            i.accepted_risk=accepted_risk
            i.save()

            ROP_list.append(getROP(LT,d,sigma,accepted_risk))
            return HttpResponse("FUck")

    #單期訂購模型
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

def analyze_c_info(request):
    c_list=list(Customer.objects.all())
    return HttpResponse("test")

