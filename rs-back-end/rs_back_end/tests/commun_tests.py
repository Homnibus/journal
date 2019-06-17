import json

from django.http import JsonResponse
from django.test import TestCase
from rs_back_end.commun.codex import Page
from rs_back_end.commun.utils import (
  JsonResponseContainer,
  java_string_hashcode,
  min_paginator_rang,
  max_paginator_rang,
)


class CommunTest(TestCase):
  def test_page_assert_init(self):
    date = "01/01/0001"
    page = Page(date)
    self.assertEqual(page.date, date)
    self.assertIsNone(page.note_form)
    self.assertIsNone(page.new_task_form)
    self.assertEqual(page.tasks_form, [])


class UtilsTest(TestCase):
  def test_json_response_container_assert_return_json_response(self):
    message = "TEST_OK"
    json_response_container = JsonResponseContainer()
    json_response_container.data.update({"test": message})
    response = json_response_container.get_json_response()

    self.assertEqual(response.status_code, 200)
    self.assertIsInstance(response, JsonResponse)
    self.assertEqual(json.loads(response.content)["test"], message)

  def test_java_string_hashcode_assert_equal(self):
    message = "TEST MESSAGE"
    message_hash = -502353319

    self.assertEqual(java_string_hashcode(message), message_hash)


class UtilsMinPaginatorRangTest(TestCase):
  def setUp(self):
    self.current_page = 1
    self.max_page = 1
    self.step = 1

  def test_min_paginator_rang_current_page_none_assert_type_error(self):
    current_page = None
    with self.assertRaises(TypeError):
      min_paginator_rang(current_page, self.max_page, self.step)

  def test_min_paginator_rang_current_page_zero_assert_error_index_error(self):
    current_page = 0
    with self.assertRaises(IndexError):
      min_paginator_rang(current_page, self.max_page, self.step)

  def test_min_paginator_rang_current_page_negative_assert_error_index_error(self):
    current_page = -1
    with self.assertRaises(IndexError):
      min_paginator_rang(current_page, self.max_page, self.step)

  def test_min_paginator_rang_max_page_none_assert_type_error(self):
    max_page = None
    with self.assertRaises(TypeError):
      min_paginator_rang(self.current_page, max_page, self.step)

  def test_min_paginator_rang_max_page_zero_assert_index_error(self):
    max_page = 0
    with self.assertRaises(IndexError):
      min_paginator_rang(self.current_page, max_page, self.step)

  def test_min_paginator_rang_max_page_negative_assert_index_error(self):
    max_page = -1
    with self.assertRaises(IndexError):
      min_paginator_rang(self.current_page, max_page, self.step)

  def test_min_paginator_rang_step_none_assert_type_error(self):
    step = None
    with self.assertRaises(TypeError):
      min_paginator_rang(self.current_page, self.max_page, step)

  def test_min_paginator_rang_step_zero_assert_index_error(self):
    step = 0
    with self.assertRaises(IndexError):
      min_paginator_rang(self.current_page, self.max_page, step)

  def test_min_paginator_rang_step_negative_assert_index_error(self):
    step = -1
    with self.assertRaises(IndexError):
      min_paginator_rang(self.current_page, self.max_page, step)

  def test_min_paginator_rang_current_page_greater_than_max_page_assert_index_error(
    self
  ):
    current_page = 2
    with self.assertRaises(IndexError):
      min_paginator_rang(current_page, self.max_page, self.step)

  def test_min_paginator_rang_simple_assert_return_one(self):
    min_value = min_paginator_rang(self.current_page, self.max_page, self.step)
    self.assertEqual(min_value, 1)

  def test_min_paginator_rang_middle_assert_return_step(self):
    current_page = 4
    max_page = 8
    step = 2
    min_value = min_paginator_rang(current_page, max_page, step)
    self.assertEqual(min_value, 2)

  def test_min_paginator_rang_end_assert_return_step_plus_step(self):
    current_page = 8
    max_page = 8
    step = 2
    min_value = min_paginator_rang(current_page, max_page, step)
    self.assertEqual(min_value, 4)

  def test_min_paginator_rang_start_assert_return_start(self):
    current_page = 1
    max_page = 8
    step = 2
    min_value = min_paginator_rang(current_page, max_page, step)
    self.assertEqual(min_value, 1)


class UtilsMaxPaginatorRangTest(TestCase):
  def setUp(self):
    self.current_page = 1
    self.max_page = 1
    self.step = 1

  def test_max_paginator_rang_current_page_none_assert_type_error(self):
    current_page = None
    with self.assertRaises(TypeError):
      max_paginator_rang(current_page, self.max_page, self.step)

  def test_max_paginator_rang_current_page_zero_assert_error_index_error(self):
    current_page = 0
    with self.assertRaises(IndexError):
      max_paginator_rang(current_page, self.max_page, self.step)

  def test_max_paginator_rang_current_page_negative_assert_error_index_error(self):
    current_page = -1
    with self.assertRaises(IndexError):
      max_paginator_rang(current_page, self.max_page, self.step)

  def test_max_paginator_rang_max_page_none_assert_type_error(self):
    max_page = None
    with self.assertRaises(TypeError):
      max_paginator_rang(self.current_page, max_page, self.step)

  def test_max_paginator_rang_max_page_zero_assert_index_error(self):
    max_page = 0
    with self.assertRaises(IndexError):
      max_paginator_rang(self.current_page, max_page, self.step)

  def test_max_paginator_rang_max_page_negative_assert_index_error(self):
    max_page = -1
    with self.assertRaises(IndexError):
      max_paginator_rang(self.current_page, max_page, self.step)

  def test_max_paginator_rang_step_none_assert_type_error(self):
    step = None
    with self.assertRaises(TypeError):
      max_paginator_rang(self.current_page, self.max_page, step)

  def test_max_paginator_rang_step_zero_assert_index_error(self):
    step = 0
    with self.assertRaises(IndexError):
      max_paginator_rang(self.current_page, self.max_page, step)

  def test_max_paginator_rang_step_negative_assert_index_error(self):
    step = -1
    with self.assertRaises(IndexError):
      max_paginator_rang(self.current_page, self.max_page, step)

  def test_max_paginator_rang_current_page_greater_than_max_page_assert_index_error(
    self
  ):
    current_page = 2
    with self.assertRaises(IndexError):
      max_paginator_rang(current_page, self.max_page, self.step)

  def test_max_paginator_rang_simple_assert_return_one(self):
    max_value = max_paginator_rang(self.current_page, self.max_page, self.step)
    self.assertEqual(max_value, 1)

  def test_max_paginator_rang_middle_assert_return_step(self):
    current_page = 4
    max_page = 8
    step = 2
    max_value = max_paginator_rang(current_page, max_page, step)
    self.assertEqual(max_value, 6)

  def test_max_paginator_rang_end_assert_return_end(self):
    current_page = 8
    max_page = 8
    step = 2
    max_value = max_paginator_rang(current_page, max_page, step)
    self.assertEqual(max_value, 8)

  def test_max_paginator_rang_start_assert_return_step_plus_step(self):
    current_page = 1
    max_page = 8
    step = 2
    max_value = max_paginator_rang(current_page, max_page, step)
    self.assertEqual(max_value, 5)
