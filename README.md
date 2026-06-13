# AURUM — Luxury Fine Dining Restaurant Website
### A full-stack Django web application with premium UI/UX

---

```
  ░█████╗░██╗░░░██╗██████╗░██╗░░░██╗███╗░░░███╗
  ██╔══██╗██║░░░██║██╔══██╗██║░░░██║████╗░████║
  ███████║██║░░░██║██████╔╝██║░░░██║██╔████╔██║
  ██╔══██║██║░░░██║██╔══██╗██║░░░██║██║╚██╔╝██║
  ██║░░██║╚██████╔╝██║░░██║╚██████╔╝██║░╚═╝░██║
  ╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝░╚═════╝░╚═╝░░░░╚═╝
```

> *"Where Art Meets the Table"* — A Michelin-starred sanctuary of culinary excellence, brought to life on the web.

---

## ✨ Features

### 🎨 Frontend
| Feature | Details |
|---|---|
| **Design System** | Dark luxury theme — deep black, warm gold (#C9A96E), cream |
| **Typography** | Cormorant Garamond (serif) + Jost (sans-serif) — premium pairing |
| **Hero Section** | Full-screen auto-playing image slider with smooth Ken Burns effect |
| **Animations** | Intersection Observer scroll reveals, counter animations, parallax |
| **Cursor Glow** | Subtle gold radial gradient follows mouse on desktop |
| **Loader Screen** | Branded preloader with animated progress bar |
| **Micro-interactions** | Hover dish reveals, image zoom, button lifts, nav underlines |
| **Responsive** | Mobile-first, tested at 320px → 1600px+ |
| **Ticker Banner** | Scrolling awards & accolades strip below hero |

### 📄 Pages
| Page | URL | Description |
|---|---|---|
| **Home** | `/` | Full-featured landing page with all sections |
| **Menu** | `/menu/` | Interactive AJAX-filtered menu with live search |
| **Reservation** | `/reservation/` | AJAX form with real-time feedback |
| **About** | `/about/` | Story, animated timeline, mission & values |
| **Chef** | `/chef/` | Executive chef profile, training, signature dishes |
| **Events** | `/events/` | Upcoming events listing + detail pages |
| **Gallery** | `/gallery/` | Category-filtered photo gallery with lightbox |
| **Contact** | `/contact/` | AJAX contact form + embedded map + social links |
| **404 / 500** | — | Custom branded error pages |

### 🔧 Backend (Django)
| Feature | Details |
|---|---|
| **Models** | MenuItem, Chef, Reservation, Event, GalleryImage, Testimonial, Award, NewsletterSubscriber, ContactMessage |
| **Admin** | Fully customised with colour-coded badges, thumbnail previews, list filters |
| **AJAX API** | `/api/menu/` — live menu filtering & search |
| **AJAX API** | `/api/newsletter/` — newsletter signup |
| **AJAX Forms** | Reservation & contact forms submit via `fetch()` — no page reload |
| **Email** | Reservation confirmation emails on submit |
| **Seed Data** | `python manage.py seed_data` — populates all models with rich sample data |
| **Context Processor** | Restaurant settings (name, address, hours) injected into every template |
| **Custom Template Tags** | `currency`, `star_rating`, `active_nav`, `render_menu_item` |
| **WhiteNoise** | Static file serving without a separate web server in development |

---

## 🚀 Quick Start

### Option 1 — Automated Setup (Recommended)

```bash
cd aurum_restaurant
chmod +x setup.sh
bash setup.sh
source venv/bin/activate
python manage.py runserver
```

Open **http://127.0.0.1:8000** — site is live with sample data.

---

### Option 2 — Manual Setup

**1. Create virtual environment**
```bash
cd aurum_restaurant
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure environment**
```bash
cp .env.example .env
# Edit .env and set your SECRET_KEY
```

**4. Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

**5. Seed sample data**
```bash
python manage.py seed_data
```

**6. Create admin user**
```bash
python manage.py createsuperuser
```

**7. Collect static files**
```bash
python manage.py collectstatic
```

**8. Run the development server**
```bash
python manage.py runserver
```

---

## 📁 Project Structure

```
aurum_restaurant/
├── aurum_project/               # Django project config
│   ├── settings.py              # All settings (incl. restaurant meta)
│   ├── urls.py                  # Root URL configuration
│   └── wsgi.py
│
├── restaurant/                  # Main app
│   ├── models.py                # All 9 data models
│   ├── views.py                 # All page + AJAX views
│   ├── forms.py                 # Reservation, Contact, Newsletter forms
│   ├── admin.py                 # Fully customised admin panels
│   ├── urls.py                  # App URL routes
│   ├── apps.py
│   ├── context_processors.py    # Global restaurant settings
│   ├── templatetags/
│   │   └── restaurant_tags.py   # Custom template filters & tags
│   └── management/
│       └── commands/
│           └── seed_data.py     # Database seeding command
│
├── templates/
│   ├── base.html                # Master layout (navbar, footer, loader)
│   ├── 404.html
│   ├── 500.html
│   └── restaurant/
│       ├── home.html            # Full homepage
│       ├── menu.html            # Interactive menu page
│       ├── reservation.html     # Booking form page
│       ├── reservation_success.html
│       ├── about.html           # Restaurant story + timeline
│       ├── chef.html            # Executive chef profile
│       ├── events.html          # Events listing
│       ├── event_detail.html    # Single event page
│       ├── gallery.html         # Photo gallery
│       ├── contact.html         # Contact form + map
│       └── partials/
│           └── menu_item.html   # Reusable menu card component
│
├── static/
│   ├── css/
│   │   └── aurum.css            # Complete luxury stylesheet (~650 lines)
│   └── js/
│       └── aurum.js             # All JS: slider, reveals, AJAX, cursor
│
├── media/                       # User-uploaded files (runtime)
├── requirements.txt
├── manage.py
├── setup.sh                     # One-command setup script
├── .env.example
└── README.md
```

---

## 🗄️ Data Models

### `MenuItem`
Stores all dishes with category, pricing, dietary flags (`vegan`, `halal`, `spicy`, `gluten_free`, `chef_pick`), image (file upload or external URL), availability, and display order.

### `Chef`
Executive chef profile: bio, philosophy, quote, images, stats (years, Michelin stars, awards, cookbooks).

### `Reservation`
Complete booking record: guest details, date/time, party size, seating preference, special requests, status workflow (`pending → confirmed → seated → completed`), auto-generated confirmation number.

### `Event`
Restaurant events with support for recurring (e.g. "Every Friday") and one-off dates. Featured flag for homepage display.

### `GalleryImage`
Categorised photo library: ambiance, food, events, team. Supports file upload or external URL.

### `Testimonial`
Guest reviews with 1–5 star rating, avatar, role/title. Used in homepage carousel.

### `Award`
Accolades displayed in the awards strip and ticker (Michelin stars, James Beard, World's 50 Best, etc.).

### `NewsletterSubscriber`
Email subscriptions with active/inactive toggle. Includes admin export action.

### `ContactMessage`
Stores messages from the contact form with read/unread tracking.

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/menu/` | GET | Filter & search menu items. Params: `category`, `q` |
| `/api/newsletter/` | POST | Subscribe email. Body: `{ "email": "..." }` |

Both return JSON. All form submissions also support AJAX via `X-Requested-With: XMLHttpRequest` header.

---

## ⚙️ Admin Panel

Visit **http://127.0.0.1:8000/admin** (default: `admin` / `aurum2026`).

The admin is extensively customised:
- **Menu Items**: colour-coded category badges, dietary icon badges, inline thumbnail, live `is_available` toggle
- **Reservations**: status colour badges (pending = orange, confirmed = green, etc.), date hierarchy, confirmation number
- **Events**: thumbnail + display date, featured toggle
- **Gallery**: thumbnail grid, category filter
- **Newsletter**: bulk email export action
- **Contact Messages**: read/unread toggle

---

## 🎨 Design System

```css
/* Gold Palette */
--g:   #C9A96E   /* Primary gold */
--gl:  #E8D4A8   /* Light gold (hover) */
--gd:  #A07840   /* Dark gold */

/* Background Scale */
--b1:  #060606   /* Deepest black */
--b2:  #0C0C0C   /* Section backgrounds */
--b3:  #141414   /* Cards, forms */
--b4:  #1C1C1C   /* Hover states */

/* Text Scale */
--t1:  #EDE4D0   /* Primary text (warm cream) */
--t2:  #A09080   /* Secondary / body text */
--t3:  #5A5040   /* Labels, placeholders */
```

**Fonts:**
- `Cormorant Garamond` — headings, prices, italic accents (elegance, weight 300–700)
- `Jost` — body, UI labels, buttons (clean, modern, weight 200–600)

---

## 🌐 Deployment (Production)

**1. Update `.env`**
```bash
DEBUG=False
SECRET_KEY=<50-char random string>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.your-provider.com
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=your-password
```

**2. Use PostgreSQL** — add `psycopg2-binary` to requirements and set `DATABASE_URL`.

**3. Gunicorn + Nginx** (recommended)
```bash
pip install gunicorn
gunicorn aurum_project.wsgi:application --bind 0.0.0.0:8000
```

**4. SSL** — configure via Nginx + Let's Encrypt (Certbot).

**5. Static & Media** — serve via Nginx or a CDN (S3 + CloudFront recommended for media).

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `Django>=5.0` | Web framework |
| `Pillow` | Image processing for uploads |
| `whitenoise` | Static file serving |
| `python-decouple` | `.env` file configuration |
| `django-cleanup` | Auto-delete old media files on model update |
| `django-crispy-forms` | Enhanced form rendering |

---

## 🙌 Credits

- **Images**: [Unsplash](https://unsplash.com) — fine dining photography
- **Fonts**: [Google Fonts](https://fonts.google.com) — Cormorant Garamond & Jost
- **Framework**: [Django](https://djangoproject.com) — Python web framework

---

*Built with craft and care for those who appreciate the extraordinary.*
