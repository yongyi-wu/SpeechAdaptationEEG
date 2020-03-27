import pandas as pd
import numpy as np


def join_events(eventType1, eventType2):
      ###joins two event types in two vectors of strings 
      ###to full join into the desired events
      full_events = []
      for i in range(len(eventType1)):
            for j in range(len(eventType1)):
                  full_events.append('/'.join([eventType1[i], eventType2[j]]))
      return(full_events)

