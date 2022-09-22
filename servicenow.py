from Tools import tools_v000 as tools
import os
from os.path import dirname
from selenium.webdriver.common.keys import Keys
import time


# -10 for the name of this project ServiceNow
save_path = os.path.dirname(os.path.abspath("__file__"))
propertiesFolder_path = save_path + "/"+ "Properties"

# Example of used
incident_change_id = tools.readProperty(propertiesFolder_path, 'ServiceNow', 'incident_change_id=')
user_name = tools.readProperty(propertiesFolder_path, 'ServiceNow', 'user_name=')

caller = ""
incidentTitle = ""
description_text = ""


def connectToServiceNow(user_name) :
    tools.driver.get("https://nn.service-now.com")
    
    # place the username :
    tools.waitLoadingPageByID2(20, 'i0116')
    
    username_input = tools.driver.find_element_by_id('i0116')
    username_input.send_keys(user_name)
    time.sleep(1)
    username_input.send_keys(Keys.ENTER)
    time.sleep(1)
    
    # Need to wait the load of the page
    tools.waitLoadingPageByXPATH2(20, '//*[@id="user_info_dropdown"]/div/span[1]')

def connectToServiceNowIncidentChange(incident_change_id) :
    tools.driver.get("https://nn.service-now.com/text_search_exact_match.do?sysparm_search=" + incident_change_id)
    
    # Need to wait the load of the page
    tools.waitLoadingPageByXPATH2(20, '//*[@id="sys_readonly.incident.number"]')
    
def collectData() :
    # Caller
    global caller
    caller = tools.driver.find_element_by_xpath('//*[@id="sys_display.incident.caller_id"]')

    # Short description (incidentTitle)
    global incidentTitle
    incidentTitle = tools.driver.find_element_by_xpath('//*[@id="incident.short_description"]')

    # Description (description_text)
    global description_text
    description_text = tools.driver.find_element_by_xpath('//*[@id="incident.description"]').text.encode('ascii', 'ignore')

# # Testing 
# # Open Browser
# tools.openBrowserChrome()   

# # Connect to ServiceNow
# connectToServiceNow(user_name);

# # Go to the incident or change
# connectToServiceNowIncidentChange(incident_change_id);

# # Need to collect data
# collectData()

