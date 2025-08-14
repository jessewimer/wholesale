from django.db import models

class Product(models.Model):
    item_number = models.IntegerField(null=True, unique=True)
    sku = models.CharField(max_length=11, null=True)
    notes = models.TextField(null=True)
    active = models.CharField(max_length=10, null=True)
    category = models.CharField(max_length=25, null=True)
    super_type = models.CharField(max_length=25, null=True)
    veg_type = models.CharField(max_length=25, null=True)
    sub_type = models.CharField(max_length=25, null=True)
    variety = models.CharField(max_length=30, null=True)
    description = models.TextField(null=True)
    quickbooks_code = models.CharField(max_length=50, null=True)
    photo = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.variety

    @classmethod
    def set_price(cls, price):
        for product in cls.objects.all():
            product.set_price(price)

    def print_products(cls):
        for product in cls.objects.all():
            print(f'Item Number: {product.item_number} -- {product.variety}')





'''
# These are models converted from the tkinter/sqlalchemy database
class Variety(models.Model):
    sku_prefix = models.CharField(max_length=50, primary_key=True)
    var_name = models.CharField(max_length=255, blank=True, null=True)
    crop = models.CharField(max_length=255, blank=True, null=True)
    common_spelling = models.CharField(max_length=255, blank=True, null=True)
    common_name = models.CharField(max_length=255, blank=True, null=True)
    group = models.CharField(max_length=255, blank=True, null=True)
    veg_type = models.CharField(max_length=255, blank=True, null=True)
    species = models.CharField(max_length=255, blank=True, null=True)
    supergroup = models.CharField(max_length=255, blank=True, null=True)
    subtype = models.CharField(max_length=255, blank=True, null=True)
    days = models.CharField(max_length=50, blank=True, null=True)
    active = models.BooleanField(default=True)
    stock_qty = models.CharField(max_length=50, blank=True, null=True)

    desc_line1 = models.TextField(blank=True, null=True)
    desc_line2 = models.TextField(blank=True, null=True)
    desc_line3 = models.TextField(blank=True, null=True)
    back1 = models.TextField(blank=True, null=True)
    back2 = models.TextField(blank=True, null=True)
    back3 = models.TextField(blank=True, null=True)
    back4 = models.TextField(blank=True, null=True)
    back5 = models.TextField(blank=True, null=True)
    back6 = models.TextField(blank=True, null=True)
    back7 = models.TextField(blank=True, null=True)

    wholesale_notes = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.sku_prefix} - {self.var_name or ''}"

        
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    variety = models.ForeignKey(Variety, on_delete=models.CASCADE, related_name="products")
    pkg_size = models.CharField(max_length=50, blank=True, null=True)
    sku_suffix = models.CharField(max_length=50, blank=True, null=True)
    alt_sku = models.CharField(max_length=50, blank=True, null=True)
    lineitem_name = models.CharField(max_length=255, blank=True, null=True)

    rack_location = models.CharField(max_length=100, blank=True, null=True)
    env_type = models.CharField(max_length=50, blank=True, null=True)
    env_multiplier = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    ly_sold_online = models.IntegerField(blank=True, null=True)
    ly_sold_stores = models.IntegerField(blank=True, null=True)

    total_sold_online = models.IntegerField(blank=True, null=True)
    total_sold_stores = models.IntegerField(blank=True, null=True)
    num_printed = models.IntegerField(blank=True, null=True)
    num_printed_next_year = models.IntegerField(default=0)
    scoop_size = models.CharField(max_length=50, blank=True, null=True)
    print_back = models.BooleanField(default=False)
    bulk_pre_pack = models.IntegerField(blank=True, null=True)
    ws_item_num = models.IntegerField(blank=True, null=True)

    is_sub_product = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.variety.sku_prefix} - {self.pkg_size or ''}"


class VarNote(models.Model):
    variety = models.ForeignKey(Variety, on_delete=models.CASCADE, related_name="notes")
    note = models.TextField()
    date = models.DateField(blank=True, null=True)


class VarWholeSaleNotes(models.Model):
    variety = models.ForeignKey(Variety, on_delete=models.CASCADE, related_name="wholesale_notes_list")
    note = models.TextField()
    date = models.DateField(blank=True, null=True)


class ProductNote(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="notes")
    note = models.TextField()
    date = models.DateField(blank=True, null=True)


class RadType(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="rad_type")
    rad_type = models.CharField(max_length=100)


class InitialProductOffering(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="initial_offerings")
    year = models.IntegerField()
    tracked = models.BooleanField(default=False)
    initial_offering = models.IntegerField(default=0)


class Sales(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sales")
    quantity = models.IntegerField()
    year = models.IntegerField()
    wholesale = models.BooleanField(default=False)


class Growout(models.Model):
    variety = models.OneToOneField(Variety, on_delete=models.CASCADE, related_name="growout_info")
    sow_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    notes = models.TextField(blank=True, null=True)


class MiscSale(models.Model):
    variety = models.ForeignKey(Variety, on_delete=models.CASCADE, related_name="misc_sales")
    lbs = models.FloatField()
    date = models.DateField()
    customer = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)


class MiscProduct(models.Model):
    lineitem_name = models.CharField(max_length=255)
    sku = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)   

class LastSelected(models.Model):
    hostname = models.CharField(max_length=255, unique=True)
    variety = models.ForeignKey(Variety, on_delete=models.CASCADE, related_name="last_selected_for")

    class Meta:
        verbose_name_plural = "Last Selected"


'''



