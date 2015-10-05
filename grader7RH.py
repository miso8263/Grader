#!/usr/bin/env python3
""" 
Grader for CSCI 1300 - Experienced
Assignment 7
Expects command line arguments:
(1) Path to sudent submission
(2) Path to grader files
Outputs grade out of 100 pts to stdout
"""

import sys
import random
import subprocess
import time
import os
import shutil

FILENAME = "Assignment7"

def grade(argv):
	student_files = os.listdir(argv[0])
	file_count = 0
	for entry in student_files:
		if entry == FILENAME:
			file_count += 1
			student_file = entry
	if (file_count > 1):
		sys.stderr.write("More than one file received.  Expected one file.")
		exit(1)
	elif(file_count == 0):
		sys.stderr.write("{:s} not found. Check that it compiles correctly.  Naming must be exact.".format(FILENAME))
		exit(1)
	
	
	#begin grading
	sub_path = os.path.abspath("{:s}/{:s}".format(argv[0], student_file))
	sys.stderr.write("Grading {:s}\n".format(student_file))
	sys.stderr.write("__________________________\n")
	
	#change to their directory
	os.chdir(argv[0])
	
	score = 0
	football_inputs = ['16 25 267 1 2', '324 461 3969 35 10', '180 316 2647 18 6', '319 516 3529 24 12', '362 557 3297 31 11']
	football_answers = [79.92, 112.79, 95.53, 87.91, 91.23]
	football_words = ["poor", "great", "great", "mediocre", "good"]
	football_error = 0.5
	
	cycling_inputs = ['75 12 10 1', '100 5 10 1','63 15 10.8 4', '90 15 5 5', '50 10 7 2']
	cycling_answers = [8611.58, 8717.4, 10699.0, 1321.2, 3025.26]
	cycling_errors = [2700.0, 2700.0, 3403.0, 338.0, 927.0]
	
	sys.stderr.write("\n\n-------- Testing Football Problem --------\n\n")
	for j in range (1, 6):
		sys.stderr.write("\n-------- Running test"+str(j)+" --------\n")
		file_list = football_inputs[j-1].split()
		try:
			prog_output = subprocess.check_output([sub_path, '-f', '-p', file_list[0], '-a', file_list[1], '-y', file_list[2], '-t', file_list[3], '-i', file_list[4]])
		except Exception as e:
			sys.stderr.write("Error occured running program: {:s}\n".format(str(e)))
			exit(1)
		
		prog_string = prog_output.decode()
		prog_string = prog_string.rstrip("\n")
		prog_string = prog_string.rstrip(".")
		prog_string = prog_string.rstrip("!")
		prog_words = prog_string.split(" ")
		
		student_answer = 0
		for word in prog_words:
			try:
				word = word.strip(",")
				word = word.strip(".")
				student_answer = eval(word)
			except Exception as e:
				pass
		high_bound = football_answers[j-1] + football_error
		low_bound = football_answers[j-1] - football_error
		
		if (student_answer < high_bound) and (student_answer > low_bound):
			sys.stderr.write("\nReceived: {:f}\n".format(student_answer))
			sys.stderr.write("Expected: {:.2f}\n".format(football_answers[j-1]))
			sys.stderr.write("Correct!\n")
			score += 5
		elif (student_answer == 0):
			inputstr = "-f -p "+ file_list[0] + " -a " + file_list[1] + " -y " + file_list[2] + " -t " + file_list[3] + " -i " + file_list[4]
			sys.stderr.write("\nInput was: {:s} \n".format(inputstr))
			sys.stderr.write("\nReceived: {:s}\n".format(prog_string))
			sys.stderr.write("Expected: {:.2f}\n".format(football_answers[j-1]))
			sys.stderr.write("Incorrect!  Could not find number in student output.  Check that numbers are separated by spaces.\n")
		else:
			inputstr = "-f -p "+ file_list[0] + " -a " + file_list[1] + " -y " + file_list[2] + " -t " + file_list[3] + " -i " + file_list[4]
			sys.stderr.write("\nInput was: {:s} \n".format(inputstr))
			sys.stderr.write("\nFound: {:f}\n".format(student_answer))
			sys.stderr.write("Expected: {:.2f}\n".format(football_answers[j-1]))
			sys.stderr.write("Incorrect!\n")
			
		if football_words[j-1] in prog_words:
			sys.stderr.write("\nReceived: {:s}\n".format(prog_string))
			sys.stderr.write("Looking for: {:s}\n".format(football_words[j-1]))
			sys.stderr.write("Correct!\n")
			score += 5
		else:
			inputstr = "-f -p "+ file_list[0] + " -a " + file_list[1] + " -y " + file_list[2] + " -t " + file_list[3] + " -i " + file_list[4]
			sys.stderr.write("\nInput was: {:s} \n".format(inputstr))
			sys.stderr.write("\nReceived: {:s}\n".format(prog_string))
			sys.stderr.write("Looking for: {:s}\n".format(football_words[j-1]))
			sys.stderr.write("Incorrect!\nMake sure your word is spelled correctly and is separated by spaces.\n")
	
	sys.stderr.write("\n\n-------- Testing Cycling Problem --------\n\n")
	for k in range (1, 6):
		sys.stderr.write("\n-------- Running test"+str(k)+" --------\n")
		file_list = cycling_inputs[k-1].split()
		try:
			prog_output = subprocess.check_output([sub_path, '-c', '-m', file_list[0], '-b', file_list[1], '-v', file_list[2], '-d', file_list[3]])
		except Exception as e:
			sys.stderr.write("Error occured running program: {:s}\n".format(str(e)))
			exit(1)
		
		prog_string = prog_output.decode()
		prog_string = prog_string.rstrip("\n")
		prog_list = prog_string.split("\n")
		
		last_line = prog_list[-1]
		last_list = last_line.split(" ")
		
		student_answer = 0
		for word in last_list:
			word = word.strip(".")
			word = word.strip(",")
			try:
				student_answer = eval(word)
			except Exception as e:
				pass
		
		high_bound = cycling_answers[k-1] + cycling_errors[k-1]
		low_bound =  cycling_answers[k-1] - cycling_errors[k-1]
		if (student_answer < high_bound) and (student_answer > low_bound):
			sys.stderr.write("\nReceived: {:f}\n".format(student_answer))
			sys.stderr.write("Expected final average in the range: {:.2f}\n".format(cycling_answers[k-1]))
			sys.stderr.write("Correct!\n")
			score += 10
		elif(student_answer == 0):
			inputstr = "-c -m "+ file_list[0] + " -b " + file_list[1] + " -v " + file_list[2] + " -d " + file_list[3]
			sys.stderr.write("\nInput was: {:s} \n".format(inputstr))
			sys.stderr.write("\nReceived: {:s}\n".format(prog_string))
			sys.stderr.write("Expected final average in the range: {:.2f}\n".format(cycling_answers[k-1]))
			sys.stderr.write("Incorrect!  Could not find number in student output.  Check that numbers are separated by spaces.\n")
		else:
			inputstr = "-c -m "+ file_list[0] + " -b " + file_list[1] + " -v " + file_list[2] + " -d " + file_list[3]
			sys.stderr.write("\nInput was: {:s} \n".format(inputstr))
			sys.stderr.write("\nFound: {:f}\n".format(student_answer))
			sys.stderr.write("Expected final average in the range: {:.2f}\n".format(cycling_answers[k-1]))
			sys.stderr.write("Incorrect!\nCheck that your loop runs the correct number of minutes\nand that you are seeding and calculating your random Cf correctly.\n")
		
		
	sys.stderr.write("__________________________\n")
	sys.stderr.write("Score ---------------> {:2d}/100\n".format(score))
	sys.stdout.write("{:2d}\n".format(score))
	return 0
	
if __name__ == "__main__":
	sys.exit(grade(sys.argv[1:]))
