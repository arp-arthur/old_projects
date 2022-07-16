from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class InstagramBot():
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(CHROME_DRIVER_PATH)

    def go_to_website(self):
        self.driver.get('https://www.instagram.com')

    def sleep(self, secs):
        time.sleep(secs)

    def add_user_and_password(self, user, password):
        fields = self.driver.find_elements(By.XPATH, "//input[@class='_2hvTZ'")
        values = [user, password]
        i = 0
        for field in fields:
            field.click()
            field.send_keys(values[i])
            i += 1
            self.sleep(1)

        self.driver.find_element(By.CLASS_NAME, 'sqdOP  L3NKy   y3zKF     ').click()

    def shutdown(self):
        self.driver.quit()



CHROME_DRIVER_PATH = './chrome_driver/chromedriver.exe'

bot = InstagramBot()

bot.go_to_website()
bot.sleep(10)
bot.add_user_and_password('arp_arthur', 'arp@241247')
bot.sleep(10)
bot.shutdown()
