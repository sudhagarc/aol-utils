#!/usr/bin/env python

from eventbrite import Eventbrite
import json

class Event():
    def __init__(self, eventbrite):
        self.eventIds = []
        self.eventbrite = eventbrite

    def getAllEvents(self):
        events = self.eventbrite.api("get", "/users/me/owned_events", {})
        self.addEvents(events['events'])

        # return
        while 'continuation' in events['pagination']:
            contId = events['pagination']['continuation']
            events = self.eventbrite.api("get",
                    "/users/me/owned_events?continuation=" + contId, {})
            self.addEvents(events['events'])
            print(json.dumps(events['pagination'], indent=2))

    def addEvents(self, events):
        for event in events:
            if event['status'] == 'completed':
                self.eventIds.append(event['id'])

    def getEventIds(self):
        return self.eventIds


class Orders():
    def __init__(self, eventbrite, csv_file):
        self.orders = []
        self.eventbrite = eventbrite
        self.csv_file = open(csv_file, 'a')

    def __del__(self):
        self.csv_file.close()

    def getOrdersByEvent(self, eventId):
        orders = self.eventbrite.api("get", "/events/" + eventId +
                "/orders", {})
        self.addOrders(orders['orders'])

        while 'continuation' in orders['pagination']:
            contId = orders['pagination']['continuation']
            orders = self.eventbrite.api("get",
                    "/events/" + eventId + "/orders?continuation=" + contId,
                    {})
            self.addOrders(orders['orders'])
            print(json.dumps(orders['pagination'], indent=2))

    def addOrders(self, orders):
        for order in orders:
            o = {
                    'name': order['name'],
                    'email': order['email']
                }
            self.orders.append(o)

    def getOrdersCount(self):
        return len(self.orders)

    def getOrders(self):
        return self.orders

    def dumpCsv(self):
        for order in self.orders:
            # print("%s,%s" % (order['name'], order['email']))
            orderLine = order['name'] + ',' + order['email'] + '\n'
            self.csv_file.write(orderLine.encode('utf8'))


def main():
    eventbrite = Eventbrite('<ENTER-YOUR-TOKEN-HERE>')
    event = Event(eventbrite)
    event.getAllEvents()
    eventIds = event.getEventIds()

    orders = Orders(eventbrite, 'all_orders.csv')
    for eid in eventIds:
        print("Event id: ", eid)
        orders.getOrdersByEvent(eid)
        #if orders.getOrdersCount():
        #    break

    '''
    orders_ = orders.getOrders()
    for order in orders_:
        print("%s,%s" % (order['name'], order['email']))
    '''
    orders.dumpCsv()

def test():
    f = open('test', 'w')
    uniStr = unichr(40960) + u'abcd' + unichr(1972)
    print uniStr
    f.write(uniStr.encode('utf8'))
    f.close()

if __name__ == "__main__":
    #test()
    main()
