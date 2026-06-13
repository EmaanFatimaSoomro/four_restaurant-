from django.db import models
from django.utils.text import slugify
from django.utils import timezone


# ─────────────────────────────────────────────────────
#  MENU
# ─────────────────────────────────────────────────────
class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('starters',  'Starters'),
        ('seafood',   'Seafood'),
        ('main',      'Main Course'),
        ('steaks',    'Steaks'),
        ('desserts',  'Desserts'),
        ('beverages', 'Beverages'),
        ('signature', 'Signature'),
        ('seasonal',  'Seasonal Specials'),
    ]

    name          = models.CharField(max_length=200)
    slug          = models.SlugField(unique=True, blank=True)
    category      = models.CharField(max_length=50, choices=CATEGORY_CHOICES, db_index=True)
    description   = models.TextField()
    price         = models.DecimalField(max_digits=8, decimal_places=2)
    image         = models.ImageField(upload_to='menu/', blank=True, null=True)
    image_url     = models.URLField(blank=True, help_text='External image URL (used if no file uploaded)')
    is_vegan      = models.BooleanField(default=False)
    is_halal      = models.BooleanField(default=False)
    is_spicy      = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)
    is_chef_pick  = models.BooleanField(default=False)
    is_featured   = models.BooleanField(default=False, db_index=True)
    is_available  = models.BooleanField(default=True, db_index=True)
    order         = models.PositiveIntegerField(default=0)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'order', 'name']
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'

    def __str__(self):
        return f'{self.get_category_display()} — {self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url or ''

    @property
    def dietary_tags(self):
        tags = []
        if self.is_chef_pick:  tags.append(('pick', "Chef's Pick"))
        if self.is_vegan:      tags.append(('vegan', 'Vegan'))
        if self.is_halal:      tags.append(('halal', 'Halal'))
        if self.is_spicy:      tags.append(('spicy', 'Spicy'))
        if self.is_gluten_free: tags.append(('gf', 'Gluten-Free'))
        return tags

    def to_dict(self):
        return {
            'id': self.pk,
            'name': self.name,
            'category': self.category,
            'category_label': self.get_category_display(),
            'description': self.description,
            'price': str(self.price),
            'price_display': f'${self.price:,.0f}',
            'image': self.get_image,
            'is_vegan': self.is_vegan,
            'is_halal': self.is_halal,
            'is_spicy': self.is_spicy,
            'is_gluten_free': self.is_gluten_free,
            'is_chef_pick': self.is_chef_pick,
            'dietary_tags': self.dietary_tags,
        }


# ─────────────────────────────────────────────────────
#  CHEF
# ─────────────────────────────────────────────────────
class Chef(models.Model):
    name              = models.CharField(max_length=200)
    role              = models.CharField(max_length=200, default='Executive Chef')
    bio               = models.TextField()
    philosophy        = models.TextField(blank=True)
    quote             = models.TextField(blank=True)
    image             = models.ImageField(upload_to='chefs/', blank=True, null=True)
    image_url         = models.URLField(blank=True)
    accent_image      = models.ImageField(upload_to='chefs/', blank=True, null=True)
    accent_image_url  = models.URLField(blank=True)
    years_experience  = models.PositiveIntegerField(default=0)
    michelin_stars    = models.PositiveIntegerField(default=0)
    awards_count      = models.PositiveIntegerField(default=0)
    cookbooks_count   = models.PositiveIntegerField(default=0)
    is_featured       = models.BooleanField(default=True)
    order             = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Chef'

    def __str__(self):
        return self.name

    @property
    def get_image(self):
        return self.image.url if self.image else self.image_url

    @property
    def get_accent_image(self):
        return self.accent_image.url if self.accent_image else self.accent_image_url


