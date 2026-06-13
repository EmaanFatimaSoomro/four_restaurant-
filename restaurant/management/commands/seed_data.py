"""
python manage.py seed_data

Populates the database with rich sample content so the site is
immediately ready to preview with no manual data entry required.
"""
from django.core.management.base import BaseCommand
from restaurant.models import (
    MenuItem, Chef, Event, GalleryImage,
    Testimonial, Award, NewsletterSubscriber,
)


MENU = [
    # Starters
    dict(c='starters', n='Foie Gras Terrine', d='Brioche toast points, Sauternes gel, micro herbs, pickled Muscat grapes', p=48, pick=True, img='https://images.unsplash.com/photo-1432139555190-58524dae6a55?w=400&q=80', featured=True),
    dict(c='starters', n='Oysters Rockefeller', d='Six Pacific oysters, wilted spinach cream, crispy pancetta, lemon caviar', p=36, gf=True, img='https://images.unsplash.com/photo-1541529086526-db283c563270?w=400&q=80'),
    dict(c='starters', n='Burrata & Heritage Tomato', d='Buffalo burrata, Sicilian tomatoes, basil oil, aged balsamic, fleur de sel', p=28, vegan=True, gf=True, img='https://images.unsplash.com/photo-1547592180-85f173990554?w=400&q=80'),
    dict(c='starters', n='Wagyu Tartare', d='Hand-cut A5 Wagyu, quail egg yolk, Dijon, capers, brioche crisps', p=52, pick=True, img='https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400&q=80'),
    # Seafood
    dict(c='seafood', n='Pan-Seared Halibut', d='Saffron beurre blanc, cauliflower purée, caperberries, dill oil, micro greens', p=85, gf=True, pick=True, img='https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400&q=80', featured=True),
    dict(c='seafood', n='Maine Lobster Thermidor', d='Half lobster, cognac flambé, gruyère gratin, brandy bisque reduction', p=115, gf=True, img='https://images.unsplash.com/photo-1559339352-11d035aa65de?w=400&q=80', featured=True),
    dict(c='seafood', n='Scottish Salmon Gravlax', d='Dill-cured salmon, crème fraîche, trout roe, rye bread crisp', p=62, gf=True, img='https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=400&q=80'),
    dict(c='seafood', n='Scallops Saint-Jacques', d='Pan-seared hand-dived scallops, cauliflower, pancetta, hazelnut beurre noisette', p=72, gf=True, pick=True, img='https://images.unsplash.com/photo-1534482421-64566f976cfa?w=400&q=80'),
    # Main
    dict(c='main', n='Black Truffle Risotto', d='Carnaroli rice, 36-month Parmigiano-Reggiano, summer black truffle shavings', p=68, vegan=True, gf=True, pick=True, img='https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&q=80', featured=True),
    dict(c='main', n='Duck à l\'Orange', d='Confit duck leg, blood orange gastrique, roasted heritage root vegetables', p=72, gf=True, img='https://images.unsplash.com/photo-1432139509613-5c4255815697?w=400&q=80'),
    dict(c='main', n='Roasted Rack of Lamb', d='French-trimmed rack, pistachio crust, minted jus, gratin dauphinois', p=88, pick=True, img='https://images.unsplash.com/photo-1544025162-d76694265947?w=400&q=80'),
    dict(c='main', n='Stuffed Morel Mushroom', d='Wild morels, herb ricotta, pea purée, truffle foam — plant-forward and deeply satisfying', p=56, vegan=True, gf=True, img='https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=400&q=80'),
    # Steaks
    dict(c='steaks', n='A5 Wagyu Tenderloin', d='Japanese A5 Wagyu 8oz, pomme purée, Périgord black truffle, 12-yr aged jus', p=195, gf=True, pick=True, img='https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=400&q=80', featured=True),
    dict(c='steaks', n='Dry-Aged Ribeye 32oz', d='45-day dry-aged USDA Prime, bone-in, béarnaise sauce, truffle frites', p=145, gf=True, img='https://images.unsplash.com/photo-1600891964092-4316c288032e?w=400&q=80'),
    dict(c='steaks', n='Châteaubriand for Two', d='Centre-cut filet, sauce Périgueux, seasonal vegetables, pomme soufflée', p=220, gf=True, pick=True, img='https://images.unsplash.com/photo-1558030006-450675393462?w=400&q=80'),
    # Desserts
    dict(c='desserts', n='Valrhona Chocolate Soufflé', d='Dark chocolate soufflé, crème anglaise, Tahitian vanilla ice cream, edible gold', p=34, pick=True, img='https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400&q=80', featured=True),
    dict(c='desserts', n='Crêpe Suzette Flambée', d='Grand Marnier tableside flambé, candied orange zest, vanilla ice cream', p=28, img='https://images.unsplash.com/photo-1502301103665-0b95cc738daf?w=400&q=80'),
    dict(c='desserts', n='Mille-Feuille', d='Caramelised puff pastry, pastry cream, raspberry coulis, rose petal', p=26, vegan=True, img='https://images.unsplash.com/photo-1481391319762-47dff72954d9?w=400&q=80'),
    # Signature
    dict(c='signature', n='Aurum 8-Course Tasting Menu', d='Chef Marcus\'s seasonal gastronomic journey — eight exquisite courses with optional wine pairing', p=285, pick=True, img='https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400&q=80', featured=True),
    dict(c='signature', n='Champagne Brunch', d='Weekend brunch with unlimited Veuve Clicquot and seasonal à la carte selections', p=120, img='https://images.unsplash.com/photo-1551183053-bf91798d43bc?w=400&q=80'),
    dict(c='signature', n='Wine & Dine Pairing', d='Five courses with matched wines from our grand cru cellar, guided by sommelier Élise', p=195, pick=True, img='https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=400&q=80'),
]

