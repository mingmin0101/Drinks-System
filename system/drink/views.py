from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from drink.models import Customer


def add_member(request):
    if ('customer_name' in request.GET and request.GET['customer_name']) and ('phone' in request.GET and request.GET['phone']) and ('gender' in request.GET and request.GET['gender']) :
        name = request.GET['customer_name']
        phone = request.GET['phone']
        gender = request.GET['gender']
        Customer.objects.create(name=name, customer_phone=phone, gender=gender, points=0)
    return render_to_response('add_member.html',locals())



def order(request):
    




    return HttpResponse('成功撰寫視圖函式')