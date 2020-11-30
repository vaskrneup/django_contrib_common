# Django App For managing API Driven Apps.

### The app contains models following models for making development easier

* ### Available Models
    * #### `AbstractBaseModel` same as django's default `django.db.models.Model` but contains additional methods and fields.
        * **field `creation_date`: Stores creation date of the object.**
        * **field `update_date`: Stores last update date of the object.**
        * **method `set_request` || `set_request(self, request: HttpRequest)`: Sets request object in model so that it used be used internally or by inherited models. Request object is stored in `_request` which can be accessed through `get_request()`.**
        * **method `get_request` || `get_request(self)`: Gets request object in model so that it used be used internally or by inherited models.**
        * **method `humanized_creation_date` || `humanized_creation_date(self)`: Gets `creation_date` as `3 days ago`, `hour ago` etc.**
        * **method `humanized_update_date` || `humanized_update_date(self)`: Gets `update_date` as `3 days ago`, `hour ago` etc.**
        * **method `is_new` || `is_new(self)`: returns `True` if the object is being created. returns `False` if the object is being updated.** 
        * **method `get_fields` || `get_fields(self, as_list=False, include_parents=True, include_hidden=False) -> (dict, list)`: returns name of fields as `dict`, if passed `as_list=False`, then `list` will be returned.**
        * **method `serialize` || `serialize(self, fields: dict = None, exclude: iter = None, format_: str = "json") -> dict`: returns model data in provided format, available format: `["json"]` (Other format support will be added soon).**    
        * **method `get_excluded_fields` || `get_excluded_fields(self) `: Override this method to return excluded fields, these fields will never be included when using serialize, even if field name is passed.**
        * **`Please refer to docstrings and comments for more info.`**
    
    * #### `AbstractBaseUUIDModel` contains all features of `AbstractBaseModel` except primary key datatype is changed to `UUID`.
        * **field `id`: same as django model default pk, except `default=uuid.uuid4` is set for creating unique value by default.**
    
    * #### `AbstractBaseSlugModel` contains all features of `AbstractBaseModel` in addition `slug field` is added.
        * **constant field `SLUG_FROM_FIELD`: field provided will be used for creating `slug by default`, random hex value will be appended at the end.**
        * **field `slug`: stores slug for the object, will be auto generated if not set using `SLUG_FROM_FIELD` value.**
        * **field `get_slug_value`: is used internally to get slug value, override this if you wish to change how `slug` is formed. `Slug must be unique`**
    
    * #### `AbstractBaseSlugUUIDModel` contains all features of `AbstractBaseModel`, `AbstractBaseUUIDModel` and `AbstractBaseSlugModel`.

* ### Available Forms
    * #### `JsonModelForm` same as django's `django.forms.ModelForm`, But contains additional features and accepts optional `request` as keyword argument when initializing the form.
        * **method `pre_init` || `pre_init(self)`: override this method to run code after the form is initialized.**
        * **method `post_init` || `post_init(self)`: override this method to run code before the form is initialized.**
        * **method `get_request` || `get_request(self)`: Gets the `request` object. If not set `ValueError will be raised`.**
        * **method `set_request` || `set_request(self, request)`: Sets the `request` object.**
        * **method `get_errors` || `get_errors(self, format_="json")`: Gets error in the format specified, for now supports `JSON` only.**
        * **method `set_field_attr` || `set_field_attr(self, fields: list, attr: str, value=None)`: Sets field attribute in bulk, `set_field_attr(self, fields: list, attr: str, value=None)`; `value` will be set to the `each field`'s `attr`.**
        * **method `make_fields_required` || `def make_fields_required(self, fields)`: Makes provided fields required.**
