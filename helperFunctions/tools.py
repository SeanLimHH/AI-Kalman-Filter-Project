__all__ = ('updateXYFromPredictions','getLatLongTupleFromFlight','getXYFromFlight', 'set_lat_lon_from_x_y','getComparablePropertiesFromFlight','getAveragePropertiesAcrossFlightsForPlot','cleanStringForDisplay')

import numpy as np

def updateXYFromPredictions(flight, predictions): # Predictions should be a m by 2 matrix
    flight.data[['x', 'y']] = predictions
    return flight

def getLatLongTupleFromFlight(flight):
    desiredTuple = np.array(flight.data[['latitude','longitude']])
    desiredTuple = tuple(map(tuple,desiredTuple))
    return desiredTuple

def getXYFromFlight(flight):
    return flight.data.loc[:, ['x', 'y']].values

def set_lat_lon_from_x_y(flight, projection_for_flight):
    """
    set_lat_lon_from_x_y(flight) updates the given flight's latitudes and longitudes to reflect its x, y positions
    in the data.
    The intended use of this function is to:
      1. make a (deep) copy of a flight that you got from get_radar_data
      2. use a kalman filter on that flight and set the x, y columns of the data to the filtered positions
      3. call set_lat_lon_from_x_y() on that flight to set its latitude and longitude columns according to the
        filtered x,y positions
    Step 3 is necessary, if you want to plot the data, because plotting is based on the lat/lon coordinates and not
    based on x,y.

    :param flight:
    :return: the same flight
    """
    projection = projection_for_flight[flight.flight_id]
    if projection is None:
        print("No projection found for flight %s. You probably did not get this flight from get_radar_data()." % (
            flight.flight_id))

    lons, lats = projection(flight.data["x"], flight.data["y"], inverse=True)
    flight.data["longitude"] = lons
    flight.data["latitude"] = lats
    return flight


def getComparablePropertiesFromFlight(allFlights, excludeProperties=None):
    # Returns all properties that ALL flights have.
    allFlightProperties = set(allFlights[0].data.columns.values)
    if excludeProperties:
        allFlightProperties -= set(excludeProperties)
    
    # Remove properties not present in all flights
    for flight in allFlights[1:]: # Use the first flight as a comparison base. So we use this to compare to every other flight.
        flightProperties = set(flight.data.columns.values)
        allFlightProperties &= flightProperties # If the flight property does not exist for any flight; take it out from all flight properties.

    return allFlightProperties


def getAveragePropertiesAcrossFlightsForPlot(allFlights, undesiredProperties=None):
    import pandas as pd
    averageOfProperties = {}
    
    desiredProperties = []
    for flight in allFlights:
        # I only want to plot numeric columns.
        # I need this loop to ensure that all properties of all flights are iterated;
        # This is because some flights do not have certain properties.
        numericColumns = flight.data.select_dtypes(include=['number'])
        desiredProperties = set(desiredProperties) | set(col for col in numericColumns.columns if col not in undesiredProperties)

    # Here we shall compute the mean for each flight's properties. If the flight does not have
    # the property, we set it to 0
    for property in desiredProperties:
        propertyValues = []

        for flight in allFlights:
            if property in flight.data.columns:
                propertyValues.append(flight.data[property].mean())
            else:
                propertyValues.append(0)
        averageOfProperties[property] = propertyValues

    # Filter out all 0s. If all properties have value 0, remove it out; do not plot.
    propertiesToRemove = [prop for prop, values in averageOfProperties.items() if all(value == 0 for value in values)]
    for property in propertiesToRemove:
        del averageOfProperties[property]
    
    return averageOfProperties
 

    
def cleanStringForDisplay(dirtyString):
    formattedString = dirtyString.title()
    formattedString = formattedString.replace('_', ' ')
    formattedString = formattedString.strip()
    return formattedString
