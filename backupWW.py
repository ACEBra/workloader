from selenium import webdriver
import time

login_url = 'http://xx.xx.xx.xx'
user = '//*[@id="user_email"]'
password = '//*[@id="user_password"]'
login_button = '//*[@id="new_user"]/div[2]/div/div[1]/input'
user_mgmt_menu = '//*[@id="user-menu-button"]'
sys_mgmt_menu = '//*[@id="user-menu-container"]/ul/li[7]/a'
bacup_restore_menu = '//*[@id="main"]/div/div[1]/div/div[2]/div/div[1]/div/div/ul/li[7]/a/span'
backup_button = '//*[@id="main"]/div/div[1]/div/div[2]/div/div[2]/div[2]/div/form[2]/div/div[2]/a'


# open workload wisdom
driver = webdriver.Chrome(executable_path=r"C:\chromedriver_win32\chromedriver.exe")
driver.maximize_window()

# type username & password and login
driver.get(login_url)
username = driver.find_element_by_xpath(user)
username.send_keys("admin@example.com")
passwd = driver.find_element_by_xpath(password)
passwd.send_keys('password')
login = driver.find_element_by_xpath(login_button)
login.click()

# enter system management menu
admin = driver.find_element_by_xpath(user_mgmt_menu)
admin.click()
time.sleep(1)
sm = driver.find_element_by_xpath(sys_mgmt_menu)
sm.click()

# goto backup & restore sub menu
br = driver.find_element_by_xpath(bacup_restore_menu)
br.click()
time.sleep(1)
backup = driver.find_element_by_xpath(backup_button)
backup.click()

#click OK button on the alert to initiate backup
alt = driver.switch_to.alert
time.sleep(1)
alt.accept()
#alt.dismiss()
