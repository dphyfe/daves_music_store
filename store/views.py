"""
Views for the public-facing `store` app.

This module provides the pages used by customers: the homepage with
featured products, product lists with filters/search, product detail,
category pages, and minimal cart operations that leverage a session-
backed `Cart` model.

Design notes:
- Keep views lightweight. Heavy filtering and business logic is
  delegated to helper functions (`_parse_filters`, `_apply_filters`).
- The cart is session-backed (see `get_or_create_cart`) so views rely
  on a session key rather than user authentication.
"""

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Instrument, Category


def home(request):
    """Homepage view with featured instruments.

    Shows instruments marked as `featured` and `in_stock`. Supports a
    simple brand filter via query parameters `?brand=...` (multiple
    values allowed). Results are capped to the first 6 items for the
    homepage layout.
    """

    featured_instruments = Instrument.objects.filter(featured=True, in_stock=True)
    categories = Category.objects.all()

    # Distinct list of brands to populate filter controls in the template
    brands = Instrument.objects.values_list("brand", flat=True).distinct().order_by("brand")

    # Selected brands come from query parameters like ?brand=Fender&brand=Gibson
    selected_brands = request.GET.getlist("brand")

    if selected_brands:
        # Narrow the featured set to selected brands
        featured_instruments = featured_instruments.filter(brand__in=selected_brands)

    # Limit the number of featured instruments displayed on the homepage
    featured_instruments = featured_instruments[:6]

    context = {
        "featured_instruments": featured_instruments,
        "categories": categories,
        "brands": brands,
        "selected_brands": selected_brands,
    }
    return render(request, "store/home.html", context)


