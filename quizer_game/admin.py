from django.contrib import admin

from .models import Quiz, Question, Choice, Player

# Register your models here.

# admin.site.register(Quiz)
# admin.site.register(Question)
# admin.site.register(Choice)
# admin.site.register(Player)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('topic', )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'number', 'quiz')
    list_filter = ('quiz',)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'value', 'question')
    list_filter = ('question',)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'quiz', 'is_achieved', 'is_failed', 'time')
    list_filter = ('name', 'quiz', 'is_achieved', 'is_failed')
