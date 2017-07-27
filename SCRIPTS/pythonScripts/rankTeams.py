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
	x.execute("""DROP TABLE teamData;""")
	conn.commit()
except:
	conn.rollback()

x.execute("""
CREATE TABLE teamData (teamName VARCHAR(20), gameDate DATE,pointsAllowed SMALLINT(20), totalPointsAllowed SMALLINT(20), dailyDefenseRanking SMALLINT(20));""")

year = 2015

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def rank_teams():
  teams = ('ATL','BOS','NJN','CHA','CHI','CLE','DAL','DEN','DET','GSW','HOU','IND','LAC','LAL','MEM','MIA','MIL','MIN','NOH','NYK','OKC','ORL','PHI','PHO','POR','SAC','SAS','TOR','UTA','WAS')
  teams = ('ATL','BOS','NJN','CHA','MIL')
  print "Scraping team: ", 
  team_data=[]
  for team in teams:
    print team,',',
    url = 'http://www.basketball-reference.com/play-index/tscore.cgi?request=1&match=combined&year_min='+str(year)+'&year_max='+str(year)+'&team_id='+team+'&opp_id=&quarter_is_1=Y&quarter_is_2=Y&quarter_is_3=Y&quarter_is_4=Y&quarter_is_5=Y&is_playoffs=N&round_id=&game_num_type=&game_num_min=&game_num_max=&game_month=&game_location=&game_result=&is_overtime=&c1stat=&c1comp=gt&c1val=&c2stat=&c2comp=gt&c2val=&c3stat=&c3comp=gt&c3val=&order_by=date_game&order_by_asc=Y'
    response = urllib2.urlopen(url)
    page_source = response.read()
    soup = BeautifulSoup(page_source)
    table = soup.find("table",id="stats")
    table_subset = table.findAll("tr")
    TPA=0
    date_array=[]
    new_date_array=[]
    PA_array=[]
    TPA_array=[]
    team_array=[]
    start_date = date(2014, 10, 29)
    end_date = date(2015, 4, 15)
    for single_date in daterange(start_date, end_date):
		date_string = single_date.strftime("%Y-%m-%d")
		try:
			x.execute("""INSERT INTO teamData (teamName, gameDate) VALUES (%s, %s);""", (str(team),date_string,))
			conn.commit()
		except:
			conn.rollback()
			
    for row in range(0,len(table_subset)):
		
		cells = table_subset[row].findAll("td")
		try:
			date1 = cells[1].find(text=True)
			#print "first date", date1
			date_object = datetime.strptime(date1, '%a, %b %d, %Y')
			#print "second date", date_object
			date_string = date_object.strftime('%Y-%m-%d')
			#print "third date", date_string
			date_array.append(date1)
			#print "fourth date"
			PA = int(cells[7].find(text=True))
			PA_array.append(PA)
			TPA=TPA+PA
			TPA_array.append(TPA)
			#print "submit"
			
			for single_date in daterange(start_date, end_date):
				date_string1 = single_date.strftime("%Y-%m-%d")
				date_object2 = datetime.strptime(str(single_date), '%Y-%m-%d')
				#print date_object2, date_object
				if date_string1==date_string:
					x.execute("""UPDATE teamData SET totalPointsAllowed='"""+str(TPA)+"""',pointsAllowed='"""+str(PA)+"""' WHERE (gameDate='"""+date_string+"""') AND (teamName='"""+str(team)+"""');""")
					conn.commit()
					
					#x.execute("""UPDATE teamData SET totalPointsAllowed='"""+str(TPA)+"""' WHERE (gameDate='"""+date_string+"""') AND (teamName='"""+str(team)+"""');""")
					#conn.commit()
				elif date_object2 > date_object:
					#print "NOT FOUND",team,date_string,str(TPA)
					execute_string=("""UPDATE teamData SET pointsAllowed='0',totalPointsAllowed='"""+str(TPA)+"""' WHERE (gameDate='"""+date_string1+"""') AND (teamName='"""+str(team)+"""');""")
					x.execute(execute_string)
					conn.commit()
					#print "committed"

		except:
			#print "error"
			sys.exc_info()[0]
			next
			conn.rollback()

    team_array.append(team)		
    team_array.append(date_array)
    team_array.append(PA_array)
    team_array.append(TPA_array)
	#x.execute("""INSERT INTO testTable(teamID,Date,Ranking)  VALUES (%s,%s,%s)""",(team,date_array,PA_array))
	 
    team_data.append(team_array)
#team_data #team, date, PA, TPA, ranking
  file_name = 'defense_data.txt'
  f = open(file_name,'w')
  #print 'Writing data to '+ file_name
  for select in range(0,len(teams)):
	f.write(str(team_data[select][0])+'\n')
	f.write(str(team_data[select][1])+'\n')
	f.write(str(team_data[select][2])+'\n')
	f.write(str(team_data[select][3])+'\n\n')
  f.close

  ###########################
  ### RANKING THE DEFENSE ###
  ###########################
  
  ranking_array=[]
  for day in range(0,len(team_data[0][1])):
    day_tpa=[]
    for select in range(0,len(teams)):
		day_tpa.append(team_data[select][3][day])
    ranking=[]	
   # print 'Day '+str(day)+': ',sorted(day_tpa)
    sorted_day_tpa = sorted(day_tpa)
    for select1 in range(0,len(teams)):
		ranking.append(sorted_day_tpa.index(team_data[select1][3][day]))
    ranking_array.append(ranking)
  
  #print ranking_array

  for team in range(0,len(teams)):
	team_array=[]
	for day in range(0,len(team_data[0][1])):
		team_array.append(int(ranking_array[day][team])+1)

	team_data[team].append(team_array)
	#print team_data[team][0],team_data[team][4]
	
  file_name = 'defense_ranking_'+str(year)+'.txt'
  f = open(file_name,'w')
 # print 'Writing data to '+ file_name
  for team in range(0,len(teams)):
    f.write(str(team_data[team][0])+"|"+str(team_data[team][4])+'\n')
  f.close
  
  #plotRanking(team_data,teams)
  #print team_data
  return team_data

if __name__ == '__main__':
	team_data=rank_teams()