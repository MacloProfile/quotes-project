from django import forms

from app.models.quote import Quote


class QuoteAdd(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['quote', 'source', 'weight']

    def clean(self):
        quote = self.cleaned_data['quote']

        if len(quote) > 300:
            raise forms.ValidationError("Слишком длинная цитата (максимум 300 символов)")

        if len(quote) < 3:
            raise forms.ValidationError("Слишком короткая цитата (минимум 3 символов)")

