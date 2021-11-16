import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains

import logging
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.ERROR)

import pandas as pd
import time
PATH = "C:\Program Files (x86)\chromedriver.exe"

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--day", help="day of the week", default= 0)

args = parser.parse_args()

pd_info = pd.DataFrame(columns = ['Club','Direccion','Día','Pista','Horas Libres'])

dias = {'0':''}

op = webdriver.ChromeOptions()
op.add_argument('headless')
driver = webdriver.Chrome(PATH, options=op)

driver.get('https://deportesweb.madrid.es/')
driver.maximize_window()
print(driver.title)



time.sleep(1)
try:
    cookies = WebDriverWait(driver, 15).until(  # 15 sec
            EC.presence_of_element_located((By.XPATH ," /html/body/div[1]/div/a"))
    )
    cookies.click()
except:
    pass

login = WebDriverWait(driver, 15).until(  # 15 sec
        EC.presence_of_element_located((By.XPATH ,"/html/body/form/div[3]/div[2]/div/div[2]/div[3]/div/div/ul/li[2]/div/div/div/button"))
)
login.click()

reserva_espacios = WebDriverWait(driver, 15).until(  # 15 sec
        EC.presence_of_element_located((By.XPATH ,"/html/body/form/div[3]/div[2]/div/div[2]/div[4]/ul/li[6]"))
)
reserva_espacios.click()

time.sleep(2)
if int(args.day) == 0:
    date_ini = 1
    date_end = 8
else:
    date_ini = int(args.day)
    date_end = int(args.day) + 1


try:
    clubs = WebDriverWait(driver, 5).until(  # 15 sec
        EC.presence_of_all_elements_located((By.XPATH,'/html/body/form/div[3]/div[2]/div/div[3]/div[2]/div[3]/div[2]/ul/li'))
    )
    num_clubs = len(clubs)
    for club in range(1,num_clubs+1):
        espacio = WebDriverWait(driver, 5).until(  # 15 sec
                EC.presence_of_element_located((By.XPATH ,"/html/body/form/div[3]/div[2]/div/div[3]/div[2]/div[3]/div[2]/ul/li["+str(club)+"]"))
        )
        if 'Pepu Hernández' in espacio.text:
            continue
        else:
            espacio.click()

        nombre_club  = espacio.text
        print('Club : ', nombre_club.split('\n')[0])
        activities = WebDriverWait(driver, 5).until(  # 15 sec
                EC.presence_of_all_elements_located((By.XPATH,'/html/body/form/div[3]/div[2]/div/div[3]/div[3]/div[3]/div[2]/ul/li'))
        )
        activities_by_club = len(activities)
        #print('Actividades : ',activities_by_club)
        for padel in range(1,activities_by_club+1): #6
            try:
                padel_joven = WebDriverWait(driver, 2).until(  # 15 sec
                          EC.presence_of_element_located((By.XPATH, "/html/body/form/div[3]/div[2]/div/div[3]/div[3]/div[3]/div[2]/ul/li["+str(padel)+"]"))
                )

                if 'Pádel joven' in padel_joven.text:
                    padel_joven.click()

                    for day in range(int(date_ini), int(date_end)):

                        dia_semana = WebDriverWait(driver, 3).until(  # 15 sec
                            EC.presence_of_element_located((By.XPATH,
                                                            '/html/body/form/div[3]/div[2]/div/div[3]/div[4]/div[2]/div[2]/div/div/div/a[' + str(
                                                                day) + ']'))
                        )
                        dia_semana.click()
                        dia = dia_semana.text
                        time.sleep(0.5)

                        pistas = WebDriverWait(driver, 3).until(  # 15 sec
                            EC.presence_of_all_elements_located((By.XPATH,
                                                                 '/html/body/form/div[3]/div[2]/div/div[3]/div[5]/div[2]/div[2]/div/table/tbody/tr[2]/td[2]/table/tbody/tr'))
                        )
                        #print('pistas: ',len(pistas)-1)

                        for num_pista in range(2,1+len(pistas)):
                            pista = WebDriverWait(driver, 3).until(  # 15 sec
                                EC.presence_of_element_located((By.XPATH,'/html/body/form/div[3]/div[2]/div/div[3]/div[5]/div[2]/div[2]/div/table/tbody/tr[2]/td[1]/table/tbody/tr['+str(num_pista)+']/td/span')
                                                               )
                            )
                            nombre_pista = pista.text
                            #print('Pista : ',nombre_pista)
                            time.sleep(0.2)
                            horas = WebDriverWait(driver, 3).until(  # 15 sec
                                EC.presence_of_all_elements_located((By.XPATH,'/html/body/form/div[3]/div[2]/div/div[3]/div[5]/div[2]/div[2]/div/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td'))
                            )
                            num_horas = len(horas)
                            horas_libres = []
                            for j in range(1, num_horas+1):
                                hora_padel = WebDriverWait(driver, 2).until(  # 15 sec
                                    EC.presence_of_element_located((By.XPATH,
                                                                    '/html/body/form/div[3]/div[2]/div/div[3]/div[5]/div[2]/div[2]/div/table/tbody/tr[2]/td[2]/table/tbody/tr['+str(num_pista)+']/td[' + str(
                                                                        j) + ']/img'))
                                )
                                try:
                                    hora = hora_padel.get_attribute('onclick').split("javascript:celdaCuadrante(")[1].split("'")[5]
                                    estado = hora_padel.get_attribute('estado')
                                except:
                                    hora = ''
                                    estado = ''

                                if estado == 'Libre':
                                    horas_libres.append(hora)

                            pd_info.loc[len(pd_info)] = [nombre_club.split('\n')[0], nombre_club.split('\n')[1], dia,nombre_pista, horas_libres]
                        #print(pd_info)
                        volver_dias = WebDriverWait(driver, 5).until(  # 15 sec
                            EC.presence_of_element_located(
                                (By.XPATH, '/html/body/form/div[3]/div[2]/div/div[3]/div[1]/div/div[2]/ul/li[3]/button'))
                        )
                        volver_dias.click()
                        time.sleep(0.5)
                    break
            except: pass
        volver_club = WebDriverWait(driver, 5).until(  # 15 sec
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/form/div[3]/div[2]/div/div[3]/div[1]/div/div[2]/ul/li[1]/button'))
        )
        volver_club.click()
        time.sleep(0.5)


    print(pd_info)
    pd_info.to_excel('padel_madrid.xlsx', index = False)
    driver.quit()
except Exception as e:
    print('Error ',str(e))
    print(pd_info)
    pd_info.to_excel('padel_madrid.xlsx', index=False)
    driver.quit()