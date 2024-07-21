from django.contrib import admin
from .models import UserProfile, MealTime, Medicine

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'name', 'birth_date', 'get_related_user')
    search_fields = ('user__username', 'name')

    def get_related_user(self, obj):
        if obj.user_type == 'senior':
            return ', '.join([protector.user.username for protector in obj.protectors])
        elif obj.user_type == 'protector':
            return obj.senior_user.username if obj.senior_user else 'None'
        return 'None'
    
    get_related_user.short_description = 'Related User'

@admin.register(MealTime)
class MealTimeAdmin(admin.ModelAdmin):
    list_display = ('user', 'meal_type', 'time')
    search_fields = ('user__username', 'meal_type')

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'time', 'days')
    search_fields = ('user__username', 'name')
