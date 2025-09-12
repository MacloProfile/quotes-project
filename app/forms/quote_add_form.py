from django import forms

from app.models.quote import Quote


class QuoteAdd(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['quote', 'source', 'weight']
