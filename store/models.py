from django.db import models
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    """Categories for musical instruments"""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Instrument(models.Model):
    """Model for musical instruments in the store"""

    CONDITION_CHOICES = [
        ("new", "New"),
        ("used_excellent", "Used - Excellent"),
        ("used_good", "Used - Good"),
        ("used_fair", "Used - Fair"),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="instruments")
    brand = models.CharField(max_length=100)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default="new")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0, help_text="Customer rating out of five")
    description = models.TextField()
    specifications = models.TextField(blank=True, help_text="Technical specifications")
    image = models.ImageField(upload_to="instruments/", blank=True, null=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False, help_text="Display on homepage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.brand} {self.name}"

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})
