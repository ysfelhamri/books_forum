from django import forms
from .models import User, Review, Recommendation, Discussion, Rating, Reply
from django.contrib.auth.forms import UserCreationForm
from books.models import Book
from django.forms.widgets import FileInput

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=10)
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('review', 'verdict', 'chapters_read_on_review', )

    def __init__(self, *args, **kwargs):
        self.book = kwargs.pop('book', None)
        super().__init__(*args, **kwargs)

    def clean_chapters_read_on_review(self):
        chapters_read = self.cleaned_data.get('chapters_read_on_review')
        if chapters_read < 0:
            raise forms.ValidationError("The number of chapters read cannot be negative.")
        if self.book and chapters_read > self.book.chapters:
            raise forms.ValidationError(f'The number of chapters read cannot exceed the total number of chapters in the book ({self.book.chapters}).')
        return chapters_read

class RecommendationForm(forms.ModelForm):
    book_recommended = forms.ModelChoiceField(
        queryset=Book.objects.none(),  # Initial empty queryset
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        label='Recommend a Book'
    )

    class Meta:
        model = Recommendation
        fields = ('book_recommended', 'recommendation')

    def __init__(self, *args, **kwargs):
        book_original = kwargs.pop('book_original', None)
        super().__init__(*args, **kwargs)
        if book_original:
            self.fields['book_recommended'].queryset = Book.objects.exclude(id=book_original.id)

    def clean_book_recommended(self):
        book_recommended = self.cleaned_data.get('book_recommended')
        book_original = self.initial.get('book_original')
        if book_recommended == book_original:
            raise forms.ValidationError("You cannot recommend the same book.")
        return book_recommended
    
class DiscussionForm(forms.ModelForm):
    starting_topic = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Discussion
        fields = ('title', 'discussion_type', 'starting_topic')


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score', 'chapters', 'volumes', 'status']  
        widgets = {
            'volumes': forms.NumberInput(attrs={'class': 'small-input'}),
            'chapters': forms.NumberInput(attrs={'class': 'small-input'}),
            'score': forms.Select(attrs={'class': 'small-input'}),
            'status': forms.Select(attrs={'class': 'small-input'}),
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('reply', )
        widgets = {
            'reply': forms.Textarea(attrs={'rows': 8}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'birthday', 'image', 'about']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }