from django import forms

PAYMENT = {
    ('C', 'Карта'),
    ('Q', 'Qiwi'),
}


class CheckoutForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Andrey',
        'class': 'form-control',
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '+7 (999) 123 4567',
        'class': 'form-control',
    }))
    telegram = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'form-control',
    }), required=False)
    payment = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT)
