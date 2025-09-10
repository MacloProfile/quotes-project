from django import forms

from app.models import Quote


class QuoteAdd(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['quote', 'source', 'weight']
