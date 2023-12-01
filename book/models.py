from django.db import models

# Create your models here.
class Book(models.Model):
    Genre = ( 
          ('ファンタジー','ファンタジー'),
          ('文学','文学'),
          ('児童文学','児童文学'),
          ('SF','SF'),
          ('小説','小説'),
          ('ミステリー','ミステリー'),
          ('ホラー','ホラー'),
          ('漫画','漫画')
        )
    No = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=Genre)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    price = models.BigIntegerField()
    stock = models.BooleanField()

# Output for json
    def get_data(self):
        return {
            'No':self.No,
            'title':self.title,
            'category':self.category,
            'author':self.author,
            'published_date':self.published_date,
            'price':self.price,
            'stock':self.stock, 
        } 

class Meta:
        ordering= ['No','-published_date']
        db_table= 'book'
    