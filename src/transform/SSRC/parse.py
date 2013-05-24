# i/o module
import io
# regex module
import re
# used for sys.argv
import sys
# used to pause the program at the end of its run
import time
#
# used to iterate over the lines of all files listed in sys.argv[1:]
# import fileinput
#
# opens the text file,
# places the lines into an array,
# and closes the file
f = open(sys.argv[1], 'r');
data = f.readlines();
f.close();
#
# creates a new text file to store
# the sorted component fields in
fileNameEx = re.compile('[\S^.]*.');
fileNameM = fileNameEx.match(sys.argv[1]);
cleanFileName = fileNameM.group(0).strip('.');
sortedFile = cleanFileName + '_sorted.txt';
sortedf = open(sortedFile, 'x');
#
# regular expressions
restartEx = re.compile(' RESTART ');
timestampEx = re.compile(' TIMESTAMP' );
decEx = re.compile('\d*');
spaceDecEx = re.compile(' \d*');
uidEx = re.compile('UID \d*');
pidEx = re.compile('PID \d*');
pNameEx = re.compile(' \?\?');
pNameEx2 = re.compile(' [\S]* [A-Z] ');
pNameEx3 = re.compile(' \S* ');
absEx = re.compile(' [A-Z] ');
timesEx = re.compile(' \d*\.\d* ');
callEx = re.compile(' \S*[(].*[)] ');
rtrnEx = re.compile('= \S* ?');
rtrnEx2 = re.compile(' \S* ?');
repsEx = re.compile(' [(]\d*[)] ?');
#
# component fields
offset = [];
uid = [];
pid = [];
process = [];
abs = [];
times = [];
call = [];
rtrn = [];
reps = [];
#
#line iterator
i = 0;
for line in data:
	lineNum = str(i+1);
	sortedf.write('Line ');
	sortedf.write(lineNum);
	sortedf.write(':\n');
	if restartEx.search(line):
		#print('RESTART!\n');
		sortedf.write('RESTART!\n\n');
		time.sleep(0.5);
	elif timestampEx.search(line):
		#print('TIMESTAMP!\n');
		sortedf.write('TIMESTAMP!\n\n');
		time.sleep(0.5);
	else:
		#print(line);
		# finds and stores offset
		offM = decEx.match(line);
		offset.append(offM.group(0));
		#print('Offset:', offM.group(0));
		sortedf.write('Offset: ');
		sortedf.write(offM.group(0));
		sortedf.write('\n');
		#
		# finds and stores UID
		# begins by finding the string that matches
		# the regex "UID #*"; then finds the actual
		# UID number within the substring
		uidM = uidEx.search(line);
		uidM2 = spaceDecEx.search(uidM.group(0));
		cleanUid = uidM2.group(0).strip();
		uid.append(cleanUid);
		#print('UID:', cleanUid);
		sortedf.write('UID: ');
		sortedf.write(cleanUid);
		sortedf.write('\n');
		#
		# finds and stores the PID
		# begins by finding the string that matches
		# the regex "PID #*"; then finds the actual
		# PID number within the substring
		pidM = pidEx.search(line);
		pidM2 = spaceDecEx.search(pidM.group(0));
		cleanPid = pidM2.group(0).strip();
		pid.append(cleanPid);
		#print('PID:', cleanPid);
		sortedf.write('PID: ');
		sortedf.write(cleanPid);
		sortedf.write('\n');
		#
		# finds and stores the process
		# searches for "??" before looking
		# for an actual process directory/name
		pNameM = pNameEx.search(line);
		if pNameM:
			cleanPName = pNameM.group(0).strip();
			process.append(cleanPName);
			#print('Process:', cleanPName);
			sortedf.write('Process: ');
			sortedf.write(cleanPName);
			sortedf.write('\n');
		else:
			pNameM2 = pNameEx2.search(line);
			pNameM3 = pNameEx3.match(pNameM2.group());
			cleanPName3 = pNameM3.group(0).strip();
			process.append(cleanPName3);
			#print('Process:', cleanPName3);
			sortedf.write('Process: ');
			sortedf.write(cleanPName3);
			sortedf.write('\n');
		#
		# finds and stores the A/B/S value
		absM = absEx.search(line);
		cleanAbs = absM.group(0).strip();
		abs.append(cleanAbs);
		sortedf.write('A/B: ');
		sortedf.write(cleanAbs);
		sortedf.write('\n');
		#print('A/B:', cleanAbs);
		#
		# finds and stores the timestamp
		timesM = timesEx.search(line);
		cleanTimes = timesM.group(0).strip();
		times.append(cleanTimes);
		#print("Timestamp:", cleanTimes);
		sortedf.write('Timestamp: ');
		sortedf.write(cleanTimes);
		sortedf.write('\n');
		#
		# finds and stores the system call
		callM = callEx.search(line);
		cleanCall = callM.group(0).strip();
		call.append(cleanCall);
		#print('Call:', cleanCall);
		sortedf.write('Call: ');
		sortedf.write(cleanCall);
		sortedf.write('\n');
		#
		# finds the return value for the
		# system call found above and stores it
		rtrnM = rtrnEx.search(line);
		rtrnM2 = rtrnEx2.search(rtrnM.group(0));
		cleanRtrn = rtrnM2.group(0).strip();
		rtrn.append(cleanRtrn);
		#print("Return:", cleanRtrn);
		sortedf.write('Return: ');
		sortedf.write(cleanRtrn);
		sortedf.write('\n');
		#
		# if available, finds the number of repetitions
		# of the system call found above and stores it
		repsM = repsEx.search(line);
		if repsM:
			cleanReps = repsM.group(0).strip(' ()');
			cleanerReps = cleanReps.strip('()');
			reps.append(cleanReps);
			#print("Repetitions:", cleanReps);
			sortedf.write('Repetitions: ');
			sortedf.write(cleanReps);
			sortedf.write('\n');
		else:
			reps.append('1');
			sortedf.write('Repetitions: ');
			sortedf.write('1');
			sortedf.write('\n');
		#time.sleep(0.025);
		#print('\n');
		sortedf.write('\n');
	i = i + 1;
sortedf.close();
#time.sleep(10);