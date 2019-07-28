from django.http import JsonResponse
from django.shortcuts import _get_queryset

from rs_back_end.commun.error import HttpNotFound
from rs_back_end.models import get_current_timestamp, Page, Codex


def create_or_get_today_page(codex_id):
  """
  Return the page of the day. Create it if it does not exist.
  """
  codex = Codex.objects.get(id=codex_id)
  # Get the page of the day if it exist
  # TODO: try to upgrade the way this check is down ?
  today = get_current_timestamp().date()
  page = Page.objects.filter(codex=codex, date=today).first()
  # If the page does not exist, create a new one
  if page is None:
    page = Page(
      codex=codex,
      date=today
    )
    page.save()
  return page


def java_string_hashcode(string):
  """
  Return the java hash code of a string
  """
  string_hash = 0
  for char in string:
    string_hash = (31 * string_hash + ord(char)) & 0xFFFFFFFF
  return ((string_hash + 0x80000000) & 0xFFFFFFFF) - 0x80000000


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
