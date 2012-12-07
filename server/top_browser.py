#  the counts per action per Browser
#
#  run: 
#			python top_browser.py logfile > top_browser.out
#
from mrjob.job import MRJob
import json

class Top_Browser(MRJob):
	def mapper(self, line_no, line):
		cell = json.loads(line)
		yield cell['user-agent'],1
		
	def reducer(self, item, counts):
		total = sum(counts)
		yield item, total

if __name__ == '__main__':        
	Top_Browser.run()
