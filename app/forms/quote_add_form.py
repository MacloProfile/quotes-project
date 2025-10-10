from django import forms
from app.models.quote import Quote


def _normalize_quotes(text: str) -> str:
    text = text.strip()

    if text and text[0] in ('"', "'", '«', '<') and text[-1] in ('"', "'", '»', '>'):
        text = text[1:-1].strip()

    text = text.rstrip('.').strip()

    replacements = {
        '"': '“',
        "'": '“',
        '‘': '“',
        '’': '”',
        '«': '“',
        '»': '”',
        '<': '“',
        '>': '”',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


class QuoteAdd(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['quote', 'source', 'weight']

    def clean_quote(self):
        quote = self.cleaned_data.get('quote', '')
        return _normalize_quotes(quote)

    def clean_source(self):
        source = self.cleaned_data.get('source', '')
        return _normalize_quotes(source)
