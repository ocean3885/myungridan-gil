# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CalendaData(models.Model):
    cd_no = models.AutoField(primary_key=True, blank=True, null=False)
    cd_sgi = models.IntegerField()
    cd_sy = models.IntegerField()
    cd_sm = models.TextField()
    cd_sd = models.TextField()
    cd_ly = models.IntegerField()
    cd_lm = models.TextField()
    cd_ld = models.TextField()
    cd_hyganjee = models.TextField(blank=True, null=True)
    cd_kyganjee = models.TextField(blank=True, null=True)
    cd_hmganjee = models.TextField(blank=True, null=True)
    cd_kmganjee = models.TextField(blank=True, null=True)
    cd_hdganjee = models.TextField(blank=True, null=True)
    cd_kdganjee = models.TextField(blank=True, null=True)
    cd_hweek = models.TextField(blank=True, null=True)
    cd_kweek = models.TextField(blank=True, null=True)
    cd_stars = models.TextField(blank=True, null=True)
    cd_moon_state = models.TextField(blank=True, null=True)
    cd_moon_time = models.TextField(blank=True, null=True)
    cd_leap_month = models.IntegerField(blank=True, null=True)
    cd_month_size = models.IntegerField(blank=True, null=True)
    cd_hterms = models.TextField(blank=True, null=True)
    cd_kterms = models.TextField(blank=True, null=True)
    cd_terms_time = models.TextField(blank=True, null=True)
    cd_keventday = models.TextField(blank=True, null=True)
    cd_ddi = models.TextField()
    cd_sol_plan = models.TextField(blank=True, null=True)
    cd_lun_plan = models.TextField(blank=True, null=True)
    holiday = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'calenda_data'



