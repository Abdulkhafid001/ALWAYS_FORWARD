from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from jersey_store.models import *
from jersey_store.utils import cartData, guestOrder
from django.core.mail import send_mail
import ssl
import smtplib
from email.message import EmailMessage
from website_code.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD


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
    context = {'product': product, 'cartItems': cartItems}
    return render(request, 'store/detail.html', context)


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

# brand_view functionality takes a category and display all the product under that category


def brand_view(request, brand_name):
    data = cartData(request)
    cartItems = data['cartItems']
    # Filter products based on the category
    product = Product.objects.filter(brand=brand_name)
    context = {'products': product, 'cartItems': cartItems,
               'category_name': brand_name}
    return render(request, 'store/category_products.html', context)


# category_view functionality takes a category and display all the product under that category


def category_view(request, category_name):
    data = cartData(request)
    cartItems = data['cartItems']
    # Filter products based on the category
    product = Product.objects.filter(category=category_name)
    context = {'products': product, 'cartItems': cartItems,
               'category_name': category_name}
    return render(request, 'store/products.html', context)
# type_view functionality takes a category and display all the product under that type


def type_view(request, type_name):
    data = cartData(request)
    cartItems = data['cartItems']
    # Filter products based on the category
    product = Product.objects.filter(type=type_name)
    context = {'products': product, 'cartItems': cartItems,
               'category_name': type_name}
    return render(request, 'store/products.html', context)


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
    data2 = cartData(request)

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
    send_order_confirmation_email(data, order, data2['items'])
    return JsonResponse({'message': 'Payment submitted..'}, safe=False)

# function to send email after an order an order is completed


def send_order_confirmation_email(data, order, items):
    subject = 'Order Confirmation'
    message = f"Thank you"
    body = f"Dear {data['userInfo']['name']}, we have received your order with transaction id: {order.transaction_id}. The items you ordered are:\n"
    for item in items:
        body += f"- {item.product.name} x{item.quantity}, Total:{item.get_total}\n"
    body += f"We will ship to this address: {data['shippingInfo']['address']}, {data['shippingInfo']['city']}, {data['shippingInfo']['state']}, {data['shippingInfo']['zipcode']}. Call us at: +24 8099991032"
    from_email = EMAIL_HOST_USER
    customer_mail = [data['userInfo']['email']]

    # instantiate email message
    em = EmailMessage()
    em['From'] = from_email
    em['To'] = customer_mail
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login('kabiruabdulkhafid@gmail.com', EMAIL_HOST_PASSWORD)
        smtp.sendmail(EMAIL_HOST_USER, customer_mail, em.as_string())
