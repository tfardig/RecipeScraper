# coding: utf8
import unittest
from nose.tools import eq_
from recipescraper.parser import RecipeHTMLParser


class RecipeHTMLParserTestCase(unittest.TestCase):

    def setUp(self):
        self.parser = RecipeHTMLParser()

    def test_match_ingredient_start(self):
        eq_(self.parser._match_ingredient_start('Ingredienser'), True)
        eq_(self.parser._match_ingredient_start('Inasdsd'), False)

    def test_match_instruction_start(self):
        eq_(self.parser._match_instruction_start('Gör så här:'), True)
        eq_(self.parser._match_instruction_start('Instructions'), True)
        eq_(self.parser._match_instruction_start(
            'Instructions and more text'), False)

    def test_start_instruction(self):
        data = """<div><h1>Instructions"""
        self.parser.feed(data)
        eq_(self.parser.instruction_parsing, True)
        eq_(self.parser.tag_stack, ['div', 'h1'])

    def test_start_instruction_sv(self):
        data = """<div><h1>Gör så här"""
        self.parser.feed(data)
        eq_(self.parser.instruction_parsing, True)
        eq_(self.parser.tag_stack, ['div', 'h1'])

    def test_parse(self):
        data = """<div><h1>Ingredients</h1>
        <ul><li><span>i</span><span>1</span></li>
        <li><span>i</span><span>2</span></li></ul>
        </div><div><h1>Instructions</h1>
        <ul><li>instruction1</li></ul></div>"""
        self.parser.feed(data)
        eq_(self.parser.ingredients, [['i', '1'], ['i', '2']])
        eq_(self.parser.instructions, [['instruction1']])
