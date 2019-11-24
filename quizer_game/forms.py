from django import forms
from .models import Quiz, Question, Choice

# class QuizForm(forms.Form):
#     topic = forms.CharField(max_length=200)


class QuizModelForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['topic']
        widgets = {'topic': forms.TextInput(attrs={'class': 'form-control'}),
                   }

    def clean_title(self):
        title = self.cleaned_data.get('topic')
        if title.lower() == 'abc':
            raise forms.ValidationError("this is not valid title")
        return title


class QuestionModelForm(forms.ModelForm):
    class Meta:

        model = Question
        fields = ['text']
        widgets = {'text': forms.TextInput(attrs={'class': 'form-control'}),
                   }
    def clean_text(self):
        text = self.cleaned_data.get('text')
        if text.lower() == 'abc':
            raise forms.ValidationError("this is not valid title")
        return text




