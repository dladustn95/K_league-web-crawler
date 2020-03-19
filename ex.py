from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys

client = MongoClient('localhost', 27017)
db = client.test
test_collection = db.test_collection
#db = test_collection.find()
#for i in db:
#    print(i)
#test_collection.remove();
#test_collection.insert({"team":"team1", "record":[{'round':1, 'where':'where1'},{"round":2, 'where':'where2'}]})

options = Options()
options.headless = True
driver = webdriver.Chrome(executable_path='D:/기타/k/chromedriver.exe', options=options)

driver.get('http://data.kleague.com/')
driver.get('http://portal.kleague.com/mainFrame.do')

driver.implicitly_wait(100);
inputElement = driver.find_element_by_link_text('데이터센터')
inputElement.send_keys("\n") #send enter for links, buttons
#driver.find_element_by_link_text('데이터센터').click()

select = Select(driver.find_element_by_name('meetYear'))
select.select_by_value(str(2019))

seqselect = Select(driver.find_element_by_name('meetSeq'))
seqselect.select_by_value(str(1))
for i in range(1,39):
    round = i;
    print(round)
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

        #팀 이름
        hometeam = driver.find_element_by_xpath('//*[@id="frm"]/div[2]/div[2]/span[1]')
        awayteam = driver.find_element_by_xpath('//*[@id="frm"]/div[3]/div[1]/span[3]')

        #홈팀 기록
        #공격
        homeAttList = driver.find_element_by_xpath('//*[@id="homeAttList"]/tbody')
        homeAttListText = str(homeAttList.text).split('\n')
        for idx, text in enumerate(homeAttListText):
            homeAttListText[idx] = text.split(' ')

        #패스
        inputElement = driver.find_element_by_xpath('//*[@id="btnPassFlag"]')
        inputElement.send_keys("\n")
        homePassList = driver.find_element_by_xpath('//*[@id="homePassList"]/tbody')
        homePassListText = str(homePassList.text).split('\n')
        for idx, text in enumerate(homePassListText):
            homePassListText[idx] = text.split(' ')

        #수비
        inputElement = driver.find_element_by_xpath('//*[@id="btnDefFlag"]')
        inputElement.send_keys("\n")
        homeDefList = driver.find_element_by_xpath('//*[@id="homeDefList"]/tbody')
        homeDefListText = str(homeDefList.text).split('\n')
        for idx, text in enumerate(homeDefListText):
            homeDefListText[idx] = text.split(' ')

        driver.implicitly_wait(50);

        #원정팀 기록
        #공격
        inputElement = driver.find_element_by_xpath('//*[@id="btnAwayTeam"]')
        inputElement.send_keys("\n")
        inputElement = driver.find_element_by_xpath('//*[@id="btnAttFlag"]')
        inputElement.send_keys("\n")
        awayAttList = driver.find_element_by_xpath('//*[@id="awayAttList"]/tbody')
        awayAttListText = str(awayAttList.text).split('\n')
        for idx, text in enumerate(awayAttListText):
            awayAttListText[idx] = text.split(' ')

        #패스
        inputElement = driver.find_element_by_xpath('//*[@id="btnPassFlag"]')
        inputElement.send_keys("\n")
        awayPassList = driver.find_element_by_xpath('//*[@id="awayPassList"]/tbody')
        awayPassListText = str(awayPassList.text).split('\n')
        for idx, text in enumerate(awayPassListText):
            awayPassListText[idx] = text.split(' ')

        #수비
        inputElement = driver.find_element_by_xpath('//*[@id="btnDefFlag"]')
        inputElement.send_keys("\n")
        awayDefList = driver.find_element_by_xpath('//*[@id="awayDefList"]/tbody')
        awayDefListText = str(awayDefList.text).split('\n')
        for idx, text in enumerate(awayDefListText):
            awayDefListText[idx] = text.split(' ')

        #날씨
        weather = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div/ul/li[4]/span[2]')
        weather = weather.text.replace(" ","")
        weather = weather.replace("(", ")")
        weather = weather.replace("℃",")").split(")")
        weatherText = weather[0]
        temperature = weather[1]

        #print(len(homeAttListText))
        #print(homeAttListText)
        #기록 DB에 저장
        for idx, player in enumerate(homeAttListText):
            if int(player[3]) > 0:
                test_collection.update_one({'team': hometeam.text, 'name': player[1], "backNum": player[0]},
                                           {'$push': {
                                               'record': {'round': round, 'matchTeam': awayteam.text, 'stadium': matchText,
                                                          'weather': weatherText, 'temperature': temperature,
                                                          'pos':player[2], 'mins': player[3], 'matchRate': player[4],
                                                          'attRecord': {'goal': homeAttListText[idx][5],
                                                                        'sht': homeAttListText[idx][6],
                                                                        'sot': homeAttListText[idx][7],
                                                                        'paSht': homeAttListText[idx][8],
                                                                        'paSot': homeAttListText[idx][9],
                                                                        'drb': homeAttListText[idx][10],
                                                                        'drbPer': homeAttListText[idx][11],
                                                                        'f3In': homeAttListText[idx][12]},
                                                          'passRecord': {'pass': homePassListText[idx][5],
                                                                         'passPer': homePassListText[idx][6],
                                                                         'keyP': homePassListText[idx][7],
                                                                         'frontPass': homePassListText[idx][8],
                                                                         'backPass': homePassListText[idx][9],
                                                                         'attPass': homePassListText[idx][10],
                                                                         'attPassPer': homePassListText[idx][11],
                                                                         'defPass': homePassListText[idx][12],
                                                                         'defPassPer': homePassListText[idx][13],
                                                                         'longPass': homePassListText[idx][14],
                                                                         'longPassPer': homePassListText[idx][15],
                                                                         'cross': homePassListText[idx][16],
                                                                         'crossPer': homePassListText[idx][17]},
                                                          'defRecord': {'compete': homeDefListText[idx][5],
                                                                        'competePer': homeDefListText[idx][6],
                                                                        'air': homeDefListText[idx][7],
                                                                        'airPer': homeDefListText[idx][8],
                                                                        'tackle': homeDefListText[idx][9],
                                                                        'tacklePer': homeDefListText[idx][10],
                                                                        'clr': homeDefListText[idx][11],
                                                                        'inter': homeDefListText[idx][12],
                                                                        'foul': homeDefListText[idx][13],
                                                                        'yel': homeDefListText[idx][14],
                                                                        'red': homeDefListText[idx][15]}}}},
                                           upsert=True)

        for idx, player in enumerate(awayAttListText):
            if int(player[3]) > 0:
                test_collection.update_one({'team': awayteam.text, 'name': player[1], "backNum": player[0]},
                                           {'$push': {
                                               'record': {'round': round, 'matchTeam': hometeam.text,
                                                          'stadium': matchText,
                                                          'weather': weatherText, 'temperature': temperature,
                                                          'pos': player[2], 'mins': player[3], 'matchRate': player[4],
                                                          'attRecord': {'goal': awayAttListText[idx][5],
                                                                        'sht': awayAttListText[idx][6],
                                                                        'sot': awayAttListText[idx][7],
                                                                        'paSht': awayAttListText[idx][8],
                                                                        'paSot': awayAttListText[idx][9],
                                                                        'drb': awayAttListText[idx][10],
                                                                        'drbPer': awayAttListText[idx][11],
                                                                        'f3In': awayAttListText[idx][12]},
                                                          'passRecord': {'pass': awayPassListText[idx][5],
                                                                         'passPer': awayPassListText[idx][6],
                                                                         'keyP': awayPassListText[idx][7],
                                                                         'frontPass': awayPassListText[idx][8],
                                                                         'backPass': awayPassListText[idx][9],
                                                                         'attPass': awayPassListText[idx][10],
                                                                         'attPassPer': awayPassListText[idx][11],
                                                                         'defPass': awayPassListText[idx][12],
                                                                         'defPassPer': awayPassListText[idx][13],
                                                                         'longPass': awayPassListText[idx][14],
                                                                         'longPassPer': awayPassListText[idx][15],
                                                                         'cross': awayPassListText[idx][16],
                                                                         'crossPer': awayPassListText[idx][17]},
                                                          'defRecord': {'compete': awayDefListText[idx][5],
                                                                        'competePer': awayDefListText[idx][6],
                                                                        'air': awayDefListText[idx][7],
                                                                        'airPer': awayDefListText[idx][8],
                                                                        'tackle': awayDefListText[idx][9],
                                                                        'tacklePer': awayDefListText[idx][10],
                                                                        'clr': awayDefListText[idx][11],
                                                                        'inter': awayDefListText[idx][12],
                                                                        'foul': awayDefListText[idx][13],
                                                                        'yel': awayDefListText[idx][14],
                                                                        'red': awayDefListText[idx][15]}}}},
                                           upsert=True)

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
