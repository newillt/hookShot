#!/usr/bin/python
import numpy as np
#import matplotlib.pyplot as plt
import MySQLdb
import urllib2
import sys
#from mpldatacursor import datacursor
from bs4 import BeautifulSoup
from itertools import izip_longest
from datetime import timedelta, date, datetime


conn = MySQLdb.connect(host="localhost",user="root",passwd="20150919taylor",db="database1")
x=conn.cursor()
try: 
	x.execute("""DROP TABLE playerData;""")
	conn.commit()
except:
	conn.rollback()

x.execute("""
CREATE TABLE playerData (playerName VARCHAR(255), gameDate DATE,opp VARCHAR(20), defenseRank SMALLINT(20), minPlayed SMALLINT(20),points SMALLINT(20),FGM SMALLINT(20),FGA SMALLINT(20), fantPTS SMALLINT(20),fantSal VARCHAR(20));""")

start_date = date(2014, 10, 29)
end_date = date(2015, 4, 15)
year = 2015

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def player_fp_data():

	id_list=(4496,4727,4574,4341,3970,4084,4767,4260,3860,4374,1997,3619,4261,3940,3397,3853,4262,4736,4085,4621,3510,3972,4590,4738,3621,3866,4080,4263,4078,4462,4248,4625,4264,4690,3514,3882,3862,4502,3474,3702,4522,3733,4086,4076,4556,4507,4494,4071,3974,4666,4619,4234,4757,4696,4458,4691,4200,3518,3735,4266,4560,4709,3736,3520,4267,3461,3521,4582,4750,4269,3008,3975,3976,4740,4629,4693,3878,1881,4196,4654,4615,4441,3401,4363,3463,4599,3738,3739,4708,4597,3740,4616,4569,4766,4203,2448,4575,4209,4088,3307,3978,4763,4686,4213,4712,4214,4611,4668,4235,4751,4370,4228,3523,3979,3524,4741,4544,4719,4274,4570,4561,4754,4732,3116,4275,4472,4226,4501,4564,4173,3338,4658,4656,4584,4482,4276,3984,4752,4731,4186,4211,4572,4610,3629,3527,4632,4760,4090,4178,4091,4092,4720,4578,4489,3985,2223,3404,3986,4726,4670,4344,4185,3745,4762,4492,4697,4729,4517,4278,3430,4207,4707,4503,4695,4456,3910,4596,4280,4613,3747,3989,4281,4468,3858,4585,4717,4417,3958,3749,4082,4735,3751,1449,4498,3990,3308,3857,4239,4283,4167,3021,4620,3406,4593,4705,3636,4730,4077,3756,4451,3759,4765,3991,4193,4504,4665,3760,4581,3992,3533,4172,4587,4623,4722,4457,3583,4543,4171,4628,4224,4530,3637,4678,4733,4340,4412,3535,3996,3827,4285,3318,4190,4287,4525,4688,4101,4030,3408,4102,4179,4566,3538,4212,4558,3898,4734,4744,3998,3639,4216,4601,3640,4104,3641,3642,3765,4701,4764,4379,3766,4743,4369,4473,4289,3541,3645,4684,3311,4540,4711,4182,4187,4664,3768,4355,4555,4434,4168,3304,4698,4053,4756,4292,4533,3543,3544,4552,4692,3913,4511,4107,4295,4405,3545,4442,3546,4618,4648,4532,4770,3031,4745,4382,3547,4109,4600,4526,4514,4003,4655,4748,4768,4159,4592,4110,3772,4415,4591,4404,4521,4411,4523,4297,3651,4075,4112,4074,3891,3833,4713,4377,4383,3777,4689,3039,4500,4158,3133,3652,4164,3779,4072,4113,4700,4586,4657,4675,4669,4725,4114,4650,4589,4230,4007,4183,4598,4490,3783,3041,4484,3141,4467,4245,4333,3904,4682,4660,4617,2404,4298,4364,4739,4449,4407,4453,4115,4459,4753,4518,4299,4594,4567,4510,4637,4659,4694,1900,4300,4573,3656,4531,4013,4652,4759,3895,2374,4681,4721,4529,4627,4583,4563,4301,3552,3553,4710,3446,4728,3313,4461,4302,3786,4673,4699,4116,3556,2428,4303,4607,4542,4305,4653,4674,3593,4742,4631,4170,3789,4546,3416,4749,4622,4680,3790,3314,3861,4579,4608,3302,3560,4483,4559,4671,4485,4702,3793,4509,3872,4073,4549,4414,4683,4083,4535,3418,4676,4747,4313,4595,3503,4488,3931,4314,4020,4397,4524,4375,4547,4460,4376,4641,4435,4677,4408,4315,3669,4023,3670,4737,4672,4571,4746,4649,4122,4024,4703,4662,4316,4317,4769,4723,3419,4026,4475,4551,4221,4527,4478,3677,4199,3054,4202,4644,4420,4384,4452,3865,4534,4124,4367,4380,4227,4049,3871,3805,3164,4318,4358,4354,3678,4497,3679,4320,3807,4761,4373,3571,4515,4126,4440,4321,3356,4661,4724,4716,4056,4758,4755,4714,3811,3573,4079,4324,4687,4704,4685,3814,4416,4326,3816,4032,3817,3574,4255,3923,4718,4565,4612,4034,4426,3683,4469,4679,4036,4667,4037,4715,4614,4516)
	#id_list=(4614,4516)
	mon_list=('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')
	id_data=[]
	for id in id_list:
		k=0
		url = 'http://rotoguru1.com/cgi-bin/playrh.cgi?'+str(id)+'x'
		response = urllib2.urlopen(url)
		page_source = response.read()
		soup = BeautifulSoup(page_source)
		table = soup.find("table", border=0)
		table_subset = table.findAll("tr")
		name2=str(table_subset[0].findAll('td')[1].findAll('b')[0].find(text=True))
		name=(name2.split(',')[1]+' '+name2.split(',')[0]).strip()
		print 'Finding FP for: ',name

		#print len(table_subset)
		table_sub = table_subset[11]
		rows=[]
		list=[]
		list2=[]
		list2.append(name)
		for row in range(11,len(table_sub.findAll('tr'))-5):
			row_data = table_sub.findAll('tr')[row].findAll('td')
			list=[]
			try:
				for i in range(0,5):
				
					if i==0:
						data=str(str(row_data[i].find(text=True))) #9-Oct
						data2=data.split('-') 	#[9][10]
						if int(data2[0])>9:
							data2.append(year-1) #[9][10][2014]
						else:
							data2.append(year)
									
						data=str(data2[2])+'-'+str(data2[0])+'-'+str(data2[1])			
					
					elif i==4:
						data=str(row_data[i].find(text=True)).replace(',','')
					else:
						data=str(row_data[i].find(text=True))
					#print data
					list.append(data)
						
			except:
				next
			#print list[0],list[4]
			
			try:
				for single_date in daterange(start_date, end_date):
					date_string1 = single_date.strftime("%Y-%m-%d")
					date_object2 = datetime.strptime(str(single_date), '%Y-%m-%d')
					#print date_object2, date_object
					if date_string1==list[0]:
						#print 'found',name,list[0],list[3],list[4]
						try:
							exe_string=str("INSERT INTO playerData (playerName, gameDate,  fantPTS, fantSal) VALUES ('"+name+"','"+str(list[0])+"','"+str(list[3])+"','"+str(list[4]).strip()+"');")
							#print exe_string
							x.execute(exe_string)
							conn.commit()
						except:
							print 'sql error'
							conn.rollback()
					else:
						next
						#print "NOT FOUND",team,date_string,str(TPA)
						'''execute_string=("""UPDATE teamData SET pointsAllowed='0',totalPointsAllowed='"""+str(TPA)+"""' WHERE (gameDate='"""+date_string1+"""') AND (teamName='"""+str(team)+"""');""")
						x.execute(execute_string)
						conn.commit()
						#print "committed"'''
			except:
				next
				
			list2.append(list)
		id_data.append(list2)
		#print list2
		#print id_data[0][1]
	f = open('id_data.txt','w')
	f.write(str(id_data))
	f.close()
	return id_data
	
