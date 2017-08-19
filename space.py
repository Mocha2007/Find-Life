import random
from math import ceil
ufile=open("u.sav", "r")#universe
ffile=open("f.sav", "r")#fleet
pfile=open("p.sav", "r")#player money, stats, etc
sfile=open("s.sav", "r")#surveyed
uuuu=''
ffff=''
pppp=''
ssss=''
for line in ufile:
	uuuu=line
for line in ffile:
	ffff=line
for line in pfile:
	pppp=line
for line in sfile:
	ssss=line
#you are the head of science exploration of a galactic federation thing. you manage science ships looking for life, and you win if you find some. life exists on the homeworld (duh) and on exactly one other system.
#the universe is a 20ly wide cube
#~.0105 stars per cubic lightyear (1/95)
#spacecraft travel at 0.9 c
halflength=9
usize=range(-halflength,halflength+1)
def die(n,m,adj):
	total=0
	for i in range(n):
		total+=random.randint(1,m)
	return total+adj
def d6():
	return die(1,6,0)
def d20():
	return die(1,20,0)
def rchar():
	return random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
def isstar():
	if random.random()<1/95:
		return True
	return False
def rname():
	syllables=['mer','cu','ry','ve','nus','ter','ra','ju','pi','sa','turn','u','ra','nep','tun','ha','tsu','ne','mi','ku']
	return random.choice(syllables)+random.choice(syllables)
def rshipname():
	fict=['Endurance','Enterprise','Hedgehog','Liberty','Nostromo','Orville','Protector','Radiant Star','Serenity','Voyager']#Spacecraft in fictional works, and also the liberty which was the placeholder name
	fact=['Atlantis','Blizzard','Discovery','Eagle','Endeavour','Falcon','Intrepid','Jules Verne','Odyssey','Orion','Unity']#IRL spacecraft, with Blizzard for Buran
	navy=['Beagle']#boat names
	return random.choice(fict+fact+navy)
def roman(n):
	if n<11:return ['0','I','II','III','IV','V','VI','VII','VIII','IX','X'][n]
	return str(n)
def rencounter(systemname):
	random.seed(systemname)
	return random.choice(['Organic chemical readings','Collision of two moons','Beautiful auroras','Contamination','Restless crew'])
	
def cleanup(u):
	'''This does the following things:
	1. makes the center star K, G, or F.
	2. gives classes to each star, places one encounter on each system (homeworld = 'homeworld' and microbe = 'microbe')
	3. generates microbes and makes sure the microbes aren't on any of the following:
		* T
		* Y
		* Rogue planet
	'''
	#step 1
	print('Code C1')
	center=findcenter(u)
	classgen='benis'
	while classgen[0] not in 'KGF':
		classgen=starclass(center+random.choice(desc('T'))*random.randint(1,999))
	for star in u:#finding this fucking star again
		if star[0]==center:
			star+=[classgen,'Homeworld']
	#step 2 - gives classes to remaining stars
	print('Code C2')
	for star in u:
		if star!=center and starclass(star[0])[0]!='R':
			star+=[starclass(star[0]),rencounter(star[0])]
		else:
			star+=[starclass(star[0]),random.choice(['Rogue planet avoided!','Vessel lost to rogue planet.'])]
	#step 3 - random applicable star
	print('Code C3')
	nomicrobes=1
	while nomicrobes:
		star=random.choice(u)
		if star!=center and star[4][0] not in 'TYR':#can't be center or TYR class
			if (star[4][0] in 'KGF') or (d6()==1):#either has to be KGF or has to win the 1d6 die roll
				star[5]='Microbes'
				nomicrobes=0
	#end
	return u
def universegen():
	#random.seed(1)
	u=[]
	for x in usize:
		for y in usize:
			for z in usize:
				if isstar():
					u+=[[rchar()+rchar()+str(int(x*y*z%100)),x,y,z]]
	return cleanup(u)
