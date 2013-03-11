from twisted.internet.defer import inlineCallbacks, returnValue

from twilix.stanzas import Message
from twilix.base.myelement import EmptyStanza

from translation_api import MultitranAPI

class MessageHandler(Message):

    @inlineCallbacks
    def anyHandler(self):
        reply = self.get_reply()
        reply.body = yield MultitranAPI.translate(self.body, self.to.user)
        returnValue(reply)

class MessageTranslation(object):

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def init(self):
        self.dispatcher.registerHandler((MessageHandler, self))