def player_data():
	##############################
	### GET ACTIVE PLAYER LIST ###
	##############################
	#http://www.basketball-reference.com/players/z/
	import string
	player_data=[]
	string.ascii_lowercase
	alpha = list(string.ascii_lowercase)
	active_players=[]
	for letter in (alpha):
		try:
			print "Scraping letter: ", letter
			url = 'http://www.basketball-reference.com/players/'+letter+'/'
			#print url
			response = urllib2.urlopen(url)
			page_source = response.read()
			soup = BeautifulSoup(page_source)
			table = soup.find("table",id="players")
			table_subset = table.findAll("tr")

			for row in range(1,len(table_subset)-1):
				cells = table_subset[row].findAll("td")
				active_players.append(cells[0].find('strong'))
		except:
			next

	#active_players.remove(None)
	active_players=filter(None,active_players)
	print 'Active Players: ', len(active_players)
	player_link=[]
	player_name=[]
	for player in active_players:
		player_link.append('http://www.basketball-reference.com'+str(player).split('"')[1])
		bad_str = str(player).replace('<', ',')
		bader_str = str(bad_str).replace('>', ',')
		player_name.append(bader_str.split(",")[4])

############################
### GET PLAYER GAME DATA ###
############################
	true_player=len(active_players)
	for player in range(0,len(active_players)):
		replace_string= '/gamelog/'+str(year)+'/'
		#print str(player_link)
		new_url = str(player_link[player]).replace('.html',replace_string)
		
