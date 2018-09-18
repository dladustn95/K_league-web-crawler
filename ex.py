from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

client = MongoClient('localhost', 27017)
db = client.test
test_collection = db.test_collection
#db = test_collection.find()
#for i in db:
#    print(i)
#test_collection.remove();
#test_collection.insert({"team":"team1", "record":[{'round':1, 'where':'where1'},{"round":2, 'where':'where2'}]})


driver = webdriver.Chrome('C:/Users/LYS/Desktop/K/python/chromedriver')

driver.get('http://data.kleague.com/')
driver.get('http://portal.kleague.com/mainFrame.do')

driver.implicitly_wait(100);
inputElement = driver.find_element_by_link_text('데이터센터')
inputElement.send_keys("\n") #send enter for links, buttons
#driver.find_element_by_link_text('데이터센터').click()

for i in range(1,28):
    round = i;
    select1 = Select(driver.find_element_by_name('roundId'))
    select1.select_by_value(str(round))
    select3 = Select(driver.find_element_by_name('gameId'))
    select3.select_by_value(str((round-1)*6 + 1))

    inputElement = driver.find_element_by_link_text('PLAYER STATS')
    inputElement.send_keys("\n")
    #driver.find_element_by_link_text('PLAYER STATS').click()

    #driver.find_element_by_name("option[value='" + str(round) + "']").click();

    for i in range(0,6):

        #게임 선택 및 경기장
        select3 = Select(driver.find_element_by_name('gameId'))
        select3.select_by_value(str((round-1)*6 + 1 + i))
        match = driver.find_element_by_class_name('match-prame-boxTxt02')
        matchText = match.text.replace(" ","")
        print(matchText)

        #팀 이름
        hometeam = driver.find_element_by_xpath('//*[@id="frm"]/div[2]/div[2]/span[1]')
        print(hometeam.text)
        awayteam = driver.find_element_by_xpath('//*[@id="frm"]/div[3]/div[1]/span[3]')
        print(awayteam.text)

        #홈팀 기록
        homeAttList = driver.find_element_by_xpath('//*[@id="homeAttList"]/tbody')
        homeAttListText = str(homeAttList.text).replace('\n', ' ').split(' ')

        inputElement = driver.find_element_by_xpath('//*[@id="btnPassFlag"]')
        inputElement.send_keys("\n")
        homePassList = driver.find_element_by_xpath('//*[@id="homePassList"]/tbody')
        homePassListText = str(homePassList.text).replace('\n', ' ').split(' ')

        inputElement = driver.find_element_by_xpath('//*[@id="btnDefFlag"]')
        inputElement.send_keys("\n")
        homeDefList = driver.find_element_by_xpath('//*[@id="homeDefList"]/tbody')
        homeDefListText = str(homeDefList.text).replace('\n', ' ').split(' ')

        driver.implicitly_wait(50);

        #원정팀 기록
        inputElement = driver.find_element_by_xpath('//*[@id="btnAwayTeam"]')
        inputElement.send_keys("\n")
        inputElement = driver.find_element_by_xpath('//*[@id="btnAttFlag"]')
        inputElement.send_keys("\n")
        awayAttList = driver.find_element_by_xpath('//*[@id="awayAttList"]/tbody')
        awayAttListText = str(awayAttList.text).replace('\n', ' ').split(' ')

        inputElement = driver.find_element_by_xpath('//*[@id="btnPassFlag"]')
        inputElement.send_keys("\n")
        awayPassList = driver.find_element_by_xpath('//*[@id="awayPassList"]/tbody')
        awayPassListText = str(awayPassList.text).replace('\n', ' ').split(' ')

        inputElement = driver.find_element_by_xpath('//*[@id="btnDefFlag"]')
        inputElement.send_keys("\n")
        awayDefList = driver.find_element_by_xpath('//*[@id="awayDefList"]/tbody')
        awayDefListText = str(awayDefList.text).replace('\n',' ').split(' ')

        #날씨
        weather = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div/ul/li[4]/span[2]')
        weather = weather.text.replace(" ","")
        weather = weather.replace("(", ")")
        weather = weather.replace("℃",")").split(")")
        weatherText = weather[0]
        temperature = weather[1]

        #기록 DB에 저장
        for i in range(0,int(len(homePassListText)/18)):
            test_collection.update_one({'team': hometeam.text, 'name': homeAttListText[1 + i * 14], "backNum": homeAttListText[0 + i * 14], 'pos':homeAttListText[2+i*14]},
                                    {'$push': {'record': {'round': round, 'matchTeam': awayteam.text, 'stadium': matchText, 'weather': weatherText,
                                                         'temperature': temperature, 'mins': homeAttListText[3 + i * 14],'matchRate': homeAttListText[4 + i * 14],
                                                'attRecord': {'goal': homeAttListText[5 + i * 14], 'sht': homeAttListText[6 + i * 14],  'sot': homeAttListText[7 + i * 14], 'paSht': homeAttListText[8 + i * 14],
                                                            'paSot': homeAttListText[9 + i * 14], 'drb': homeAttListText[10 + i * 14], 'drbPer': homeAttListText[11 + i * 14],
                                                            'f3FFouled': homeAttListText[12 + i * 14], 'f3In': homeAttListText[13 + i * 14] },
                                                'passRecord': {'pass': homePassListText[5 + i * 18], 'passPer': homePassListText[6 + i * 18], 'keyP': homePassListText[7 + i * 18],
                                                            'frontPass': homePassListText[8 + i * 18], 'backPass': homePassListText[9 + i * 18], 'attPass': homePassListText[10 + i * 18],
                                                            'attPassPer': homePassListText[11 + i * 18], 'defPass': homePassListText[12 + i * 18], 'defPassPer': homePassListText[13 + i * 18],
                                                            'longPass': homePassListText[14 + i * 18], 'longPassPer': homePassListText[15 + i * 18], 'cross': homePassListText[16 + i * 18],
                                                            'crossPer': homePassListText[17 + i * 18]},
                                                'defRecord': {'compete': homeDefListText[5 + i * 16], 'competePer': homeDefListText[6 + i * 16], 'air': homeDefListText[7 + i * 16],
                                                            'airPer': homeDefListText[8 + i * 16], 'tackle': homeDefListText[9 + i * 16], 'tacklePer': homeDefListText[10 + i * 16],
                                                            'clr': homeDefListText[11 + i * 16], 'inter': homeDefListText[12 + i * 16], 'foul': homeDefListText[13 + i * 16], 'yel': homeDefListText[14 + i * 16],
                                                            'red': homeDefListText[15 + i * 16]}}}}, upsert = True)
        for i in range(0,int(len(awayPassListText)/18)):
            test_collection.update_one({'team': awayteam.text, 'name': awayAttListText[1 + i * 14], "backNum": awayAttListText[0 + i * 14],'pos': awayAttListText[2 + i * 14]},
                                    {'$push': {'record': {'round': round, 'matchTeam': hometeam.text, 'stadium': matchText, 'weather': weatherText,
                                                          'temperature': temperature, 'mins': awayAttListText[3 + i * 14], 'matchRate': awayAttListText[4 + i * 14],
                                                'attRecord': {'goal': awayAttListText[5 + i * 14], 'sht': awayAttListText[6 + i * 14], 'sot': awayAttListText[7 + i * 14], 'paSht': awayAttListText[8 + i * 14],
                                                             'paSot': awayAttListText[9 + i * 14], 'drb': awayAttListText[10 + i * 14], 'drbPer': awayAttListText[11 + i * 14],
                                                             'f3FFouled': homeAttListText[12 + i * 14], 'f3In': homeAttListText[13 + i * 14]},
                                                'passRecord': {'pass': awayPassListText[5 + i * 18], 'passPer': awayPassListText[6 + i * 18], 'keyP': awayPassListText[7 + i * 18],
                                                            'frontPass': awayPassListText[8 + i * 18], 'backPass': awayPassListText[9 + i * 18], 'attPass': awayPassListText[10 + i * 18],
                                                            'attPassPer': awayPassListText[11 + i * 18], 'defPass': awayPassListText[12 + i * 18], 'defPassPer': awayPassListText[13 + i * 18],
                                                            'longPass': awayPassListText[14 + i * 18], 'longPassPer': awayPassListText[15 + i * 18], 'cross': awayPassListText[16 + i * 18],
                                                            'crossPer': awayPassListText[17 + i * 18]},
                                               'defRecord': {'compete': awayDefListText[5 + i * 16], 'competePer': awayDefListText[6 + i * 16], 'air': awayDefListText[7 + i * 16],
                                                            'airPer': awayDefListText[8 + i * 16], 'tackle': awayDefListText[9 + i * 16], 'tacklePer': awayDefListText[10 + i * 16],
                                                            'clr': awayDefListText[11 + i * 16], 'inter': awayDefListText[12 + i * 16], 'foul': awayDefListText[13 + i * 16], 'yel': awayDefListText[14 + i * 16],
                                                            'red': awayDefListText[15 + i * 16]}}}}, upsert=True)

        driver.implicitly_wait(100);

print('-----------')
"""
t = []
for i in range(len(list)):
    t.append(list[i].replace('\n',' ').split(' '))

#t = list[0].replace('\n',' ').split(' ')

print(t)
"""
print('-----------')
driver.quit()
