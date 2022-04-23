# Libraries

import pandas as pd


# Utils
def isCurrentTab(currentTab, tabId):
    currentTab = currentTab.replace('/', "")

    if currentTab == '':
        return tabId == 'company'
    else:
        return currentTab == tabId


t1b1_df = pd.read_csv('data/t1b1.csv')
