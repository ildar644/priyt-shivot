from django.contrib import admin
from .models import (PetType, Shelter, Pet, HelpInfo, Favorite, 
                     Sponsorship, HappyStory, FAQ, PetComparison, Comment, AdoptionApplication, PaymentInfo)


@admin.register(PetType)
class PetTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email']
    search_fields = ['name', 'address']
    list_filter = ['name']


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'pet_type', 'age_in_years', 'shelter', 'is_adopted', 'date_added']
    list_filter = ['pet_type', 'shelter', 'is_adopted', 'date_added']
    search_fields = ['name', 'character']
    readonly_fields = ['date_added']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'pet_type', 'age', 'photo', 'shelter')
        }),
        ('Подробности', {
            'fields': ('history', 'character', 'special_needs')
        }),
        ('Статус', {
            'fields': ('is_adopted', 'date_added')
        }),
    )


@admin.register(HelpInfo)
class HelpInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'content']
    list_editable = ['order', 'is_active']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'pet', 'date_added']
    list_filter = ['date_added', 'pet__pet_type']
    search_fields = ['user__username', 'pet__name']


@admin.register(Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
    list_display = ['user', 'pet', 'sponsorship_type', 'amount', 'date_created', 'is_active']
    list_filter = ['sponsorship_type', 'is_active', 'date_created']
    search_fields = ['user__username', 'pet__name']
    list_editable = ['is_active']


@admin.register(HappyStory)
class HappyStoryAdmin(admin.ModelAdmin):
    list_display = ['pet', 'title', 'new_owner_name', 'adoption_date', 'is_published']
    list_filter = ['is_published', 'adoption_date']
    search_fields = ['pet__name', 'title', 'new_owner_name']
    list_editable = ['is_published']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['question', 'answer']
    list_editable = ['order', 'is_active']


@admin.register(PetComparison)
class PetComparisonAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_created']
    list_filter = ['date_created']
    search_fields = ['user__username']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'pet', 'content_preview', 'date_created', 'is_approved']
    list_filter = ['is_approved', 'date_created', 'pet__pet_type']
    search_fields = ['user__username', 'pet__name', 'content']
    list_editable = ['is_approved']
    readonly_fields = ['date_created']
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Превью комментария"


@admin.register(AdoptionApplication)
class AdoptionApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'pet', 'status', 'date_created', 'phone']
    list_filter = ['status', 'date_created', 'pet__pet_type', 'has_yard']
    search_fields = ['full_name', 'phone', 'email', 'pet__name']
    list_editable = ['status']
    readonly_fields = ['date_created', 'date_updated']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('pet', 'user', 'status', 'date_created', 'date_updated')
        }),
        ('Контактные данные', {
            'fields': ('full_name', 'phone', 'email', 'address')
        }),
        ('Жилищные условия', {
            'fields': ('housing_type', 'has_yard', 'other_pets')
        }),
        ('Опыт и мотивация', {
            'fields': ('experience', 'motivation', 'work_schedule', 'family_members')
        }),
        ('Дополнительно', {
            'fields': ('additional_info', 'admin_notes')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('pet', 'user')


@admin.register(PaymentInfo)
class PaymentInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'payment_type', 'is_active', 'order']
    list_filter = ['payment_type', 'is_active']
    search_fields = ['title', 'recipient_name', 'card_number']
    list_editable = ['is_active', 'order']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'payment_type', 'description', 'is_active', 'order')
        }),
        ('Банковские реквизиты', {
            'fields': ('recipient_name', 'inn', 'kpp', 'account_number', 'bank_name', 'bik', 'payment_purpose'),
            'classes': ('collapse',),
            'description': 'Заполняется для банковских переводов'
        }),
        ('Карта/Кошелек/СБП', {
            'fields': ('card_number', 'card_holder', 'phone_number'),
            'classes': ('collapse',),
            'description': 'Заполняется для карт, кошельков и СБП'
        }),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Добавляем help_text для полей
        form.base_fields['payment_type'].help_text = "Выберите тип платежа для отображения соответствующих полей"
        return form
