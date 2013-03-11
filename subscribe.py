from twilix.stanzas import Presence
from twilix.base.myelement import EmptyStanza

class SubscrHandler(Presence):
    """
    Extends Presence class.
    Defines handlers for subscribe queries.
    """

    def availableHandler(self):
        if self.host.validator(self.to.user):
            return self.get_reply()

    def probeHandler(self):
        if self.host.validator(self.to.user):
            reply = self.get_reply()
            reply.to = reply.to.bare()
            reply.type_ = 'presence'
            return reply
        else:
            return EmptyStanza()

    def subscribeHandler(self):
        if self.host.validator(self.to.user):
            reply = self.get_reply()
            reply.type_ = 'subscribed'
            return reply, self.probeHandler()

    def subscribedHandler(self):
        return EmptyStanza()

    def unsubscribedHandler(self):
        reply = Presence(to=self.from_, from_=self.to, type_='unsubscribed')
        return reply

class Subscription(object):
    def __init__(self, dispatcher, validator):
        self.dispatcher = dispatcher
        self.jid = None
        self.validator = validator

    def init(self):
        self.dispatcher.registerHandler((SubscrHandler, self))
