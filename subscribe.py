from twilix.stanzas import Presence
from twilix.base.myelement import EmptyStanza
from twilix.base.exceptions import WrongElement

class ValidSubscrHandler(Presence):
    """
    Extends Presence class.
    Defines handlers for valid subscribe queries.
    """

    def clean_to(self, value):
        if self.host:
            if not self.host.validator(value.user):
                raise WrongElement
        return value

    def availableHandler(self):
        return self.get_reply()

    def probeHandler(self):
        reply = self.get_reply()
        reply.to = reply.to.bare()
        reply.type_ = 'presence'
        return reply

    def subscribeHandler(self):
        reply = self.get_reply()
        reply.type_ = 'subscribed'
        return reply, self.probeHandler()

    def subscribedHandler(self):
        return EmptyStanza()

    def unsubscribedHandler(self):
        reply = Presence(to=self.from_, from_=self.to, type_='unsubscribed')
        return reply

class InvalidSubscrHandler(Presence):
    """
    Extends Presence class.
    Defines handlers for invalid subscribe queries.
    """

    def clean_to(self, value):
        if self.host:
            if self.host.validator(value.user):
                raise WrongElement
        return value

    def availableHandler(self):
        return EmptyStanza()

    def probeHandler(self):
        return EmptyStanza()

    def subscribeHandler(self):
        return EmptyStanza()

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
        self.dispatcher.registerHandler((ValidSubscrHandler, self))
        self.dispatcher.registerHandler((InvalidSubscrHandler, self))
