import re
import linecache
import numpy as np

# Loops though the folders T_XXXX and save the temp + std 
# and potE + std
for runTemp in range(750, 1401, 25):


	logfile = './T_'+str(runTemp)+'/log.lammps'

	numlines = 0
	stopIteration = 350000 
	stopForLoop = False

	# Find the line-nbrs for the data and initTemperature from logfile
	with open(logfile, 'r') as logFile:
		for line in logFile:
			numlines += 1
			if 'T equal' in line: # Find the initial temp
				iniTemperature = int(re.findall('\d+',line)[0])
			elif 'Created' in line and 'atoms' in line:
				nbrAtoms = int(re.findall('\d+',line)[0])



			elif '# Run simulation' in line: # Find the first and last line of simulation
				simLine = numlines
				numInteration = int(re.findall('\d+',linecache.getline(logfile, simLine+3))[0])
				startInteration = int(re.findall('\d+',linecache.getline(logfile, simLine+6))[0])
				stopIteration = numInteration + startInteration
			elif str(stopIteration) in line and numlines > simLine:
				stopLine = numlines
				stopForLoop = True # Stop after the first stopIteration after startIteration has been found
			
			if stopForLoop: break


	temperArray = np.array([])
	potEnergyArray = np.array([])

	# Get the temperature and energy from the simulation
	for line in range(simLine+6,stopLine+1): 
		temperArray =  np.append(temperArray,float(re.findall('\d+.\d+',linecache.getline(logfile, line))[1]))
		potEnergyArray =  np.append(potEnergyArray,float(re.findall('\d+.\d+',linecache.getline(logfile, line))[3]))
	temperature = np.average(temperArray)
	temperatureStd = np.std(temperArray,ddof=1)
	potEnergy = np.average(potEnergyArray)/nbrAtoms #pot energy per atom
	potEnergyStd = np.std(potEnergyArray,ddof=1)/nbrAtoms
	result = str(iniTemperature)+'\t'+str(temperature)+'\t'+str(temperatureStd)+'\t'+str(potEnergy)+'\t'+str(potEnergyStd)+'\n'

	with open('temperatureData', 'a') as myfile:
		myfile.write(result)
