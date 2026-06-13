import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import (
    MenuItem, Chef, Reservation, Event, GalleryImage,
    Testimonial, Award, NewsletterSubscriber, ContactMessage,
)
from .forms import ReservationForm, ContactForm, NewsletterForm


# ─────────────────────────────────────────────────────
#  HOME
# ─────────────────────────────────────────────────────
def home(request):
    ctx = {
        'page': 'home',
        'featured_dishes':  MenuItem.objects.filter(is_featured=True, is_available=True)[:4],
        'chef':             Chef.objects.filter(is_featured=True).first(),
        'testimonials':     Testimonial.objects.filter(is_active=True, is_featured=True)[:6],
        'awards':           Award.objects.filter(is_active=True),
        'events':           Event.objects.filter(is_active=True, is_featured=True)[:3],
        'gallery_images':   GalleryImage.objects.filter(is_active=True, is_featured=True)[:6],
        'reservation_form': ReservationForm(),
        'newsletter_form':  NewsletterForm(),
    }
    return render(request, 'restaurant/home.html', ctx)


# ─────────────────────────────────────────────────────
#  MENU PAGE
# ─────────────────────────────────────────────────────
def menu(request):
    active_cat = request.GET.get('category', 'all')
    qs = MenuItem.objects.filter(is_available=True)
    if active_cat != 'all':
        qs = qs.filter(category=active_cat)

    ctx = {
        'page':            'menu',
        'menu_items':      qs,
        'categories':      MenuItem.CATEGORY_CHOICES,
        'active_category': active_cat,
        'newsletter_form': NewsletterForm(),
    }
    return render(request, 'restaurant/menu.html', ctx)


# ─────────────────────────────────────────────────────
#  AJAX — MENU FILTER
# ─────────────────────────────────────────────────────
@require_GET
def api_menu(request):
    category = request.GET.get('category', 'all')
    search   = request.GET.get('q', '').strip()

    qs = MenuItem.objects.filter(is_available=True)
    if category != 'all':
        qs = qs.filter(category=category)
    if search:
        qs = qs.filter(name__icontains=search) | qs.filter(description__icontains=search)

    return JsonResponse({'items': [item.to_dict() for item in qs], 'count': qs.count()})


# ─────────────────────────────────────────────────────
#  RESERVATION
# ─────────────────────────────────────────────────────
def reservation(request):
    form = ReservationForm()

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if form.is_valid():
            res = form.save()
            _send_reservation_email(res)

            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'message': f'Thank you, {res.first_name}! Reservation #{res.confirmation_no} received.',
                    'confirmation': res.confirmation_no,
                })
            messages.success(request,
                f'Thank you, {res.first_name}! Your reservation (#{res.confirmation_no}) has been received. '
                'We will confirm within 24 hours.')
            return redirect('reservation_success')

        if is_ajax:
            return JsonResponse({'success': False, 'errors': form.errors}, status=422)

    ctx = {'page': 'reservation', 'form': form, 'newsletter_form': NewsletterForm()}
    return render(request, 'restaurant/reservation.html', ctx)


def reservation_success(request):
    return render(request, 'restaurant/reservation_success.html',
                  {'page': 'reservation', 'newsletter_form': NewsletterForm()})


def _send_reservation_email(res):
    try:
        send_mail(
            subject=f'New Reservation #{res.confirmation_no} — {res.full_name}',
            message=(
                f'Reservation #{res.confirmation_no}\n\n'
                f'Name:     {res.full_name}\n'
                f'Email:    {res.email}\n'
                f'Phone:    {res.phone or "—"}\n'
                f'Date:     {res.date}\n'
                f'Time:     {res.get_time_display()}\n'
                f'Guests:   {res.guests}\n'
                f'Seating:  {res.get_seating_display()}\n'
                f'Requests: {res.special_requests or "—"}\n'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.RESERVATION_EMAIL],
            fail_silently=True,
        )
    except Exception:
        pass


# ─────────────────────────────────────────────────────
#  ABOUT
# ─────────────────────────────────────────────────────
def about(request):
    ctx = {
        'page': 'about',
        'newsletter_form': NewsletterForm(),
    }
    return render(request, 'restaurant/about.html', ctx)


# ─────────────────────────────────────────────────────
#  CHEF
# ─────────────────────────────────────────────────────
def chef(request):
    chefs = Chef.objects.all().order_by('order')
    ctx = {
        'page': 'chef',
        'chefs': chefs,
        'chef': chefs.filter(is_featured=True).first(),
        'newsletter_form': NewsletterForm(),
    }
    return render(request, 'restaurant/chef.html', ctx)


# ─────────────────────────────────────────────────────
#  EVENTS
# ─────────────────────────────────────────────────────
def events(request):
    ctx = {
        'page': 'events',
        'events': Event.objects.filter(is_active=True),
        'newsletter_form': NewsletterForm(),
    }
    return render(request, 'restaurant/events.html', ctx)


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug, is_active=True)
    ctx = {
        'page': 'events',
        'event': event,
        'other_events': Event.objects.filter(is_active=True).exclude(pk=event.pk)[:3],
        'reservation_form': ReservationForm(),
        'newsletter_form': NewsletterForm(),
    }
    return render(request, 'restaurant/event_detail.html', ctx)


# ─────────────────────────────────────────────────────
#  GALLERY
# ─────────────────────────────────────────────────────
def gallery(request):
    cat = request.GET.get('cat', 'all')
    qs  = GalleryImage.objects.filter(is_active=True)
    if cat != 'all':
        qs = qs.filter(category=cat)
    ctx = {
        'page':       'gallery',
        'images':     qs,
        'categories': GalleryImage.CATEGORY_CHOICES,
        'active_cat': cat,
        'newsletter_form': NewsletterForm(),
    }
    return render(request, 'restaurant/gallery.html', ctx)


# ─────────────────────────────────────────────────────
#  CONTACT
# ─────────────────────────────────────────────────────
def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if form.is_valid():
            msg = form.save()
            if is_ajax:
                return JsonResponse({'success': True, 'message': 'Message received! We\'ll respond within 24 hours.'})
            messages.success(request, 'Your message has been received. We\'ll be in touch shortly.')
            return redirect('contact')
        if is_ajax:
            return JsonResponse({'success': False, 'errors': form.errors}, status=422)
    ctx = {'page': 'contact', 'form': form, 'newsletter_form': NewsletterForm()}
    return render(request, 'restaurant/contact.html', ctx)


# ─────────────────────────────────────────────────────
#  AJAX — NEWSLETTER
# ─────────────────────────────────────────────────────
@require_POST
def api_newsletter(request):
    try:
        data  = json.loads(request.body)
        email = data.get('email', '').strip().lower()
    except (json.JSONDecodeError, AttributeError):
        email = request.POST.get('email', '').strip().lower()

    if not email or '@' not in email:
        return JsonResponse({'success': False, 'message': 'Please enter a valid email address.'}, status=400)

    obj, created = NewsletterSubscriber.objects.get_or_create(
        email=email, defaults={'is_active': True}
    )
    if not created:
        if obj.is_active:
            return JsonResponse({'success': False, 'message': 'This email is already subscribed.'})
        obj.is_active = True
        obj.save()

    return JsonResponse({'success': True, 'message': 'Welcome to the FOUR Family!'})


# ─────────────────────────────────────────────────────
#  ERROR PAGES
# ─────────────────────────────────────────────────────
def page_not_found(request, exception=None):
    return render(request, '404.html', status=404)

def server_error(request):
    return render(request, '500.html', status=500)