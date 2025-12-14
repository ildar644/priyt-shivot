from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class PetType(models.Model):
    """Модель для типов питомцев (кошка, собака и т.д.)"""
    name = models.CharField(max_length=50, verbose_name="Тип питомца")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    class Meta:
        verbose_name = "Тип питомца"
        verbose_name_plural = "Типы питомцев"
    
    def __str__(self):
        return self.name


class Shelter(models.Model):
    """Модель приюта"""
    name = models.CharField(max_length=200, verbose_name="Название приюта")
    address = models.TextField(verbose_name="Адрес")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    website = models.URLField(blank=True, verbose_name="Веб-сайт")
    description = models.TextField(verbose_name="Описание приюта")
    
    class Meta:
        verbose_name = "Приют"
        verbose_name_plural = "Приюты"
    
    def __str__(self):
        return self.name


class Pet(models.Model):
    """Модель питомца"""
    name = models.CharField(max_length=100, verbose_name="Кличка")
    age = models.PositiveIntegerField(verbose_name="Возраст (месяцы)")
    photo = models.ImageField(upload_to='pets/', verbose_name="Фотография")
    history = models.TextField(verbose_name="История питомца")
    character = models.TextField(verbose_name="Характер")
    special_needs = models.TextField(blank=True, verbose_name="Особенности")
    is_adopted = models.BooleanField(default=False, verbose_name="Усыновлен")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    
    # Внешние ключи
    pet_type = models.ForeignKey(
        PetType, 
        on_delete=models.CASCADE, 
        verbose_name="Тип питомца"
    )
    shelter = models.ForeignKey(
        Shelter, 
        on_delete=models.CASCADE, 
        verbose_name="Приют"
    )
    
    class Meta:
        verbose_name = "Питомец"
        verbose_name_plural = "Питомцы"
        ordering = ['-date_added']
    
    def __str__(self):
        return f"{self.name} ({self.pet_type.name})"
    
    def get_absolute_url(self):
        return reverse('pet_detail', kwargs={'pk': self.pk})
    
    @property
    def age_in_years(self):
        """Возраст в годах и месяцах"""
        years = self.age // 12
        months = self.age % 12
        if years > 0:
            return f"{years} г. {months} мес."
        return f"{months} мес."


class HelpInfo(models.Model):
    """Модель для информации о способах помощи приюту"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    
    class Meta:
        verbose_name = "Информация о помощи"
        verbose_name_plural = "Информация о помощи"
        ordering = ['order']
    
    def __str__(self):
        return self.title


class Favorite(models.Model):
    """Модель избранных питомцев"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name="Питомец")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    
    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        unique_together = ['user', 'pet']
    
    def __str__(self):
        return f"{self.user.username} - {self.pet.name}"


