from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import (Pet, HelpInfo, Favorite, Sponsorship, 
                     HappyStory, FAQ, PetComparison, Comment, AdoptionApplication, PaymentInfo)
from .forms import CommentForm, AdoptionApplicationForm


class PetListView(ListView):
    """Главная страница со списком питомцев"""
    model = Pet
    template_name = 'pets/pet_list.html'
    context_object_name = 'pets'
    paginate_by = 12
    
    def get_queryset(self):
        return Pet.objects.filter(is_adopted=False).select_related('pet_type', 'shelter')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Получаем список ID избранных питомцев для текущего пользователя
            favorite_pet_ids = Favorite.objects.filter(
                user=self.request.user
            ).values_list('pet_id', flat=True)
            context['favorite_pet_ids'] = list(favorite_pet_ids)
        else:
            context['favorite_pet_ids'] = []
        return context


class PetDetailView(DetailView):
    """Страница отдельного питомца"""
    model = Pet
    template_name = 'pets/pet_detail.html'
    context_object_name = 'pet'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Проверяем, есть ли питомец в избранном у текущего пользователя
            context['is_favorite'] = Favorite.objects.filter(
                user=self.request.user, 
                pet=self.object
            ).exists()
        else:
            context['is_favorite'] = False
        
        # Добавляем комментарии и форму
        context['comments'] = Comment.objects.filter(
            pet=self.object, 
            is_approved=True
        ).select_related('user')
        
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
            
            # Проверяем, подавал ли пользователь заявку на этого питомца
            context['user_application'] = AdoptionApplication.objects.filter(
                pet=self.object, user=self.request.user
            ).first()
        
        return context


def help_info_view(request):
    """Страница 'Как помочь приюту?'"""
    help_items = HelpInfo.objects.filter(is_active=True)
    payment_methods = PaymentInfo.objects.filter(is_active=True).order_by('order', 'title')
    
    return render(request, 'pets/help_info.html', {
        'help_items': help_items,
        'payment_methods': payment_methods
    })


def test(request):
    return render(request, "index.html")


# Система избранного
@login_required
def add_to_favorites(request, pet_id):
    """Добавить питомца в избранное"""
    pet = get_object_or_404(Pet, id=pet_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, pet=pet)
    
    if created:
        messages.success(request, f'{pet.name} добавлен в избранное!')
    else:
        messages.info(request, f'{pet.name} уже в избранном!')
    
    return redirect('pet_detail', pk=pet_id)


@login_required
def remove_from_favorites(request, pet_id):
    """Удалить питомца из избранного"""
    pet = get_object_or_404(Pet, id=pet_id)
    try:
        favorite = Favorite.objects.get(user=request.user, pet=pet)
        favorite.delete()
        messages.success(request, f'{pet.name} удален из избранного!')
    except Favorite.DoesNotExist:
        messages.error(request, 'Питомец не найден в избранном!')
    
    return redirect('pet_detail', pk=pet_id)


@login_required
def favorites_list(request):
    """Список избранных питомцев"""
    favorites = Favorite.objects.filter(user=request.user).select_related('pet')
    return render(request, 'pets/favorites.html', {'favorites': favorites})


# Виртуальное опекунство
@login_required
def sponsor_pet(request, pet_id):
    """Страница спонсорства питомца"""
    pet = get_object_or_404(Pet, id=pet_id)
    
    if request.method == 'POST':
        sponsorship_type = request.POST.get('sponsorship_type')
        amount = request.POST.get('amount')
        message = request.POST.get('message', '')
        
        Sponsorship.objects.create(
            user=request.user,
            pet=pet,
            sponsorship_type=sponsorship_type,
            amount=amount,
            message=message
        )
        
        messages.success(request, f'Спасибо за помощь {pet.name}! Ваша поддержка очень важна.')
        return redirect('pet_detail', pk=pet_id)
    
    return render(request, 'pets/sponsor.html', {'pet': pet})


