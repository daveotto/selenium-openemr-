from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import requests

from shutil import copyfile

import csv
import pickle
import time
import os
import zipfile
import glob
import subprocess

pdffiles = []
idcardfile = []
sourcepath = 'c:\\users\\staff\\downloads\\'
workingpath = sourcepath+'IQ\\'
with open(workingpath+'export.csv', newline='') as csvfile:
    excel = csv.reader(csvfile, delimiter=',', quotechar='"')
    excel = list(excel)

def click_2_xpath(xpat):
    el = driver.find_element_by_xpath(xpat)
    el.click()
    return

def click_2_id(id):
    btn = driver.find_element_by_id(id)
    btn.click()

def click_2_name(name):
    btn = driver.find_element_by_name(name)
    btn.click()

def click_2_value(val):
    btn = driver.find_element_by_value(val)
    btn.click()

def read_IDcarc_name():
    idcardfile = []
    for f in os.listdir(workingpath):
        if f.endswith(".pdf") and f.startswith("img"):
            idcardfile.append(f)
            #print("read id " + idcardfile[0])
    return idcardfile
    
def read_pdf_names():
    pdfnames = []
    for f in os.listdir(workingpath):
        cnt = 0
        if f.endswith(".pdf") and not f.startswith("img"):
            pdfnames.append(f)
            #print("read pdf " + pdfnames[cnt])
            cnt = cnt +1
    return pdfnames



def add_pt_phone_message():
    #open soap note caret menu
    lems=driver.find_elements_by_xpath('.//span[@class = "icon-caret"]')
    lems[0].click()
    #get dropdown orange menu list, PROBABLY DONT NEED
    #lems=driver.find_elements_by_xpath('.//div[@class = "btn-group"]/ul[@class="dropdown-menu"]')
    botstr = "//ul[@class='dropdown-menu']//*[contains(text(),'Patient Phone Message')]"
    el = driver.find_element_by_xpath(botstr)
    el.click()

def click_save():
    save = driver.find_element_by_xpath("//button[contains(text(),'Save')]")
    save.click()
    return

def setpasthist():
    
    el=driver.find_element_by_xpath("//*[@id='past-medical-history']/header/a[1]")
    el.click()
    el2=driver.find_element_by_xpath("//textarea[@placeholder='Enter major events']")
    el2.send_keys("Surgeries: " + excel[1][57] + " " +excel[1][58]+ " "+excel[1][59])
    el3=driver.find_element_by_xpath("//textarea[@placeholder='Enter ongoing medical problems']")
    el3.send_keys("Illnesses: "  + excel[1][54] + " " +excel[1][55]+ " "+excel[1][56])
    el4=driver.find_element_by_xpath("//textarea[@placeholder='Enter family health history']")
    el4.send_keys("Family: " + excel[1][65] + " " +excel[1][66])
    click_save()
    
def nav2pmh():
    el=driver.find_element_by_xpath("//*[@id='past-medical-history']/header/a[1]")
    el.click()
    el2=driver.find_element_by_xpath("//textarea[@placeholder='Enter major events']")
    el2.send_keys("Surgeries: " + excel[1][57] + " " +excel[1][58]+ " "+excel[1][59])
    el3=driver.find_element_by_xpath("//textarea[@placeholder='Enter ongoing medical problems']")
    el3.send_keys("Illnesses: "  + excel[1][54] + " " +excel[1][55]+ " "+excel[1][56])
    el4=driver.find_element_by_xpath("//textarea[@placeholder='Enter family health history']")
    el4.send_keys("Family: " + excel[1][65] + " " +excel[1][66])
    click_save()
    
def nav2summary():
    te = driver.current_url
    k = te.rfind("timeline")
    newurl = te[:k] + "summary"
    driver.get(newurl)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Print chart')]")))
    click_by_css_dataelement('smoking-status-add-button')

def clear_alerts():
    time.sleep(3)
    try:
        alert = browser.switch_to_alert()
        while alert:
            alert.accept()
            #print ("alert accepted")
            time.sleep(1)
            alert = browser.switch_to_alert()
    except:
        print ("no alert")

def clear_popups():
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Close"]'))).click()
    return

def hitescape():
    actions = ActionChains(driver)
    actions.send_keys(Keys.ESCAPE)
    actions.perform()
    actions.send_keys(Keys.ESCAPE)
    actions.perform()
    
