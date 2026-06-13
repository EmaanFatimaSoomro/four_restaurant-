from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Customise admin site
admin.site.site_header  = settings.ADMIN_SITE_HEADER
admin.site.site_title   = settings.ADMIN_SITE_TITLE
admin.site.index_title  = settings.ADMIN_INDEX_TITLE

urlpatterns = [
    path('admin/', admin.site.urls),
    path('portal/', include('four_admin.urls', namespace='four_admin')),
    path('', include('restaurant.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'restaurant.views.page_not_found'
handler500 = 'restaurant.views.server_error'