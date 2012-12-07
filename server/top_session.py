#  the counts per action per Session
#
#  run: 
#			python top_session.py logfile 
#
from mrjob.job import MRJob
import json

class Top_Session(MRJob):
	def mapper(self, line_no, line):
		cell = json.loads(line)
		yield cell['id'],1
		
	def reducer(self, item, counts):
		total = sum(counts)
		yield item, total

if __name__ == '__main__':        
	Top_Session.run()