EVENTS = [
    dict(
        title='Jazz & Fine Dining Evening',
        desc='Surrender to the soulful melodies of our resident jazz quartet while savouring the seasonal tasting menu — a perfect weekly ritual.',
        short='Live jazz every Friday with the seasonal tasting menu.',
        date_display='Every Friday — 8:00 PM',
        img='https://images.unsplash.com/photo-1530103862676-de8c9debad1d?w=700&q=80',
        recurring=True,
    ),
    dict(
        title='Bordeaux Grand Cru Tasting',
        desc='A curated journey through rare Bordeaux vintages expertly guided by our master sommelier, with exclusive canape pairings throughout.',
        short='Rare Bordeaux vintages with matched canapes.',
        date_display='Jun 28, 2026 — 7:00 PM',
        img='https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=700&q=80',
    ),
    dict(
        title='Private Dining & Celebrations',
        desc='Celebrate life\'s most precious moments in our exclusive private dining rooms, thoughtfully tailored to your every wish.',
        short='Exclusive rooms for intimate celebrations.',
        date_display='Available Year-Round',
        img='https://images.unsplash.com/photo-1519671282429-b44660ead0a7?w=700&q=80',
        recurring=True,
    ),
    dict(
        title='Chef\'s Table Experience',
        desc='An exclusive eight-seat dining experience in the heart of our kitchen, watching Chef Marcus and his brigade create your meal course by course.',
        short='Front-row seats in the kitchen.',
        date_display='Every Saturday — 7:00 PM',
        img='https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=700&q=80',
        recurring=True,
    ),
]

