from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import *
from .models import *


# @login_required(login_url='login')
def log(request):
    if request.method == 'POST':  # data sent by user
        form = UserForm(request.POST)
        us = User.objects.get(password=form['password'].value())
        ps = User.objects.get(username=form['username'].value())
        if form.is_valid() and us == ps:
            userr = User.objects.get(password=form['password'].value())
            if userr.role == 'WORKER':
                return user(request, userr.id)
            elif userr.role == 'ADMIN':  # or userr.role == 'GADMIN':
                return admin(request, userr.id)
            else:
                return gadmin(request, userr.id)
        else:
            form = UserForm()
            d = 'неверно имя пользователя или пароль'
            return render(request, 'login.html', {'car_form': form,
                                                  'd': d})
    else:  # display empty form
        form = UserForm()
        return render(request, 'login.html', {'car_form': form})


def user(request, id):
    id = id
    userr = User.objects.get(id=id)
    staaf = Staff.objects.get(user_id=id)
    filt = {'staff_id': staaf.user_id, 'condition': 'в работе', }
    ordd = Order.objects.all().filter(staff_id=staaf.user_id)
    ordd = ordd.filter(condition__in=['в работе', 'создан'])
    return render(request, "user.html", {'user': userr, 'staff': staaf, 'order': ordd, 'id': id})


def user_res(request, id):
    ordd = Order.objects.all().filter(staff_id=id)
    ordd = ordd.filter(condition__in=['в работе', 'создан'])
    Staff.objects.filter(user_id=id).update(condition=None, control='0')
    print(ordd)
    for od in ordd:
        if od.shipping == False:
            od.condition = 'доставлен'
            od.save(update_fields=["condition"])
            prod_vhod = int(od.quantity)
            prod_last = int(od.product.quantity)
            prod = prod_last + prod_vhod
            print(prod)
            Product.objects.filter(id=od.product_id).update(quantity=prod)
        else:
            od.condition = 'отправлен'
            od.save(update_fields=["condition"])
            prod_vihod = int(od.quantity)
            prod_last = int(od.product.quantity)
            prod = prod_last - prod_vihod
            print(prod)
            Product.objects.filter(id=od.product_id).update(quantity=prod)
    return user(request, id)


def admin(request, id):
    ad = User.objects.get(id=id)
    prodd = {}
    for i in range(1, 11):
        prod = Product.objects.all().filter(quantity=i)
        if prod:
            for p in prod:
                prodd[p.name] = i
    return render(request, 'admin.html', {'ad': ad, 'prod': prodd})


def gadmin(request, id):
    ad = User.objects.get(id=id)
    return render(request, 'gadmin.html', {'ad': ad})


def product_list(request):
    prod = Product.objects.all()
    return render(request, 'product_list.html', {'prod': prod, })


def roduct_list_gad(request):
    prod = Product.objects.all()
    return render(request, 'roduct_list_gad.html', {'prod': prod})


def product_update(request, id):
    prod = Product.objects.get(id=id)
    return render(request, 'product_update.html', {'prod': prod})


def update_prod(request, id):
    if request.method == 'POST':  # data sent by user
        name = request.POST.get('name_field')
        category = request.POST.get('category_field')
        text = request.POST.get('text_field')
        quantity = request.POST.get('quantity_field')
        Product.objects.filter(name=name).update(name=name, category=category, text=text, quantity=quantity)
    us = User.objects.get(role='GADMIN')
    return gadmin(request, us.id)


def delete_prod(request, id):
    Product.objects.get(id=id).delete()
    us = User.objects.get(role='GADMIN')
    return gadmin(request, us.id)


def product(request):
    if request.method == 'POST':  # data sent by user
        form = ProductForm(request.POST)
        print(form)
        if form.is_valid():
            obj = Product()
            obj.name = form['name'].value()
            obj.category = form.cleaned_data['category']
            obj.text = form.cleaned_data['text']
            obj.quantity = form.cleaned_data['quantity']
            obj.condractor_on_stock = form.cleaned_data['condractor_on_stock']
            obj.save()
            us = User.objects.get(role='GADMIN')
            return gadmin(request, us.id)
        else:
            form = ProductForm()
            post = Condractor_on_stock.objects.all()
            prod = Product.objects.order_by().values('category').distinct()
            print(prod)
            return render(request, 'product.html', {'car_form': form,
                                                    'p': post,
                                                    'prod': prod})
    else:  # display empty form
        form = ProductForm()
        post = Condractor_on_stock.objects.all()
        prod = Product.objects.order_by().values('category').distinct()
        return render(request, 'product.html', {'car_form': form,
                                                'p': post,
                                                'prod': prod})


def order_list(request):
    ordd = Order.objects.all()
    return render(request, 'order_list.html', {'order': ordd})


def order_list_gad(request):
    ordd = Order.objects.all()
    return render(request, 'order_list_gad.html', {'order': ordd})


def delete_order(request, id):
    Order.objects.get(id=id).delete()
    us = User.objects.get(role='GADMIN')
    return gadmin(request, us.id)