def nav2pathist():
    try:
        WebDriverWait(driver, 1).until(EC.alert_is_present())
    except:
        print ("no alert")
    alerts = checkalert()
    while alerts:
        alerts = checkalert()
    hitescape()
    time.sleep(1)
    clear_alerts()
    time.sleep(1)
    clear_alerts()
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_name("pat"))
    #click the history hot link, first on the left under pt name
    el = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/table[2]/tbody/tr/td/a[1]")));
    time.sleep(1)
    clear_alerts()
    el.click()
    return

def shortcut():
    el = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu logo"]/div/div/span[5]/div/div')));
    el.click()
    el = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu logo"]/div/div/span[5]/div/ul/li[1]/div')));
    el.click()
    time.sleep(2)

    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="framesDisplay"]/div[3]/iframe'))
    el = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pid_6"]/td[1]')));
    #el = driver.find_element_by_xpath( '//*[@id="pid_6"]/td[1]')
    el.click()
    
    
    return

def nav2lifestyle():
    #time.sleep(5)
    clear_alerts()
    #time.sleep(3)
    #clear_alerts()
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_name("pat"))
    el = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/div[2]/div/a[2]")));
    el.click()
    time.sleep(2)
    el = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='header_tab_Lifestyle']")));
    el.click()
    #set the smoking status combobox
    set_by_xpath('//*[@id="form_tobacco"]', excel[1][60])
    #alcohol
    set_by_xpath('//*[@id="form_alcohol"]', excel[1][64])
    #what does pt smoke
    set_by_xpath('//*[@id="form_recreational_drugs"]', excel[1][61])
    
    
    #for now just push all the allergies, surgeries, conditions and family history into this text box
    #first go to 'other' section
    el = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="header_tab_Other"]')));
    el.click()
    
    misc_string = "Surgeries: " + excel[1][57]
    misc_string = "\nSurgery to extrememties, neck, back: " + excel[1][58]
    misc_string = "\nOther surgery: " + excel[1][59]
    misc_string = "\nMedication allergies: " + excel[1][51] + " " + excel[1][52]
    misc_string = "\nOther allergies: " + excel[1][53]
    misc_string = "\nIllnesses: " + excel[1][54]
    misc_string = "\nOther conditions: " + excel[1][54] + " " + excel[1][55]
    misc_string = "\nBlood relatives: " + excel[1][65]
    set_by_xpath('//*[@id="form_additional_history"]', misc_string)
    
    #close the form
    el = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="HIS"]/small/div[1]/button')));
    el.click()
    #close the history
    el = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/div[2]/div/a[1]")));
    el.click()
    return

def enter_allergies():
    time.sleep(4)
    checkalert()
    #click the allergies button
    el = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="patient_stats_issues"]/tbody/tr[2]/td/div[1]/table/tbody/tr/td[1]/a')));
    checkalert()
    el.click()
    time.sleep(1)

    
    #click the add button for medicine allergies
    el = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="patient_stats"]/form/a')));
    el.click()
    time.sleep(1)
    driver.switch_to.default_content()
    count = len(driver.find_elements_by_xpath("//iframe"))
    #print ("iframecount in rightside " + str(count))
    driver.switch_to.frame(driver.find_element_by_id("modalframe"))
    #put the allergy in this editbox
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/form/table/tbody/tr[3]/td[2]/input')));
    time.sleep(2)
    #print ("med allergies are " +excel[1][52])
    #print ("other allergies are " +excel[1][53])
    if len(excel[1][52]) > 0:    
        set_by_xpath('/html/body/div[1]/div/form/table/tbody/tr[3]/td[2]/input',excel[1][52]);
    else:
        set_by_xpath('/html/body/div[1]/div/form/table/tbody/tr[3]/td[2]/input',"NKDA (No known drug allergies)");
    #click save
    click_2_xpath('/html/body/div[1]/div/form/center/p/input[1]');
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_name("pat"))

    
    #click the add button for other allergies
    time.sleep(1)
    el = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="patient_stats"]/form/a')));
    el.click()
    time.sleep(1)
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_id("modalframe"))
    #put the allergy in this editbox
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/form/table/tbody/tr[3]/td[2]/input')));
    if len(excel[1][53]) > 0:    
        set_by_xpath('/html/body/div[1]/div/form/table/tbody/tr[3]/td[2]/input',excel[1][53]);
    else:
                 set_by_xpath('/html/body/div[1]/div/form/table/tbody/tr[3]/td[2]/input',"No known other allergies");
    #click save
    click_2_xpath('/html/body/div[1]/div/form/center/p/input[1]');
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_name("pat"))
        
    #click back
    time.sleep(5)
    click_2_xpath('//*[@id="back"]');
    
    return

