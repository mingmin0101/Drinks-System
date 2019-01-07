from django.db import models

# entity table
class Customer(models.Model):
    customer_phone = models.CharField(max_length=10)
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=3)
    points = models.DecimalField(max_digits=10, decimal_places=0)
    create_time = models.DateTimeField()
    latest_order_time = models.DateTimeField()  # we have to .save() to change it

    def __str__(self):              
        return self.name

class Supplier(models.Model):
    supplier_name = models.CharField(max_length=20)
    supplier_address = models.CharField(max_length=50, blank=True)
    supplier_phone = models.CharField(max_length=10)

    def __str__(self):              
        return self.supplier_name

class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=5, decimal_places=0)
    is_processed = models.BooleanField(default=False)
    is_sufficient=models.BooleanField(default=False)
    supplier = models.ManyToManyField(Supplier, through='Ingredient_offerd_by_supplier')

    def __str__(self):              
        return self.ingredient_name       

class Product(models.Model):
    product_name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=3, decimal_places=0)
    ingredient = models.ManyToManyField(Ingredient, through='Product_made_by_ingredient')
    
    def __str__(self):              
        return self.product_name

class ROP_Parameters(models.Model):
    ingredient_name = models.CharField(max_length=20)
    LT = models.FloatField()
    d  = models.FloatField()
    sigma = models.FloatField()
    accepted_risk= models.FloatField()
    ROP = models.FloatField(default=0)

class S0_Parameters(models.Model):
    ingredient_name = models.CharField(max_length=20)
    d  = models.FloatField()
    sigma = models.FloatField()
    accepted_risk= models.FloatField()
    S0 = models.FloatField(default=0)

class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=5, decimal_places=0)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through='Order_has_product')

    def __str__(self):              
        return str(self.id)



# relationship table
# https://stackoverflow.com/questions/4443190/djangos-manytomany-relationship-with-additional-fields
class Order_has_product(models.Model):
    cup_size = models.CharField(max_length=10)
    ice_level = models.CharField(max_length=10)
    sugar_level = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=3, decimal_places=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def __str__(self):              
        return "order no." + str(self.order.id) + ", product: " + self.product.product_name 

class Product_made_by_ingredient(models.Model):
    amount = models.DecimalField(max_digits=5, decimal_places=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):              
        return self.product.product_name + self.ingredient.ingredient_name 

class Ingredient_offerd_by_supplier(models.Model):
    date = models.DateTimeField()
    amount = models.DecimalField(max_digits=5, decimal_places=0)
    unit_price = models.DecimalField(max_digits=3, decimal_places=0)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self):              
        return self.supplier.supplier_name + self.ingredient.ingredient_name 