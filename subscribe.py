from twilix.stanzas import Presence
from twilix.base.myelement import EmptyStanza

class SubscrHandler(Presence):
    """
    Extends Presence class.
    Defines handlers for subscribe queries.
    """
    def probeHandler(self):
        if unicode(self.to.bare()) in self.host.items:
            reply = self.get_reply()
            reply.to = reply.to.bare()
            reply.type_ = 'presence'
            return reply
        else:
            return EmptyStanza()

    def subscribeHandler(self):
        if unicode(self.to.bare()) in self.host.items:
            reply = self.get_reply()
            reply.type_ = 'subscribed'
            return reply, self.probeHandler()

    def subscribedHandler(self):
        return EmptyStanza()

    def unsubscribedHandler(self):
        reply = Presence(to=self.from_, from_=self.to, type_='unsubscribed')
        return reply
