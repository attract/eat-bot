def get_user_serializer(serializer_obj):
    user = None
    request = serializer_obj.context.get("request")
    if request and hasattr(request, "user"):
        user = request.user

    return user