# ─────────────────────────────────────────────────────
#  RESERVATION
# ─────────────────────────────────────────────────────
class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('seated',    'Seated'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show',   'No Show'),
    ]
    SEATING_CHOICES = [
        ('main',    'Main Dining Room'),
        ('private', 'Private Room'),
        ('chefs',   "Chef's Table"),
        ('terrace', 'Terrace'),
        ('bar',     'Bar & Lounge'),
    ]
    TIME_CHOICES = [
        ('18:00', '6:00 PM'), ('18:30', '6:30 PM'), ('19:00', '7:00 PM'),
        ('19:30', '7:30 PM'), ('20:00', '8:00 PM'), ('20:30', '8:30 PM'),
        ('21:00', '9:00 PM'), ('21:30', '9:30 PM'), ('22:00', '10:00 PM'),
    ]

    first_name       = models.CharField(max_length=100)
    last_name        = models.CharField(max_length=100)
    email            = models.EmailField()
    phone            = models.CharField(max_length=30, blank=True)
    date             = models.DateField()
    time             = models.CharField(max_length=10, choices=TIME_CHOICES)
    guests           = models.PositiveSmallIntegerField(default=2)
    seating          = models.CharField(max_length=20, choices=SEATING_CHOICES, default='main')
    special_requests = models.TextField(blank=True)
    occasion         = models.CharField(max_length=200, blank=True)
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    confirmation_no  = models.CharField(max_length=12, blank=True, unique=True)
    notes            = models.TextField(blank=True, help_text='Internal staff notes')
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', 'time']
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'

    def __str__(self):
        return f'{self.full_name} — {self.date} at {self.get_time_display()}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        if not self.confirmation_no:
            import random, string
            self.confirmation_no = 'AUR-' + ''.join(random.choices(string.digits, k=6))
        super().save(*args, **kwargs)


# ─────────────────────────────────────────────────────
#  EVENT
# ─────────────────────────────────────────────────────
class Event(models.Model):
    title        = models.CharField(max_length=200)
    slug         = models.SlugField(unique=True, blank=True)
    description  = models.TextField()
    short_desc   = models.CharField(max_length=300, blank=True)
    image        = models.ImageField(upload_to='events/', blank=True, null=True)
    image_url    = models.URLField(blank=True)
    date         = models.DateField(null=True, blank=True)
    time         = models.TimeField(null=True, blank=True)
    date_display = models.CharField(max_length=100, blank=True, help_text='e.g. "Every Friday"')
    price        = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    is_recurring = models.BooleanField(default=False)
    is_featured  = models.BooleanField(default=True)
    is_active    = models.BooleanField(default=True)
    order        = models.PositiveIntegerField(default=0)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'date']
        verbose_name = 'Event'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def get_image(self):
        return self.image.url if self.image else self.image_url

    @property
    def display_date(self):
        if self.date_display:
            return self.date_display
        if self.date:
            return self.date.strftime('%b %d, %Y')
        return 'Date TBA'


# ─────────────────────────────────────────────────────
#  GALLERY
# ─────────────────────────────────────────────────────
class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ('ambiance', 'Restaurant Ambiance'),
        ('food',     'Food Photography'),
        ('events',   'Events'),
        ('team',     'Our Team'),
    ]

    title    = models.CharField(max_length=200, blank=True)
    caption  = models.TextField(blank=True)
    image    = models.ImageField(upload_to='gallery/', blank=True, null=True)
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='food')
    is_featured = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    order    = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'

    def __str__(self):
        return self.title or f'Gallery image #{self.pk}'

    @property
    def get_image(self):
        return self.image.url if self.image else self.image_url


# ─────────────────────────────────────────────────────
#  TESTIMONIAL
# ─────────────────────────────────────────────────────
class Testimonial(models.Model):
    name      = models.CharField(max_length=200)
    role      = models.CharField(max_length=200, blank=True)
    quote     = models.TextField()
    avatar    = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    avatar_url = models.URLField(blank=True)
    rating    = models.PositiveSmallIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)
    order     = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f'{self.name} — {self.quote[:60]}…'

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else self.avatar_url

    @property
    def stars(self):
        return '★' * self.rating


# ─────────────────────────────────────────────────────
#  AWARD
# ─────────────────────────────────────────────────────
class Award(models.Model):
    name        = models.CharField(max_length=200)
    subtitle    = models.CharField(max_length=200, blank=True)
    icon        = models.CharField(max_length=10, default='🏆')
    year_range  = models.CharField(max_length=100, blank=True)
    is_active   = models.BooleanField(default=True)
    order       = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


# ─────────────────────────────────────────────────────
#  NEWSLETTER
# ─────────────────────────────────────────────────────
class NewsletterSubscriber(models.Model):
    email       = models.EmailField(unique=True)
    name        = models.CharField(max_length=100, blank=True)
    is_active   = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = 'Newsletter Subscriber'

    def __str__(self):
        return self.email


# ─────────────────────────────────────────────────────
#  CONTACT MESSAGE
# ─────────────────────────────────────────────────────
class ContactMessage(models.Model):
    name       = models.CharField(max_length=200)
    email      = models.EmailField()
    subject    = models.CharField(max_length=300)
    message    = models.TextField()
    is_read    = models.BooleanField(default=False)
    replied_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'

    def __str__(self):
        return f'{self.name} — {self.subject}'
