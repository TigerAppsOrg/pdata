# pdata/pdata/wsgi.py
# pdata
# Author: Michael Friedman
# Date: December 1st, 2017
# Description: WSGI Configuration

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pdata.settings")
application = get_wsgi_application()
