from blog.models import Category

categories = ['Technology', 'Lifestyle', 'Business', 'Health', 'Education', 'Travel', 'Food', 'Sports']

for title in categories:
    category, created = Category.objects.get_or_create(title=title)
    if created:
        print(f'Created category: {title}')
    else:
        print(f'Category already exists: {title}')