def enter_med_problems():
    #click the med problem button
    time.sleep(1)
    el = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="patient_stats_issues"]/tbody/tr[1]/td/div[1]/table/tbody/tr/td[1]/a')));
    el.click()
    #click the add button
    time.sleep(1)
    el = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="patient_stats"]/form/a')));
    el.click()
    time.sleep(1)
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_id("modalframe"))
    #set title to whatever is in the excel field
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/form/table/tbody/tr[3]/td[2]/input')));
    if len(excel[1][65]) > 0:
        set_by_xpath('/html/body/div[1]/div/form/table/tbody/tr[3]/td[2]/input', excel[1][65])
    else:
        set_by_xpath('/html/body/div[1]/div/form/table/tbody/tr[3]/td[2]/input', "No known medical problems")
    #set outcome to unassigned
    set_by_xpath('//*[@id="form_outcome"]', "Unassigned")
    #click save
    click_2_xpath('/html/body/div[1]/div/form/center/p/input[1]');
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_name("pat"))
    #click back
    time.sleep(3)
    click_2_xpath('//*[@id="back"]');

    return

def nav_2_right_side_tabs():
    time.sleep(3)
    checkalert()
    time.sleep(3)
    checkalert()

    enter_allergies()
        
    enter_med_problems()
        
    return    

def uploaddrops():
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_name("pat"))
    #open documents
    el = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/table[2]/tbody/tr/td/a[3]")));
    el.click()
    #click intake docs node
    el = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="objTreeMenu_1_node_1_6"]/nobr/a/span')));
    el.click()
    time.sleep(1)

    #get the list of intake docs
    pdffiles = read_pdf_names()
    
    #go to the intake documents category
    for filename in pdffiles:
        filename = workingpath + filename            
        set_by_xpath("//*[@id='source-name']", filename)
        click_2_xpath("//*[@id='documents_actions']/form[1]/div[3]/p[3]/input")
        time.sleep(1)
        #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='documents_actions']/form[1]/div[3]/p[3]/input")));

    #get PT ID/ins scan if there is one
    idcardfname = read_IDcarc_name()
    #print (idcardfname[0])
    if len(idcardfname) > 0:
        cardname = workingpath + idcardfname[0]
        #open patient information node
        try:
            click_2_xpath("//*[@id='objTreeMenu_1_node_1_10']/nobr/img[1]")
        except:
            print ("node looks open")
        #select ID card
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="objTreeMenu_1_node_1_10_1"]/nobr/a')));
        click_2_xpath('//*[@id="objTreeMenu_1_node_1_10_1"]/nobr/a/span')
        time.sleep(1)
        #UL ID
        set_by_xpath("//*[@id='source-name']", cardname)
        click_2_xpath("//*[@id='documents_actions']/form[1]/div[3]/p[3]/input")
    
    return

def checkalert():
    try:
        alert = driver.switch_to.alert
        alert.text
        alert.accept()
        return true
    except:
        print ("noalert")
        return False
    
