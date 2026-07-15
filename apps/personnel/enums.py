from django.db import models


class Sex(models.TextChoices):
    """
    Стать військовослужбовця.
    """

    MALE = "male", "Чоловіча"
    FEMALE = "female", "Жіноча"
