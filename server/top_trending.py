#  the trending url
#
#  run: 
#			python top_trending.py logfile 
#
from datetime import datetime, timedelta
from mrjob.job import MRJob
import json
now = datetime.now ()

class Top_trending(MRJob):
	def mapper(self, line_no, line):
		cell = json.loads(line)
		
		if	(now - datetime.strptime(cell['datetime'], "%a, %d-%b-%Y %H:%M:%S PST")) < timedelta(days =1) and cell['action']=="redirect":
			yield cell['long'],1
		
	def reducer(self, item, counts):
		total = sum(counts)
		yield item, total

if __name__ == '__main__':        
	Top_trending.run()