def testff():
    #whocheck = driver.find_element_by_name("form_cb2")
    driver.switch_to.frame(driver.find_element_by_name("pat"))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'form_fname')))
    
    #who block
    set_by_id("form_fname", excel[1][1])
    set_by_id("form_mname", excel[1][2])
    set_by_id("form_lname", excel[1][3])
    set_by_id("form_ss", excel[1][6])
    set_by_id("form_sex", excel[1][5])
    set_by_id("form_DOB", excel[1][4])
    set_by_id("form_status", excel[1][7])
    #NOK info will be stored in the 4 generic fields
    nokname = excel[1][33] + ", " + excel[1][31] + " " + excel[1][32]
    set_by_id("form_genericname1", nokname)
    #relation
    set_by_id("form_genericval1", excel[1][34])
    #phone
    set_by_id("form_genericname2", excel[1][35])
    #address
    nokaddr = excel[1][219] +  " " + excel[1][38] +  " " + excel[1][220] + ", " + excel[1][221] + "  " + excel[1][222]
    set_by_id("form_genericval2", nokaddr)
    #close the who block
    click_2_id("form_cb_1")
    
    #open the block for contact info
    click_2_id("form_cb_2")
    set_by_id("form_phone_cell", excel[1][10])
    set_by_id("form_email", excel[1][14])
    set_by_id("form_phone_home", excel[1][11])
    set_by_id("form_phone_biz", excel[1][12])
    addrstring = excel[1][199] + " " + excel[1][9]
    set_by_id("form_street", addrstring)
    set_by_id("form_city", excel[1][200])
    set_by_id("form_state", excel[1][201])
    set_by_id("form_postal_code", excel[1][202])
    #close the block
    click_2_id("form_cb_2")

    #open the block for choices
    click_2_id("form_cb_3")
    #set hipaa received.  This is true if the forms are complete
    set_by_xpath('//*[@id="form_hipaa_notice"]',"YES")
    #NEED TO ADD Q TO IQ:  ALLOW EMAIL, ALLOW TEXT MESSAGE
    #set voicemessage authorization
    if excel[1][219] == "Yes":
        set_by_xpath('//*[@id="form_hipaa_voice"]',"YES")
    else:
        set_by_xpath('//*[@id="form_hipaa_voice"]',"NO")
    set_by_xpath('//*[@id="form_hipaa_allowsms"]',"NO")
    set_by_xpath('//*[@id="form_hipaa_allowemail"]',"NO")
    #close the block
    click_2_id("form_cb_3")
    
    #open the insurance block
    click_2_name("form_cb_ins")
    #G info block
    relation = excel[1][16]
    set_by_id("form_i1subscriber_relationship", relation)
    if relation != "Self":
        set_by_name("i1subscriber_fname", excel[1][20])
        set_by_name("i1subscriber_mname", excel[1][21])
        set_by_name("i1subscriber_lname", excel[1][22])
        addrstring = excel[1][199] + " " + excel[1][9]
        set_by_name("i1subscriber_street", addrstring)

        set_by_id("form_i1subscriber_state", excel[1][211])
        set_by_name("i1subscriber_city", excel[1][210])
        set_by_name("i1subscriber_postal_code", excel[1][211])

        #name of the insurance is in field 17
        set_by_xpath("//*[@id='div_ins']/table[1]/tbody/tr[2]/td[1]/table/tbody/tr[1]/td[2]/input", excel[1][17])
        #member id in field 18
        set_by_xpath("//*[@id='div_ins']/table[1]/tbody/tr[2]/td[1]/table/tbody/tr[3]/td[2]/input", excel[1][18])
        #group id in field 19
        set_by_xpath("//*[@id='div_ins']/table[1]/tbody/tr[2]/td[1]/table/tbody/tr[4]/td[2]/input", excel[1][19])
        
        

    set_by_name("i1subscriber_phone", excel[1][26])                        
    set_by_id("i1subscriber_DOB", excel[1][23])            

    #finish the form
    click_2_id("create")
    time.sleep(2)
    
    driver.switch_to.default_content()
    
    count = len(driver.find_elements_by_xpath("//iframe"))
    #print ("iframecount in testff " + str(count))
    driver.switch_to.frame(driver.find_element_by_id("modalframe"))

    time.sleep(3)
    #el = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Confirm Create New Patient']")));
    el = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@value='Confirm Create New Patient']")));
    el.click();
    return
    
def put_value_2_xpath(xpat,val):
    el = driver.find_element_by_xpath(xpat)
    actions = ActionChains(driver)
    actions.move_to_element(el).perform()
    el.send_keys(val)
    return
    
def load_cookie(file1):
    try:
        with open(file1, 'rb') as cookie:
            return pickle.load(cookie)
    except FileNotFoundError as fnf:
        return 0;

def set_by_xpath(xpat, data):
    el = driver.find_element_by_xpath(xpat)
    el.send_keys(data)
    return

def set_by_id(field, data):
    el = driver.find_element_by_id(field)
    el.send_keys(data)
    return

def set_by_classname(field, data):
    el = driver.find_element_by_class_name(field)
    #print(el)
    el.send_keys(data)
    return

