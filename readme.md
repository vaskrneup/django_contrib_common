# Django App For managing API Driven Apps.

### The app contains models following models for making development easier

* ### `AbstractBaseModel` same as django's default `django.db.models.Model` but contains additional methods and fields.
    * ##### field `creation_date`: Stores creation date of the object.
    * ##### field `update_date`: Stores last update date of the object.
    * ##### method `set_request`: Sets request object in model so that it used be used internally or by inherited models. Request object is stored in `_request` which can be accessed through `get_request()`.
    * ##### method `humanized_creation_date`: Gets `creation_date` as `3 days ago`, `hour ago` etc.
    * ##### method `humanized_update_date`: Gets `update_date` as `3 days ago`, `hour ago` etc.
    * ##### method `is_new`: returns `True` if the object is being created. returns `False` if the object is being updated. 
    * ##### method `get_fields`: returns name of fields as `dict`, if passed `as_list=False`, then `list` will be returned.
    * ##### method `serialize`: returns model data in provided format, available format: `["json"]` (Other format support will be added soon).    
    * ##### method `get_excluded_fields`: Override this method to return excluded fields, these fields will never be included when using serialize, even if field name is passed.
    * #### `Please refer to docstrings and comments for more info.`

* ### `AbstractBaseUUIDModel` contains all features of `AbstractBaseModel` except primary key datatype is changed to `UUID`.
    * ##### field `id`: same as django model default pk, except `default=uuid.uuid4` is set for creating unique value by default.

* ### `AbstractBaseSlugModel` contains all features of `AbstractBaseModel` in addition `slug field` is added.
    * ##### constant field `SLUG_FROM_FIELD`: field provided will be used for creating `slug by default`, random hex value will be appended at the end.
    * ##### field `slug`: stores slug for the object, will be auto generated if not set using `SLUG_FROM_FIELD` value.
    * ##### field `get_slug_value`: is used internally to get slug value, override this if you wish to change how `slug` is formed. `Slug must be unique`

* ### `AbstractBaseSlugUUIDModel` contains all features of `AbstractBaseModel`, `AbstractBaseUUIDModel` and `AbstractBaseSlugModel`.
