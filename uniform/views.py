from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Product
from .cart import Cart

def uniform(request):
    """Render the uniform page."""
    return render(request, 'uniform/uniform.html', { 'segment': 'Uniform Store' })

# 🟢 CART
def add_to_cart(request):
    cart = Cart(request)

    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))

    cart.add(product_id, quantity)

    return JsonResponse({
        'success': True,
        'cart_count': len(cart)
    })


# 🟢 CART PAGE
def cart_view(request):
    cart = Cart(request)

    cart_items = []
    total = 0

    for product_id, item in cart.cart.items():
        product = Product.objects.get(id=product_id)

        subtotal = product.price * item['quantity']
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': item['quantity'],
            'subtotal': subtotal
        })

    return render(request, 'uniform/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# 🟢 REMOVE ITEM
def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)

    return redirect('cart')