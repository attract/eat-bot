def get_field_validators(Model, field_name):
    return Model._meta.get_field(field_name).validators


def get_field_obj(Model, field_name):
    return Model._meta.get_field(field_name)
