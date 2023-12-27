from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cartData, guestOrder
from django.core.mail import send_mail, EmailMessage
from website_code.settings import EMAIL_HOST_USER


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def merch(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/products.html', context)


# detail view this view get the product of a product and get it's lone data
def detail_view(request, product_id):
    data = cartData(request)
    cartItems = data['cartItems']
    # get product based on id
    product = Product.objects.get(id=product_id)
    print(product.name)
    context = {'product': product, 'cartItems': cartItems}
    return render(request, 'store/detail.html', context)


def shoes(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/products.html', context)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

# customize view


def customize(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/customize.html', context)


def contact(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/contact.html', context)


def faq(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/faq.html', context)


def policy(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/policy.html', context)


def terms_and_conditions(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/terms-and-conditions.html', context)


def about(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/about.html', context)


def update_item(request):
    data = json.loads(request.body.decode('utf-8'))
    productId = data.get('productId')
    action = data.get('action')
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body.decode('utf-8'))
    user_name = data['userInfo']['name']
    user_email = data['userInfo']['email']
    user_phone = data['userInfo']['phone']

    print('name: ', user_name)
    print('email: ', user_email)
    print(data['shippingInfo']['address'])
    print(data['shippingInfo']['zipcode'])
    print(data['shippingInfo']['city'])
    print(data['shippingInfo']['state'])

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    # get total
    total = float(data['userInfo']['total'])
    # set transaction_id to order model
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    # if order.shipping == True:
    shipping = ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shippingInfo']['address'],
        city=data['shippingInfo']['city'],
        state=data['shippingInfo']['state'],
        zipcode=data['shippingInfo']['zipcode']
    )
    shipping.save()
    # Send email to the user
    # send_order_confirmation_email(data, order, shipping)
    return JsonResponse({'message':'Payment submitted..'}, safe=False)

# function to send email after an order an order is completed
def send_order_confirmation_email(data, order, shipping):
    subject = 'Order Confirmation'
    message = f'Thank you {data['userInfo']['name']} for your order! Your order with transaction ID {order.transaction_id} has been received.\n\nShipping Details:\nName: {data['userInfo']['name']}\nEmail: {data['userInfo']['email']}\nAddress: {shipping.address}\nCity: {shipping.city}\nState: {shipping.state}\nZip Code: {shipping.zipcode}\n\nTotal Amount: {order.get_cart_total}\n\nCall us at: 09168424529'

    from_email = EMAIL_HOST_USER
    recipient_list = [data['userInfo']['email']]

    send_mail(subject, message, from_email,
              recipient_list, fail_silently=False)
