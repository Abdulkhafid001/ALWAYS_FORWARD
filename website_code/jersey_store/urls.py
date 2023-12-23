from django.urls import path

from jersey_store import views

urlpatterns = [
    # Leave as empty string for base url
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('customize/', views.customize, name="customize"),
    path('products/', views.merch, name="products"),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
    path('faq/', views.faq, name="faq"),
    path('terms-and-conditions/', views.terms_and_conditions,
         name="termsandconditions"),
    path('policy/', views.policy, name="policy"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
]
