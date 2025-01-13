from Tools import tools_v000 as tools
import os
from os.path import dirname
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
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

delay_properties = 15

def connectToServiceNow(user_name) :
    tools.driver.get("https://nn.service-now.com")
    
    # # place the username :
    # tools.waitLoadingPageByID2(20, 'i0116')
    
    # username_input = tools.driver.find_element(By.ID, 'i0116')
    # username_input.send_keys(user_name)
    # time.sleep(1)
    # username_input.send_keys(Keys.ENTER)
    # time.sleep(1)
    
    # # Need to test if the connection is succeed or not
    # # Test if there is or not another possibility to connect
    # if tools.waitLoadingPageByXPATH2(delay_properties, '//*[@id="differentVerificationOption"]') :
    #     otherConnection = tools.driver.find_element(By.XPATH, '//*[@id="differentVerificationOption"]')
    #     otherConnection.click()

    #     # Used the validation via the app
    #     tools.waitLoadingPageByXPATH2(delay_properties, '//*[@id="verificationOption1"]')
    #     verificationOption1 = tools.driver.find_element(By.XPATH, '//*[@id="verificationOption1"]')
    #     verificationOption1.click()

    # # Need to wait the load of the page
    # tools.waitLoadingPageByXPATH2(20, '//*[@id="user_info_dropdown"]/div/span[1]')

    tools.waitLoadingPageByXPATH2(20, '//*[@id="item-heading_greeting"]//h1')

def connectToServiceNowIncidentChange(incident_change_id) :
    tools.driver.get("https://nn.service-now.com/text_search_exact_match.do?sysparm_search=" + incident_change_id)
    
def collectData() :
    global caller, incidentTitle, description_text  # Déclarer les variables globales ici

    # Need to check if it's an incident/change or a Problem issue
    if (tools.waitLoadingPageByXPATH2(20, '//*[@id="sys_readonly.incident.number"]')) :
        # Caller
        caller = tools.driver.find_element(By.XPATH, '//*[@id="sys_display.incident.caller_id"]').get_attribute('value').encode('utf-8').decode()

        # Short description (incidentTitle)
        incidentTitle = tools.driver.find_element(By.XPATH, '//*[@id="incident.short_description"]').get_attribute('value').encode('utf-8').decode()

        # Description (description_text)
        description_text = tools.driver.find_element(By.XPATH, '//*[@id="incident.description"]').text.encode('ascii', 'ignore').decode()
    else :
        # Open by
        # caller = tools.driver.find_element(By.XPATH, '//*[@id="problem_task.opened_by_label"]').get_attribute('value').encode('utf-8').decode()
        caller = tools.driver.find_element(By.XPATH, '//*[@id="problem.opened_by_label"]').get_attribute('value').encode('utf-8').decode()
        
        # Short description (incidentTitle)
        # incidentTitle = tools.driver.find_element(By.XPATH, '//*[@id="problem_task.short_description"]').get_attribute('value').encode('utf-8').decode()
        incidentTitle = tools.driver.find_element(By.XPATH, '//*[@id="problem.short_description"]').get_attribute('value').encode('utf-8').decode()

        # Description (description_text)
        # description_text = tools.driver.find_element(By.XPATH, '//*[@id="problem_task.description"]').text.encode('ascii', 'ignore').decode()
        description_text = tools.driver.find_element(By.XPATH, '//*[@id="problem.description"]').text.encode('ascii', 'ignore').decode()

# # Testing 
# # Open Browser
# tools.openBrowserChrome()   

# # Connect to ServiceNow
# connectToServiceNow(user_name);

# # Go to the incident or change
# connectToServiceNowIncidentChange(incident_change_id);

# # Need to collect data
# collectData()