def product_list(request):
    """List searchable and filterable products.

    Supports the following query parameters:
    - `category`: category slug to filter by
    - `condition`: one of the condition choices (e.g. 'new', 'used')
    - `brand`: repeatable parameter to filter by brand (e.g. ?brand=Fender)
    - `search`: full-text-like search across `name`, `brand`, and `description`
    """

    instruments = Instrument.objects.filter(in_stock=True)
    categories = Category.objects.all()

    # Optional category filtering with validation via get_object_or_404
    category_slug = request.GET.get("category")
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        instruments = instruments.filter(category=category)

    # Filter by `condition` if provided
    condition = request.GET.get("condition")
    if condition:
        instruments = instruments.filter(condition=condition)

    # Brand filter (allows multiple brands)
    selected_brands = request.GET.getlist("brand")
    if selected_brands:
        instruments = instruments.filter(brand__in=selected_brands)

    # Simple search across several text fields
    search_query = request.GET.get("search")
    if search_query:
        instruments = instruments.filter(
            Q(name__icontains=search_query)
            | Q(brand__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    brands = Instrument.objects.values_list("brand", flat=True).distinct().order_by("brand")

    context = {
        "instruments": instruments,
        "categories": categories,
        "selected_category": category_slug,
        "selected_condition": condition,
        "search_query": search_query,
        "brands": brands,
        "selected_brands": selected_brands,
    }
    return render(request, "store/product_list.html", context)


def product_detail(request, slug):
    """Detailed view of a single instrument.

    Also selects a small set of related instruments from the same
    category for display under the product details.
    """

    instrument = get_object_or_404(Instrument, slug=slug)
    related_instruments = (
        Instrument.objects.filter(category=instrument.category, in_stock=True)
        .exclude(id=instrument.id)
        [:4]
    )

    context = {
        "instrument": instrument,
        "related_instruments": related_instruments,
    }
    return render(request, "store/product_detail.html", context)


def category_list(request):
    """Simple list of all categories for navigation pages."""

    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "store/category_list.html", context)


def _parse_filters(request):
    """Centralize parsing of query parameters used by category pages.

    Returns a tuple: (condition, deals_active, selected_brands)
    - `condition`: normalized condition value or None
    - `deals_active`: boolean indicating whether the `deals` toggle is set
    - `selected_brands`: list of brand names selected by the user
    """

    condition = request.GET.get("condition")
    if condition in {"", "all"}:
        condition = None

    # `?deals=1` toggles deals (featured items)
    deals_active = request.GET.get("deals") == "1"

    selected_brands = request.GET.getlist("brand")
    return condition, deals_active, selected_brands


def _apply_filters(queryset, condition, deals_active, selected_brands=None):
    """Apply shared filtering rules to a queryset used by category pages.

    This function is intentionally small and composable so it can be
    reused across multiple category-specific views.
    """

    if condition == "new":
        queryset = queryset.filter(condition="new")
    elif condition == "used":
        queryset = queryset.exclude(condition="new")

    if deals_active:
        # In this project `featured` is reused as a lightweight "deal" flag
        queryset = queryset.filter(featured=True)

    if selected_brands:
        queryset = queryset.filter(brand__in=selected_brands)

    return queryset


def _category_context(request, queryset, page_title, page_description):
    """Compose a consistent template context for category-style pages.

    Accepts a base `queryset` containing instruments and returns a
    dictionary containing UI-related flags and the filtered instruments.
    """

    condition, deals_active, selected_brands = _parse_filters(request)
    filtered = _apply_filters(queryset, condition, deals_active, selected_brands)

    brands = Instrument.objects.values_list("brand", flat=True).distinct().order_by("brand")

    return {
        "instruments": filtered,
        "page_title": page_title,
        "page_description": page_description,
        "categories": Category.objects.all(),
        "selected_condition": condition,
        "deals_active": deals_active,
        "star_range": range(1, 6),
        "condition_all_checked": condition in (None, "", "all"),
        "condition_new_checked": condition == "new",
        "condition_used_checked": condition == "used",
        "brands": brands,
        "selected_brands": selected_brands,
    }


def guitars_page(request):
    """Guitars category page.

    Uses `_category_context` to build a template-friendly payload.
    """

    queryset = Instrument.objects.filter(category__slug="guitars", in_stock=True)
    context = _category_context(
        request,
        queryset,
        page_title="Guitars",
        page_description="Explore our collection of acoustic and electric guitars",
    )
    return render(request, "store/guitars.html", context)


def basses_page(request):
    """Bass Guitars category page."""

    queryset = Instrument.objects.filter(category__slug="bass-guitars", in_stock=True)
    context = _category_context(
        request,
        queryset,
        page_title="Bass Guitars",
        page_description="Find your perfect bass guitar - electric and acoustic models",
    )
    return render(request, "store/basses.html", context)


def drums_page(request):
    """Drums & percussion category page."""

    queryset = Instrument.objects.filter(category__slug="drums", in_stock=True)
    context = _category_context(
        request,
        queryset,
        page_title="Drums & Percussion",
        page_description="Complete drum kits and percussion instruments",
    )
    return render(request, "store/drums.html", context)


def horns_page(request):
    """Horns and wind instruments category page."""

    queryset = Instrument.objects.filter(category__slug="wind-instruments", in_stock=True)
    context = _category_context(
        request,
        queryset,
        page_title="Horns & Wind Instruments",
        page_description="Saxophones, trumpets, flutes, and more",
    )
    return render(request, "store/horns.html", context)


def keyboards_page(request):
    """Keyboards and pianos category page."""

    queryset = Instrument.objects.filter(category__slug="keyboards", in_stock=True)
    context = _category_context(
        request,
        queryset,
        page_title="Keyboards & Pianos",
        page_description="Digital pianos, synthesizers, and MIDI keyboards",
    )
    return render(request, "store/keyboards.html", context)


def amps_effects_page(request):
    """Amps and effects page.

    Builds a broader queryset that looks for explicit amp/effect categories
    or instruments whose name contains related keywords.
    """

    queryset = Instrument.objects.filter(
        Q(category__slug="amps-effects")
        | Q(name__icontains="amp")
        | Q(name__icontains="effect")
        | Q(name__icontains="pedal"),
        in_stock=True,
    )
    context = _category_context(
        request,
        queryset,
        page_title="Amps & Effects",
        page_description="Amplifiers, effect pedals, and audio gear",
    )
    return render(request, "store/amps_effects.html", context)


def lessons_page(request):
    """Static-ish page describing music lessons offered by the store."""

    context = {
        "page_title": "Music Lessons",
        "page_description": "Learn to play with our expert instructors",
    }
    return render(request, "store/lessons.html", context)


def get_or_create_cart(request):
    """Return the session-backed `Cart` for the current request.

    If the session has no `session_key`, a new session is created. The
    returned `Cart` is retrieved or created based on that key.
    """

    from .models import Cart

    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def cart_view(request):
    """Display the current shopping cart and its items."""

    cart = get_or_create_cart(request)
    cart_items = cart.items.all()

    context = {"cart": cart, "cart_items": cart_items}
    return render(request, "store/cart.html", context)


def add_to_cart(request, slug):
    """Add an instrument to the user's cart.

    If the item already exists in the cart, increment its quantity.
    Redirects back to the cart view after the operation.
    """

    from django.shortcuts import redirect
    from .models import CartItem

    instrument = get_object_or_404(Instrument, slug=slug)
    cart = get_or_create_cart(request)

    # Get or create cart item; `unique_together` on CartItem enforces
    # one row per (cart, instrument) pair.
    cart_item, created = CartItem.objects.get_or_create(cart=cart, instrument=instrument)

    if not created:
        # Item already in cart, increase quantity
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart_view")


def update_cart_item(request, item_id):
    """Update the quantity for a cart item from a POST form.

    If the provided quantity is 0 (or invalid), the item is removed.
    """

    from django.shortcuts import redirect
    from .models import CartItem

    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = request.POST.get("quantity", 1)

    try:
        quantity = int(quantity)
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    except ValueError:
        # Invalid input -- ignore and redirect back to the cart
        pass

    return redirect("cart_view")


def remove_from_cart(request, item_id):
    """Remove a `CartItem` by id and return to the cart view."""

    from django.shortcuts import redirect
    from .models import CartItem

    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()

    return redirect("cart_view")
