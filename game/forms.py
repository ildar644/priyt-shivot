from django import forms
from .models import Comment, AdoptionApplication


class CommentForm(forms.ModelForm):
    """Форма для добавления комментариев"""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Поделитесь своими впечатлениями о питомце...',
                'class': 'comment-textarea'
            })
        }
        labels = {
            'content': 'Ваш комментарий'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].required = True


class AdoptionApplicationForm(forms.ModelForm):
    """Форма заявки на усыновление"""
    
    class Meta:
        model = AdoptionApplication
        fields = [
            'full_name', 'phone', 'email', 'address',
            'housing_type', 'has_yard', 'other_pets',
            'experience', 'motivation', 'work_schedule',
            'family_members', 'additional_info'
        ]
        
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Иванов Иван Иванович'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7 (999) 123-45-67'}),
            'email': forms.EmailInput(attrs={'placeholder': 'ivan@example.com'}),
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'г. Москва, ул. Примерная, д. 1, кв. 1'}),
            'housing_type': forms.TextInput(attrs={'placeholder': 'Квартира, частный дом, дача...'}),
            'other_pets': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Опишите других питомцев или укажите "нет"'}),
            'experience': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Расскажите о вашем опыте содержания животных'}),
            'motivation': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Почему вы хотите взять именно этого питомца?'}),
            'work_schedule': forms.TextInput(attrs={'placeholder': 'Полный день, удаленная работа, свободный график...'}),
            'family_members': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Состав семьи, возраст детей, отношение к животным'}),
            'additional_info': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Любая дополнительная информация'}),
        }
        
        labels = {
            'full_name': 'Полное имя',
            'phone': 'Телефон',
            'email': 'Email',
            'address': 'Адрес проживания',
            'housing_type': 'Тип жилья',
            'has_yard': 'Есть двор или сад',
            'other_pets': 'Другие питомцы',
            'experience': 'Опыт содержания животных',
            'motivation': 'Мотивация',
            'work_schedule': 'График работы',
            'family_members': 'Состав семьи',
            'additional_info': 'Дополнительная информация',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем некоторые поля обязательными
        required_fields = ['full_name', 'phone', 'email', 'address', 'housing_type', 'experience', 'motivation']
        for field_name in required_fields:
            self.fields[field_name].required = True