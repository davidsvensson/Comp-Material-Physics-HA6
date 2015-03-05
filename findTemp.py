import re
import linecache
import numpy as np

numlines = 0
stopIteration = 350000 
stopForLoop = False
with open('log.lammps', 'r') as logFile:
	for line in logFile:
		numlines += 1
		if 'T equal' in line:
			iniTemperature = int(re.findall('\d+.\d+',line)[0])
		elif '# Run simulation' in line:
			simLine = numlines
			numInteration = int(re.findall('\d+',linecache.getline('log.lammps', simLine+3))[0])
			startInteration = int(re.findall('\d+',linecache.getline('log.lammps', simLine+6))[0])
			stopIteration = numInteration + startInteration
		elif str(stopIteration) in line and numlines > simLine:
			stopLine = numlines
			stopForLoop = True
		
		if stopForLoop: break


temperArray = np.array([])
energyArray = np.array([])
for line in range(simLine+6,stopLine+1):
	temperArray =  np.append(temperArray,float(re.findall('\d+.\d+',linecache.getline('log.lammps', line))[1]))

	energyArray =  np.append(energyArray,float(re.findall('\d+.\d+',linecache.getline('log.lammps', line))[2]))
