from django.utils.translation import gettext


class HttpError(Exception):
    def __init__(
        self,
        status_code=500,
        message=gettext("Unexpected error"),
        explanation=gettext("An unexpected error occurred"),
    ):
        # Call the base class constructor
        super().__init__(message)
        self.status_code = status_code
        self.message = message
        self.explanation = explanation


class HttpMethodNotAllowed(HttpError):
    def __init__(self):
        # Call the base class constructor
        super().__init__(
            status_code=405,
            message=gettext("Method not allowed."),
            explanation=gettext(
                "The request method is known by the server but is not supported by the target resource."
            ),
        )


class HttpForbidden(HttpError):
    def __init__(self):
        # Call the base class constructor
        super().__init__(
            status_code=403,
            message=gettext("Forbidden."),
            explanation=gettext(
                "The server understood the request but refuses to authorize it"
            ),
        )


class HttpNotFound(HttpError):
    def __init__(self, resource_name=""):
        # Call the base class constructor
        if not isinstance(resource_name, str):
            super().__init__()
            return

        super().__init__(
            status_code=404,
            message=gettext("Resource not found."),
            explanation=gettext(
                "The server can't find the requested resource {resource_name}."
            ).format(resource_name=resource_name),
        )


class HttpConflict(HttpError):
    """ This error might be raise when a database IntegrityError append"""

    def __init__(self, resource_name=""):
        # Call the base class constructor
        if not isinstance(resource_name, str):
            super().__init__()
            return

        super().__init__(
            status_code=409,
            message=gettext("Conflict with current state of the server."),
            explanation=gettext(
                "The requested action on the resource {resource_name} is in conflict with the current state of the "
                "server. "
            ).format(resource_name=resource_name),
        )


class HttpInvalidFormData(HttpError):
    def __init__(self, form_errors=None, fields_error=None):
        if fields_error is None:
            fields_error = {}
        if form_errors is None:
            form_errors = {}

        # This error need at least one form error information to be relevant
        if len(form_errors) == 0 and len(fields_error) == 0:
            super().__init__()
            return

        # Call the base class constructor
        super().__init__(
            status_code=400,
            message=gettext("Bad request"),
            explanation=gettext(
                "The server could not understand the request due to invalid syntax."
            ),
        )
        # Add the validation errors
        self.form_errors = form_errors
        self.fields_error = fields_error