# Сравнение питомцев
def compare_pets(request):
    """Страница сравнения питомцев"""
    pet_ids = request.GET.getlist('pets')
    pets = Pet.objects.filter(id__in=pet_ids, is_adopted=False)
    
    if len(pets) < 2:
        messages.error(request, 'Выберите минимум 2 питомцев для сравнения!')
        return redirect('pet_list')
    
    return render(request, 'pets/compare.html', {'pets': pets})


# Счастливые истории
class HappyStoriesListView(ListView):
    """Список счастливых историй"""
    model = HappyStory
    template_name = 'pets/happy_stories.html'
    context_object_name = 'stories'
    paginate_by = 6
    
    def get_queryset(self):
        return HappyStory.objects.filter(is_published=True)


class HappyStoryDetailView(DetailView):
    """Детали счастливой истории"""
    model = HappyStory
    template_name = 'pets/happy_story_detail.html'
    context_object_name = 'story'


# FAQ
def faq_view(request):
    """Страница FAQ"""
    faqs = FAQ.objects.filter(is_active=True)
    categories = faqs.values_list('category', flat=True).distinct()
    
    faq_by_category = {}
    for category in categories:
        faq_by_category[category] = faqs.filter(category=category)
    
    return render(request, 'pets/faq.html', {'faq_by_category': faq_by_category})


# AJAX для избранного
@login_required
def toggle_favorite_ajax(request, pet_id):
    """AJAX переключение избранного"""
    pet = get_object_or_404(Pet, id=pet_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, pet=pet)
    
    if not created:
        favorite.delete()
        is_favorite = False
        message = f'{pet.name} удален из избранного'
    else:
        is_favorite = True
        message = f'{pet.name} добавлен в избранное'
    
    return JsonResponse({
        'is_favorite': is_favorite,
        'message': message
    })


# Регистрация пользователя
def signup_view(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('pet_list')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})


# Комментарии
@login_required
def add_comment(request, pet_id):
    """Добавление комментария к питомцу"""
    pet = get_object_or_404(Pet, id=pet_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.pet = pet
            comment.user = request.user
            comment.save()
            messages.success(request, 'Ваш комментарий добавлен!')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    
    return redirect('pet_detail', pk=pet_id)


@login_required
def delete_comment(request, comment_id):
    """Удаление комментария (только автор может удалить)"""
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.user == request.user:
        pet_id = comment.pet.id
        comment.delete()
        messages.success(request, 'Комментарий удален!')
    else:
        messages.error(request, 'Вы можете удалять только свои комментарии!')
    
    return redirect('pet_detail', pk=comment.pet.id)


# Заявки на усыновление
@login_required
def adoption_application(request, pet_id):
    """Страница подачи заявки на усыновление"""
    pet = get_object_or_404(Pet, id=pet_id)
    
    # Проверяем, не подавал ли пользователь уже заявку на этого питомца
    existing_application = AdoptionApplication.objects.filter(
        pet=pet, user=request.user
    ).first()
    
    if existing_application:
        messages.info(request, f'Вы уже подали заявку на {pet.name}. Статус: {existing_application.get_status_display()}')
        return redirect('pet_detail', pk=pet_id)
    
    if request.method == 'POST':
        form = AdoptionApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.pet = pet
            application.user = request.user
            application.save()
            messages.success(request, f'Заявка на усыновление {pet.name} подана! Мы свяжемся с вами в ближайшее время.')
            return redirect('pet_detail', pk=pet_id)
    else:
        form = AdoptionApplicationForm()
    
    return render(request, 'pets/adoption_application.html', {
        'pet': pet,
        'form': form
    })


@login_required
def my_applications(request):
    """Список заявок пользователя"""
    applications = AdoptionApplication.objects.filter(
        user=request.user
    ).select_related('pet').order_by('-date_created')
    
    return render(request, 'pets/my_applications.html', {
        'applications': applications
    })