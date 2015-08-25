# coding: utf8
from HTMLParser import HTMLParser
import re


class RecipeHTMLParser(HTMLParser):

    ingredient_start_rex = ['ingredienser', 'ingredients']
    instruction_start_rex = ['gör så här', 'instructions']
    tag_stack = []
    ingredient_parsing = False
    instruction_parsing = False
    ingredients = []
    instructions = []
    element_tags = ['ul', 'li']
    data_element = []
    current_data = ''

    def _match_any(self, data, rexes):
        return any(re.match('^.{0,3}%s.{0,3}$' % r, data,
                            re.IGNORECASE) for r in rexes)

    def _match_ingredient_start(self, data):
        return self._match_any(data, self.ingredient_start_rex)

    def _match_instruction_start(self, data):
        return self._match_any(data, self.instruction_start_rex)

    def handle_starttag(self, tag, attrs):
        self.tag_stack.append(tag)

    def handle_endtag(self, tag):
        if self.tag_stack:
            self.tag_stack.pop()
        if not self.tag_stack:
            self.ingredient_parsing = False
            self.instruction_parsing = False

        if self.ingredient_parsing and self.data_element:
            if tag in self.element_tags:
                self.ingredients.extend(
                    self.parse_ingredients(self.data_element))
                self.data_element = []
        if self.instruction_parsing and self.data_element:
            if tag in self.element_tags:
                self.instructions.extend(
                    self.parse_instructions(self.data_element))
                self.data_element = []

    @staticmethod
    def parse_ingredients(data):
        return [data] if data else []

    @staticmethod
    def parse_instructions(data):
        return [data] if data else []

    def handle_data(self, data):
        data = data.strip()
        if self.ingredient_parsing:
            if data:
                self.data_element.append(data.strip())
        elif self.instruction_parsing:
            if data:
                self.data_element.append(data.strip())
        else:
            if self._match_ingredient_start(data):
                self.ingredient_parsing = True
                self.tag_stack = self.tag_stack[-2:]
            elif self._match_instruction_start(data):
                self.tag_stack = self.tag_stack[-2:]
                self.instruction_parsing = True


def test_parse():
    import requests
    # url = u'http://www.recept.nu/' + (
    #     'markus_aujalay/soppor_och_grytor/\fisk_och_skaldjur/fiskgryta/')
    url = 'http://www.arla.se/recept/auberginer-i-ugn/'
    data = requests.get(url).text

    if u'Gör så här' in data:
        print 'yes'
    parser = RecipeHTMLParser()
    parser.feed(data)
    print parser.instructions
    print parser.ingredients

if __name__ == '__main__':
    test_parse()
