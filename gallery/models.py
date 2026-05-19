from django.db import models

class GalleryItem(models.Model):
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption if self.caption else f"Gallery Image {self.id}"
