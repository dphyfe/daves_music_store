# Dave's World of Music - Musical Instrument Store

![Dave's World of Music Homepage](https://github.com/user-attachments/assets/d5e8c3e5-8b4e-4f3e-9c8e-8f3c3e8f3e8f)

A beautiful, modern web UI for a musical instrument store selling new and used instruments.

## Features

- 🎸 Browse musical instruments by category (Guitars, Bass, Drums, Keyboards, Wind, Strings)
- 🔍 Search functionality to find instruments quickly
- 🏷️ Filter by condition (New, Used - Excellent, Used - Good, Used - Fair)
- 💰 Featured instruments showcase on homepage
- 📱 Fully responsive design for mobile and desktop
- 🎨 Modern, attractive UI with smooth animations
- 🛒 Product detail pages with specifications
- 🔧 Admin panel for managing inventory

## Technology Stack

- **Backend:** Django 5.2.8
- **Database:** SQLite
- **Frontend:** HTML5, CSS3
- **Icons:** Font Awesome 6.4.0

## Setup Instructions

### Prerequisites
- Python 3.12 or higher

### Installation

1. **Activate the virtual environment:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. **Install dependencies (if not already installed):**
   ```powershell
   pip install django pillow
   ```

3. **Run migrations:**
   ```powershell
   python manage.py migrate
   ```

4. **Create a superuser (for admin access):**
   ```powershell
   python manage.py createsuperuser
   ```

5. **Start the development server:**
   ```powershell
   python manage.py runserver
   ```

6. **Visit the store:**
   - Homepage: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## Project Structure

```
daves_music_store/
├── daves_music_store/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/                       # Main store app
│   ├── models.py               # Category & Instrument models
│   ├── views.py                # View functions
│   ├── admin.py                # Admin configuration
│   ├── urls.py                 # URL patterns
│   └── templates/store/        # HTML templates
│       ├── base.html
│       ├── home.html
│       ├── product_list.html
│       ├── product_detail.html
│       └── category_list.html
├── static/css/                 # Static CSS files
│   └── style.css
├── media/                      # User-uploaded images
├── manage.py
└── populate_db.py             # Sample data script
```

## Database Models

### Category
- name
- slug
- description

### Instrument
- name
- slug
- category (Foreign Key)
- brand
- condition (new, used_excellent, used_good, used_fair)
- price
- description
- specifications
- image
- in_stock
- featured
- created_at
- updated_at

## Adding Products

You can add products in two ways:

1. **Via Admin Panel:**
   - Navigate to http://127.0.0.1:8000/admin/
   - Login with your superuser credentials
   - Add categories and instruments through the interface

2. **Programmatically:**
   - Run the populate_db.py script to add sample data
   - Or use Django shell: `python manage.py shell`

## Sample Data

The database comes pre-populated with:
- 6 categories (Guitars, Bass Guitars, Drums, Keyboards, Wind Instruments, String Instruments)
- 11 sample instruments including various guitars, basses, drums, keyboards, and more

## Pages

1. **Homepage** - Featured instruments and categories
2. **All Instruments** - Complete product listing with filters
3. **Categories** - Browse by instrument category
4. **Product Detail** - Detailed view with specifications and related products
5. **Admin Panel** - Manage inventory, categories, and products

## Customization

- **Colors:** Edit CSS variables in `static/css/style.css`
- **Categories:** Add/modify in admin panel or models.py
- **Images:** Upload product images through admin panel
- **Content:** Edit templates in `store/templates/store/`

## Future Enhancements

- Shopping cart functionality
- User authentication and accounts
- Order processing
- Payment integration
- Product reviews and ratings
- Wishlist feature
- Email notifications

## License

This project is for educational purposes.

---

**Dave's World of Music** - Your destination for quality musical instruments! 🎸🥁🎹🎺