def set_by_tagname(field, data):
    el = driver.find_element_by_tag_name(field)
    #print(el)
    el.send_keys(data)
    return

def set_by_name(field, data):
    el = driver.find_element_by_name(field)
    #print(el)
    el.send_keys(data)
    return

def set_by_linktext(field, data):    
    el = driver.find_element_by_link_text(field)
    #print(el)
    el.send_keys(data)
    return
    
def set_by_txtcontent(field, data):
    srstr = "//*[contains(text(), \"" + field + "\")]"
    #print (srstr)
    el = driver.find_element_by_xpath(srstr)
    el.send_keys(data)
    return

def click_by_txtcontent(field):
    srstr = "//*[contains(text(), \"" + field + "\")]"
    #print (srstr)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, srstr)))
    el = driver.find_element_by_xpath(srstr)
    el.click()
    return
    
def set_by_css_dataelement(field, data):
    #el = driver.find_element_by_css_selector(field);
    srstr = '[data-element=\"' + field + '"]'
    #print (srstr)
    el = driver.find_element_by_css_selector(srstr)
    #print (el)
    el.send_keys(data)
    return

def click_by_css_dataelement(field):
    #el = driver.find_element_by_css_selector(field);
    srstr = '[data-element=\"' + field + '"]'
    #print (srstr)
    el = driver.find_element_by_css_selector(srstr)
    el.click()
    return
    
def set_by_css_dataqa(field, data):
    #el = driver.find_element_by_css_selector(field);
    srstr = '[data-qa=\"' + field + '"]'
    #print (srstr)
    el = driver.find_element_by_css_selector(srstr)
    #print (el)
    el.send_keys(data)
    return
        
def set_span_by_text(field, data):
    lems=driver.find_elements_by_xpath('.//span[@class = ""]')
    for el in lems:
        if el.text == field:
            srstr = 'arguments[0].innerHTML = \"' + data + '\";'
            driver.execute_script(srstr, el)
            srstr = 'arguments[0].innerText = \"' + data + '\";'
            driver.execute_script(srstr, el)
            return

def set_span_by_text_new(field, data):
    topstr = "//span[contains(text(),'" + field + "')]"
    el = driver.find_element_by_xpath(topstr)
    el.click()
    botstr = "//ul[@class='ember-select-results']//*[contains(text(),'" + data + "')]"
    el = driver.find_element_by_xpath(botstr)
    el.click()
    return

def set_smoking(data):
    lab = driver.find_element_by_xpath("//label[@for='smoking-option-0']")
    buts = driver.find_elements_by_xpath("//div[@class='panel-section']/div[*]")
    for but in buts:
        if but.text == data:
            but.click()
    click_save()
    return


def open_connect():
    #driver.get("https://static.practicefusion.com/apps/ehr/index.html?c=1385407302#/login")
    #driver.get("https://day.bounceme.net:54443/openemr/interface/login/login.php?site=default")
    driver.get("https://www.qualityucmi.net")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'authUser')))

def PF_login():
    loginID = driver.find_element_by_id("authUser")
    loginID.clear()
    loginID.send_keys("")
    loginID.send_keys("datadriver")
    loginPW = driver.find_element_by_id("clearPass")
    loginPW.send_keys("DataPusher2018")
    loginbt = driver.find_element_by_class_name("btn-default")
    loginbt.click()

def open_patientclient_menu ():
    toplevmenu = "//*[contains(text(), 'Patient/Client')]"
    click_2_xpath(toplevmenu)
    newptmenu = "//*[contains(text(), 'New/Search')]"
    click_2_xpath(newptmenu)
    
#el = driver.findElement(By.cssSelector("a[href*='Female')]"));
# Create a new instance of the Firefox driver

#driver = webdriver.Chrome()
chrome_options = Options()
chrome_options.add_argument("user-data-dir=C:/Users/day/AppData/Local/Google/Chrome/User Data/Default")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(chrome_options=chrome_options)


open_connect()
PF_login()

open_patientclient_menu()
testff()
time.sleep(3)
#shortcut()
nav2pathist()
nav2lifestyle()
nav_2_right_side_tabs()
uploaddrops()

input("\n take a look then Press ENTER to continue...")

driver.close()
driver.quit()
quit()
