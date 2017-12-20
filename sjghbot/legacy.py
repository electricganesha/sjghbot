import getopt
import sys
import time
from datetime import datetime

import poloniex


USAGE = (
    'sjghbot.py -p <period length> '
               '-c <currency pair> '
               '-n <period of moving average>'
)


def main(argv):

    # define the variables we will use
    period = 10
    pair = "BTC_XMR"
    prices = []
    currentMovingAverage = 0
    lengthOfMA = 0
    startTime = False
    endTime = False
    historicalData = False
    tradePlaced = False
    typeOfTrade = False
    dataDate = ""
    orderNumber = ""
    dataPoints = []
    localMax = []
    currentResistance = 0.018

    try:
        opts, args = getopt.getopt(
            argv,
            "hp:c:n:s:e:",
            ["period=", "currency=", "points="]
        )
    except getopt.GetoptError:
        print(USAGE)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(USAGE)
            sys.exit()
        elif opt in ("-p", "--period"):
            # TODO accept in minutes and convert
            if (int(arg) in [300, 900, 1800, 7200, 14400, 86400]):
                period = arg
            else:
                print(
                    'Poloniex requires periods in 300,900,1800,7200,14400, or'
                    ' 86400 second increments'
                )
                sys.exit(2)
        elif opt in ("-c", "--currency"):
            pair = arg
        elif opt in ("-n", "--points"):
            lengthOfMA = int(arg)
        elif opt in ("-s"):
            startTime = arg # store starting time value in startTime variable
        elif opt in ("-e"):
            endTime = arg # store end time value in endTime variable

    conn = poloniex.Public()

    output = open("chart.html",'w') # create an empty chart HTML file
    output.truncate() # truncate the file size with no value - variable size
    header = """
        <html><head><script type="text/javascript" src="https://www.gstatic.com'
        '/charts/loader.js"></script><script type="text/javascript">google.char'
        'ts.load('current', {'packages':['corechart']});google.charts.setOnLoad'
        'Callback(drawChart);function drawChart() {var data = new google.visual'
        'ization.DataTable();data.addColumn('string', 'time');data.addColumn('n'
        'umber', 'value');data.addColumn({type: 'string', role:'annotation'});d'
        'ata.addColumn({type: 'string', role:'annotationText'});data.addColumn('
        ''number', 'trend');data.addRows([
    """
    output.write(header)

    if (startTime):
        historicalData = conn.chart_data(
            currency_pair=pair,
            start=startTime,
            end=endTime,
            period=period
        )

    while True:
        if (startTime and historicalData):
            # returns the last object in the historicalData list
            nextDataPoint = historicalData.pop(0)
            lastPairPrice = nextDataPoint['weightedAverage']
            dataDate = datetime\
                .fromtimestamp(int(nextDataPoint['date']))\
                .strftime('%Y-%m-%d %H:%M:%S')
        elif(startTime and not historicalData):
            for point in dataPoints:
                point_attributes = (
                    'date',
                    'price',
                    'label',
                    'desc',
                    'trend'
                )
                point_output = "['"
                point_output += ','.join([point[a] for a in point_attributes])
                point_output += "],\n"
                output.write(point_output)
            footer = """
                ]);var options = {title: 'Price Chart',legend: { position: 'bot'
                "tom' }};var chart = new google.visualization.LineChart(documen"
                't.getElementById('curve_chart'));chart.draw(data, options);}</'
                'script></head><body><div id="curve_chart" style="width: 100%; '
                'height: 100%"></div></body></html>
            """
            output.write(footer)
            exit()
        else: # if there is no start time
            currentValues = conn.api_query("returnTicker") # Returns the ticker for all markets. POLONIEX API (see https://poloniex.com/support/api/)
            lastPairPrice = currentValues[pair]["last"] # returns the last currency pair (e.g. BTC_XMR) price ("last" property of the API)
            dataDate = datetime.utcnow() # defines the date as the current date

        # adds points to the list with the following properties : date, price, trend, label, desc
        dataPoints.append({'date':dataDate, 'price': str(lastPairPrice), 'trend': str(currentResistance), 'label': 'null', 'desc': 'null'})

        # if there are more than 2 data points AND the forehand price is bigger than the penultimate price AND the forehand price is higher than the pre-forehand price
        if ( (len(dataPoints) > 2) and (dataPoints[-2]['price'] > dataPoints[-1]['price']) and (dataPoints[-2]['price'] > dataPoints[-3]['price']) ):
            dataPoints[-2]['label'] = "'MAX'" # LABEL the point as a MAX point
            dataPoints[-2]['desc'] = "'This is a local maximum'" # LABEL the point as a local maximum

            numberOfSimilarLocalMaxes = 0
            for oldMax in localMax: # for each local maximum
                # if current local maximum is bigger than the forehand price - .0001 AND current local maximum is lower than the forehand price + .0001
                if ( (float(oldMax) > (float(dataPoints[-2]['price']) - .0001) ) and (float(oldMax) < (float(dataPoints[-2]['price']) + .0001) ) ):
                    numberOfSimilarLocalMaxes = numberOfSimilarLocalMaxes + 1 # increment number of similar local maximums

            if (numberOfSimilarLocalMaxes > 2): # if there are more than 2 local maximums - NORMALIZE LOCAL MAXIMUMS
                currentResistance = dataPoints[-2]['price'] # update local resistance with the forehand price
                dataPoints[-2]['trend'] = dataPoints[-2]['price']  # update the forehand trend with the forehand price
                dataPoints[-1]['trend'] = dataPoints[-2]['price']  # update the penultimate trend with the forehand price

            localMax.append(dataPoints[-2]['price']) # add the forehand price to the localMax list

        if (len(prices) > 0): # if the prices list is not empty
            currentMovingAverage = sum(prices) / float(len(prices)) # update currentMovingAverage with sum of all the prices / number of prices
            previousPrice = prices[-1] # previousPrice is equal to penultimate price
            if (not tradePlaced): # if there isn't a trade order
                if ( (lastPairPrice > currentMovingAverage) and (lastPairPrice < previousPrice) ): # if the last price is bigger than current moving average AND last price smaller than previous price
                    # SELL
                    print("SELL ORDER")
                    #orderNumber = conn.sell(pair,lastPairPrice,.01) # LIVE TRADING - DO NOT UNCOMMENT
                    tradePlaced = True
                    typeOfTrade = "short"
                elif ( (lastPairPrice < currentMovingAverage) and (lastPairPrice > previousPrice) ): # if the last price is smaller than current moving average AND last price bigger than previous price
                    # BUY
                    print("BUY ORDER")
                    #orderNumber = conn.buy(pair,lastPairPrice,.01) # LIVE TRADING - DO NOT UNCOMMENT
                    tradePlaced = True
                    typeOfTrade = "long"
            elif (typeOfTrade == "short"): # if we have a short trade
                if ( lastPairPrice < currentMovingAverage ): # if last price is smaller than moving average
                    # EXIT
                    print("EXIT TRADE")
                    #conn.cancel(pair,orderNumber) # LIVE TRADING - DO NOT UNCOMMENT
                    tradePlaced = False
                    typeOfTrade = False
            elif (typeOfTrade == "long"): # if we have a long trade
                if ( lastPairPrice > currentMovingAverage ): # if last price is bigger than moving average
                    # EXIT
                    print("EXIT TRADE")
                    #conn.cancel(pair,orderNumber)
                    tradePlaced = False
                    typeOfTrade = False
        else:
            previousPrice = 0

        # print result of analysis to console
        print("%s Period: %ss %s: %s Moving Average: %s" % (dataDate,period,pair,lastPairPrice,currentMovingAverage))

        prices.append(float(lastPairPrice)) # append result to prices list
        prices = prices[-lengthOfMA:] # update prices variable with the price index of the last moving average
        if (not startTime):
            time.sleep(int(period)) # wait for "period" seconds


if __name__ == "__main__":
    main(sys.argv[1:])
