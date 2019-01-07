from django.shortcuts import render, render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from drink.models import Customer,Ingredient,Order, Order_has_product, Product,ROP_Parameters
from scipy import stats
import datetime
import json

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
    if('genrateOrder' in request.GET and request.GET['genrateOrder'] and
        'genOrder' in request.GET and request.GET['genOrder']):
        # 增加一筆Order資料
        # 顧客先暫時當作沒有會員
        noMember = Customer.objects.get(name='noMember')
        orderCreate_date = datetime.datetime.now()
        orderCreate = Order.objects.create(date=orderCreate_date , total_price=0, customer=noMember)
        orderid = Order.objects.get(date=orderCreate_date).id
        ordernum = {'num':orderid }

        # 新增這筆Order資料裡面的所有Order_has_product資料
        orderArray = request.GET['genOrder']
        orderArray1 = json.loads(orderArray)
        for orderItem in orderArray1:
            drink = orderItem.get('drink')
            sugar = orderItem.get('sugar')
            ice = orderItem.get('ice')
            size = orderItem.get('cupsize')
            order_num = orderItem.get('amount')
            order = Order.objects.get(id=orderid)
            product = Product.objects.get(product_name=drink)
            Order_has_product.objects.create(cup_size=size, ice_level=ice, sugar_level=sugar, amount=order_num, product=product, order=order)

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
        LT_str=str(i.ingredient_name)+"_LT"
        d_str=str(i.ingredient_name)+"_d"
        sigma_str=str(i.ingredient_name)+"_sigma"
        accepted_risk_str=str(i.ingredient_name)+"_accepted_risk"

        if(LT_str in request.GET and d_str in request.GET and sigma_str in request.GET and accepted_risk_str in request.GET):
            LT = float(request.GET[LT_str])
            d  = float(request.GET[d_str])
            sigma=float(request.GET[sigma_str])
            accepted_risk=float(request.GET[accepted_risk_str])

            i.LT=LT
            i.d=d
            i.sigma=sigma
            i.accepted_risk=accepted_risk
            i.save()

            ROP_list.append(getROP(LT,d,sigma,accepted_risk))

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

