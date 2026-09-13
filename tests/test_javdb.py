import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from lxml import etree

from scrapinglib.sites.javdb import Javdb


class JavdbTests(unittest.TestCase):
    def setUp(self):
        self.parser = Javdb()
        self.parser.init()
        self.parser.updateCore(None)
        self.parser.number = 'SOE-419'
        self.parser.search_delay = 0

    def test_actor_markup(self):
        cases = [
            ('<a class="actor-female" href="/actors/1">Alice</a>', ['Alice']),
            ('<a href="/actors/1">Alice</a><strong class="symbol female"/>', ['Alice']),
            ('<a class="actor-male" href="/actors/1">Bob</a>', []),
            ('<a href="/actors/1">Unknown</a>', []),
            ('', []),
            ('<a class="extra actor-female" href="/actors/1"> Alice <b>A</b> </a>', ['Alice A']),
            ('<a class="actor-female" href="/actors/1">Alice</a>'
             '<a class="actor-male" href="/actors/2">Bob</a>'
             '<a class="actor-female" href="/actors/3">Carol</a>', ['Alice', 'Carol']),
            ('<a href="/actors/1">Unknown</a>'
             '<a href="/actors/2">Bob</a><strong class="symbol male"/>'
             '<a href="/actors/3">Carol</a><strong class="female symbol"/>', ['Carol']),
            ('<a class="actor-male" href="/actors/1">Bob</a>'
             '<strong class="symbol female"/>', []),
        ]
        for markup, expected in cases:
            with self.subTest(markup=markup):
                tree = etree.HTML('<span class="value">' + markup + '</span>')
                self.assertEqual(self.parser.getActors(tree), expected)

    def test_fc2_actor_fallback(self):
        self.parser.number = 'FC2-12345'
        self.assertEqual(self.parser.getActors(etree.HTML('<html/>')), '\u7d20\u4eba')
        self.assertTrue(self.parser.fixstudio)

    def mock_search(self, cards):
        self.parser.session = Mock()
        self.parser.session.get.return_value = SimpleNamespace(
            text='<div class="movie-list">' + cards + '</div>',
            url='https://javdb.com/search?q=SOE-419&f=all',
            status_code=200,
        )

    def test_exact_match_preserves_card_index(self):
        self.mock_search(
            '<div><a href="/v/unknown"><div class="video-title">Unknown</div></a></div>'
            '<div><a href="/v/wrong"><div class="video-title"><strong>SOE-4190</strong></div></a></div>'
            '<div><a href="/v/neOpw"><div class="video-title"><strong> SOE-419 </strong></div></a></div>'
        )
        self.assertEqual(self.parser.queryNumberUrl('soe-419'), 'https://javdb.com/v/neOpw')
        self.assertEqual(self.parser.queryid, 2)

    def test_empty_and_nonmatching_search(self):
        for cards in [
            '',
            '<div><a href="/v/unknown">Unknown</a></div>',
            '<div><a href="/v/wrong"><div class="video-title"><strong>SOE-4190</strong></div></a></div>',
        ]:
            with self.subTest(cards=cards):
                self.mock_search(cards)
                with self.assertRaisesRegex(ValueError, 'number not found'):
                    self.parser.queryNumberUrl('SOE-419')

    def test_missing_detail_url(self):
        self.mock_search('<div><a><div class="video-title"><strong>SOE-419</strong></div></a></div>')
        with self.assertRaisesRegex(ValueError, 'missing detail URL'):
            self.parser.queryNumberUrl('SOE-419')

    def test_western_search(self):
        self.mock_search('')
        with self.assertRaisesRegex(ValueError, 'number not found'):
            self.parser.queryNumberUrl('Studio.26.01.01')
        self.mock_search('<div><a href="/v/first">Studio</a></div>')
        self.assertEqual(self.parser.queryNumberUrl('Studio.26.01.01'), 'https://javdb.com/v/first')
        self.assertEqual(self.parser.queryid, 0)

    def test_parse_error_logs_context_and_traceback(self):
        with patch.object(self.parser, 'getNum', side_effect=ValueError('broken markup')):
            with self.assertLogs('scrapinglib.base_scraper', level='WARNING') as logs:
                result = self.parser.dictformat(etree.HTML('<html/>'))
        self.assertEqual(result, {'title': ''})
        self.assertIn('site=javdb number=SOE-419', logs.output[0])
        self.assertIn('ValueError: broken markup', logs.output[0])
        self.assertIsNotNone(logs.records[0].exc_info)


if __name__ == '__main__':
    unittest.main()
