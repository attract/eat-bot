from django.contrib.auth import get_user_model
User = get_user_model()


def create_user(email, password, model):
    user = model.objects.filter(email=email)
    if not user:
        model.objects.create_superuser(email, password)
        msg = '%s created successfully' % email
    else:
        msg = '%s already exist' % email
    print(msg)

create_user('admin@admin.com', '123123', User)
