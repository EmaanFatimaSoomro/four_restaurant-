from django import forms
from django.utils import timezone
from .models import Reservation, ContactMessage, NewsletterSubscriber


class ReservationForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'finp', 'id': 'res-date'}),
    )

    class Meta:
        model = Reservation
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'date', 'time', 'guests', 'seating', 'special_requests',
        ]
        widgets = {
            'first_name':       forms.TextInput(attrs={'class': 'finp', 'placeholder': 'James'}),
            'last_name':        forms.TextInput(attrs={'class': 'finp', 'placeholder': 'Anderson'}),
            'email':            forms.EmailInput(attrs={'class': 'finp', 'placeholder': 'james@example.com'}),
            'phone':            forms.TextInput(attrs={'class': 'finp', 'placeholder': '+1 (212) 000-0000'}),
            'time':             forms.Select(attrs={'class': 'finp'}),
            'guests':           forms.Select(attrs={'class': 'finp'},
                                             choices=[(i, f'{i} Guest{"s" if i>1 else ""}') for i in range(1, 13)]),
            'seating':          forms.Select(attrs={'class': 'finp'}),
            'special_requests': forms.Textarea(attrs={
                'class': 'finp', 'rows': 3,
                'placeholder': 'Dietary requirements, celebrations, seating preferences…',
            }),
        }

    def clean_date(self):
        d = self.cleaned_data['date']
        if d < timezone.localdate():
            raise forms.ValidationError("Please select a future date.")
        return d


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name':    forms.TextInput(attrs={'class': 'finp', 'placeholder': 'Your full name'}),
            'email':   forms.EmailInput(attrs={'class': 'finp', 'placeholder': 'your@email.com'}),
            'subject': forms.TextInput(attrs={'class': 'finp', 'placeholder': 'How can we help?'}),
            'message': forms.Textarea(attrs={'class': 'finp', 'rows': 5,
                                             'placeholder': 'Your message…'}),
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'nl-inp', 'placeholder': 'Your email address'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if NewsletterSubscriber.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError("This email is already subscribed.")
        return email
