import pandas as pd
import numpy as np


def join_events(eventType1, eventType2):
      ###joins two event types in two vectors of strings 
      ###to full join into the desired events
      full_events = []
      for i in range(len(eventType1)):
            for j in range(len(eventType1)):
                  full_events.append('/'.join([eventType1[i], eventType2[j]]))
      return full_events


def pick_event_type(eventType1, eventType2, e1color = 'Crimson', e2color = 'CornFlowerBlue', e1ltyp = '-', e2ltyp = '--'):
	###Assuming eventType1 is always the block i.e., canonical and reverse
	###eventype 1 will always differ in color and eventtype2 in linestyle
	###default colors are set
	###linestyle is fixed
	event_list = join_events(eventType1, eventType2)
	color = {eventType1[0]:e1color, eventType1[1]:e2color}
	linestyles = {eventType2[0]:e1ltyp, eventType2[1]:e2ltyp}

	return event_list, color, linestyles