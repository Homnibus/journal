from django.http import JsonResponse
from django.shortcuts import _get_queryset

from projets.commun.error import HttpNotFound


def java_string_hashcode(string):
    """
    Return the java hash code of a string
    """
    string_hash = 0
    for char in string:
        string_hash = (31 * string_hash + ord(char)) & 0xFFFFFFFF
    return ((string_hash + 0x80000000) & 0xFFFFFFFF) - 0x80000000


class JsonResponseContainer:
    def __init__(self):
        self.data = {}
        self.status = 200

    def get_json_response(self):
        return JsonResponse(self.data, status=self.status)


def min_paginator_rang(current_page, max_page, step):
    """
    :param current_page: The current page of the paginator
    :param max_page: The last page of the paginator
    :param step: The maximum number of page to have before the current paginator page
    :return: The minimum page number to show to have if possible 'step' page before the current page
    """
    if current_page <= 0 or max_page <= 0 or step <= 0 or current_page > max_page:
        raise IndexError
    return min(max(current_page - step, 1), max(max_page - step - step, 1))


def max_paginator_rang(current_page, max_page, step):
    """
    :param current_page: The current page of the paginator
    :param max_page: The last page of the paginator
    :param step: The maximum number of page to have after the current paginator page
    :return: The maximum page number to show to have if possible 'step' page before the current page
    """
    if current_page <= 0 or max_page <= 0 or step <= 0 or current_page > max_page:
        raise IndexError
    return max(min(current_page + step, max_page), min(step + step + 1, max_page))


def get_object_or_not_found(klass, *args, **kwargs):
    """
    Use get() to return an object, or raise a HttpNotFound exception if the object
    does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Like with QuerySet.get(), MultipleObjectsReturned is raised if more than
    one object is found.
    """
    queryset = _get_queryset(klass)
    if not hasattr(queryset, "get"):
        klass__name = (
            klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        )
        raise ValueError(
            "First argument to get_object_or_404() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        raise HttpNotFound(queryset.model._meta.object_name)