def order_staff(request, id):
    order = Order.objects.get(id=id)
    staf = Staff.objects.all().values()
    return render(request, 'order_staff.html', {'ord': order, 'staf': staf})


def order(request, id):
    if request.method == 'POST':  # data sent by user
        mes = request.POST.get('name_field')
        obj = Order.objects.get(id=id)
        obj.staff_id = mes
        obj.condition = 'в работе'
        obj.save(update_fields=["staff_id"])
        obj.save(update_fields=["condition"])
        if obj.shipping == False:
            Staff.objects.filter(user_id=mes).update(condition='приём товара', control='1')
        else:
            Staff.objects.filter(user_id=mes).update(condition='сбор заказа', control='1')
    us = User.objects.get(role='ADMIN')
    return admin(request, us.id)


def pastav_list(request):
    pastav = Condractor_on_stock.objects.all()
    prod = Product.objects.all().values()
    return render(request, 'partner_list.html', {'pas': pastav, 'prod': prod})


def pastav_list_gad(request):
    pastav = Condractor_on_stock.objects.all()
    prod = Product.objects.all().values()
    return render(request, 'pastav_list_gad.html', {'pas': pastav, 'prod': prod})


def pastav_update(request, id):
    prod = Condractor_on_stock.objects.get(id=id)
    return render(request, 'pastav_update.html', {'prod': prod})


def update_pastav(request, id):
    if request.method == 'POST':  # data sent by user
        company = request.POST.get('company_field')
        number = request.POST.get('number_field')
        email = request.POST.get('email_field')
        Condractor_on_stock.objects.filter(company=company).update(company=company, number=number, email=email)
    us = User.objects.get(role='GADMIN')
    return gadmin(request, us.id)


def delete_pastav(request, id):
    Condractor_on_stock.objects.get(id=id).delete()
    us = User.objects.get(role='GADMIN')
    return gadmin(request, us.id)


def partner_save(request):
    if request.method == 'POST':  # data sent by user
        form = Condractor_on_stock_Form(request.POST)
        if form.is_valid():
            obj = Condractor_on_stock()
            obj.company = form.cleaned_data['company']
            obj.number = form.cleaned_data['number']
            obj.email = form.cleaned_data['email']
            obj.condition = None
            obj.quantity = None
            obj.save()
            us = User.objects.get(role='GADMIN')
            return gadmin(request, us.id)
    else:  # display empty form
        form = Condractor_on_stock_Form()
        return render(request, 'partner_save.html', {'car_form': form})


def worker_list(request):
    worker1 = Staff.objects.all()
    worker2 = User.objects.all().values()
    return render(request, 'worker_list.html', {'wor1': worker1, 'wor2': worker2})


def user_list(request):
    userr = User.objects.all().values()
    return render(request, 'user_list.html', {'us': userr})


def user_delete(request, id):
    User.objects.get(id=id).delete()
    us = User.objects.get(role='GADMIN')
    return gadmin(request, us.id)


def user_save(request):
    if request.method == 'POST':  # data sent by user
        form = UseForm(request.POST)
        if form.is_valid():
            obj = User()
            obj.username = form.cleaned_data['username']
            obj.password = form.cleaned_data['password']
            obj.role = form.cleaned_data['role']
            obj.save()
            id = obj.id

            obj1 = Staff()
            obj1.user_id = id
            obj1.efficiency = 0
            obj1.control = 0
            obj1.condition = None
            obj1.save()
            us = User.objects.get(role='GADMIN')
            return gadmin(request, us.id)
    else:  # display empty form
        form = UseForm
        return render(request, 'user_save.html', {'car_form': form})


def zakaz_skladu(request):
    if request.method == 'POST':  # data sent by user
        form = OrderForm(request.POST)
        if form.is_valid():
            obj = Order()
            obj.condition = 'создан'
            obj.quantity = form.cleaned_data['quantity']
            obj.shipping = True
            obj.product = form.cleaned_data['product']
            obj.staff = None
            obj.save()
            return render(request, 'zakaz_skladu_thenk.html')
    else:  # display empty form
        form = OrderForm()
        return render(request, 'zakaz_skladu.html', {'car_form': form})


def zakaz_skladu_thenk(request):
    return render(request, 'zakaz_skladu_thenk.html')


def zakaz_on_skladu(request):
    if request.method == 'POST':  # data sent by user
        pk = Product.objects.get(name=request.POST.get('product'))
        obj = Order()
        obj.condition = 'привезли'
        obj.quantity = request.POST.get('quantity')
        obj.shipping = False
        obj.product_id = pk.id
        obj.staff = None
        obj.save()
        print(obj)
        us = User.objects.get(role='ADMIN')
        return admin(request, us.id)
    else:  # display empty form
        form = OrderForm()
        prod = Product.objects.all()
        com = Condractor_on_stock.objects.all()
        return render(request, 'zakaz_on_skladu.html', {'car_form': form,
                                                        'prod': prod,
                                                        'com': com})
