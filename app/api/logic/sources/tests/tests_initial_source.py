from django.test import TestCase

from ..base_source import BaseSource


class TestBaseSource(TestCase):
      
    def test_trims_text_success_test(self):
      source = BaseSource()
      self.assertTrue(source._cleanText('   cleaned text   ') == 'cleaned text')
    
    def test_removes_double_space_success_test(self):
      source = BaseSource()
      self.assertTrue(source._cleanText('cleaned   text') == 'cleaned text')

    def test_trims_text_removes_double_space_success_test(self):
      source = BaseSource()
      self.assertTrue(source._cleanText('   cleaned   text   ') == 'cleaned text')