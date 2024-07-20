from django.contrib import admin
from .models import UserProfile, MealTime, Medicine

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'name', 'birth_date')
    search_fields = ('user__username', 'name')

@admin.register(MealTime)
class MealTimeAdmin(admin.ModelAdmin):
    list_display = ('user', 'meal_type', 'time')
    search_fields = ('user__username', 'meal_type')

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'time', 'days')
    search_fields = ('user__username', 'name')
