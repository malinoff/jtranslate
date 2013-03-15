# -*- coding: utf-8 -*-
import urllib
from lxml import etree

from twisted.web.client import getPage
from twisted.web.error import Error
from twisted.internet.error import DNSLookupError, TimeoutError
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue

class MultitranAPI(object):


    langs = {'en': ('English', 1),
             'de': ('German', 3),
             'fr': ('French', 4),
             'es': ('Spain', 5),
             'it': ('Italian', 23),
             'nl': ('Dutch', 24),
             'lv': ('Latvian', 27),
             'et': ('Estonian', 26),
             'ja': ('Japanese', 28),
             'af': ('African', 31),
             'eo': ('Esperanto', 34),
             'xal': ('Kalmyk', 35)
             }

    @classmethod
    def get_languages(cls):
        return dict(map(lambda x: (x[0], x[1][0]), cls.langs.items()))

    @classmethod
    @inlineCallbacks
    def _get_transcription(cls, word):
        # get page with transcription
        word = word.encode('utf-8')
        transl = u'перевод'.encode('utf-8')
        wrd = urllib.quote_plus(word)
        page = 'http://slovari.yandex.ru/%s/%s/#lingvo/' % (wrd, transl)
        page = yield getPage(page)
        # find transcription
        html = etree.HTML(page)
        title = html.xpath('//h1[@class="b-translation__title"]/child::text()')
        title = title[0].strip('\r\n').rstrip('[').strip()
        # check yandex auto replace unkown words
        if title.lower() == word.lower():
            transcription = html.xpath('//span[@class="b-translation__tr"]')
            if transcription:
                returnValue(transcription[0].text)

    @classmethod
    @inlineCallbacks
    def _get_translation(cls, word, lang):
        translation = ''
        # get page with translation
        wrd = word.encode('cp1251', 'xmlcharrefreplace')
        params = urllib.urlencode({'s': wrd, 'CL': 1, 'l1': lang})
        page = 'http://www.multitran.ru/c/m.exe?%s' % params
        try:
            page = yield getPage(page)
        except (Error, DNSLookupError, TimeoutError) as e:
            returnValue('Service error. Please, try later.')
        html = etree.HTML(page)
        # find table with translation
        trs = html.xpath('//form[@id="translation"]/../table[2]/tr')
        x = trs[0].xpath('td')[0].xpath('descendant::text()')
        # uknown word
        if len(x) == 1:
            returnValue('Sorry, can not translate "%s"' % word)
        translation += '%s' % x[0].rstrip('\r\n')
        translation += '%s' % x[1].rstrip('\r\n')

        try:
            transcription = yield cls._get_transcription(word)
        except (Error, DNSLookupError, TimeoutError) as e:
            pass
        else:
            if transcription:
                translation += ' [%s] ' % transcription

        for elem in x[2:]:
            translation += '%s' % elem.rstrip('\r\n')
        translation += '\n'
        for tr in trs[1:]:
            tds = tr.xpath('td')
            for td in tds:
                for elem in td.xpath('descendant::text()'):
                    translation += '%s' % elem.rstrip('\r\n')
            translation += '\n'
        returnValue(translation)

    @classmethod
    def translate(cls, word, lang):
        if isinstance(lang, basestring):
            lang = cls.langs[str(lang)][1]
        translation = cls._get_translation(word, lang)
        return translation
