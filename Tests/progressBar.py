import time
def tqdmbar():
	from tqdm import tqdm
	for i in tqdm (range(101), 
		desc="Loading...",
		ascii=True, ncols=75):
		time.sleep(0.1)
	print("Program is completed enjoy: (.) (.)")

def progress():
	import progressbar
	widgets = [' [',
			progressbar.Timer(format= 'elapsed time: %(elapsed)s'),
			'] ',
			progressbar.Bar('*'),' (',
			progressbar.ETA(), ') ',
			]

	bar = progressbar.ProgressBar(max_value=200, 
								widgets=widgets).start()

	for i in range(200):
		time.sleep(0.1)
		bar.update(i)

def codeBySomeoneElse():
	import sys,random
	def progressBar(count_value, total, suffix=''):
		bar_length = 100
		filled_up_Length = int(round(bar_length* count_value / float(total)))
		percentage = round(100.0 * count_value/float(total),1)
		bar = '=' * filled_up_Length + '-' * (bar_length - filled_up_Length)
		sys.stdout.write('[%s] %s%s ...%s\r' %(bar, percentage, '%', suffix))
		sys.stdout.flush()
	for i in range(11):
		time.sleep(random.random())
		progressBar(i,10)
	#This function was Contributed by PL VISHNUPPRIYAN

codeBySomeoneElse()	