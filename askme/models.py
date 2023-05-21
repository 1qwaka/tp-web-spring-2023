from django.db import models

# Create your models here.
QUESTIONS = [
    {
        "title": f"some question {i}",
        "text": f"some text {i}",
        "id": i,
    } for i in range(30)
]
