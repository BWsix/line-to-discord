from django.db import models

class Group(models.Model):
  id = models.CharField(max_length=40, primary_key=True, unique=True)
  name = models.CharField(max_length=55, default="(empty)")
  manager = models.CharField(max_length=40)

  def __str__(self):
    return f"{self.name}"

class Hook(models.Model):
  owner = models.ForeignKey('Group', on_delete=models.CASCADE)
  name = models.CharField(max_length=30, default="(empty)")
  url = models.CharField(max_length=150, null=True)

  def __str__(self):
    return f'from "{self.owner}" to "{self.name}" '
