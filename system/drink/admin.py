from django.contrib import admin
from drink.models import Customer, Supplier, Ingredient, Product, Order, Order_has_product, Product_made_by_ingredient, Ingredient_offerd_by_supplier

# Register your models here.
admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Ingredient)         
admin.site.register(Product)         
admin.site.register(Order)         
admin.site.register(Order_has_product)         
admin.site.register(Product_made_by_ingredient)         
admin.site.register(Ingredient_offerd_by_supplier)                  
