import re
import linecache
import numpy as np

# Loops though the folders T_XXXX and save the temp + std 
# and potE + std
for runTemp in ['npt1','npt2']:


	logfile = './'+runTemp+'/log.lammps'

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
				numInteration = int(re.findall('\d+',linecache.getline(logfile, simLine+5))[0])
				startInteration = int(re.findall('\d+',linecache.getline(logfile, simLine+8))[0])
				stopIteration = numInteration + startInteration
			elif str(stopIteration) in line and numlines > simLine:
				stopLine = numlines
				stopForLoop = True # Stop after the first stopIteration after startIteration has been found
			
			if stopForLoop: break


	temperArray = np.array([])
	potEnergyArray = np.array([])
	volArray = np.array([])

	# Get the temperature and energy from the simulation
	for line in range(simLine+8,stopLine+1): 
		temperArray =  np.append(temperArray,float(re.findall('\d+.\d+',linecache.getline(logfile, line))[1]))
		potEnergyArray =  np.append(potEnergyArray,float(re.findall('\d+.\d+',linecache.getline(logfile, line))[3]))
		sizeStr = re.findall('\d+.\d+',linecache.getline(logfile, line))[8:11]		
		size = [0,0,0]
		size[0] = float(sizeStr[0])
		size[1] = float(sizeStr[1])
		size[2] = float(sizeStr[2])
		vol = size[0]*size[1]*size[2]
		volArray = np.append(volArray, vol)
	

	temperature = np.average(temperArray)
	temperatureStd = np.std(temperArray,ddof=1)
	potEnergy = np.average(potEnergyArray)/nbrAtoms #pot energy per atom
	potEnergyStd = np.std(potEnergyArray,ddof=1)/nbrAtoms
	volume = np.average(volArray)/nbrAtoms
	result = str(iniTemperature)+'\t'+str(temperature)+'\t'+str(temperatureStd)+'\t'+str(potEnergy)+'\t'+str(potEnergyStd)+'\t'+str(volume)+'\n'

	with open('tempVolData', 'a') as myfile:
		myfile.write(result)
