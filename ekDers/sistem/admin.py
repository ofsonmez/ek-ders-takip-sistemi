from django.contrib import admin
from .models import  Profile, BolumBaskani, Dersler

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['Name', 'Sicil']

    def Name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'

    def Sicil(self, obj):
        return obj.user.username

class BolumBaskaniAdmin(admin.ModelAdmin):
    list_display =  ['ad', 'bolum']

    class Meta:
        model = BolumBaskani

class DerslerAdmin(admin.ModelAdmin):
    list_display = ['dersiVeren', 'dersKodu', 'dersAdı', 'dersKredisi']

    class Meta:
        model = Dersler

admin.site.register(Profile, ProfileAdmin)
admin.site.register(BolumBaskani, BolumBaskaniAdmin)
admin.site.register(Dersler, DerslerAdmin)