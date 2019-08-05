from courses.models import *
from accounts.models import *

course = Course.objects.get(id=1)
user = User.objects.get(id=1)

for i in range(100):
    ArticleModel.objects.create(title='abcd{}'.format(i) , author=user, content="temp", course=course, type=0)