# Make this a proper Python package
# (Optional Celery exposure; harmless if Celery not used)
try:
    from .celery import app as celery_app  # noqa: F401
    __all__ = ("celery_app",)
except Exception:
    __all__ = ()
