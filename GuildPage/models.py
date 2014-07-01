from django.core.mail.backends import smtp


class MyEmailBackend(smtp.EmailBackend):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('timeout', 42)
        super(MyEmailBackend, self).__init__(*args, **kwargs)