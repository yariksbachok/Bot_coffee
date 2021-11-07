from django.db import models

# Create your models here.

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Goods(models.Model):
    name = models.TextField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    price_first = models.IntegerField(blank=True, null=True)
    price_second = models.IntegerField(blank=True, null=True)
    link_photo = models.TextField(blank=True, null=True)
    main = models.TextField(blank=True, null=True)
    id_goods = models.AutoField(primary_key=True, blank=True)

    class Meta:
        managed = False
        db_table = 'goods'


class GroupMsg(models.Model):
    id_user = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_msg = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group_msg'


class PollsGoods(models.Model):
    name = models.CharField(max_length=200)
    info = models.CharField(max_length=10000)
    price_first = models.CharField(max_length=1000)
    price_second = models.CharField(max_length=1000)
    link_photo = models.CharField(max_length=1000)
    main = models.CharField(max_length=1000)
    id_goods = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'polls_goods'


class Profile(models.Model):
    id = models.CharField(max_length=1000000000, primary_key=True)
    phone = models.TextField(blank=True, null=True)
    fio = models.TextField(db_column='FIO', blank=True, null=True)  # Field name made lowercase.
    nova_poshta = models.TextField(blank=True, null=True)
    adrees = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    last_zakaz = models.TextField(blank=True, null=True)
    promo_profile = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'profile'


class Setting(models.Model):
    id = models.CharField(max_length=1000000000, primary_key=True)
    notification = models.TextField(blank=True, null=True)
    notifical_day = models.TextField(blank=True, null=True)
    promo = models.TextField(blank=True, null=True)
    promo_day = models.IntegerField(blank=True, null=True)
    promo_date = models.TextField(blank=True, null=True)
    salse_promo = models.IntegerField(blank=True)

    class Meta:
        managed = False
        db_table = 'setting'


class Zakaz(models.Model):
    id = models.CharField(max_length=1000000000)
    grind = models.TextField(blank=True, null=True)
    method = models.TextField(blank=True, null=True)
    weight = models.TextField(db_column='Weight', blank=True, null=True)  # Field name made lowercase.
    quantity = models.TextField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.
    orderr = models.TextField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    id_coffe = models.IntegerField(blank=True, null=True)
    id_order = models.AutoField(primary_key=True, blank=True)
    basket = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    promo = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'zakaz'