class Sponsorship(models.Model):
    """Модель виртуального опекунства"""
    SPONSORSHIP_TYPES = [
        ('food', 'Корм'),
        ('medical', 'Лечение'),
        ('toys', 'Игрушки'),
        ('general', 'Общая поддержка'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Спонсор")
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name="Питомец")
    sponsorship_type = models.CharField(max_length=20, choices=SPONSORSHIP_TYPES, verbose_name="Тип помощи")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    message = models.TextField(blank=True, verbose_name="Сообщение питомцу")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    
    class Meta:
        verbose_name = "Спонсорство"
        verbose_name_plural = "Спонсорство"
        ordering = ['-date_created']
    
    def __str__(self):
        return f"{self.user.username} -> {self.pet.name} ({self.get_sponsorship_type_display()})"


class HappyStory(models.Model):
    """Модель счастливых историй"""
    pet = models.OneToOneField(Pet, on_delete=models.CASCADE, verbose_name="Питомец")
    title = models.CharField(max_length=200, verbose_name="Заголовок истории")
    story = models.TextField(verbose_name="История")
    new_owner_name = models.CharField(max_length=100, verbose_name="Имя нового хозяина")
    adoption_date = models.DateField(verbose_name="Дата усыновления")
    photo_after = models.ImageField(upload_to='happy_stories/', verbose_name="Фото в новом доме")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Счастливая история"
        verbose_name_plural = "Счастливые истории"
        ordering = ['-date_created']
    
    def __str__(self):
        return f"{self.pet.name} - {self.title}"


class FAQ(models.Model):
    """Модель часто задаваемых вопросов"""
    question = models.CharField(max_length=300, verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")
    category = models.CharField(max_length=100, verbose_name="Категория")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    
    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"
        ordering = ['category', 'order']
    
    def __str__(self):
        return self.question


class PetComparison(models.Model):
    """Модель для сравнения питомцев"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    pets = models.ManyToManyField(Pet, verbose_name="Питомцы для сравнения")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Сравнение питомцев"
        verbose_name_plural = "Сравнения питомцев"
    
    def __str__(self):
        return f"Сравнение от {self.user.username}"


class Comment(models.Model):
    """Модель комментариев к питомцам"""
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='comments', verbose_name="Питомец")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    content = models.TextField(verbose_name="Комментарий")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_approved = models.BooleanField(default=True, verbose_name="Одобрен")
    
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-date_created']
    
    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}..."


class AdoptionApplication(models.Model):
    """Модель заявки на усыновление"""
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('approved', 'Одобрена'),
        ('rejected', 'Отклонена'),
        ('completed', 'Завершена'),
    ]
    
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='applications', verbose_name="Питомец")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Заявитель")
    
    # Контактная информация
    full_name = models.CharField(max_length=200, verbose_name="Полное имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    address = models.TextField(verbose_name="Адрес проживания")
    
    # Информация о жилье
    housing_type = models.CharField(max_length=100, verbose_name="Тип жилья")
    has_yard = models.BooleanField(default=False, verbose_name="Есть двор/сад")
    other_pets = models.TextField(blank=True, verbose_name="Другие питомцы")
    
    # Опыт и мотивация
    experience = models.TextField(verbose_name="Опыт содержания животных")
    motivation = models.TextField(verbose_name="Почему хотите взять этого питомца")
    
    # Дополнительная информация
    work_schedule = models.CharField(max_length=200, verbose_name="График работы")
    family_members = models.TextField(verbose_name="Состав семьи")
    additional_info = models.TextField(blank=True, verbose_name="Дополнительная информация")
    
    # Статус заявки
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    admin_notes = models.TextField(blank=True, verbose_name="Заметки администратора")
    
    # Даты
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата подачи")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Заявка на усыновление"
        verbose_name_plural = "Заявки на усыновление"
        ordering = ['-date_created']
        unique_together = ['pet', 'user']  # Один пользователь - одна заявка на питомца
    
    def __str__(self):
        return f"{self.full_name} → {self.pet.name} ({self.get_status_display()})"


class PaymentInfo(models.Model):
    """Модель для банковских реквизитов и способов оплаты"""
    PAYMENT_TYPES = [
        ('bank', 'Банковский перевод'),
        ('card', 'Банковская карта'),
        ('sbp', 'СБП'),
        ('wallet', 'Электронный кошелек'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Название")
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES, verbose_name="Тип платежа")
    
    # Банковские реквизиты
    recipient_name = models.CharField(max_length=300, blank=True, verbose_name="Получатель")
    inn = models.CharField(max_length=20, blank=True, verbose_name="ИНН")
    kpp = models.CharField(max_length=20, blank=True, verbose_name="КПП")
    account_number = models.CharField(max_length=50, blank=True, verbose_name="Расчетный счет")
    bank_name = models.CharField(max_length=200, blank=True, verbose_name="Банк")
    bik = models.CharField(max_length=20, blank=True, verbose_name="БИК")
    payment_purpose = models.CharField(max_length=300, blank=True, verbose_name="Назначение платежа")
    
    # Карта/кошелек
    card_number = models.CharField(max_length=50, blank=True, verbose_name="Номер карты/кошелька")
    card_holder = models.CharField(max_length=200, blank=True, verbose_name="Держатель карты")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Номер телефона")
    
    # Дополнительная информация
    description = models.TextField(blank=True, verbose_name="Описание")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")
    
    class Meta:
        verbose_name = "Способ оплаты"
        verbose_name_plural = "Способы оплаты"
        ordering = ['order', 'title']
    
    def __str__(self):
        return f"{self.title} ({self.get_payment_type_display()})"
    
    def get_copy_text(self):
        """Возвращает текст для копирования в зависимости от типа платежа"""
        if self.payment_type == 'bank':
            return f"""Получатель: {self.recipient_name}
ИНН: {self.inn}
КПП: {self.kpp}
Расчетный счет: {self.account_number}
Банк: {self.bank_name}
БИК: {self.bik}
Назначение платежа: {self.payment_purpose}"""
        elif self.payment_type == 'card':
            return self.card_number.replace(' ', '')
        elif self.payment_type == 'sbp':
            return self.phone_number
        elif self.payment_type == 'wallet':
            return self.card_number
        return ""
