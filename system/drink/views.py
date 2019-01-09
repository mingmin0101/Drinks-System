from django.shortcuts import render, render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from drink.models import Customer,Ingredient,Order, Order_has_product, Product,ROP_Parameters,S0_Parameters
from django.template.defaulttags import register
from scipy import stats
from operator import itemgetter
from datetime import *
import json
import copy



def main_page(request):

    return render_to_response('main_page.html')

def management(request):

    return render_to_response('management.html')

def add_member(request):
    # 查詢會員
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
    
    # 使用點數
    if('usePoint' in request.GET and request.GET['usePoint'] and 'point_used_by_custo' in request.GET and request.GET['point_used_by_custo']):
        custom = Customer.objects.get(customer_phone=request.GET['point_used_by_custo'])
        custo_phone = custom.customer_phone
        custo_name = custom.name
        custo_point = custom.points - int(request.GET['usePoint'])
        
        Customer.objects.filter(customer_phone=custo_phone).update(points=custo_point)


    # 新增會員
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
        'genOrder' in request.GET and request.GET['genOrder'] and 'total' in request.GET and request.GET['total'] and request.GET['total']!='0'):
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
        sumCups = 0
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

            sumCups += int(order_num)

        # 總額裡面的價錢(包含點數使用扣掉的錢)
        # sumDollar = int(request.GET['total'])
        thisOrder.update(total_price=sumDollar)
        
        # 會員每買一杯就增加點數一點
        if custo.exists():
            if(request.GET['usePoint']!=""):
                pointDect = request.GET['usePoint']
                sumCups = sumCups + Customer.objects.get(customer_phone=orderCusto).points - int(pointDect)
                custo.update(points=sumCups)
            else:
                sumCups = sumCups + Customer.objects.get(customer_phone=orderCusto).points
                custo.update(points=sumCups)

    
    return render_to_response('order.html', locals())


def split(list, n):
    n = max(1, n)
    return (list[i:i+n] for i in xrange(0, len(list), n))
    

def customer_info(request):
    customer_list=list(Customer.objects.all().order_by('latest_order_time'))
    order_list=list(Order.objects.all())
    pre_customer_rfm_list1=get_customer_r1()
    pre_customer_rfm_list2=get_customer_r2()
    pre_customer_rfm_list3=get_customer_r3()
    pre_customer_rfm_list4=get_customer_r4()
    pre_customer_rfm_list5=get_customer_r5()
    customer_ait=get_customer_AIT()
    

    return render(request,'customer_info.html',locals())

def get_customer_rfm_list():
    customer_rfm_list=[]
    return customer_rfm_list
def get_customer_AIT():
    customer_list=list(Customer.objects.all())
    order_list=list(Order.objects.all())
    pre_customer_AIT_list=[]
    for customer in customer_list:
        order_list=list(Order.objects.all().filter(customer=customer))
        recency=customer.latest_order_time
        if str(recency)<'2019-01-01':
            frequency=0
            for order in order_list:
                frequency += 1
            AIT=1/frequency
            pre_customer_AIT_list.append([customer.name,AIT])
    return pre_customer_AIT_list
def sales_info(request):
    return render_to_response('sales_info.html')


def variable_setting(request):
    return render_to_response('variable_setting.html')

def inventory_prediction(request):
    return render_to_response('inventory_prediction.html')   
    

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
            i_process_amount_str=i.ingredient_name+"_processamount"

        for i in processed_i_list:
            if i.ingredient_name+"_processamount" in request.GET:
                process_val=int(request.GET[i.ingredient_name+"_processamount"])
                if process_val > 0:
                    if i.ingredient_name=="紅茶":
                        rtea=Ingredient.objects.get(ingredient_name="紅茶茶葉")
                        rtea.amount-=process_val
                        rtea.save()
                    elif i.ingredient_name=="綠茶":
                        gtea=Ingredient.objects.get(ingredient_name="綠茶茶葉")
                        gtea.amount-=process_val
                        gtea.save()
                    elif i.ingredient_name=="煮過的珍珠":
                        bubble=Ingredient.objects.get(ingredient_name="珍珠")
                        bubble.amount-=process_val
                        bubble.save()
                    i.amount = i.amount + process_val                    
                    i.save()
                    return HttpResponseRedirect('ingredient')
                    
        return render(request,'management.html',locals())

