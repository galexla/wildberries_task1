from .settings import *

ALLOWED_HOSTS += ["testserver"]
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.memory.InMemoryStorage",
    },
}
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
INSTALLED_APPS.insert(0, "pytest_django")
