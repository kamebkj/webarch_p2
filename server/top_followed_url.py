#  the most followed URLs
#
#  run: 
#			python top_followed_url.py logfile > top_url.out
#
from mrjob.job import MRJob
import json

class Top_followed_URL(MRJob):
	def mapper(self, line_no, line):
		cell = json.loads(line)
		if cell['action']=='redirect':
			yield cell['long'],1
		
	def reducer(self, item, counts):
		total = sum(counts)
		yield item, total

if __name__ == '__main__':        
	Top_followed_URL.run()