def getROP(LT,accepted_risk):
    #再訂購點訂購法
    d=50
    sigma=10
    ROP=d * LT + stats.norm.ppf((100-accepted_risk)/100)*sigma*LT**0.5
    return round(ROP,2)

def getS0(accepted_risk):
    #單期訂購法
    d=50
    sigma=10
    S0=d + stats.norm.ppf((100-accepted_risk)/100)*sigma
    return round(S0,2)


def level_setup(request):
    i_para_list_ROP=list(ROP_Parameters.objects.all())
    i_para_list_S0=list(S0_Parameters.objects.all())

    #再訂購點訂購法
    for i in i_para_list_ROP:
        LT_str=str(i.ingredient_name)+"_LT"
        accepted_risk_str=str(i.ingredient_name)+"_accepted_risk"

        if(LT_str in request.GET and accepted_risk_str in request.GET):
            LT = float(request.GET[LT_str])
            accepted_risk=float(request.GET[accepted_risk_str])

            i.LT=LT
            i.accepted_risk=accepted_risk
            i.ROP=getROP(LT,accepted_risk)
            i.save()

    for i in i_para_list_S0:

        accepted_risk_str=str(i.ingredient_name)+"_accepted_risk"
        #if(d_str in request.GET and sigma_str in request.GET and accepted_risk_str in request.GET):
        if(accepted_risk_str in request.GET):
            accepted_risk=float(request.GET[accepted_risk_str])

            i.accepted_risk=accepted_risk
            i.S0=getS0(accepted_risk)
            i.save()

    return render(request,'variable_setting.html',locals())

def getp_i_level_dict():
    p_i_dict={}
    p_i_dict['煮過的珍珠']=20
    p_i_dict['綠茶']=20
    p_i_dict['紅茶']=20

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
    day_ingredient_list=get_day_i_list
    
    return render(request,"predict_ingredient.html",locals())

def get_day_i_list():
    day_pa_list=get_day_pa_list()
    #returns [day,{ingredient_name:amount}]
    day_ingredient_list=[]

    i_amount_temp_dict={"紅茶":0,"綠茶":0,"珍珠":0}
    for day_pa in day_pa_list:
        red_tea = day_pa[1]['紅茶']
        green_tea = day_pa[1]['綠茶']
        bubble_milk_tea = day_pa[1]['珍珠奶茶']

        i_amount_temp_dict["紅茶"]=red_tea + bubble_milk_tea
        i_amount_temp_dict["綠茶"]=green_tea
        i_amount_temp_dict["珍珠"]=bubble_milk_tea

        i_amount_dict=copy.deepcopy(i_amount_temp_dict)
        day_ingredient_list.append([day_pa[0],i_amount_dict])
    
    return day_ingredient_list


def get_time_pa_list():
    o_h_p_list=list(Order_has_product.objects.all())
    #returns [order_time,{product_name:amount }] sorted by order_time
    time_pa_list=[]

    for o_h_p in o_h_p_list:
        order_time = Order.objects.get(id=o_h_p.order.id).date
        product_name = Product.objects.get(id=o_h_p.product.id).product_name
        amount = o_h_p.amount
        time_pa_list.append([order_time,product_name,amount])
    sort(time_pa_list)
    return HttpResponse(time_pa_list)
 

