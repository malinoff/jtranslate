import sys
import time
from ConfigParser import NoOptionError, NoSectionError

from twilix.version import ClientVersion
from twilix.disco import Disco, DiscoItem
from twilix.patterns.component import TwilixComponent
from twilix.dispatcher import Dispatcher
from twilix.vcard import VCard, VCardQuery

from subscribe import Subscription
from messages import MessageTranslation
from translation_api import MultitranAPI

class jtranslateComponent(TwilixComponent):
    """
    Master class for the jabber-translate service.
    """
    def __init__(self, version, jid, conf):
        """
        Sets info about translate service.
        
        :param version: version of your service.
        
        :param jid: jid of your service.
        
        :param conf: instance of ConfigParser that binds configuration file.
        """
        TwilixComponent.__init__(self, jid)
        self.VERSION = version
        self.startTime = None

    def init(self):
        """
        Method initializing all needed services and handlers.
        """
        self.startTime = time.time()
        self.disco = Disco(self.dispatcher)
        self.version = ClientVersion(self.dispatcher,
                                    'jabber translate service',
                                    self.VERSION, 'Linux')
        self.version.init(self.disco)
        self.myvcard = VCardQuery(nickname='jtranslate',
                                  jid=self.myjid,
                                  description='\
Jabber translate service')
        self.vcard = VCard(self.dispatcher, myvcard=self.myvcard)
        self.vcard.init(self.disco)

        api = MultitranAPI()
        items = [DiscoItem(jid=u'%s@%s' % (code, self.myjid),
                           iname='Translate to %s'%lang)
                    for code, lang in api.get_languages().items()]
        self.disco.root_items.addItems(items)

        def validate(code):
            if code in api.get_languages():
                return True
            return False

        self.subscription = Subscription(self.dispatcher, validate)
        self.subscription.init()
        self.mtrans = MessageTranslation(self.dispatcher, api)
        self.mtrans.init()
        self.disco.init()
        print 'Connected!'
