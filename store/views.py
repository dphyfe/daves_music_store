from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Instrument, Category

# Create your views here.


def home(request):
    """Homepage view with featured instruments"""
    featured_instruments = Instrument.objects.filter(featured=True, in_stock=True)[:6]
    categories = Category.objects.all()
    context = {
        "featured_instruments": featured_instruments,
        "categories": categories,
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

    # Search functionality
    search_query = request.GET.get("search")
    if search_query:
        # Match against multiple fields for a broader search
        instruments = instruments.filter(Q(name__icontains=search_query) | Q(brand__icontains=search_query) | Q(description__icontains=search_query))

    context = {
        "instruments": instruments,
        "categories": categories,
        "selected_category": category_slug,
        "selected_condition": condition,
        "search_query": search_query,
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
    return condition, deals_active


def _apply_filters(queryset, condition, deals_active):
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

    return queryset


def _category_context(request, queryset, page_title, page_description):
    """Build a consistent context payload for category templates"""
    condition, deals_active = _parse_filters(request)
    filtered = _apply_filters(queryset, condition, deals_active)
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
