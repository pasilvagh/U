import pp, sys, os

_input = ""
_output = ""
sep = 8

results = {}

#a callback to get results from each job execution
def aggregate_results(result):
	results[result[0]] = result[1]


class LZ77Compressor:
	MAX_WINDOW_SIZE = 400
	MAX_SEP = 4

	def __init__(self, window_size=20):
		self.window_size = min(window_size, self.MAX_WINDOW_SIZE) 
		self.lookahead_buffer_size = 15 # length of match is at most 4 bits

	def separateData(self, input_file_path, output_file_path=None, sep=2):

		if (sep <= 0):
			print "sep needs to be bigger than 0"
			return None

		self.sep = min(sep, self.MAX_SEP) 

		data = None
		i = 0

		# read the input file 
		try:
			with open(input_file_path, 'rb') as input_file:
				data = input_file.read()
		except IOError:
			print 'Could not open input file ...'
			raise
		input_file.close()

		#Separate input
		separated = []
		avg = int(len(data) / float(self.sep))
		out = []
		last = 0

		while last < len(data):
			if ((last + avg) % 8 == 0):
				separated.append(data[int(last):int(last + avg)])
				last += avg
			else:
				avg += 1

		return  separated

	def compress(self,data, _ind, last):
		print ("Computing results with PID [%d]" % os.getpid())
		"""
		Given the path of an input file, its content is compressed by applying a simple 
		LZ77 compression algorithm (for each piece of the input)

		The compressed format is:
		0 bit followed by 8 bits (1 byte character) when there are no previous matches
			within window
		1 bit followed by 12 bits pointer (distance to the start of the match from the 
			current position) and 4 bits (length of the match)
		"""
		output_buffer = bitarray.bitarray(endian='big')
		i = 0
		while i < len(data):
			match = self.findLongestMatch(data, i)

			if match: 
				(bestMatchDistance, bestMatchLength) = match
				output_buffer.append(True) # valor 0
				output_buffer.frombytes(chr(bestMatchDistance >> 4))
				output_buffer.frombytes(chr(((bestMatchDistance & 0xf) << 4) | bestMatchLength))

				i += bestMatchLength

			else:
				output_buffer.append(False)
				output_buffer.frombytes(data[i])

				i += 1
		

		if last:
			output_buffer.fill()
		return (_ind,output_buffer)
		


	def findLongestMatch(self, data, current_position):
		""" 
		Finds the longest match to a substring starting at the current_position 
		in the lookahead buffer from the history window
		"""
		end_of_buffer = min(current_position + self.lookahead_buffer_size, len(data) + 1)

		best_match_distance = -1
		best_match_length = -1

		for j in range(current_position + 2, end_of_buffer):

			start_index = max(0, current_position - self.window_size)
			substring = data[current_position:j]

			for i in range(start_index, current_position):

				repetitions = len(substring) / (current_position - i)

				last = len(substring) % (current_position - i)

				matched_string = data[i:current_position] * repetitions + data[i:i+last]

				if matched_string == substring and len(substring) > best_match_length:
					best_match_distance = current_position - i 
					best_match_length = len(substring)

		if best_match_distance > 0 and best_match_length > 0:
			return (best_match_distance, best_match_length)
		return None

if len(sys.argv) < 4:
	sys.exit('Usage: %s input-file output-file processors' % sys.argv[0])
if not os.path.exists(sys.argv[1]):
	sys.exit('ERROR: input-file %s was not found!' % sys.argv[1])
elif sys.argv[2] == "":
	sys.exit('ERROR: it is necessary an output-file name')
else:
	processors = 1
	if len(sys.argv) == 4:
		processors = int(sys.argv[3])
	_input = str(sys.argv[1])
	_output = str(sys.argv[2])

	compressor = LZ77Compressor(window_size=400)

	data = compressor.separateData(_input, _output, sep)
	quant = len(data)

	if data == None:
		print "Error in separateData"
		sys.exit(0)

	#create job server for parallelism  
	ppservers = ()
	job_server = pp.Server(processors,ppservers=ppservers)
	print "Starting pp with", job_server.get_ncpus(), "workers\n"

	i = 0
	for item in data:
		if i == (len(data)-1):
			_out = job_server.submit(compressor.compress,(item,i,True),(compressor.findLongestMatch,), modules=("bitarray", "math", "sys", "os", "io",),callback=aggregate_results)
		else:
			_out = job_server.submit(compressor.compress,(item,i,False),(compressor.findLongestMatch,), modules=("bitarray", "math", "sys", "os", "io",),callback=aggregate_results)
		i = i + 1

	job_server.wait()	
	job_server.print_stats()


	# write the compressed data into a binary file if a path is provided
	if _output:
		try:
			with open(_output, 'wb') as output_file:
				for key, value in results.items():
					output_file.write(value.tobytes())
				print "File was compressed successfully and saved to output path ..."
		except IOError:
			print 'Could not write to output file path. Please check if the path is correct ...'
			raise
		output_file.close()