def get_day_pa_list():
    time_pa_list=[[9,"紅茶",2],[9,"綠茶",1],[9,"珍珠奶茶",2],[10,"綠茶",2],[10,"紅茶",1],[11,"珍珠奶茶",3],[12,"紅茶",1]]
    pa_temp_dict={"紅茶":0,"綠茶":0,"珍珠奶茶":0}

    #returns [day,{product_name:amount}]
    day_pa_list=[]

    day_temp=time_pa_list[0][0]
    count=0
    for time_pa in time_pa_list:
        if time_pa[0] == day_temp:
            amount = time_pa[2] + pa_temp_dict[time_pa[1]]
            pa_temp_dict[time_pa[1]] = amount
        else:
            pa_dict=copy.deepcopy(pa_temp_dict)
            day_pa_list.append([day_temp,pa_dict])
            day_temp=time_pa[0]
            for k in pa_temp_dict:
                pa_temp_dict[k]=0

            amount = time_pa[2] + pa_temp_dict[time_pa[1]]
            pa_temp_dict[time_pa[1]] = amount
        
        count+=1
        if count == len(time_pa_list):
            pa_dict=copy.deepcopy(pa_temp_dict)
            day_pa_list.append([day_temp,pa_dict])
            for k in pa_temp_dict:
                pa_temp_dict[k]=0

    return day_pa_list

def get_customer_r1():
    customer_list=list(Customer.objects.all())
    order_list=list(Order.objects.all())
    pre_customer_rfm_list=[]
    for customer in customer_list:
        if customer.name != 'noMember':
            order_list=list(Order.objects.all().filter(customer=customer))
            recency=customer.latest_order_time
            if str(recency)<= '2018-11-01':
                frequency=0
                money=0
                for order in order_list:
                    frequency += 1
                    money += order.total_price
                pre_customer_rfm_list.append([customer.name,recency,frequency,money])
    return sorted(pre_customer_rfm_list,key=itemgetter(1))
def get_customer_r2():
    customer_list=list(Customer.objects.all())
    order_list=list(Order.objects.all())
    pre_customer_rfm_list=[]
    for customer in customer_list:
        order_list=list(Order.objects.all().filter(customer=customer))
        recency=customer.latest_order_time
        if str(recency)<= '2018-12-01' and str(recency) >'2018-10-31':
            frequency=0
            money=0
            for order in order_list:
                frequency += 1
                money += order.total_price
            pre_customer_rfm_list.append([customer.name,recency,frequency,money])
    return sorted(pre_customer_rfm_list,key=itemgetter(1))
def get_customer_r3():
    customer_list=list(Customer.objects.all())
    order_list=list(Order.objects.all())
    pre_customer_rfm_list=[]
    for customer in customer_list:
        order_list=list(Order.objects.all().filter(customer=customer))
        recency=customer.latest_order_time
        if str(recency)>= '2018-12-01'and str(recency)<'2019-01-01':
            frequency=0
            money=0
            for order in order_list:
                frequency += 1
                money += order.total_price
            if frequency < 10:
                pre_customer_rfm_list.append([customer.name,recency,frequency,money])
    return sorted(pre_customer_rfm_list,key=itemgetter(1))
def get_customer_r4():
    customer_list=list(Customer.objects.all())
    order_list=list(Order.objects.all())
    pre_customer_rfm_list=[]
    for customer in customer_list:
        order_list=list(Order.objects.all().filter(customer=customer))
        recency=customer.latest_order_time
        if str(recency)>= '2018-12-01'and str(recency)<'2019-01-01':
            frequency=0
            money=0
            for order in order_list:
                frequency += 1
                money += order.total_price
            if frequency >= 10 and money<1000:
                pre_customer_rfm_list.append([customer.name,recency,frequency,money])
    return sorted(pre_customer_rfm_list,key=itemgetter(1))
def get_customer_r5():
    customer_list=list(Customer.objects.all())
    order_list=list(Order.objects.all())
    pre_customer_rfm_list=[]
    for customer in customer_list:
        order_list=list(Order.objects.all().filter(customer=customer))
        recency=customer.latest_order_time
        if str(recency)>= '2018-12-01'and str(recency)<'2019-01-01':
            frequency=0
            money=0
            for order in order_list:
                frequency += 1
                money += order.total_price
            if frequency >= 10 and money>=1000:
                pre_customer_rfm_list.append([customer.name,recency,frequency,money])
    return sorted(pre_customer_rfm_list,key=itemgetter(1))
            



