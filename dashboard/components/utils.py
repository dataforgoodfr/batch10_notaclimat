# Libraries

from enum import Enum
import pandas as pd


class Pages(Enum):
    COMPANY = 'company'
    COMPARE = 'compare'


# Utils
def isCurrentTab(currentTab, tabId):
    currentTab = currentTab.replace('/', "").upper()

    if currentTab == '':
        return tabId == Pages.COMPANY
    else:
        return Pages[currentTab] == tabId


t1b1_df = pd.read_csv('data/t1b1.csv')
