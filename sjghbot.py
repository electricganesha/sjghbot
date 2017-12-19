import time
import sys, getopt
import datetime

import poloniex

# main function - where the whole program rests
# TODO create an object oriented structure with modules
def main(argv):

	# define the variables we will use
	period = 10
	pair = "BTC_XMR"
	prices = []
	currentMovingAverage = 0;
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
		opts, args = getopt.getopt(argv,"hp:c:n:s:e:",["period=","currency=","points="]) # retrieves the command line parameters (arguments) passed
	except getopt.GetoptError: # if the mandatory arguments are missing (period, currency, or points)
		print 'sjghbot.py -p <period length> -c <currency pair> -n <period of moving average>' # prints the usage of the command
		sys.exit(2)

	for opt, arg in opts: # for each argument passed, verifies which function to execute
		if opt == '-h': # if argument is -h (HELP)
			print 'sjghbot.py -p <period length> -c <currency pair> -n <period of moving average>' # prints the usage of the command
			sys.exit()
		elif opt in ("-p", "--period"): # verify if period values are well input
			if (int(arg) in [300,900,1800,7200,14400,86400]): # if period is not a subset of the allowed period (in seconds) #TODO accept in minutes and convert
				period = arg # store period in period variable
			else:
				print 'Poloniex requires periods in 300,900,1800,7200,14400, or 86400 second increments' # if period is not in the range - display warning message
				sys.exit(2)
		elif opt in ("-c", "--currency"):
			pair = arg # store currency value in pair variable
		elif opt in ("-n", "--points"):
			lengthOfMA = int(arg) # store length of moving averages value in lengthOfMA variable
		elif opt in ("-s"):
			startTime = arg # store starting time value in startTime variable
		elif opt in ("-e"):
			endTime = arg # store end time value in endTime variable



	conn = poloniex.Public('key goes here','key goes here') # definition of the connection with the poloniex API

	output = open("chart.html",'w') # create an empty chart HTML file
	output.truncate() # truncate the file size with no value - variable size
	output.write("""<html><head><script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script><script type="text/javascript">google.charts.load('current', {'packages':['corechart']});google.charts.setOnLoadCallback(drawChart);function drawChart() {var data = new google.visualization.DataTable();data.addColumn('string', 'time');data.addColumn('number', 'value');data.addColumn({type: 'string', role:'annotation'});data.addColumn({type: 'string', role:'annotationText'});data.addColumn('number', 'trend');data.addRows([""") # write the headers for the html file

	if (startTime): # if there is a start time - retrieve the historical data from that period from the POLONIEX API - and stores it in a list
		historicalData = conn.api_query("returnChartData",{"currencyPair":pair,"start":startTime,"end":endTime,"period":period})

	while True: # keeps the program running ad-eternum
		if (startTime and historicalData): # if historical data was retrieved
			nextDataPoint = historicalData.pop(0) # returns the last object in the historicalData list - pop(0) -> return the object in the 0 index of the list
			lastPairPrice = nextDataPoint['weightedAverage'] # gets the weightedAverage property of the object (see https://poloniex.com/support/api/)
			dataDate = datetime.datetime.fromtimestamp(int(nextDataPoint['date'])).strftime('%Y-%m-%d %H:%M:%S') # converts the object property 'date' into a python readable date
		elif(startTime and not historicalData): # if historical data was not retrieved
			for point in dataPoints: # go through each point in dataPoints array
				output.write("['"+point['date']+"',"+point['price']+","+point['label']+","+point['desc']+","+point['trend']) # write values into the chart
				output.write("],\n") # write new line into the chart
			output.write("""]);var options = {title: 'Price Chart',legend: { position: 'bottom' }};var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));chart.draw(data, options);}</script></head><body><div id="curve_chart" style="width: 100%; height: 100%"></div></body></html>""") # write html footer
			exit()
		else: # if there is no start time
			currentValues = conn.api_query("returnTicker") # Returns the ticker for all markets. POLONIEX API (see https://poloniex.com/support/api/)
			lastPairPrice = currentValues[pair]["last"] # returns the last currency pair (e.g. BTC_XMR) price ("last" property of the API)
			dataDate = datetime.datetime.now() # defines the date as the current date

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
					print "SELL ORDER"
					#orderNumber = conn.sell(pair,lastPairPrice,.01) # LIVE TRADING - DO NOT UNCOMMENT
					tradePlaced = True
					typeOfTrade = "short"
				elif ( (lastPairPrice < currentMovingAverage) and (lastPairPrice > previousPrice) ): # if the last price is smaller than current moving average AND last price bigger than previous price
					# BUY
					print "BUY ORDER"
					#orderNumber = conn.buy(pair,lastPairPrice,.01) # LIVE TRADING - DO NOT UNCOMMENT
					tradePlaced = True
					typeOfTrade = "long"
			elif (typeOfTrade == "short"): # if we have a short trade
				if ( lastPairPrice < currentMovingAverage ): # if last price is smaller than moving average
					# EXIT
					print "EXIT TRADE"
					#conn.cancel(pair,orderNumber) # LIVE TRADING - DO NOT UNCOMMENT
					tradePlaced = False
					typeOfTrade = False
			elif (typeOfTrade == "long"): # if we have a long trade
				if ( lastPairPrice > currentMovingAverage ): # if last price is bigger than moving average
					# EXIT
					print "EXIT TRADE"
					#conn.cancel(pair,orderNumber)
					tradePlaced = False
					typeOfTrade = False
		else:
			previousPrice = 0

		# print result of analysis to console
		print "%s Period: %ss %s: %s Moving Average: %s" % (dataDate,period,pair,lastPairPrice,currentMovingAverage)

		prices.append(float(lastPairPrice)) # append result to prices list
		prices = prices[-lengthOfMA:] # update prices variable with the price index of the last moving average
		if (not startTime):
			time.sleep(int(period)) # wait for "period" seconds


if __name__ == "__main__":
	main(sys.argv[1:])
