from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def smart_truncate(text, max_length=100):
    """Умное обрезание текста с сохранением целых слов"""
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    # Обрезаем до максимальной длины
    truncated = text[:max_length]
    
    # Находим последний пробел, чтобы не обрезать слово посередине
    last_space = truncated.rfind(' ')
    if last_space > max_length * 0.7:  # Если пробел не слишком далеко от конца
        truncated = truncated[:last_space]
    
    return truncated + "..."

@register.filter
def character_preview(text, max_words=8):
    """Превью характера питомца с красивым форматированием"""
    if not text:
        return ""
    
    words = text.split()
    if len(words) <= max_words:
        return text
    
    preview = ' '.join(words[:max_words])
    return preview + "..."

@register.filter
def format_character(text):
    """Форматирование характера для карточки питомца"""
    if not text:
        return ""
    
    # Обрезаем до разумной длины
    if len(text) > 80:
        sentences = text.split('.')
        if len(sentences) > 1 and len(sentences[0]) < 80:
            return sentences[0] + "."
        else:
            return smart_truncate(text, 80)
    
    return text