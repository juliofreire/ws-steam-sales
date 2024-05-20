# Import packages
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd


def abrir_navegador():
    options = webdriver.FirefoxOptions()
    options.set_preference('intl.accept_languages', 'pt')
    while True:
        try:
            navegador = webdriver.Firefox(options=options)
        except Exception as err:
            pass
            # escreverLog("ERRO AO TENTAR ABRIR O NAVEGADOR")
        else:
            return navegador

def verificar_elemento(navegador, xpath, cron=10, opcao=0):
    # opcao = 0: 'visibility_of_element_located'
    # opcao = 1: 'elementToBeClickable()'
    try:
        match opcao:
            case 0:
                WebDriverWait(navegador, timeout=cron).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            case 1:
                WebDriverWait(navegador, timeout=cron).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    except:
        return -1
    else:
        return 0


def clicar_interagir(navegador, xpath, acao, valor='', tempoEspera=5):
    # acao = 0: 'click()'
    # acao = 1: 'send_keys()'
    # tempoEspera = data_dict['sleep']['aguarda_elemento']
    match acao:
        case 0:
            while True:
                if verificar_elemento(navegador, xpath, opcao=1) == 0:
                    navegador.find_element('xpath', xpath).click()
                    return
                else:
                    navegador.refresh()
                    time.sleep(tempoEspera)
        case 1:
            while True:
                if verificar_elemento(navegador, xpath, opcao=0) == 0:
                    navegador.find_element('xpath', xpath).send_keys(valor)
                    return
                else:
                    navegador.refresh()
                    time.sleep(tempoEspera)


def reiniciar_aba(navegador):
    navegador.close()
    navegador.switch_to.window(navegador.window_handles[0])
    while True:
        try:
            navegador.switch_to.new_window('tab')
        except:
            pass
        else:
            break

def get_texto(navegador, xpath, cron=10, op=0):
    try:
        elemento = WebDriverWait(navegador, timeout=cron).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    except:
        return -1
    if op == 1:
        return elemento.get_attribute('value')
    return elemento.text


firefox = abrir_navegador()
firefox.get("https://steamdb.info/sales/")
# print(verificar_elemento(firefox, xpath='//*[@id="DataTables_Table_0"]/tbody/tr[1]/td[5]'))
# print(get_texto(firefox, xpath='//*[@id="DataTables_Table_0"]/tbody/tr[1]/td[5]'))

clicar_interagir(firefox, xpath='//*[@id="dt-length-0"]', acao=0)
clicar_interagir(firefox, xpath='//*[@id="dt-length-0"]', acao=1, valor='a')
clicar_interagir(firefox, xpath='//*[@id="DataTables_Table_0_wrapper"]/div[1]/div[1]/label', acao=0)
clicar_interagir(firefox, xpath='//*[@id="DataTables_Table_0_wrapper"]/div[1]/div[1]/label', acao=0, valor=Keys.END)

initial_index = 3
row = 1
col = initial_index
firefox.execute_script("window.scrollBy(0, 100);")

# header:
# //*[@id="DataTables_Table_0"]/thead/tr/th[5]
# body:
# //*[@id="DataTables_Table_0"]/tbody/tr[1]/td[5]
# //*[@id="DataTables_Table_0"]/tbody/tr[1]/td[6]
# //*[@id="DataTables_Table_0"]/tbody/tr[1]/td[8]
# //*[@id="DataTables_Table_0"]/tbody/tr[1]/td[9]
# /html/body/div[4]/div[1]/div[2]/div[2]/div[2]/div[3]/div/div[2]/table/tbody/tr[1]/td[9]
# /html/body/div[4]/div[1]/div[2]/div[2]/div[2]/div[3]/div/div[2]/table/tbody/tr[1]/td[8]

column_names = []
while (verificar_elemento(firefox, xpath='//*[@id="DataTables_Table_0"]/thead/tr/th['+str(col)+']', cron=1)+1):
    column_names.append(get_texto(firefox, xpath='//*[@id="DataTables_Table_0"]/thead/tr/th['+str(col)+']'))
    col += 1
df = pd.DataFrame(columns=column_names)
col = initial_index


# row inicial = 1, col inicial = 5
while(verificar_elemento(firefox, xpath='//*[@id="DataTables_Table_0"]/tbody/tr['+str(row)+']/td['+str(col)+']', cron=0)+1):
    buffer = []
    name = ''
    while(verificar_elemento(firefox, xpath='//*[@id="DataTables_Table_0"]/tbody/tr['+str(row)+']/td['+str(col)+']', cron=0)+1):
        firefox.execute_script("window.scrollBy(0, 5);")
        # print('//*[@id="DataTables_Table_0"]/tbody/tr['+str(row)+']/td['+str(col)+']')
        # print(get_texto(firefox, xpath='//*[@id="DataTables_Table_0"]/tbody/tr['+str(row)+']/td['+str(col)+']'))
        buffer.append(get_texto(firefox, xpath='//*[@id="DataTables_Table_0"]/tbody/tr['+str(row)+']/td['+str(col)+']', cron=1))
        col+=1
    
    for letter in buffer[0]:
        if letter == "\n":
            break
        name += letter

    buffer[0]=name
    df.loc[len(df)] = buffer
    col = initial_index
    row += 1

    print(df)

df.to_csv("out.csv", index=True)
