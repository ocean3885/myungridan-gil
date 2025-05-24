# from django.db import models
# class Manseryuk(models.Model):

#     name = models.CharField(max_length=20)
#     year = models.CharField(max_length=4)
#     month = models.CharField(max_length=2)
#     day = models.CharField(max_length=2)

#     YD_CHOICES = [
#         ("평달", "평달"),
#         ("윤달", "윤달"),
#     ]
#     yd = models.CharField(max_length=10, null=True, choices=YD_CHOICES,
#                           default="평달")

#     hour = models.CharField(max_length=2, null=True)
#     min = models.CharField(max_length=2, null=True)

#     GEN_CHOICES = [
#         ("남", "남"),
#         ("여", "여"),
#     ]
#     gen = models.CharField(max_length=1, choices=GEN_CHOICES)

#     SL_CHOICES = [
#         (1, "양력"),
#         (2, "음력"),
#     ]

#     sl = models.IntegerField(choices=SL_CHOICES)

#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name
