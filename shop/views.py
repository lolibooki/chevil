from django.shortcuts import render
from .forms import AddProductForm
from .models import Product
from django.contrib import messages


def storage(request):
    products = Product.objects.all()
    if request.method == 'POST':
        product_form = AddProductForm(request.POST,
                                      files=request.FILES)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, 'محصول جدید اضافه شد')
        else:
            messages.error(request, 'خطا در ایجاد محصول')
    else:
        product_form = AddProductForm()
    return render(request,
                  'storage.html',
                  {'section':'storage',
                   'products':products,
                   'product_form':product_form})
# Create your views here.


def statistic(request):
    return render(request,
                  'statistic.html',
                  {'section':'statistic'})