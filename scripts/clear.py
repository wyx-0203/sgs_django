from django.core.cache import cache
import os

cache.keys('*')

def clear():
    for key in cache.keys('*'):
        cache.delete(key)

os.system("echo yes | python3 sgs/manage.py collectstatic")