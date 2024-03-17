from django.db import models
import datetime


class Manseryuk(models.Model):

    today = datetime.date.today()

    name = models.CharField(max_length=20)

    YEAR_CHOICES = []
    for r in range(1900, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r, r))

    year = models.IntegerField(
        blank=False, null=False,
        choices=YEAR_CHOICES, default=datetime.datetime.now().year
        )
    month = models.IntegerField(default=today.month)
    day = models.IntegerField(default=today.day)

    YD_CHOICES = [
        ("평달", "평달"),
        ("윤달", "윤달"),
    ]
    yd = models.CharField(max_length=10, null=True, choices=YD_CHOICES,
                          default="평달")

    TIME_CHOICES = [
        ("자", "23:30~01:30"), ("축", "01:30~03:30"), ("인", "03:30~05:30"),
        ("묘", "05:30~07:30"), ("진", "07:30~09:30"), ("사", "09:30~11:30"),
        ("오", "11:30~13:30"), ("미", "13:30~15:30"), ("신", "15:30~17:30"),
        ("유", "17:30~19:30"), ("술", "19:30~21:30"), ("해", "21:30~23:30"),
    ]
    time = models.CharField(max_length=1, choices=TIME_CHOICES)

    GEN_CHOICES = [
        ("남", "남"),
        ("여", "여"),
    ]
    gen = models.CharField(max_length=1, choices=GEN_CHOICES)

    SL_CHOICES = [
        (1, "양력"),
        (2, "음력"),
    ]

    sl = models.IntegerField(choices=SL_CHOICES)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name