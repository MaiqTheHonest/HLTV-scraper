import time
from selenium import webdriver
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

hrefs = []
playerList = []

options = Options()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
#options.add_argument("--headless")
options.add_argument("--disable-crash-reporter")
options.add_argument("--disable-popup-blocking") # crucial, otherwise new tab opening is treated as a popup
driver = uc.Chrome(options = options)

driver.get('https://www.hltv.org/stats/teams?startDate=2023-01-01&endDate=2023-12-31')  # any url from stats/teams



windows_teamList  = driver.current_window_handle

elements = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "td.teamCol-teams-overview>a")))
time.sleep(3)



def unpack(xpath):
    stat_value = WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located((By.XPATH, xpath))
    ).text
    return stat_value




for element in elements:
    
    hrefs.append(element.get_attribute("href")) # Collect the required href attributes and store in a list

for href in hrefs[:2]:

    driver.execute_script("window.open('" + href +"');")
    windows_after = driver.window_handles
    window_Team = [x for x in windows_after if x != windows_teamList][1] 
    driver.switch_to.window(window_Team)

    lineups = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Lineups')]"))).click()
    

    #scraping lineups
    bs = BeautifulSoup(driver.page_source,"lxml")
    lineupContainers = bs.find_all("div", class_= "lineup-container")
    teamName = (bs.find("span", class_ = "context-item-name")).text
    
    i = 0  # reset i for new team in team list
    

    for lineupContainer in lineupContainers:
        
        lineupYear = ((lineupContainer.find("div", class_= "lineup-year")).text).replace('Replace context with lineup', '')
        mapsPlusWinrate = (lineupContainer.find_all("div", class_ = "large-strong"))  # grabs both maps and winrate
        mapsPlayed = int(mapsPlusWinrate[0].text)
        Winrate = round(int((mapsPlusWinrate[1].text).split()[0])/mapsPlayed, 2)
        
        # get the first 5 members, increase i by 1, get the next 5 members, increase i by 1 etc.
        lineupMembers = (WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.teammate-info>a"))))[5*i : 5*(1+i)]
        i += 1
        j = 0
        newhrefs = []  # reset hrefs for new lineup container
        playerPrelimNames = []
        

        for lineupMember in lineupMembers:
        
            newhrefs.append(lineupMember.get_attribute("href")) # Collect the required href attributes and store in a list
            playerPrelimNames.append(lineupMember.find_element(By.CSS_SELECTOR, "div.text-ellipsis").text)

        for newhref in newhrefs:
            
            playerPrelimName = playerPrelimNames[j]
            j += 1

            if not any(d['playerName'] == playerPrelimName for d in playerList):  # checks if current player name is in playerList already
                valueToFill = True
                driver.execute_script("window.open('" + newhref +"');")
                windows_after = driver.window_handles
                window_Player = [x for x in windows_after if x != window_Team][2]
                driver.switch_to.window(window_Player)

                # scraping individual player stats
                statList = dict()
                pbs = BeautifulSoup(driver.page_source,"lxml")
                playerName = pbs.find("h1", class_= "summaryNickname").text
                stats = pbs.find_all("div", class_="stats-row")
                statTopPanel = pbs.find_all("div", class_ = "summaryStatBreakdownDataValue")
                statImpact = statTopPanel[3].text
                statKAST = (statTopPanel[2].text).strip("%")

            else:
                valueToFill = False

            for stat in stats:
                    
                statPair = stat.find_all("span")

                if valueToFill == True:
                    actualStat = (statPair[1].text).strip("%")
                else:
                    actualStat = 'NA'  # sets to NA if this is a repeat of the player
                    statImpact = 'NA'
                    statKAST = 'NA'
                    statOKratio = 'NA'
                    statOK = 'NA'
                    statRifleKills = 'NA'
                    statSniperKills = 'NA'
                    statSmgKills = 'NA'
                    statPistolKills = 'NA'
                    playerName = 'NA'
                    
                statList = {**statList, **dict({f"{statPair[0].text}" : actualStat})} # ** merges 2 dicts

            if valueToFill == True:  # additional player stats scraping
                
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Individual')]"))).click()
                
                statOKratio = unpack('/html/body/div[2]/div[8]/div[2]/div[1]/div/div[6]/div/div[1]/div[5]/div[3]/span[2]')
                statOK = unpack('/html/body/div[2]/div[8]/div[2]/div[1]/div/div[6]/div/div[1]/div[5]/div[1]/span[2]')
                statRifleKills = unpack("/html/body/div[2]/div[8]/div[2]/div[1]/div/div[6]/div/div[2]/div[5]/div[1]/span[2]")
                statSniperKills = unpack("/html/body/div[2]/div[8]/div[2]/div[1]/div/div[6]/div/div[2]/div[5]/div[2]/span[2]")
                statSmgKills = unpack("/html/body/div[2]/div[8]/div[2]/div[1]/div/div[6]/div/div[2]/div[5]/div[3]/span[2]")
                statPistolKills = unpack("/html/body/div[2]/div[8]/div[2]/div[1]/div/div[6]/div/div[2]/div[5]/div[4]/span[2]")




            playerList = playerList + [{**dict({"playerName" : playerName}),
                                            **dict({"teamName" : teamName + ' ' + lineupYear}), 
                                            **dict({"mapsPlayed" : mapsPlayed}), 
                                            **dict({"winrate" : Winrate}),
                                            **dict({"hltv impact" : statImpact}),
                                            **dict({"KAST (%)" : statKAST}),
                                            **dict({"openingKills" : statOK}),
                                            **dict({"OKratio" : statOKratio}),
                                            **dict({"rifleKills" : statRifleKills}),
                                            **dict({"sniperKills" : statSniperKills}),
                                            **dict({"smgKills" : statSmgKills}),
                                            **dict({"pistolKills" : statPistolKills}),  **statList}]

            if valueToFill == True:
                driver.close() # close the tab if it actually has been opened
    
            driver.switch_to.window(window_Team) # switch_to the parent_window_handle

    driver.close()
    driver.switch_to.window(windows_teamList)

driver.quit()  