##########################
### GET PLAYER FP DATA ###
### fp_data[player][date][stat]
##########################
				
		try:
			print "Scraping player data: ", player_name[player], new_url
			pts_array = []
			date_array = []
			gs_array=[]
			op_array=[]
			op2_array=[]
			mp_array=[]
			fgm_array=[]
			fga_array=[]
			player_array=[]
			fp_array2=[]
			fs_array=[]
			url = new_url
			response = urllib2.urlopen(url)
			page_source = response.read()
			soup = BeautifulSoup(page_source)
			table = soup.find("table",id="pgl_basic")
			table_subset = table.findAll("tr")
			#print table_subset
			for date in range(0,len(table_subset)+10):
				#print "INSIDE OF FOR LOOP", date
				try:
					cells = table_subset[date].findAll("td")
					if str(cells[8].find(text=True))=='Inactive':
						next
					elif str(cells[8].find(text=True))=='Did Not Play':
						next
					else:
						date2=str(cells[2].find(text=True))
						fp_array=[]
						player_fp_index=[]
													
						date_array.append(date2)
						pts_array.append(int(cells[27].find(text=True)))
						gs_array.append(float(cells[28].find(text=True)))
						mp_formatted = str(cells[9].find(text=True))
						mp=(float(mp_formatted.split(':')[1])/60)+(float(mp_formatted.split(':')[0]))
						mp_array.append(mp)
						fgm_array.append(str(cells[10].find(text=True)))
						fga_array.append(str(cells[11].find(text=True)))
						#print str(cells[9].find(text=True))
						op = str(cells[6].find(text=True))
						op2_array.append(op)
						#playerName VARCHAR(255), gameDate DATE,opp SMALLINT(20), defenseRank SMALLINT(20), minPlayed SMALLINT(20),points SMALLINT(20),FGM SMALLINT(20),FGA SMALLINT(20), fantPTS SMALLINT(20),fantSal SMALLINT(20))

						
						###########################
						### INSERT DATA INTO DB ###
						###########################
						#print "POINTS ON DATE: ",int(cells[27].find(text=True)), str(int(cells[27].find(text=True)))
					for single_date in daterange(start_date, end_date):
						date_string1 = single_date.strftime("%Y-%m-%d")
						date_object2 = datetime.strptime(str(single_date), '%Y-%m-%d')
						#print date_object2, date_object
						if date_string1==date2:

							try:
								exe_string="""UPDATE playerData SET opp='"""+str(op)+"""',minPlayed='"""+str(mp)+"""',points='"""+str(int(cells[27].find(text=True)))+"""', FGM='"""+str(cells[10].find(text=True))+"""',FGA='"""+str(cells[11].find(text=True))+"""' WHERE (gameDate='"""+date_string1+"""') AND (playerName='"""+str(player_name[player])+"""');"""
								#print exe_string
								x.execute(exe_string)			
								conn.commit()
							except:
								conn.rollback()
							
							exe_string=str("INSERT INTO playerData (playerName, gameDate,  fantPTS, fantSal) VALUES ('"+name+"','"+str(list[0])+"','"+str(list[3])+"','"+str(list[4]).strip()+"');")
							print exe_string
							x.execute(exe_string)
							conn.commit()
						else:
							next	
				except:
					next

					player_array.append(player_name[player])
			player_array.append(date_array)
			player_array.append(op_array)
			player_array.append(mp_array)			
			player_array.append(pts_array)
			player_array.append(fgm_array)
			player_array.append(fga_array)
			player_array.append(gs_array)
			player_array.append(op2_array)
			player_array.append(fp_array2)
			player_array.append(fs_array)
			
			player_data.append(player_array)
			
		except:
			print 'scraping error', new_url
			true_player = true_player-1
			next
	
	file_name = 'full_player_data_'+str(year)+'.txt'
	print 'Writing full player data to '+ file_name
	print "True Playa's: ", true_player
	f = open(file_name,'w')

	for player in range(0,true_player):
		try:
			#print 'Writing player ',player_data[player][0]
			player_data[player]
			f.write(str(player_data[player][0])+'\n'+str(player_data[player][1])+'\n'+str(player_data[player][2])+'\n'+str(player_data[player][3])+'\n'+str(player_data[player][4])+'\n'+str(player_data[player][5])+'\n'+str(player_data[player][6])+'\n'+str(player_data[player][7])+'\n'+str(player_data[player][8])+'\n'+str(player_data[player][9])+'\n'+str(player_data[player][10])+'\n\n')
			
		except:
			next
		f.close

	for player in range(0,true_player):
		file_name2 = 'PGD_'+str(player_data[player][0])+'_formatted_data_'+str(year)+'.csv'
		file_name = 'PGD_'+str(player_data[player][0])+'_formatted_data_'+str(year)+'.txt'
		f = open(file_name,'w')
		f2 = open(file_name2,'w')
		f.write('4\n5\nDATE OPP DEF_RANK MP POINTS FGM FGA FANTPTS FANTSAL\n')
		f2.write('DATE, OPP, DEF_RANK, MP, POINTS, FGM, FGA,FANTPTS,FANTSAL\n')
		#print player_data
		try:
			for game in range(0,82):
				#f.write(str(player_data[player][1][game])+str(player_data[player][8][game])+str(player_data[player][2][game])+str(player_data[player][3][game])+str(player_data[player][4][game])+str(player_data[player][5][game])+str(player_data[player][6][game])+str(player_data[player][9][game])+str(player_data[player][10][game])+'\n')
				#f2.write(str(player_data[player][1][game])+','+str(player_data[player][8][game])+','+str(player_data[player][2][game])+','+str(player_data[player][3][game])+','+str(player_data[player][4][game])+','+str(player_data[player][5][game])+','+str(player_data[player][6][game])+','+str(player_data[player][9][game])+','+str(player_data[player][10][game])+'\n')
				arr=[1,8,2,3,4,5,6,9,10]
				for index in arr:
					try:
						f.write(str(player_data[player][index][game])+' ')
						f2.write(str(player_data[player][index][game])+',')
						#print(str(game)+' '+str(player_data[player][1][game])+' '+str(player_data[player][8][game])+' '+str(player_data[player][2][game])+' '+str(player_data[player][3][game])+' '+str(player_data[player][4][game])+' '+str(player_data[player][5][game])+' '+str(player_data[player][6][game])+' '+str(player_data[player][9][game])+' '+str(player_data[player][10][game])+'\n')
						#f2.write(str(player_data[player][1][game])+','+str(player_data[player][8][game])+','+str(player_data[player][2][game])+','+str(player_data[player][3][game])+','+str(player_data[player][4][game])+','+str(player_data[player][5][game])+','+str(player_data[player][6][game])+','+str(player_data[player][9][game])+','+str(player_data[player][10][game])+'\n')
					except:
						next
				f.write('\n')
				f2.write('\n')
		except:
			next
		
		f.close()
		f2.close()
	
	
	#print player_data[player][1]
	#print(str(game)+' '+str(player_data[player][1][80])+' '+str(player_data[player][8][80])+' '+str(player_data[player][2][80])+' '+str(player_data[player][3][80])+' '+str(player_data[player][4][80])+' '+str(player_data[player][5][80])+' '+str(player_data[player][6][80])+' '+str(player_data[player][9][80])+' '+str(player_data[player][10][80])+'\n')
	
	f2.close()
	
	
if __name__ == '__main__':
	fp_data=player_fp_data()
	player_data()