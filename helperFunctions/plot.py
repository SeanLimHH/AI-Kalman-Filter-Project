import matplotlib.pyplot as plt
from . import tools
import numpy as np

__all__ = ('plotContrastFlightXY', 'plotContrastFlightLongitudeLatitude', 'plotDifferencesAcrossFlights','plotAveragePropertiesAcrossFlights','plotFlightLongitudeLatitude')

def plotContrastFlightXY(flightOne, flightTwo, flightOneLabel = "First", flightTwoLabel = "Second"):
    
    flightOneLabel = tools.cleanStringForDisplay(flightOneLabel)
    flightTwoLabel = tools.cleanStringForDisplay(flightTwoLabel)


    plt.plot(flightOne.data['x'], flightOne.data['y'], label=flightOneLabel, color='b')
    
    plt.plot(flightTwo.data['x'], flightTwo.data['y'], label=flightTwoLabel, color='r')
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'{flightOneLabel} vs {flightTwoLabel}')
    plt.legend()
    
    plt.show()

def plotContrastFlightLongitudeLatitude(flightOne, flightTwo, flightOneLabel = "First", flightTwoLabel = "Second"):

    flightOneLabel = tools.cleanStringForDisplay(flightOneLabel)
    flightTwoLabel = tools.cleanStringForDisplay(flightTwoLabel)
    
    plt.plot(flightOne.data['longitude'], flightOne.data['latitude'], label=flightOneLabel, color='b')
    
    plt.plot(flightTwo.data['longitude'], flightTwo.data['latitude'], label=flightTwoLabel, color='r')
    
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(f'{flightOneLabel} vs {flightTwoLabel}')
    plt.legend()
    plt.show()

def plotDifferencesAcrossFlights(allFlightIDs, allDifferences, differenceType, colour = 'r'):
    
    differenceType = tools.cleanStringForDisplay(differenceType)
    
    numberOfFlights = len(allFlightIDs)
    flightLabels = [f'{flightID}' for flightID in allFlightIDs]
    bar_width = 0.75
    
    fig, ax = plt.subplots(figsize=(12, 8))
    index = np.arange(numberOfFlights)
    
    rects = ax.bar(index, allDifferences, bar_width, label=f'{differenceType} Difference', color=colour)
    ylabel = f'{differenceType} Differences'
    title = f'{differenceType} Differences Across Flights'

    ax.set_xlabel('Flights')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(index)
    ax.set_xticklabels(flightLabels, rotation=90)
    plt.show()


def plotAveragePropertiesAcrossFlights(allFlightIDs, averageProperties):
    numberOfFlights = len(allFlightIDs)
    flightLabels = [f'{flightID}' for flightID in allFlightIDs]
    
    for propertyName, values in averageProperties.items():
        
        propertyName = tools.cleanStringForDisplay(propertyName)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        index = range(numberOfFlights)

        rects = ax.bar(index, values, label=f'Average {propertyName}', color='b')
        ylabel = f'Average {propertyName}'
        title = f'Average {propertyName} Across Flights'

        ax.set_xlabel('Flights')
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.set_xticks(index)
        ax.set_xticklabels(flightLabels, rotation=90)
        plt.legend()
        plt.show()


def plotFlightLongitudeLatitude(flight, flightLabel="Flight"):
    plt.plot(flight.data['longitude'], flight.data['latitude'], label=flightLabel, color='b')

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(f'{flightLabel}')
    plt.legend()
    plt.show()
