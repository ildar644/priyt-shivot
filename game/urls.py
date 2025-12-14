from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    PetListView, PetDetailView, help_info_view, test,
    add_to_favorites, remove_from_favorites, favorites_list,
    sponsor_pet, compare_pets, HappyStoriesListView, 
    HappyStoryDetailView, faq_view, toggle_favorite_ajax,
    signup_view, add_comment, delete_comment,
    adoption_application, my_applications
)

urlpatterns = [
    # Основные страницы
    path('', PetListView.as_view(), name='pet_list'),
    path('pet/<int:pk>/', PetDetailView.as_view(), name='pet_detail'),
    path('help/', help_info_view, name='help_info'),
    path('test/', test, name="main_page"),
    
    # Аутентификация
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', signup_view, name='signup'),
    
    # Избранное
    path('favorites/', favorites_list, name='favorites'),
    path('favorites/add/<int:pet_id>/', add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:pet_id>/', remove_from_favorites, name='remove_from_favorites'),
    path('ajax/favorite/<int:pet_id>/', toggle_favorite_ajax, name='toggle_favorite_ajax'),
    
    # Спонсорство
    path('sponsor/<int:pet_id>/', sponsor_pet, name='sponsor_pet'),
    
    # Сравнение
    path('compare/', compare_pets, name='compare_pets'),
    
    # Счастливые истории
    path('happy-stories/', HappyStoriesListView.as_view(), name='happy_stories'),
    path('happy-stories/<int:pk>/', HappyStoryDetailView.as_view(), name='happy_story_detail'),
    
    # FAQ
    path('faq/', faq_view, name='faq'),
    
    # Комментарии
    path('comment/add/<int:pet_id>/', add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),
    
    # Заявки на усыновление
    path('adopt/<int:pet_id>/', adoption_application, name='adoption_application'),
    path('my-applications/', my_applications, name='my_applications'),
]