import argparse
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import accountInfoGenerator as account
import getVerifCode as verifiCode
from selenium import webdriver
import fakeMail as email
import time

# Setting up argument parsing
parser = argparse.ArgumentParser(description="Instagram Auto Account Creation Bot")
args = parser.parse_args()

# Generate a random user agent
ua = UserAgent()
userAgent = ua.random
print(userAgent)

# Replace 'your path here' with your Chrome binary absolute path
driver = webdriver.Chrome()

# Save the login & pass into accounts.txt file.
acc = open("accounts.txt", "a")

driver.get("https://www.instagram.com/accounts/emailsignup/")
time.sleep(8)

try:
    cookie = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,
                                                                        '/html/body/div[3]/div/div/button[1]'))).click()
except:
    pass

name = account.username()

# Preencher o e-mail
campo_email = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH,
                                    '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div[2]/div/form/div[4]/div/label/input'))
)
fake_email = email.getFakeMail()[0]  # Corrigindo para pegar o primeiro elemento da lista
campo_email.send_keys(fake_email)
print(fake_email)

# Preencher o nome completo
campo_nome = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH,
                                    "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div[2]/div/form/div[5]/div/label/input"))
)
campo_nome.send_keys(account.generatingName())
print(account.generatingName())

# Preencher o nome de usuário
campo_username = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH,
                                    "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div[2]/div/form/div[6]/div/label/input"))
)
campo_username.send_keys(name)
print(name)

# Preencher a senha
campo_password = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH,
                                    "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div[2]/div/form/div[7]/div/label/input"))
)
acc_password = account.generatePassword()
campo_password.send_keys(acc_password)  # Você pode determinar outra senha aqui.

print(name + ":" + acc_password, file=acc)

acc.close()

WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div[2]/div/form/div[8]/div"))).click()

time.sleep(8)

# Preenche a data de nascimento com o ano 2004
campo_ano = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH,
                                    '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div/div/div[4]/div/div/span/span[3]/select'))
)
select_ano = Select(campo_ano)
select_ano.select_by_value('2004')

# Clica no botão para continuar
botao_continuar = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH,
                                '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div/div/div[6]/button'))
)
botao_continuar.click()

time.sleep(3)

# Divide o email em nome e domínio
fMail = fake_email.split("@")
mailName = fMail[0]
domain = fMail[1]

# Obtém o código de verificação
instCode = verifiCode.getInstVeriCode(mailName, domain, driver)

# Preencher o código de confirmação usando XPath
campo_codigo = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH,
                                    '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div/div[2]/form/div/div[1]/input'))
)
campo_codigo.send_keys(instCode)

# Clica no botão para confirmar o código
botao_confirmar = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH,
                                '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div/div[2]/form/div/div[2]/div'))
)
botao_confirmar.click()

time.sleep(10)

# Aceitando as notificações
driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
time.sleep(2)

# Logout
driver.find_element_by_xpath(
    "//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]/span/img").click()
driver.find_element_by_xpath(
    "//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/div[2]/div").click()

try:
    not_valid = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[4]/div')
    if (not_valid.text == 'That code isn\'t valid. You can request a new one.'):
        time.sleep(1)
        driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div[1]/div[2]/div/button').click()
        time.sleep(10)
        instCodeNew = verifiCode.getInstVeriCodeDouble(mailName, domain, driver, instCode)
        confInput = driver.find_element_by_name('email_confirmation_code')
        confInput.send_keys(Keys.CONTROL + "a")
        confInput.send_keys(Keys.DELETE)
        confInput.send_keys(instCodeNew, Keys.ENTER)
except:
    pass

time.sleep(5)
driver.quit()
