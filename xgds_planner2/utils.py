#__BEGIN_LICENSE__
# Copyright (c) 2015, United States Government, as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All rights reserved.
#
# The xGDS platform is licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#__END_LICENSE__
# pylint: disable=W0702


from django.conf import settings
from geocamUtil.loader import LazyGetModelByName

ACTIVE_FLIGHT_MODEL = LazyGetModelByName(settings.XGDS_PLANNER2_ACTIVE_FLIGHT_MODEL)
FLIGHT_MODEL = LazyGetModelByName(settings.XGDS_PLANNER2_FLIGHT_MODEL)

def getFlight(event_time, vehicle):
    """ Returns the flight that contains that event_time """
    if vehicle:
        found_flights = FLIGHT_MODEL.get().objects.exclude(end_time__isnull=True).filter(vehicle=vehicle, start_time__lte=event_time, end_time__gte=event_time)
    else:
        found_flights = FLIGHT_MODEL.get().objects.exclude(end_time__isnull=True).filter(start_time__lte=event_time, end_time__gte=event_time)
        
    if found_flights.count() == 0:
        found_active_flight =  getActiveFlight(vehicle)
        if found_active_flight:
            if event_time >= found_active_flight.start_time:
                return found_active_flight;
        return None
    else:
        return found_flights[0]
    
    
def getNextAlphabet(character):
    """
    For getting the next letter of the alphabet for prefix.
    """
    # a is '97' and z is '122'. There are 26 letters total
    nextChar = ord(character) + 1
    if nextChar > 122:
        nextChar = (nextChar - 97) % 26 + 97
    return chr(nextChar)
    
    
def getActiveFlight(vehicle):
    if vehicle:
        foundFlights = ACTIVE_FLIGHT_MODEL.get().objects.filter(flight__vehicle = vehicle)
    else:
        foundFlights = ACTIVE_FLIGHT_MODEL.get().objects.filter()
        
    if foundFlights:
        return foundFlights[0].flight
    return None