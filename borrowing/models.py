from django.db import models

import book.models
import user.models


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    book_id = models.ManyToManyField(book.models.Book)
    user_id = models.ForeignKey(user.models.User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Borrowing {self.book_id.title} expected return date {self.expected_return_date}"

    class Meta:
        ordering = ["borrow_date"]
