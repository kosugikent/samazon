from django.db import models

from django.contrib.auth.hashers import check_password, make_password


class DatedModel(models.Model):
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # DatedModelは単体で使用するのではなく、他のモデルに継承されて使用されることを表す。
        abstract = True


class User(DatedModel):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True, error_messages={'unique': '使用済みメールアドレスです'})
    postal_code = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    deleted_at = models.DateTimeField(blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    backend = models.CharField(max_length=100, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)

    def cart_total_amount(self):
        return sum(cart.sum() for cart in self.carts.all())


class MajorCategory(DatedModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Category(DatedModel):
    major_category = models.ForeignKey(MajorCategory, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        # 商品登録画面のカテゴリー一覧に表示される、カテゴリーの表示名を表す
        return self.name


class Product(DatedModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    photo = models.ImageField()
    is_recommended = models.BooleanField(default=False)


class Cart(DatedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='carts')
    qty = models.IntegerField()

    def sum(self):
        return self.product.price * self.qty


class Favorite(DatedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')


class Review(DatedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField()
    body = models.TextField()

    @property
    def score_star(self):
        return '★' * self.score


class Order(DatedModel):
    payment_intent_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.IntegerField()


class PurchaseHistory(DatedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='purchase_histories')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchase_histories')
    qty = models.IntegerField()
    amount = models.IntegerField()
