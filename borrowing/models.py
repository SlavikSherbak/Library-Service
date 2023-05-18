from django.db import models

import book.models
import user.models


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    book = models.ForeignKey(book.models.Book, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(user.models.User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Borrowing expected return date {self.expected_return_date}"

    class Meta:
        ordering = ["borrow_date"]
