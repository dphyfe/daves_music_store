from .models import Cart


def cart_context(request):
    """Add cart item count to all templates"""
    cart_item_count = 0

    if request.session.session_key:
        try:
            cart = Cart.objects.get(session_key=request.session.session_key)
            cart_item_count = cart.get_item_count()
        except Cart.DoesNotExist:
            pass

    return {"cart_item_count": cart_item_count}
