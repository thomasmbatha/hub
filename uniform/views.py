from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from .models import Product, Employee
from .cart import Cart


# 🟢 UNIFORM STORE (MAIN PAGE)
def uniform(request):
    """
    Render the uniform store page with all products.
    """
    products = Product.objects.all()

    return render(request, "uniform/uniform.html", {
        "products": products,
        "segment": "Uniform Store"
    })


# 🟢 ADD TO CART (AJAX)
def add_to_cart(request):
    cart = Cart(request)

    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))

    if product_id:
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
        product = get_object_or_404(Product, id=product_id)

        subtotal = product.price * item['quantity']
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': item['quantity'],
            'subtotal': subtotal
        })

    # Employee (safe fallback if not found)
    employee = None
    allowance = 0
    remaining = 0
    exceeded = False

    if request.user.is_authenticated:
        try:
            employee = Employee.objects.get(user=request.user)
            allowance = employee.allowance
            remaining = allowance - total
            exceeded = total > allowance
        except Employee.DoesNotExist:
            pass

    return render(request, 'uniform/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'allowance': allowance,
        'remaining': remaining,
        'exceeded': exceeded
    })


# 🟢 REMOVE ITEM FROM CART
def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)

    return redirect('cart')

def cart_json(request):
    cart = Cart(request)

    items = []
    total = 0

    for product_id, item in cart.cart.items():
        product = Product.objects.get(id=product_id)

        subtotal = product.price * item['quantity']
        total += subtotal

        items.append({
            "id": product.id,
            "name": product.name,
            "price": float(product.price),
            "quantity": item['quantity'],
            "subtotal": float(subtotal),
            "image": product.image.url if product.image else ""
        })

    return JsonResponse({
        "items": items,
        "total": float(total),
        "count": len(items)
    })