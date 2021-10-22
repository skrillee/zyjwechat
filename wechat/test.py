import datetime
import time
import pytz
import os


def user_directory_path(instance, filename):
    ext = filename.split('.').pop()
    filename = '{0}{1}.{2}'.format(instance, instance, ext)
    print(os.path.join(instance, filename))


user_directory_path('yanzhe', 'yanzhe.jpg')
