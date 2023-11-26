from django.contrib import admin
from naivebaker_app.models import Contact,Recipe,Profile,save_recipe

# Register your models here.
admin.site.register(Contact)
admin.site.register(Recipe)
admin.site.register(Profile)
admin.site.register(save_recipe)