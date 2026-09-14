from django.contrib import admin
from .models import Problem, TestCase


class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 0
    fields = ('input', 'expected', 'is_public', 'order')

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'is_public', 'created_at')
    list_filter = ('difficulty', 'is_public')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TestCaseInline]

@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('problem', 'order', 'is_public')
    list_filter = ('is_public',)