from django.contrib import admin
from .models import Quiz, Question, Choice, Player, Timer

from .models import Quiz, Question, Choice, Player

# Register your models here.


class QuestionInline(admin.TabularInline):
    model = Question
    show_change_link = True


class ChoiceInline(admin.TabularInline):
    model = Choice


class TimerInline(admin.TabularInline):
    model = Timer


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('topic', )
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('number', 'text', 'quiz')
    list_filter = ('quiz',)
    list_display_links = ('text', )
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'value', 'question')
    list_filter = ('question',)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'quiz', 'is_achieved', 'is_failed', 'time')
    list_filter = ('name', 'quiz', 'is_achieved', 'is_failed')
    fields = ['name', ('quiz', 'selected_difficulty'), ('current_question', 'position'),
              ('is_playing', 'is_achieved', 'is_failed')]
    inlines = [TimerInline]


@admin.register(Timer)
class TimerAdmin(admin.ModelAdmin):
    list_display = ('start_point', 'end_point', 'player')
