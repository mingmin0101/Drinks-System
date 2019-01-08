from django.shortcuts import render, render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from drink.models import Customer,Ingredient,Order, Order_has_product, Product,ROP_Parameters,S0_Parameters
from django.template.defaulttags import register
from scipy import stats
import datetime
import json

DEFAULT_LT=4
DEFAULT_D=2
DEFAULT_SIGMA=0.1
DEFAULT_ACCEPTED_RISK=1.5

def main_page(request):

    return render_to_response('main_page.html')

def management(request):

    return render_to_response('management.html')

def add_member(request):
    if ('customer_name' in request.GET and request.GET['customer_name']) and ('phone' in request.GET and request.GET['phone']) and ('gender' in request.GET and request.GET['gender']) :
        name = request.GET['customer_name']
        phone = request.GET['phone']
        gender = request.GET['gender']
        memberAdded_date = datetime.datetime.now()
        lastOrder_date = datetime.datetime.now()
        Customer.objects.create(name=name, customer_phone=phone, gender=gender, points=0, create_time=memberAdded_date, latest_order_time=lastOrder_date)
        
        custom = Customer.objects.get(customer_phone=request.GET['phone'])
        custo_name = custom.name
        custo_phone = custom.customer_phone
        custo_gender = custom.gender
        custo_point = custom.points
    
    if('customer_phone' in request.GET and request.GET['customer_phone']):
        
        custo = Customer.objects.filter(customer_phone=request.GET['customer_phone'])
        if custo.exists():
            custom = Customer.objects.get(customer_phone=request.GET['customer_phone'])
            custo_name = custom.name
            custo_phone = custom.customer_phone
            custo_gender = custom.gender
            custo_point = custom.points
        else:
            custo_name = "noMember"
            custo_phone = "noMember"
            custo_gender = "noMember"
            custo_point = "0"

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

        # 如果有會員，更新資料
        orderCusto = request.GET['custoData']
        thisOrder = Order.objects.filter(date=orderCreate_date)
        custo = Customer.objects.filter(customer_phone=request.GET['custoData'])
        if custo.exists():
            thisOrder.update(customer = Customer.objects.get(customer_phone=orderCusto))
            custo.update(latest_order_time=orderCreate_date)
        
        # 新增這筆Order資料裡面的所有Order_has_product資料
        orderArray = request.GET['genOrder']
        orderArray1 = json.loads(orderArray)
        sumDollar = 0
        for orderItem in orderArray1:
            drink = orderItem.get('drink')
            sugar = orderItem.get('sugar')
            ice = orderItem.get('ice')
            size = orderItem.get('cupsize')
            order_num = orderItem.get('amount')
            order = Order.objects.get(id=orderid)
            product = Product.objects.get(product_name=drink)
            Order_has_product.objects.create(cup_size=size, ice_level=ice, sugar_level=sugar, amount=order_num, product=product, order=order)
            sumDollar += product.price * int(order_num)

        thisOrder.update(total_price=sumDollar)
    
    return render_to_response('order.html', locals())


def customer_info(request):
    return render_to_response('customer_info.html')
    

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def list_ingredient(request):
        i_list=list(Ingredient.objects.all().filter(is_processed=False))
        processed_i_list=list(Ingredient.objects.all().filter(is_processed=True))
        i_para_dict=geti_level_dict()
        pi_para_dict=getp_i_level_dict()

        for i in i_list:
            i_order_amount_str=i.ingredient_name+"_orderamount"
            if i.ingredient_name+"_orderamount" in request.GET:
                order_val=int(request.GET[i.ingredient_name+"_orderamount"])
                if order_val > 0:
                    i.amount = i.amount + order_val
                    i.save()
        
        for i in processed_i_list:
            i_process_amount_str=i.ingredient_name+"_processamount"
            if i.ingredient_name+"_processamount" in request.GET:
                process_val=int(request.GET[i.ingredient_name+"_processamount"])
                if process_val > 0:
                    i.amount = i.amount + process_val
                    i.save()

        return render(request,'manager_check_i.html',locals())

def getROP(LT,d,sigma,accepted_risk):
    #再訂購點訂購法
    ROP=d * LT + stats.norm.ppf((100-accepted_risk)/100)*sigma*LT**0.5
    return ROP

def getS0(d,sigma,accepted_risk):
    #單期訂購法
    S0=d + stats.norm.ppf((100-accepted_risk)/100)*sigma
    return S0

def level_setup(request):
    i_para_list_ROP=list(ROP_Parameters.objects.all())
    i_para_list_S0=list(S0_Parameters.objects.all())

    #再訂購點訂購法
    for i in i_para_list_ROP:
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
            i.ROP=getROP(LT,d,sigma,accepted_risk)
            i.save()

    for i in i_para_list_S0:
        d_str=str(i.ingredient_name)+"_d"
        sigma_str=str(i.ingredient_name)+"_sigma"
        accepted_risk_str=str(i.ingredient_name)+"_accepted_risk"

        if(d_str in request.GET and sigma_str in request.GET and accepted_risk_str in request.GET):
            d  = float(request.GET[d_str])
            sigma=float(request.GET[sigma_str])
            accepted_risk=float(request.GET[accepted_risk_str])

            i.d=d
            i.sigma=sigma
            i.accepted_risk=accepted_risk
            i.S0=getS0(d,sigma,accepted_risk)
            i.save()

    return render(request,'level_setup.html',locals())

def getp_i_level_dict():
    p_i_dict={}
    p_i_dict['bubble_p']=20
    p_i_dict['green_tea_p']=20
    p_i_dict['red_tea_p']=20

    return p_i_dict

def geti_level_dict():
    i_para_dict={}
    i_para_list_ROP=list(ROP_Parameters.objects.all())
    for i in i_para_list_ROP:
        i_para_dict[i.ingredient_name]=i.ROP

    i_para_list_S0=list(S0_Parameters.objects.all())
    for i in i_para_list_S0:
        i_para_dict[i.ingredient_name]=i.S0
    return i_para_dict



def predict_ingredient(request):
    time_pa_list=[[9,"紅茶",2],[9,"綠茶",1],[10,"奶茶",2],[10,"綠茶",2,[11,"奶茶",3]]]
    pa_temp_dict={"紅茶":0,"綠茶":0,"奶茶":0}
    day_pa_list=[]

    day_temp=time_pa_list[0][0]
    count=0
    for time_pa in time_pa_list:
        if time_pa[0] == day_temp:
            amount = time_pa[2]
            pa_temp_dict[time_pa[1]] += amount
        else:
            day_pa_list.append([day_temp,pa_temp_dict])
            day_temp=time_pa[0]
            for k,v in pa_temp_dict:
                v=0
            
            
    return render(request,"predict_ingredient.html",locals())

"""
        count+=1

        if count == len(time_pa_list):
            day_temp=time_pa[0]
            for k,v in pa_temp_dict:
                v=0
            day_pa_list.append([day_temp,pa_temp_dict])
"""
        
            



