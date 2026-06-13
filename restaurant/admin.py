from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import (
    MenuItem, Chef, Reservation, Event, GalleryImage,
    Testimonial, Award, NewsletterSubscriber, ContactMessage,
)


# ── helpers ──────────────────────────────────────────
def thumb(url, size=60):
    if url:
        return format_html('<img src="{}" style="width:{}px;height:{}px;object-fit:cover;border-radius:3px">', url, size, size)
    return '—'


# ── MenuItem ──────────────────────────────────────────
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display  = ('thumb_preview', 'name', 'category_badge', 'price_fmt',
                     'dietary_badges', 'is_featured', 'is_available', 'order')
    list_filter   = ('category', 'is_featured', 'is_available', 'is_chef_pick',
                     'is_vegan', 'is_halal', 'is_gluten_free')
    search_fields = ('name', 'description')
    list_editable = ('is_featured', 'is_available', 'order')
    prepopulated_fields = {'slug': ('name',)}
    ordering      = ('category', 'order')
    list_per_page = 25

    fieldsets = (
        ('Item Information', {
            'fields': ('name', 'slug', 'category', 'description', 'price')
        }),
        ('Media', {
            'fields': ('image', 'image_url'),
        }),
        ('Dietary & Flags', {
            'fields': (('is_vegan', 'is_halal', 'is_spicy', 'is_gluten_free'),
                       ('is_chef_pick', 'is_featured', 'is_available', 'order')),
        }),
    )

    @admin.display(description='Preview')
    def thumb_preview(self, obj):
        return thumb(obj.get_image)

    @admin.display(description='Category')
    def category_badge(self, obj):
        colours = {
            'starters': '#6c8ebf', 'seafood': '#4da6a8', 'main': '#82b366',
            'steaks': '#d6b656', 'desserts': '#e8a0b4', 'beverages': '#9d84c0',
            'signature': '#c9a96e', 'seasonal': '#82a67d',
        }
        c = colours.get(obj.category, '#999')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 10px;border-radius:12px;font-size:11px;font-weight:500">{}</span>',
            c, obj.get_category_display()
        )

    @admin.display(description='Price')
    def price_fmt(self, obj):
        return format_html('<strong style="color:#C9A96E">${}</strong>', f'{obj.price:,.0f}')

    @admin.display(description='Dietary')
    def dietary_badges(self, obj):
        badges = []
        if obj.is_chef_pick:  badges.append(('⭐', '#C9A96E'))
        if obj.is_vegan:      badges.append(('🌿', '#4caf50'))
        if obj.is_halal:      badges.append(('H', '#2196f3'))
        if obj.is_spicy:      badges.append(('🌶', '#f44336'))
        if obj.is_gluten_free: badges.append(('GF', '#ff9800'))
        html = ' '.join(
            f'<span style="background:{c};color:#fff;padding:1px 7px;border-radius:10px;font-size:10px">{b}</span>'
            for b, c in badges
        )
        return mark_safe(html) if html else '—'


# ── Chef ─────────────────────────────────────────────
@admin.register(Chef)
class ChefAdmin(admin.ModelAdmin):
    list_display  = ('thumb_preview', 'name', 'role', 'years_experience',
                     'michelin_stars', 'is_featured')
    list_editable = ('is_featured',)

    @admin.display(description='Photo')
    def thumb_preview(self, obj):
        return thumb(obj.get_image)


# ── Reservation ───────────────────────────────────────
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display  = ('confirmation_no', 'full_name_display', 'date', 'time_display',
                 'guests', 'seating', 'status', 'status_badge', 'created_at')
    list_filter   = ('status', 'seating', 'date')
    search_fields = ('first_name', 'last_name', 'email', 'confirmation_no')
    list_editable = ('status',)
    date_hierarchy = 'date'
    ordering      = ('-date', 'time')
    readonly_fields = ('confirmation_no', 'created_at', 'updated_at')

    fieldsets = (
        ('Guest', {
            'fields': (('first_name', 'last_name'), ('email', 'phone'))
        }),
        ('Booking', {
            'fields': (('date', 'time'), ('guests', 'seating'), 'special_requests')
        }),
        ('Status', {
            'fields': (('status', 'confirmation_no'), 'notes', ('created_at', 'updated_at'))
        }),
    )

    @admin.display(description='Guest')
    def full_name_display(self, obj):
        return format_html('<strong>{}</strong><br><small style="color:#888">{}</small>',
                           obj.full_name, obj.email)

    @admin.display(description='Time')
    def time_display(self, obj):
        return obj.get_time_display()

    @admin.display(description='Status')
    def status_badge(self, obj):
        colours = {
            'pending': '#ff9800', 'confirmed': '#4caf50', 'seated': '#2196f3',
            'completed': '#9e9e9e', 'cancelled': '#f44336', 'no_show': '#795548',
        }
        c = colours.get(obj.status, '#999')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 10px;border-radius:12px;font-size:11px">{}</span>',
            c, obj.get_status_display()
        )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


# ── Event ─────────────────────────────────────────────
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display  = ('thumb_preview', 'title', 'display_date_display', 'is_featured', 'is_active', 'order')
    list_editable = ('is_featured', 'is_active', 'order')
    prepopulated_fields = {'slug': ('title',)}

    @admin.display(description='Image')
    def thumb_preview(self, obj):
        return thumb(obj.get_image)

    @admin.display(description='Date')
    def display_date_display(self, obj):
        return obj.display_date


# ── GalleryImage ──────────────────────────────────────
@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display  = ('thumb_preview', 'title', 'category', 'is_featured', 'is_active', 'order')
    list_editable = ('is_featured', 'is_active', 'order')
    list_filter   = ('category',)

    @admin.display(description='Preview')
    def thumb_preview(self, obj):
        return thumb(obj.get_image)


# ── Testimonial ───────────────────────────────────────
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display  = ('thumb_preview', 'name', 'role', 'star_display', 'is_featured', 'is_active', 'order')
    list_editable = ('is_featured', 'is_active', 'order')

    @admin.display(description='Avatar')
    def thumb_preview(self, obj):
        return thumb(obj.get_avatar, 46)

    @admin.display(description='Rating')
    def star_display(self, obj):
        return format_html('<span style="color:#C9A96E;letter-spacing:2px">{}</span>', obj.stars)


# ── Award ─────────────────────────────────────────────
@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display  = ('icon', 'name', 'subtitle', 'year_range', 'is_active', 'order')
    list_editable = ('is_active', 'order')


# ── Newsletter ────────────────────────────────────────
@admin.register(NewsletterSubscriber)
class NewsletterAdmin(admin.ModelAdmin):
    list_display  = ('email', 'name', 'is_active', 'subscribed_at')
    list_filter   = ('is_active',)
    search_fields = ('email', 'name')
    readonly_fields = ('subscribed_at',)
    actions = ['export_emails']

    @admin.action(description='Export selected emails to console')
    def export_emails(self, request, queryset):
        emails = list(queryset.values_list('email', flat=True))
        self.message_user(request, f'Emails: {", ".join(emails)}')


# ── ContactMessage ────────────────────────────────────
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter   = ('is_read',)
    search_fields = ('name', 'email', 'subject')
    list_editable = ('is_read',)
    readonly_fields = ('created_at',)
