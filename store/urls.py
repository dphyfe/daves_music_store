"""
store.urls
-----------

URL routes for the `store` application. Each route is kept simple and
points to a corresponding view in `store.views`.

Naming convention:
- Use descriptive `name` attributes so templates and `reverse()` calls
    can reference routes reliably.
"""

from django.urls import path
from . import views

urlpatterns = [
        # Homepage showing featured instruments
        path("", views.home, name="home"),

        # Category-specific pages
        path("guitars/", views.guitars_page, name="guitars"),
        path("basses/", views.basses_page, name="basses"),
        path("drums/", views.drums_page, name="drums"),
        path("horns/", views.horns_page, name="horns"),
        path("keyboards/", views.keyboards_page, name="keyboards"),
        path("amps-effects/", views.amps_effects_page, name="amps_effects"),

        # Informational page
        path("lessons/", views.lessons_page, name="lessons"),

        # Product list and categories
        path("products/", views.product_list, name="product_list"),
        path("categories/", views.category_list, name="category_list"),

        # Product detail (uses slug for SEO-friendly URLs)
        path("product/<slug:slug>/", views.product_detail, name="product_detail"),

        # Cart-related endpoints
        path("cart/", views.cart_view, name="cart_view"),
        path("cart/add/<slug:slug>/", views.add_to_cart, name="add_to_cart"),
        path("cart/update/<int:item_id>/", views.update_cart_item, name="update_cart_item"),
        path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
]
