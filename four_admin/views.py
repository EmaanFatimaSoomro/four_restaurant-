from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Avg, Count
from django.utils import timezone

from restaurant.models import (
    MenuItem, Chef, Reservation, Event, GalleryImage,
    Testimonial, NewsletterSubscriber, ContactMessage,
)

# ── Access control ────────────────────────────────────
def is_staff(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

staff_required = user_passes_test(is_staff, login_url='four_admin:login')

def admin_login_required(view_func):
    return login_required(staff_required(view_func), login_url='four_admin:login')


# ── Context helper ────────────────────────────────────
def base_ctx():
    return {
        'pending_reservations': Reservation.objects.filter(status='pending').count(),
        'pending_reviews':      Testimonial.objects.filter(is_active=False).count(),
        'unread_messages':      ContactMessage.objects.filter(is_read=False).count() if hasattr(ContactMessage, 'is_read') else 0,
    }


# ── LOGIN / LOGOUT ────────────────────────────────────
def admin_login(request):
    if request.user.is_authenticated and is_staff(request.user):
        return redirect('four_admin:dashboard')
    error = None
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user and is_staff(user):
            login(request, user)
            return redirect('four_admin:dashboard')
        error = 'Invalid credentials or insufficient permissions.'
    return render(request, 'four_admin/login.html', {'error': error})


def admin_logout(request):
    logout(request)
    return redirect('four_admin:login')


# ── DASHBOARD ─────────────────────────────────────────
@admin_login_required
def dashboard(request):
    menu_by_cat = {}
    for item in MenuItem.objects.filter(is_available=True).values('category').annotate(c=Count('id')):
        menu_by_cat[item['category']] = item['c']

    ctx = {
        **base_ctx(),
        'active': 'dashboard',
        'total_menu_items':   MenuItem.objects.count(),
        'total_reservations': Reservation.objects.count(),
        'total_subscribers':  NewsletterSubscriber.objects.filter(is_active=True).count(),
        'total_messages':     ContactMessage.objects.count(),
        'total_gallery':      GalleryImage.objects.count(),
        'featured_gallery':   GalleryImage.objects.filter(is_featured=True).count(),
        'total_events':       Event.objects.count(),
        'total_reviews':      Testimonial.objects.count(),
        'avg_rating':         Testimonial.objects.aggregate(a=Avg('rating'))['a'] or 0,
        'recent_reservations': Reservation.objects.order_by('-created_at')[:6],
        'recent_messages':     ContactMessage.objects.order_by('-created_at')[:6],
        'menu_by_category':    menu_by_cat,
    }
    return render(request, 'four_admin/dashboard.html', ctx)


# ── MENU ──────────────────────────────────────────────
@admin_login_required
def menu_list(request):
    qs = MenuItem.objects.all()
    if request.GET.get('category'):
        qs = qs.filter(category=request.GET['category'])
    if request.GET.get('available') == '1':
        qs = qs.filter(is_available=True)
    elif request.GET.get('available') == '0':
        qs = qs.filter(is_available=False)
    if request.GET.get('q'):
        qs = qs.filter(name__icontains=request.GET['q'])
    ctx = {**base_ctx(), 'active': 'menu', 'menu_items': qs, 'categories': MenuItem.CATEGORY_CHOICES}
    return render(request, 'four_admin/menu_list.html', ctx)


@admin_login_required
def menu_add(request):
    if request.method == 'POST':
        item = MenuItem()
        _save_menu_item(item, request)
        messages.success(request, f'"{item.name}" added successfully.')
        return redirect('four_admin:menu_list')
    ctx = {**base_ctx(), 'active': 'menu', 'categories': MenuItem.CATEGORY_CHOICES,
           'flags': [('is_available','Available',True),('is_featured','Featured',False),('is_chef_pick','Chef Pick',False),('is_vegetarian','Vegetarian',False),('is_spicy','Spicy',False)]}
    return render(request, 'four_admin/menu_form.html', ctx)


@admin_login_required
def menu_edit(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        _save_menu_item(item, request)
        messages.success(request, f'"{item.name}" updated.')
        return redirect('four_admin:menu_list')
    ctx = {**base_ctx(), 'active': 'menu', 'item': item, 'categories': MenuItem.CATEGORY_CHOICES,
           'flags': [('is_available','Available',item.is_available),('is_featured','Featured',item.is_featured),('is_chef_pick','Chef Pick',getattr(item,'is_chef_pick',False)),('is_vegetarian','Vegetarian',getattr(item,'is_vegetarian',False)),('is_spicy','Spicy',getattr(item,'is_spicy',False))]}
    return render(request, 'four_admin/menu_form.html', ctx)


def _save_menu_item(item, request):
    p = request.POST
    item.name        = p.get('name', '')
    item.category    = p.get('category', '')
    item.price       = p.get('price', 0)
    item.description = p.get('description', '')
    item.allergens   = p.get('allergens', '')
    if p.get('calories'):
        item.calories = int(p['calories'])
    item.is_available  = 'is_available' in p
    item.is_featured   = 'is_featured' in p
    item.is_chef_pick  = 'is_chef_pick' in p
    item.is_vegetarian = 'is_vegetarian' in p
    item.is_spicy      = 'is_spicy' in p
    if 'image' in request.FILES:
        item.image = request.FILES['image']
    item.save()


@admin_login_required
def menu_delete(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    item.delete()
    messages.success(request, 'Item deleted.')
    return redirect('four_admin:menu_list')


# ── RESERVATIONS ──────────────────────────────────────
@admin_login_required
def reservations(request):
    qs = Reservation.objects.order_by('-created_at')
    active_status = request.GET.get('status', '')
    if active_status:
        qs = qs.filter(status=active_status)
    if request.GET.get('date'):
        qs = qs.filter(date=request.GET['date'])

    status_tabs = [
        ('',          'All',       Reservation.objects.count()),
        ('pending',   'Pending',   Reservation.objects.filter(status='pending').count()),
        ('confirmed', 'Confirmed', Reservation.objects.filter(status='confirmed').count()),
        ('seated',    'Seated',    Reservation.objects.filter(status='seated').count()),
        ('completed', 'Completed', Reservation.objects.filter(status='completed').count()),
        ('cancelled', 'Cancelled', Reservation.objects.filter(status='cancelled').count()),
    ]
    ctx = {**base_ctx(), 'active': 'reservations', 'reservations': qs,
           'active_status': active_status, 'status_tabs': status_tabs}
    return render(request, 'four_admin/reservations.html', ctx)


@admin_login_required
def reservation_detail(request, pk):
    r = get_object_or_404(Reservation, pk=pk)
    ctx = {**base_ctx(), 'active': 'reservations', 'r': r}
    return render(request, 'four_admin/reservation_detail.html', ctx)


@admin_login_required
def reservation_status(request, pk):
    if request.method == 'POST':
        r = get_object_or_404(Reservation, pk=pk)
        r.status = request.POST.get('status', r.status)
        r.save()
        messages.success(request, f'Reservation #{r.confirmation_no} status updated.')
    return redirect('four_admin:reservations')


@admin_login_required
def reservation_delete(request, pk):
    get_object_or_404(Reservation, pk=pk).delete()
    messages.success(request, 'Reservation deleted.')
    return redirect('four_admin:reservations')


# ── EVENTS ────────────────────────────────────────────
@admin_login_required
def events(request):
    ctx = {**base_ctx(), 'active': 'events', 'events': Event.objects.order_by('-created_at')}
    return render(request, 'four_admin/events.html', ctx)


@admin_login_required
def events_add(request):
    if request.method == 'POST':
        e = Event()
        _save_event(e, request)
        messages.success(request, f'Event "{e.title}" added.')
        return redirect('four_admin:events')
    ctx = {**base_ctx(), 'active': 'events'}
    return render(request, 'four_admin/event_form.html', ctx)


@admin_login_required
def events_edit(request, pk):
    e = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        _save_event(e, request)
        messages.success(request, f'Event "{e.title}" updated.')
        return redirect('four_admin:events')
    ctx = {**base_ctx(), 'active': 'events', 'event': e}
    return render(request, 'four_admin/event_form.html', ctx)


def _save_event(e, request):
    p = request.POST
    e.title       = p.get('title', '')
    e.description = p.get('description', '')
    e.date        = p.get('date') or None
    e.time        = p.get('time') or None
    e.location    = p.get('location', '')
    e.price       = p.get('price') or 0
    e.is_active   = 'is_active' in p
    e.is_featured = 'is_featured' in p
    if 'image' in request.FILES:
        e.image = request.FILES['image']
    if not e.slug:
        from django.utils.text import slugify
        e.slug = slugify(e.title)
    e.save()


@admin_login_required
def events_delete(request, pk):
    get_object_or_404(Event, pk=pk).delete()
    messages.success(request, 'Event deleted.')
    return redirect('four_admin:events')


# ── GALLERY ───────────────────────────────────────────
@admin_login_required
def gallery(request):
    ctx = {**base_ctx(), 'active': 'gallery',
           'images': GalleryImage.objects.order_by('order', 'id'),
           'categories': GalleryImage.CATEGORY_CHOICES}
    return render(request, 'four_admin/gallery.html', ctx)


@admin_login_required
def gallery_add(request):
    if request.method == 'POST':
        img = GalleryImage()
        img.title       = request.POST.get('title', '')
        img.category    = request.POST.get('category', '')
        img.is_active   = 'is_active' in request.POST
        img.is_featured = 'is_featured' in request.POST
        if 'image' in request.FILES:
            img.image = request.FILES['image']
        img.save()
        messages.success(request, 'Image added.')
        return redirect('four_admin:gallery')
    ctx = {**base_ctx(), 'active': 'gallery', 'categories': GalleryImage.CATEGORY_CHOICES}
    return render(request, 'four_admin/gallery_form.html', ctx)


@admin_login_required
def gallery_delete(request, pk):
    get_object_or_404(GalleryImage, pk=pk).delete()
    messages.success(request, 'Image deleted.')
    return redirect('four_admin:gallery')


# ── STAFF / CHEFS ─────────────────────────────────────
@admin_login_required
def staff(request):
    ctx = {**base_ctx(), 'active': 'staff', 'chefs': Chef.objects.order_by('order')}
    return render(request, 'four_admin/staff.html', ctx)


@admin_login_required
def staff_add(request):
    if request.method == 'POST':
        c = Chef()
        _save_chef(c, request)
        messages.success(request, f'"{c.name}" added.')
        return redirect('four_admin:staff')
    ctx = {**base_ctx(), 'active': 'staff'}
    return render(request, 'four_admin/staff_form.html', ctx)


@admin_login_required
def staff_edit(request, pk):
    c = get_object_or_404(Chef, pk=pk)
    if request.method == 'POST':
        _save_chef(c, request)
        messages.success(request, f'"{c.name}" updated.')
        return redirect('four_admin:staff')
    ctx = {**base_ctx(), 'active': 'staff', 'chef': c}
    return render(request, 'four_admin/staff_form.html', ctx)


def _save_chef(c, request):
    p = request.POST
    c.name             = p.get('name', '')
    c.role             = p.get('role', '')
    c.bio              = p.get('bio', '')
    c.quote            = p.get('quote', '')
    c.years_experience = p.get('years_experience', 0) or 0
    c.order            = p.get('order', 0) or 0
    c.is_featured      = 'is_featured' in p
    if 'image' in request.FILES:
        c.image = request.FILES['image']
    c.save()


@admin_login_required
def staff_delete(request, pk):
    get_object_or_404(Chef, pk=pk).delete()
    messages.success(request, 'Staff member removed.')
    return redirect('four_admin:staff')


# ── REVIEWS (Testimonials) ────────────────────────────
@admin_login_required
def reviews(request):
    qs = Testimonial.objects.order_by('-created_at')
    if request.GET.get('status') == 'pending':
        qs = qs.filter(is_active=False)
    elif request.GET.get('status') == 'active':
        qs = qs.filter(is_active=True)
    ctx = {**base_ctx(), 'active': 'reviews', 'reviews': qs}
    return render(request, 'four_admin/reviews.html', ctx)


@admin_login_required
def review_toggle(request, pk):
    t = get_object_or_404(Testimonial, pk=pk)
    t.is_active = not t.is_active
    t.save()
    messages.success(request, f'Review {"approved" if t.is_active else "hidden"}.')
    return redirect('four_admin:reviews')


@admin_login_required
def review_delete(request, pk):
    get_object_or_404(Testimonial, pk=pk).delete()
    messages.success(request, 'Review deleted.')
    return redirect('four_admin:reviews')


# ── NEWSLETTER ────────────────────────────────────────
@admin_login_required
def newsletter(request):
    qs = NewsletterSubscriber.objects.order_by('-subscribed_at')
    if request.GET.get('status') == 'active':
        qs = qs.filter(is_active=True)
    elif request.GET.get('status') == 'inactive':
        qs = qs.filter(is_active=False)
    ctx = {**base_ctx(), 'active': 'newsletter',
           'subscribers': qs,
           'total_active': NewsletterSubscriber.objects.filter(is_active=True).count()}
    return render(request, 'four_admin/newsletter.html', ctx)


# ── MESSAGES ──────────────────────────────────────────
@admin_login_required
def messages_list(request):
    qs = ContactMessage.objects.order_by('-created_at')
    ctx = {**base_ctx(), 'active': 'messages', 'messages': qs}
    return render(request, 'four_admin/messages.html', ctx)


@admin_login_required
def message_detail(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if hasattr(msg, 'is_read') and not msg.is_read:
        msg.is_read = True
        msg.save()
    ctx = {**base_ctx(), 'active': 'messages', 'msg': msg}
    return render(request, 'four_admin/message_detail.html', ctx)


@admin_login_required
def message_delete(request, pk):
    get_object_or_404(ContactMessage, pk=pk).delete()
    messages.success(request, 'Message deleted.')
    return redirect('four_admin:messages_list')