GALLERY = [
    ('ambiance', 'Dining Room', 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=900&q=80'),
    ('food',     'A5 Wagyu',   'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=700&q=80'),
    ('food',     'Lobster',    'https://images.unsplash.com/photo-1559339352-11d035aa65de?w=700&q=80'),
    ('ambiance', 'Wine Room',  'https://images.unsplash.com/photo-1551183053-bf91798d43bc?w=700&q=80'),
    ('food',     'Soufflé',   'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=700&q=80'),
    ('ambiance', 'Bar',        'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=700&q=80'),
]

TESTIMONIALS = [
    dict(n='Victoria Ashworth',  r='Food Critic, New York Times',      q="An extraordinary dining experience that transcends the ordinary. Chef Marcus's tasting menu was nothing short of a spiritual journey through flavours I never thought possible.", av='https://images.unsplash.com/photo-1494790108755-2616b1b9b4f8?w=100&q=80'),
    dict(n='James Worthington',  r='CEO, Worthington Capital Group',   q="From the first amuse-bouche to the final petit four, every detail at Aurum is perfection. This is what fine dining was always meant to be.", av='https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&q=80'),
    dict(n='Sophie & Richard Laurent', r='Loyal Guests Since 2016',    q="We celebrated our 10th anniversary here and it will forever be one of the most beautiful evenings of our lives. The attention to every detail is simply breathtaking.", av='https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&q=80'),
    dict(n='Dr. Marcus Chen',    r='Wine Enthusiast & Surgeon',        q="The wine pairing by sommelier Élise was a masterclass in itself. Each bottle told a story that harmonised perfectly with Chef Marcus's exquisite creations.", av='https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&q=80'),
    dict(n='Lord Edward Pemberton', r='Michelin Guide Consultant',     q="I've dined at the world's finest tables and Aurum stands among the very best. The A5 Wagyu was the finest cut of beef I have tasted in four decades of dining.", av='https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&q=80'),
]

AWARDS = [
    dict(name='Michelin Stars',         sub='3 Stars Awarded',         icon='⭐', yr='2021 · 2022 · 2023 · 2024'),
    dict(name='James Beard Award',      sub='Outstanding Restaurant',  icon='🏆', yr='2023'),
    dict(name="World's 50 Best",        sub='Ranked #12 Globally',     icon='🌍', yr='2024'),
    dict(name='Wine Spectator',         sub='Grand Award',             icon='🍷', yr='2022–2024'),
    dict(name='Forbes Travel Guide',    sub='Five-Star Rating',        icon='📰', yr='2023–2024'),
]


class Command(BaseCommand):
    help = 'Seed the database with rich sample restaurant content'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Seeding database…'))

        # Chef
        if not Chef.objects.exists():
            Chef.objects.create(
                name='Marcus Beaumont',
                role='Executive Chef & Culinary Director',
                bio=(
                    'Trained under legendary mentors in Paris and Kyoto, Chef Marcus brings over '
                    'two decades of mastery to each plate. His philosophy bridges classical French '
                    'technique with bold contemporary vision — resulting in a cuisine that is both '
                    'timeless and startlingly modern.'
                ),
                quote=(
                    '"Cooking is not mere sustenance. It is an act of love — a story told through '
                    'flavors, a canvas where every ingredient sings of the earth it came from."'
                ),
                years_experience=22,
                michelin_stars=3,
                awards_count=14,
                cookbooks_count=4,
                image_url='https://images.unsplash.com/photo-1577219491135-ce391730fb2c?w=800&q=80',
                accent_image_url='https://images.unsplash.com/photo-1581299894007-aaa50297cf16?w=600&q=80',
            )
            self.stdout.write('  ✓ Chef created')

        # Menu items
        if not MenuItem.objects.exists():
            for i, m in enumerate(MENU):
                MenuItem.objects.create(
                    name=m['n'], category=m['c'], description=m['d'],
                    price=m['p'], image_url=m.get('img', ''),
                    is_chef_pick=m.get('pick', False),
                    is_vegan=m.get('vegan', False),
                    is_halal=m.get('halal', False),
                    is_spicy=m.get('spicy', False),
                    is_gluten_free=m.get('gf', False),
                    is_featured=m.get('featured', False),
                    order=i,
                )
            self.stdout.write(f'  ✓ {len(MENU)} menu items created')

        # Events
        if not Event.objects.exists():
            for i, e in enumerate(EVENTS):
                Event.objects.create(
                    title=e['title'], description=e['desc'],
                    short_desc=e.get('short', ''),
                    date_display=e['date_display'],
                    image_url=e.get('img', ''),
                    is_recurring=e.get('recurring', False),
                    order=i,
                )
            self.stdout.write(f'  ✓ {len(EVENTS)} events created')

        # Gallery
        if not GalleryImage.objects.exists():
            for i, (cat, title, url) in enumerate(GALLERY):
                GalleryImage.objects.create(
                    title=title, category=cat, image_url=url, order=i
                )
            self.stdout.write(f'  ✓ {len(GALLERY)} gallery images created')

        # Testimonials
        if not Testimonial.objects.exists():
            for i, t in enumerate(TESTIMONIALS):
                Testimonial.objects.create(
                    name=t['n'], role=t['r'], quote=t['q'],
                    avatar_url=t.get('av', ''), rating=5, order=i,
                )
            self.stdout.write(f'  ✓ {len(TESTIMONIALS)} testimonials created')

        # Awards
        if not Award.objects.exists():
            for i, a in enumerate(AWARDS):
                Award.objects.create(
                    name=a['name'], subtitle=a['sub'],
                    icon=a['icon'], year_range=a['yr'], order=i,
                )
            self.stdout.write(f'  ✓ {len(AWARDS)} awards created')

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!\n'))
