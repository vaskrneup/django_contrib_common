def get_attr(obj, field: str, default_return: any = None, raise_error: bool = False, *args, **kwargs):
    """provides field/method data depending on provided obj and field

    :param default_return: Returns this if field not found
    :param obj: any object to which the data is accepted
    :param field: any field/method in that class
    :param raise_error: raises error if the field doesn't exists
    :param args: additional positional arguments accepted by `obj.field` if it is callable
    :param kwargs: additional keywords arguments accepted by `obj.field` if it is callable
    :return: `obj.field` if it exists or `default_return`
    """
    try:
        out = eval(f"obj.{field}")
        if callable(out):
            return out(*args, **kwargs)
        return out
    except (NameError, AttributeError):
        if raise_error:
            raise ValueError(f"`{field}` is neither callable nor property in the provided object.")
        return default_return
