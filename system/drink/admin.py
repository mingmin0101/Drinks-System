from django.contrib import admin
from drink.models import Customer, Supplier, Ingredient, Product, Order, Order_has_product, Product_made_by_ingredient, Ingredient_offerd_by_supplier


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient_name','amount','is_processed')
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_phone','name','gender','points','create_time','latest_order_time')
# Register your models here.
admin.site.register(Customer,CustomerAdmin)
admin.site.register(Supplier)
admin.site.register(Ingredient,IngredientAdmin)
admin.site.register(Product)         
admin.site.register(Order)         
admin.site.register(Order_has_product)         
admin.site.register(Product_made_by_ingredient)         
admin.site.register(Ingredient_offerd_by_supplier)                  
