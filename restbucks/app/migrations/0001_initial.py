# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-09-20 13:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='آخرین به روزرسانی')),
                ('status', models.CharField(choices=[('waiting', 'در انتظار'), ('preparation', 'در حال آماده سازی'), ('ready', 'آماده'), ('delivered', 'تحویل داده شده')], default='waiting', max_length=20, verbose_name='وضعیت')),
                ('consume_location', models.CharField(blank=True, choices=[('take_away', 'بیرون بر'), ('in_shop', 'در فروشگاه')], default='in_shop', max_length=20, null=True)),
                ('address', models.TextField(blank=True, null=True, verbose_name='آدرس')),
                ('customer', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_set', to=settings.AUTH_USER_MODEL, verbose_name='مشتری')),
            ],
            options={
                'verbose_name': 'سفارش',
                'verbose_name_plural': 'سفارش\u200cها',
                'default_related_name': 'order_set',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='آخرین به روزرسانی')),
                ('count', models.PositiveIntegerField(verbose_name='تعداد')),
                ('milk', models.CharField(blank=True, choices=[('skim', 'کف (کم)'), ('semi', 'نصف (متوسط)'), ('whole', 'کامل (زیاد)')], help_text='Latte', max_length=20, null=True, verbose_name='شیر')),
                ('size', models.CharField(blank=True, choices=[('small', 'کوچک'), ('medium', 'متوسط'), ('large', 'بزرگ')], help_text='Cappuccino and Hot Chocolate', max_length=20, null=True, verbose_name='اندازه')),
                ('shots', models.CharField(blank=True, choices=[('single', 'تک شات'), ('double', 'دو شات'), ('triple', 'سه شات')], help_text='Espresso', max_length=20, null=True, verbose_name='شات')),
                ('kind', models.CharField(blank=True, choices=[('chocolate_chip', 'شکلاتی'), ('ginger', 'زنجبیلی')], help_text='Cookie', max_length=20, null=True, verbose_name='نوع')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_item_set', to='app.Order', verbose_name='سفارش')),
            ],
            options={
                'verbose_name': 'مورد سفارش',
                'verbose_name_plural': 'اقلام سفارش',
                'default_related_name': 'order_item_set',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='آخرین به روزرسانی')),
                ('name', models.CharField(max_length=20, verbose_name='نام')),
                ('slug', models.SlugField(unique=True, verbose_name='شناسه یکتا')),
                ('price', models.PositiveIntegerField(verbose_name='قیمت')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
                'default_related_name': 'product_set',
            },
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_item_set', to='app.Product', verbose_name='محصول'),
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='order_set', through='app.OrderItem', to='app.Product', verbose_name='محصولات'),
        ),
    ]