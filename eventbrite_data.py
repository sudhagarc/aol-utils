from eventbrite import Eventbrite
import json

eventbrite = Eventbrite('<ENTER-YOUR-TOKEN-HERE>')

def getAllEventsData():
	event_data = []
	events = eventbrite.api("get", "/users/me/owned_events", {})
	for event in events['events']:
		if event['status'] == 'completed':
			event_data.append({
			'event_id':event['id'],
			'event_name':event['name']['html'],
			'event_date':event['start']['local'],
			'attendees': getAttendeesByEvent(event['id'])})

	# return
	while 'continuation' in events['pagination']:
		contId = events['pagination']['continuation']
		events = eventbrite.api("get",
		"/users/me/owned_events?continuation=" + contId, {})
		for event in events['events']:
			if event['status'] == 'completed':
				event_data.append({
				'event_id':event['id'],
				'event_name':event['name']['html'],
				'event_date':event['start']['local'],
				'attendees': getAttendeesByEvent(event['id'])})

		print(json.dumps(events['pagination'], indent=2))
	return event_data


def getAttendeesByEvent(eventId):
	attendees_data = []
	attendees = eventbrite.api("get", "/events/" + eventId +
	    "/attendees", {})

	if attendees['attendees']:
		for a in attendees['attendees']:
			data = a['profile']
			attendees_data.append({
				'name':data.get('name'),
				'email':data.get('email'),
				'phone':data.get('cell_phone', 'empty')})

	while 'continuation' in attendees['pagination']:
		contId = attendees['pagination']['continuation']
		attendees = eventbrite.api("get",
			"/events/" + eventId + "/attendees?continuation=" + contId,
			{})
		if attendees['attendees']:
			for a in attendees['attendees']:
				data = a['profile']
				attendees_data.append({
					'name':data.get('name'),
					'email':data.get('email'),
					'phone':data.get('cell_phone', 'empty')})

		print(json.dumps(orders['pagination'], indent=2))
	return attendees_data

def formatToCsv(data, file_name):
	with open(file_name, 'w') as f:
		for event in data:
			if event['attendees']:
				for a in event['attendees']:
					f.write('''{0}, {1}, {2}, {3}, {4}\n'''.format(
						event['event_name'],
						event['event_date'],
						a['name'],
						a['email'],
						a['phone']))
