# Libraries imports

from enum import Enum
import pandas as pd
from urllib.parse import urlencode, urlparse, parse_qsl


class Pages(Enum):
    COMPANY = 'company'
    COMPARE = 'compare'


card_style = "row card rounded p-3"

component_ids = ['company_select']


# Utils
def isCurrentTab(currentTab, page):
    currentTab = currentTab.replace('/', "").upper()

    try:
        if currentTab == '':
            return page == Pages.COMPANY
        else:
            return Pages[currentTab] == page
    except KeyError:
        return False


def parse_url(url):
    parse_result = urlparse(url)
    params = parse_qsl(parse_result.query)
    state = dict(params)
    return state


# Usage
# state_to_url(state of component_ids[0], state of component_ids[1], ...)
def state_to_url(*state):
    if not state or state[0] is None or len(state[0]) == 0:
        return ''

    state = urlencode(dict(zip(component_ids, state)))
    return f'?{state}'


# t1b1_df = pd.read_csv('data/t1b1.csv')
# t1b2_df = pd.read_csv('data/t1b2.csv')
# t1b3_df = pd.read_csv('data/t1b3.csv')
# t1b4_df = pd.read_csv('data/t1b4.csv')
# t1b5_df = pd.read_csv('data/t1b5.csv')
# t1b6_df = pd.read_csv('data/t1b6.csv', sep=';')
# t1b7_df = pd.read_csv('data/t1b1-7.csv')
# t2b2_df = pd.read_csv('data/t2b2.csv')

dataviz_df = pd.read_excel('data/BDD_for_dataviz.xlsx', sheet_name='Sheet1')