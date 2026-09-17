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

    # Restored 2026-09-17 : the real SSO login steps below were commented out
    # in commit a95be9c (2024-09-27), and the automation kept working only
    # because the Chrome automation profile (BraveUserData) still had a
    # cached, valid SSO session cookie. That cached cookie has since expired,
    # which is why the connection now fails ("Loading took too much time!").
    # Restoring the actual login flow (username + MFA app push approval).
    #
    # With the dedicated managed Edge profile, Windows SSO (PRT) may log the
    # user in silently without ever showing the username field, so this step
    # must not crash when the field never appears - it just means we're
    # already authenticated.

    # place the username, only if the login page is actually shown :
    if tools.waitLoadingPageByID2(20, 'i0116') :
        username_input = tools.driver.find_element(By.ID, 'i0116')
        username_input.send_keys(user_name)
        time.sleep(1)
        username_input.send_keys(Keys.ENTER)
        time.sleep(1)

        # Need to test if the connection is succeed or not
        # Test if there is or not another possibility to connect
        if tools.waitLoadingPageByXPATH2(delay_properties, '//*[@id="differentVerificationOption"]') :
            otherConnection = tools.driver.find_element(By.XPATH, '//*[@id="differentVerificationOption"]')
            otherConnection.click()

            # Used the validation via the app
            tools.waitLoadingPageByXPATH2(delay_properties, '//*[@id="verificationOption1"]')
            verificationOption1 = tools.driver.find_element(By.XPATH, '//*[@id="verificationOption1"]')
            verificationOption1.click()

        print("En attente de la validation MFA (approuver la notification push sur le telephone)...")

        # Need to wait the load of the page - longer delay to leave time for the
        # user to approve the MFA push notification on their phone.
        tools.waitLoadingPageByXPATH2(60, '//*[@id="item-stylized_text_1"]')
    else :
        print("Pas de formulaire de login affiche - session SSO deja active.")

    # Debug screenshot : allows diagnosing login/redirect issues without
    # needing a manual print-screen from the user.
    try :
        tools.driver.save_screenshot(save_path + "/debug_after_login.png")
    except Exception :
        pass

def connectToServiceNowIncidentChange(incident_change_id) :
    tools.driver.get("https://nn.service-now.com/text_search_exact_match.do?sysparm_search=" + incident_change_id)

    # Debug screenshot : capture the state of the page right after navigating
    # to the incident/change search URL, before trying to read any field.
    time.sleep(2)
    try :
        tools.driver.save_screenshot(save_path + "/debug_after_search.png")
    except Exception :
        pass

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

