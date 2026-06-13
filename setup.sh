#!/usr/bin/env bash
# ╔══════════════════════════════════════════════════╗
#   AURUM Fine Dining — Django Setup Script
#   Run: bash setup.sh
# ╚══════════════════════════════════════════════════╝

set -e
GREEN='\033[0;32m' GOLD='\033[0;33m' NC='\033[0m'
log() { echo -e "${GOLD}[AURUM]${NC} $1"; }
ok()  { echo -e "${GREEN}  ✓ $1${NC}"; }

echo ""
echo -e "${GOLD}  ░█████╗░██╗░░░██╗██████╗░██╗░░░██╗███╗░░░███╗${NC}"
echo -e "${GOLD}  ██╔══██╗██║░░░██║██╔══██╗██║░░░██║████╗░████║${NC}"
echo -e "${GOLD}  ███████║██║░░░██║██████╔╝██║░░░██║██╔████╔██║${NC}"
echo -e "${GOLD}  ██╔══██║██║░░░██║██╔══██╗██║░░░██║██║╚██╔╝██║${NC}"
echo -e "${GOLD}  ██║░░██║╚██████╔╝██║░░██║╚██████╔╝██║░╚═╝░██║${NC}"
echo -e "${GOLD}  ╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝░╚═════╝░╚═╝░░░░╚═╝${NC}"
echo -e "         Fine Dining Restaurant — Django Setup"
echo ""

# 1. Virtual environment
log "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate
ok "Virtual environment ready"

# 2. Install packages
log "Installing Python packages..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
ok "Packages installed"

# 3. Environment file
if [ ! -f .env ]; then
  log "Creating .env file..."
  cat > .env <<'ENVEOF'
SECRET_KEY=django-insecure-aurum-replace-this-with-a-real-secret-key-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
ENVEOF
  ok ".env created"
fi

# 4. Migrations
log "Running database migrations..."
python manage.py makemigrations --verbosity=0
python manage.py migrate --verbosity=0
ok "Database ready"

# 5. Seed data
log "Seeding sample restaurant data..."
python manage.py seed_data
ok "Sample data loaded"

# 6. Static files
log "Collecting static files..."
python manage.py collectstatic --noinput --verbosity=0
ok "Static files collected"

# 7. Superuser
echo ""
log "Creating admin superuser..."
echo "  Username: admin  |  Email: admin@aurum.nyc"
echo "  (You can change this later in /admin/)"
python manage.py createsuperuser \
  --username admin \
  --email admin@aurum.nyc \
  --noinput 2>/dev/null || true
# Set password to 'aurum2026'
python manage.py shell -c "
from django.contrib.auth import get_user_model
U = get_user_model()
u = U.objects.filter(username='admin').first()
if u:
    u.set_password('aurum2026')
    u.save()
    print('  Password set to: aurum2026')
" 2>/dev/null
ok "Admin user ready"

echo ""
echo -e "${GOLD}══════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅  AURUM is ready!${NC}"
echo -e "${GOLD}══════════════════════════════════════════════${NC}"
echo ""
echo "  🌐  Website:  http://127.0.0.1:8000"
echo "  🔧  Admin:    http://127.0.0.1:8000/admin"
echo "  👤  User:     admin  |  Password: aurum2026"
echo ""
echo -e "  Run: ${GOLD}source venv/bin/activate && python manage.py runserver${NC}"
echo ""
