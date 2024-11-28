from django.db import models
from django.contrib.auth.models import User

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='favorited_by')
    favorited_at = models.DateTimeField(auto_now_add=True)  # Quando o livro foi favoritado

    class Meta:
        unique_together = ('user', 'book')  # Garante que um usuário não favorite o mesmo livro mais de uma vez

    def __str__(self):
        return f"{self.user.username} favorited {self.book.title}"
    


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name



class Collection(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    books = models.ManyToManyField('Book', related_name='collections', blank=True)  # Many-to-Many with Book

    def __str__(self):
        return self.name


class PurchaseLocation(models.Model):
    name = models.CharField(max_length=255)  # Store name or website name
    url = models.URLField(null=True, blank=True)  # Link to the store or specific book page
    address = models.TextField(null=True, blank=True)  # Physical address (if applicable)

    def __str__(self):
        return self.name


class Book(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    FORMAT_CHOICES = [
        ('hardcover', 'Hardcover'),
        ('paperback', 'Paperback'),
        ('ebook', 'Ebook'),
        ('audiobook', 'Audiobook'),
        ('pdf', 'PDF'),
    ]
    title = models.CharField(max_length=255)
    id_google = models.CharField(max_length=255)
    author = models.CharField(max_length=255)  # Storing author name(s)
    description = models.TextField(null=True, blank=True)
    publisher = models.CharField(max_length=255, null=True, blank=True)  # Publisher field
    published_date = models.CharField(max_length=50, null=True, blank=True)  # Published date as a string
    cover = models.ImageField(upload_to='book_covers/', null=True, blank=True)  # Upload for cover image
    thumbnail = models.ImageField(upload_to='books_covers/', null=True, blank=True)  # Thumbnail (additional)
    pdf = models.FileField(upload_to='books_pdfs/', null=True, blank=True)  # PDF file
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')  # Status of the book
    is_published = models.BooleanField(default=False)  # Is the book published?
    rejection_reason = models.TextField(null=True, blank=True)  # Reason for rejection (if any)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')  # User who added the book
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when updated

    # Relationships
    categories = models.ManyToManyField(Category, related_name='books', blank=True)
    tags = models.ManyToManyField(Tag, related_name='books', blank=True)
    formato = models.CharField(max_length=50, choices=FORMAT_CHOICES)
    purchase_locations = models.ManyToManyField(PurchaseLocation, related_name='books', blank=True)  # Many-to-Many with PurchaseLocation

    def __str__(self):
        return self.title