def dist(x1,y1,z1,x2,y2,z2):
	return ((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)**.5
def finddistance(star1,star2):
	#find the location of star1 and star2, im p sure this way is faster than combining the fors
	for star in universe:
		if star[0]==star1:
			stara=star[1:]
			break
	for star in universe:
		if star[0]==star2:
			starb=star[1:]
			break
	return dist(stara[0],stara[1],stara[2],starb[0],starb[1],starb[2])
def findcenter(u):
	minstar=''
	mindist=99
	for star in u:
		if dist(star[1],star[2],star[3],0,0,0)<mindist:
			minstar=star[0]
			mindist=dist(star[1],star[2],star[3],0,0,0)
	return minstar
def findname(name,index):
	for item in index:
		if item[0]==name:
			return item
def systemgeometrygen(systemname):
	random.seed(systemname)
	currentchance=1.2
	system=[]
	sma=40*random.randint(90,110)/100#in radii of the star
	while 1:
		if random.random()<currentchance:
			currentchance-=.1#decreases by 10% for each new planet after P4
			sma=sma*2*random.randint(90,110)/100
			system+=[[systemname+' '+str('abcdefghijklmnopqrstuvwxyz'[len(system)%26]),sma]]
		else:
			return system
def starclass(systemname):
	random.seed(systemname)
	n=str(random.randint(0,9))
	if random.random()<2/5:return 'M'+n+'V'#remaining = 3/5
	if random.random()<1/6:return 'L'+n+'V'#remaining=1/2
	if random.random()<1/5:return 'T'+n+'V'#remaining=2/5
	if random.random()<1/8:return 'Rogue Planet'#remaining=7/20 THESE ARE HIDDEN UNTIL DISCOVERED
	if random.random()<1/3:return 'K'+n+'V'#remaining = 7/30
	if random.random()<1/7:return 'Y'+n+'V'# remaining = 1/5
	if random.random()<1/2:return 'G'+n+'V'# remaining = 1/10
	if random.random()<1/4:return 'F'+n+'V'# remaining = 3/40
	if random.random()<1/4:return 'A'+n+'V'# remaining = 9/160
	return 'White Dwarf'
def planetclass(planetname):
	random.seed(planetname)
	if random.random()<1/4:return 'Gas Giant'
	if random.random()<1/3:return 'Ice Giant'
	if random.random()<1/50:return 'Terra'
	return 'Rock'
def desc(item):
	if item=='M':return 'Red dwarfs are very abundant, but may not be the best place for life.'
	if item=='L':return 'Brown dwarves are very cool, meaning any planet orbiting them would certainly be tidally locked.'
	if item=='T':return 'T type brown dwarves are so cold any world warm enough to harbor life would be within its roche limit - meaning such a world would immediately be torn to shreds.'
	if item=='Rogue Planet':return 'Rogue planets are frozen wastelands. Was this planet a failed star? An ejected world? Who knows.'
	if item=='K':return 'K type main sequence stars are abundant enough and benevolent enough to provide good candidates for life.'
	if item=='Y':return 'Y type brown dwarves can be so cold water can still freeze at its surface.'
	if item=='G':return 'G type main sequence stars are very sunlike, and are thus great candidates for harboring life.'
	if item=='F':return 'F type main sequence stars are much warmer than our sun, but life can still feasibly form here.'
	if item=='A':return 'A type main sequence stars are very hot, and life probably could not form here... probably.'
	if item=='White Dwarf':return 'White dwarves are dead stars. They would have eradicated any past life... but perhaps life could form again on such worlds?'
	if item=='Gas Giant':return 'Gas Giants are too dense to harbor life, but their tendency to have many moons still makes them a prime target, if they are in the habitable zone.'
	if item=='Ice Giant':return 'Unlike gas giants, ice giants are not massive enough to control many large moons, but they may still have one or two moons capable of harboring life...'
	if item=='Terra':return 'Terras are rocky worlds in the habitable zone of their star and are extremely likely to harbor life.'
	if item=='Rock':return 'Rock worlds are failed terras... either too hot, too cold, or too small. But there may be life trapped under the ice...'
	if item=='Ship':return 'The ships are small science ships, powered by nuclear reactors and magnetoplasmadynamic engines.'
	if item=='Fuel':return 'Fuel is what is used to run the nuclear reactors to power the vessel. In this case, fuel is Plutonium-239, which costs $4,000,000 per kg.'
	if item=='Propellant':return 'Propellant is what is thrown out the back to make the vessel go. In this case, propellant is Hydrogen, which costs a measly $3 per kg.'
	return 'Unknown.'
def starmap(u,x):
	map=''
	for y in usize:
		for z in usize:
			empty=1
			for star in u:
				if star[1:4]==[x,y,z]:
					map+='*'
					empty=0
					break
			if empty:map+=' '
		map+='\n'
	return map
def travelmap(u,source,destination):
	basemap=starmap(u,destination[1])
	#replace source y,z with 'O'
	#each row is len(usize)+1 (\n)
	sourceposition=(len(usize)+1)*(source[2]+halflength)+(source[3]+halflength)#IF YOU CHANGE USIZE THIS WILL BREAK!!!!!!!!!!!!!!!!!!
	newmap=basemap[:sourceposition]+'O'+basemap[sourceposition+1:]
	targetposition=(len(usize)+1)*(destination[2]+halflength)+(destination[3]+halflength)#IF YOU CHANGE USIZE THIS WILL BREAK!!!!!!!!!!!!!!!!!!
	return newmap[:targetposition]+'X'+newmap[targetposition+1:]
def launch(shipyard):
	fleetnames=[]
	for vessel in fleet:
		fleetnames+=[vessel[0]]
	numeral=len(fleetnames)//22#22 = number of unique names
	name=rshipname()
	while name in fleetnames:
		name=rshipname()
	return [name,5000,1000,'idle',shipyard,0]
#some gameplay constants
income=1e7
variance=5e6
scienceshipcost=5e7
fuelcost=4e6#per kg, Pu-239
propellantcost=3#per kg, H
fueltank=5000#kg of fuel, this should last for 14 years. probably can't be much less than 50
propellanttank=1000#kg of propellant, wild guess for now. only needed for burns.
fuelusage=30#kg/mo
vesselmass=2e8#kg
thrust=1e9#N
propellantusage=100#kg per burn, when thrusting.
surveytime=2#months.
#fuck you python, nothing i do makes this work. FINE! I GIVE UP!
# #if there are no saves, new game
# if uuuu=='':
universe=universegen()
open("u.sav", "w").write(str(universe))
# else:
	# universe=uuuu.replace("[", "").replace("]", "").split(', ')
# if ffff=='':#sample entry: ['Name',fuel,propellant,'action','target',timeremaining] actions ex. [...,'travel','dest.',2]
home=findcenter(universe)
fleet=[]
fleet+=[launch(home)]#start with a free ship
	# open("f.sav", "w").write(str(fleet))
	# #NEEDS TO BE SAVED EVERY ROUND
# else:
	# fleet=ffff.replace("[", "").replace("]", "").split(', ')
# if pppp=='':
money=5e7
	# open("p.sav", "w").write(str(money))
	# #NEEDS TO BE SAVED EVERY ROUND
# else:
	# money=int(pppp)
# if ssss=='':
surveyed=[]
	# #NEEDS TO BE SAVED EVERY ROUND
# else:
	# surveyed=ssss.replace("[", "").replace("]", "").split(', ')
# #attempt to convert all possible strings into integers
# for star in universe:
	# for item in star:
		# try:
			# print(item)
			# item=int(item)
		# except:
			# pass
# for ship in fleet:
	# for item in ship:
		# try:
			# item=int(item)
		# except:
			# pass
#calculated constants
home=findcenter(universe)
shipdesc=['Name          ','Fuel          ','Propellant    ','Action        ','Target        ','Time Remaining']
stardesc=['Name ','X    ','Y    ','Z    ','Class']
starlist=[]
for star in universe:
	starlist+=[star[0]]
month=0
#TEMPORARY DEBUG STUFF - COMMENT OUT ASAP
#while 1:
#	input(rshipname())
#MAIN
while 1:
	month+=1
	print('Year',month//12,'Month',month%12)
	#begin main
	monthlyincome=income+random.randint(-variance,variance)
	money+=monthlyincome
	print('Your money this month is $'+str(money)+'.')
	print('Your income this month is $'+str(monthlyincome)+'.')
	if money>=scienceshipcost:# and False:#this is annoying so im turning it off
		print('Would you like to buy a ship? (cost = $'+str(scienceshipcost)+') (y/n)')
		if input('r> ')=='y':
			money-=scienceshipcost
			fleet+=[launch(home)]
	#random interstellar encounters
	for ship in fleet:
		if ship[3]=='travel' and d20()==1:#will we have an encounter? 1d20
			eventid=random.randint(1,4)
			if eventid==1:
				print('Turbulence!',ship[0],'has encountered a high concentration of debris from some sort of ancient interstellar collision. The shields need to be fully raised for the duration, and thus the ship loses an extra 100 fuel.')
				ship[1]-=100
			elif eventid==2:
				print('Unusual Radiation!',ship[0],'has encountered an unusual beam of radiation nearly parallel to the path of the vessel. It is having an unusual but beneficial effect on the shields, saving 10 fuel.')
				ship[1]+=10
			elif eventid==3:
				print('Friendly Asteroid!',ship[0],'has encountered a small asteroid following the ship in a vaguely parallel path, perhaps accidentally accelerated by an ancient alien spaceship millions of years ago. The crew was able, with some slight course corrections, to encounter it and mine some rarer metals. Lose a small amount of propellant and gain a large amount of cash.')
				ship[2]-=10
				money+=5e5
			elif eventid==4:
				print('Rogue Asteroid!',ship[0],'is about to encounter a rogue asteroid, which will cost a lot of propellant to dodge, and has a risk of colliding with the spacecraft. Vessel is saved if 1d6>2 and ship has enough propellant. Lose 200 kg propellant if successful.')
				roll=d6()
				print('1d6 =',roll,'& Propellant =',ship[2])
				if roll in [1,2] or ship[2]<200:
					ship=['DEAD',0,0,'suffer','hell',-1]
				else:
					ship[2]-=200
	#deplete ship fuel
	for ship in fleet:
		ship[1]-=fuelusage
		if ship[1]<0 and ship[5]!=home:
			print(ship[0],'ran out of fuel while',ship[3],'at',ship[4],'and has been lost.')
			ship=['DEAD',0,0,'suffer','hell',-1]
	#check for dead ships
	for ship in fleet:
		if ship==['DEAD',0,0,'suffer','hell',-1]:
			fleet.remove(ship)
	#check if actions finished
	for ship in fleet:
		ship[5]-=1
		if ship[5]<1 and ship[3]!='survey':
			ship[3]='idle'
			ship[5]=0
		elif ship[5]<1:
			ship[3]='idle'
			ship[5]=0
			print('Your ship surveyed a system and found',findname(ship[4],universe)[5])
			#return random.choice(['Organic chemical readings','Collision of two moons','Beautiful auroras','Contamination','Restless crew'])
			if findname(ship[4],universe)[5]=='Microbes':
				print('YOU WIN!')
				crashthemotherfuckinggame()
			elif findname(ship[4],universe)[5]=='Organic chemical readings':
				print('Your discovery of organic chemicals on another world, even despite life, has generated even more support for the program. Income is slightly increased.')
				income+=1e6
			elif findname(ship[4],universe)[5] in ['Collision of two moons','Beautiful auroras']:
				print('The event is observed from afar. Although such events have been observed many times, they are always a stunning sight.')
			elif findname(ship[4],universe)[5]=='Contamination':
				print('Some unknown chemical has infiltrated the',random.choice(['food','air','water']),'supply and needs to be filtered out. Thankfully this is a very simple process, but it is energy-intensive and costs 50 fuel.')
				ship[1]-=50
			elif findname(ship[4],universe)[5]=='Restless crew':
				print('Some unknown chemical has infiltrated the',random.choice(['food','air','water']),'supply is causing the crew to be agitated and needs to be filtered out. Thankfully this is a very simple process, but it is energy-intensive and costs 50 fuel, however, the wages need to be increased to satisfy the crew.')
				ship[1]-=50
				income-=5e5
	#check if any ship is idling
	for ship in fleet:
		if ship[3]=='idle':
			print(ship[0],'is',ship[3],'@',ship[4],'for the next',ship[5],'months.\nWould you like to change its orders? (y/n)')#actions = travel, survey
			if input('r> ')=='y':
				print('What should',ship[0],'do? It can:\n * (c)heck star database\n * (e)ncyclopedia\n * s(h)ip catalog\n * (i)dle\n * (l)ook at supplies\n * (m)ap\n * (r)estock\n * (s)urvey\n * (t)ravel / to (n)earest unsurveyed system\n * (x) cancel reassignment')
				choice=input('r> ')
				while choice not in 'xX':
					if choice in 'Ii':ship[3]='idle'
					elif choice in 'Cc':
						print('Which star?')
						star=findname(input('r> '),universe)
						for point in range(len(stardesc)):
							print(stardesc[point],star[point])
						if star[0] in surveyed:
							print('You surveyed this star already and found',star[5])
						else:
							print('You have not yet surveyed this star.')
					elif choice in 'Ee':
						item=input('Topic?\nr> ')
						print(desc(item))
					elif choice in 'Hh':
						for vessel in fleet:
							if vessel[3]=='travel' and vessel[5]==1==vessel[1]//fuelusage:
								print(vessel[0],'>',vessel[4],'in',vessel[5],'month (',vessel[1]//fuelusage,'month fuel )')
							if vessel[3]=='travel' and vessel[5]==1:
								print(vessel[0],'>',vessel[4],'in',vessel[5],'month (',vessel[1]//fuelusage,'months fuel )')
							elif vessel[3]=='travel' and 1==vessel[1]//fuelusage:
								print(vessel[0],'>',vessel[4],'in',vessel[5],'months (',vessel[1]//fuelusage,'month fuel )')
							elif vessel[3]=='travel':
								print(vessel[0],'>',vessel[4],'in',vessel[5],'months (',vessel[1]//fuelusage,'months fuel )')
							else:
								print(vessel[0],'@',vessel[4],'(',vessel[1]//fuelusage,'months fuel )')
					elif choice in 'Ll':
						for point in range(len(shipdesc)):
							print(shipdesc[point],ship[point])
					elif choice in 'Mm':
						for star in starlist:
							print(star,round(finddistance(star,ship[4]),2))
					elif choice in 'Nn':
						#check if unserveyed
						if ship[4] not in surveyed:
							choice='s'
						#find closest system
						else:
							dest=''
							dista=99
							destinations=[]
							for vessel in fleet:
								destinations+=[vessel[4]]
							for star in universe:
								delta=finddistance(ship[4],star[0])
								if star[0] not in surveyed and star[0] not in destinations and delta<dista:
									dest=star[0]
									dista=delta
							#continue
							if ship[2]>=propellantusage:
								if ship[1]/fuelusage/12<=finddistance(ship[4],dest)+finddistance(dest,home) and ship[2]>=propellantusage*2:#once they get there, they must be able to return immediately to the homeworld.
									input("Nice try, but the crew isn't going to go with a suicide mission!")
									choice='l'
								else:
									ship[2]-=propellantusage
									ship[3]='travel'
									ship[5]=ceil(12*finddistance(ship[4],dest))
									ship[4]=dest
							else:print('Not enough propellant!')
					elif choice in 'Rr':
						delta_fuel=fueltank-ship[1]
						delta_propellant=propellanttank-ship[2]
						cost=delta_fuel*fuelcost+delta_propellant*propellantcost
						if cost<=money:
							ship[1]=fueltank
							ship[2]=propellanttank
							money-=cost
						else:print('You cannot afford that!')
					if choice in 'Ss':
						if ship[4] not in surveyed:
							ship[3]='survey'
							surveyed+=ship[4]
							ship[5]=surveytime
							surveyed+=[ship[4]]
						else:print(ship[4],'already surveyed!')
					elif choice in 'Tt':
						dest=input('Destination?\nr> ')
						if dest in starlist:
							print(travelmap(universe,findname(ship[4],universe),findname(dest,universe)))
							if ship[2]>=propellantusage:
								if ship[1]/fuelusage/12<=finddistance(ship[4],dest)+finddistance(dest,home) and ship[2]>=propellantusage*2:#once they get there, they must be able to return immediately to the homeworld.
									input("Nice try, but the crew isn't going to go with a suicide mission!")
									choice='l'
								else:
									ship[2]-=propellantusage
									ship[3]='travel'
									ship[5]=ceil(12*finddistance(ship[4],dest))
									ship[4]=dest
							else:print('Not enough propellant!')
						else:
							print('That system does not exist!')
					#check to see if a breaking choice was chosen, break if so
					if choice in 'IiNnSsTtXx':break
					choice=input('r> ')
	#im p sure this is done now
	open("f.sav", "w").write(str(fleet))
	open("p.sav", "w").write(str(money))
	open("s.sav", "w").write(str(surveyed))
	#input('Prepare for next month!')