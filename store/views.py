from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Instrument, Category

# Create your views here.


def home(request):
    """Homepage view with featured instruments"""
    featured_instruments = Instrument.objects.filter(featured=True, in_stock=True)
    categories = Category.objects.all()

    # Get distinct brands for the filter
    brands = Instrument.objects.values_list("brand", flat=True).distinct().order_by("brand")

    # Get selected brands from query params
    selected_brands = request.GET.getlist("brand")

    # Filter featured instruments by selected brands
    if selected_brands:
        featured_instruments = featured_instruments.filter(brand__in=selected_brands)

    # Limit to 6 instruments
    featured_instruments = featured_instruments[:6]

    context = {
        "featured_instruments": featured_instruments,
        "categories": categories,
        "brands": brands,
        "selected_brands": selected_brands,
    }
    return render(request, "store/home.html", context)


def product_list(request):
    """List all instruments with filtering options"""
    instruments = Instrument.objects.filter(in_stock=True)
    categories = Category.objects.all()

    # Filter by category
    category_slug = request.GET.get("category")
    if category_slug:
        # Ensure we only filter by an existing category
        category = get_object_or_404(Category, slug=category_slug)
        instruments = instruments.filter(category=category)

    # Filter by condition
    condition = request.GET.get("condition")
    if condition:
        # Narrow results down to the selected condition
        instruments = instruments.filter(condition=condition)

    # Filter by brand
    selected_brands = request.GET.getlist("brand")
    if selected_brands:
        instruments = instruments.filter(brand__in=selected_brands)

    # Search functionality
    search_query = request.GET.get("search")
    if search_query:
        # Match against multiple fields for a broader search
        instruments = instruments.filter(Q(name__icontains=search_query) | Q(brand__icontains=search_query) | Q(description__icontains=search_query))

    # Get distinct brands for the filter
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
    """Detailed view of a single instrument"""
    instrument = get_object_or_404(Instrument, slug=slug)
    related_instruments = Instrument.objects.filter(category=instrument.category, in_stock=True).exclude(id=instrument.id)[:4]

    context = {
        "instrument": instrument,
        "related_instruments": related_instruments,
    }
    return render(request, "store/product_detail.html", context)


def category_list(request):
    """View all categories"""
    categories = Category.objects.all()
    context = {
        "categories": categories,
    }
    return render(request, "store/category_list.html", context)


def _parse_filters(request):
    """Extract shared filter parameters from the request"""
    condition = request.GET.get("condition")
    if condition in {"", "all"}:
        condition = None
    # Deal flag is treated as a simple toggle via ?deals=1
    deals_active = request.GET.get("deals") == "1"
    # Get selected brands
    selected_brands = request.GET.getlist("brand")
    return condition, deals_active, selected_brands


def _apply_filters(queryset, condition, deals_active, selected_brands=None):
    """Apply shared filtering logic for category pages"""
    if condition == "new":
        # Only include brand-new stock
        queryset = queryset.filter(condition="new")
    elif condition == "used":
        # Keep anything that is not flagged as new
        queryset = queryset.exclude(condition="new")

    if deals_active:
        # Featured flag doubles as our "deal" indicator
        queryset = queryset.filter(featured=True)

    if selected_brands:
        # Filter by selected brands
        queryset = queryset.filter(brand__in=selected_brands)

    return queryset


def _category_context(request, queryset, page_title, page_description):
    """Build a consistent context payload for category templates"""
    condition, deals_active, selected_brands = _parse_filters(request)
    filtered = _apply_filters(queryset, condition, deals_active, selected_brands)

    # Get distinct brands for the filter
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
    """Guitars category page"""
    queryset = Instrument.objects.filter(category__slug="guitars", in_stock=True)
    context = _category_context(
        request,
        queryset,
        page_title="Guitars",
        page_description="Explore our collection of acoustic and electric guitars",
    )
    return render(request, "store/guitars.html", context)


def basses_page(request):
    """Bass Guitars category page"""
    queryset = Instrument.objects.filter(category__slug="bass-guitars", in_stock=True)
    context = _category_context(
        request,
        queryset,
        page_title="Bass Guitars",
        page_description="Find your perfect bass guitar - electric and acoustic models",
    )
    return render(request, "store/basses.html", context)


def drums_page(request):
    """Drums category page"""
    queryset = Instrument.objects.filter(category__slug="drums", in_stock=True)
    context = _category_context(
        request,
        queryset,
        page_title="Drums & Percussion",
        page_description="Complete drum kits and percussion instruments",
    )
    return render(request, "store/drums.html", context)


def horns_page(request):
    """Wind Instruments (Horns) category page"""
    queryset = Instrument.objects.filter(category__slug="wind-instruments", in_stock=True)
    context = _category_context(
        request,
        queryset,
        page_title="Horns & Wind Instruments",
        page_description="Saxophones, trumpets, flutes, and more",
    )
    return render(request, "store/horns.html", context)


def keyboards_page(request):
    """Keyboards category page"""
    queryset = Instrument.objects.filter(category__slug="keyboards", in_stock=True)
    context = _category_context(
        request,
        queryset,
        page_title="Keyboards & Pianos",
        page_description="Digital pianos, synthesizers, and MIDI keyboards",
    )
    return render(request, "store/keyboards.html", context)


def amps_effects_page(request):
    """Amps & Effects category page"""
    queryset = Instrument.objects.filter(
        Q(category__slug="amps-effects") | Q(name__icontains="amp") | Q(name__icontains="effect") | Q(name__icontains="pedal"),
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
    """Lessons information page"""
    context = {
        "page_title": "Music Lessons",
        "page_description": "Learn to play with our expert instructors",
    }
    return render(request, "store/lessons.html", context)


def get_or_create_cart(request):
    """Get or create a cart for the current session"""
    from .models import Cart

    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def cart_view(request):
    """Display the shopping cart"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()

    context = {
        "cart": cart,
        "cart_items": cart_items,
    }
    return render(request, "store/cart.html", context)


def add_to_cart(request, slug):
    """Add an instrument to the cart"""
    from django.shortcuts import redirect
    from .models import CartItem

    instrument = get_object_or_404(Instrument, slug=slug)
    cart = get_or_create_cart(request)

    # Get or create cart item
    cart_item, created = CartItem.objects.get_or_create(cart=cart, instrument=instrument)

    if not created:
        # Item already in cart, increase quantity
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart_view")


def update_cart_item(request, item_id):
    """Update quantity of a cart item"""
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
        pass

    return redirect("cart_view")


def remove_from_cart(request, item_id):
    """Remove an item from the cart"""
    from django.shortcuts import redirect
    from .models import CartItem

    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()

    return redirect("cart_view")
