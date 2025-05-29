from .cart import Cart

#creating context processor to make the cart work on all pages
def cart(request):
    #returning the default data from Cart
    return {'cart': Cart(request)}