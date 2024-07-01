import time
from selenium import webdriver
import html_selectors
import db_queries
import url
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import db_connection
from selenium.webdriver.chrome.service import Service as ChromeService
from subprocess import CREATE_NO_WINDOW

mode = 0

# PROGRAMA DESENVOLVIDO POR LUCAS WILLIAM MARTINS LIMA
# LinkedIn: https://www.linkedin.com/in/lucaswmlima
# Github: https://www.github.com/LucaswmLima
# Outros Trabalhos: portfolio-lucaswilliam.vercel.app

# MODO DE INICIAR A AUTOMACAO NOVA
def start_mode_0():
    global mode
    mode = 0
    db_queries.delete_all()
    db_queries.delete_all_errors()
    start_scrapping()

# MODO DE INICIAR A AUTOMACAO DE ONDE PAROU
def start_mode_1():
    global mode
    mode = 1
    start_scrapping()

def start_scrapping():
    chrome_service = ChromeService(".\driver\chromedriver.exe")
    chrome_service.creationflags = CREATE_NO_WINDOW
    driver = webdriver.Chrome(service=chrome_service)
    driver.get(url.url_login)  # ABRE O SITE DO XENTRY
    time.sleep(5)
    driver.find_element("id", html_selectors.acceptCookieButton).click()  # CLICA NO BOTAO DE ACEITAR COOKIES
    time.sleep(5)
    driver.find_element('xpath', html_selectors.loginButton).click()  # CLICA NO BOTAO DE LOGIN
    time.sleep(5)
    driver.find_element('id', html_selectors.userIdInput).send_keys(db_queries.dbUsername)  # INSERE O LOGIN DO USUARIO
    time.sleep(3)
    driver.find_element('id', html_selectors.nextLoginButton).click()  # CLICA NO BOTAO DE LOGIN
    time.sleep(3)
    driver.find_element('id', html_selectors.userPasswordInput).send_keys(db_queries.dbPassword)  # INSERE A SENHA DO USUARIO
    time.sleep(3)
    driver.find_element('id', html_selectors.submitLoginButton).click()  # CLICA NO BOTAO DE FINALIZAR O LOGIN
    time.sleep(5)

    
    # SE O MODE FOR 1 ELE COMECA DA ONDE A ULTIMA AUTOMACAO PAROU
    if mode == 1:
        print('Retomando a ultima automacao...\n')
        countIndex = db_queries.select_last_dealership() # COMEÇA O LOOP DEPOIS DA ULTIMA QUE DEU CERTO
        countIndex = countIndex + 1
        lastCorrect = db_queries.get_db_dealership(countIndex, 1)
    # SE O MODE FOR 0 ELE INICIA A AUTOMACAO NO PRIMEIRO ITEM
    else:
        print('Iniciando nova automacao...\n')
        db_queries.delete_all()
        db_queries.delete_all_errors()
        countIndex = db_queries.minDealdershipIndex
        lastCorrect = 0

    # SETA TODAS AS VARIAVEIS
    exitWhile = 0
    whileCount = 0
    dataList = []
    dataListArrays = []
    currentDealership = 0
    errorList = []

    while countIndex <= db_queries.maxDealershipIndex:
        try:             
            time.sleep(5)
            currentDealership = db_queries.get_db_dealership(countIndex, 1) # PEGA O NUMERO DA CSS ATUAL

            if currentDealership == 0:
                while currentDealership == 0:
                    countIndex = countIndex + 1
                    currentDealership = db_queries.get_db_dealership(countIndex, 1) # PEGA O NUMERO DA CSS ATUAL
                
            time.sleep(5)
            # TROCA DE CONCESSIONARIA
            driver.find_element('xpath', html_selectors.dealerShipButton).click()  # CLICA NO BOTAO DE TROCA DE CONCESSIONARIA
            time.sleep(5)
            driver.find_element('xpath', (
                f'//*[contains(text(), "{currentDealership}")]')).click()  # SELECIONA A CONCESSIONARIA ATUAL
            time.sleep(5)
            driver.find_element('xpath', html_selectors.changeDealership).click()  # CLICA EM ALTERAR A CONCESSIONARIA
            time.sleep(5)
            driver.get(url.url_data)  # ABRE O SITE DO XENTRY NA ABA DE DADOS DA CONCESSIONARIA
            time.sleep(15)

            while exitWhile == 0:
                driver.find_element('xpath', html_selectors.moreDataButton).click()  # CLICA EM CARREGAR MAIS DADOS
                time.sleep(5)
                cards = driver.find_elements(By.CSS_SELECTOR, html_selectors.cardInfo) # LE TUDO
                whileCount = whileCount + 1
                # print(f'Lista de cards expandida {whileCount} vezes')
                cardDate = cards[-4].get_attribute('innerText').strip() # PEGA O TEXTO PARA COMPARAR
                # print(f'Data atual dos dados: {cardDate}')

                # DECISOES PARA ATÉ QUANTO VAI LER, AQUI TROCA PARA MUDAR ATÉ QUANDO ELE VAI COLETAR INFOS

                # PARA SAIR POR DATA ( NA SEGUNDA DATA TEM QUE TER O ESPAÇO ENTRE A BARRA E O NUMERO E AMBAS SEREM IGUAIS)
                if '/20' in cardDate or '/ 20' in cardDate:
                    exitWhile = 1
                if '/19' in cardDate or '/ 19' in cardDate:
                    exitWhile = 1
                if '/18' in cardDate or '/ 18' in cardDate:
                    exitWhile = 1
                if '/17' in cardDate or '/ 17' in cardDate:
                    exitWhile = 1
                if '/16' in cardDate or '/ 16' in cardDate:
                    exitWhile = 1
                if '/15' in cardDate or '/ 15' in cardDate:
                    exitWhile = 1
                
                # PARA SE FIZER N VEZES
                if whileCount >= 25:
                    whileCount = 0
                    exitWhile = 1
            
            exitWhile = 0

            # SELECIONA TODOS OS CARDS DA AREA DE DADOS DA CONCESSIONARIA
            cards = driver.find_elements(By.CSS_SELECTOR, html_selectors.cardInfo)

            # PARA CADA CARD PEGA O INNERTEXT DO OBJETO E ADICIONA NO ARRAY
            for card in cards:
                data = card.get_attribute('innerText').strip()
                dataList.append(data)

            # A CADA 4 ENTIDADES SEPARA EM UM ARRAY DIFERENTE DENTRO DE UM ARRAY
            for i in range(0, len(dataList), 5):
                dataList[i] = dataList[i][:-5] # TIRA AS HORAS DA TABELA
                dataList.insert(i,currentDealership) # ADICIONA O NUMERO DA CONCESSIONARIA NO COMEÇO DE CADA LINHA
                dataListArrays.append(dataList[i: i + 5])

            db_queries.update_last_dealership(countIndex) # ATUALIZA NO BANCO A ULTIMA CONCESSIONARIA QUE DEU CERTO
            countIndex = countIndex + 1 # ATUALIZA O CONTADOR            
            driver.get(url.url_login)  # ABRE O SITE DO XENTRY
            time.sleep(5)      

            # GUARDA O NOME DA ULTIMA QUE DEU CERTO PARA SER USADO PARA CHECAR SE IRA COLOCAR NO CSV DE ERRO OU NAO      
            lastCorrect = currentDealership
            
        except:

            # CHECA SE IRÁ COLOCAR NO ERRO OU NAO, CASO A LASTCORRECT BATA COM A CURRENT, NÃO DEU ERRADO
            if lastCorrect != currentDealership:
                print (f'ERRO! concessionaria {currentDealership} nao existe ou está sem dados!')
                errorList.append(currentDealership)
                countIndex = countIndex + 1 # ATUALIZA O CONTADOR
                db_queries.insert_into_errors(errorList)
                print('Lista atual de concessionarias com erro:')
                errorListData = db_queries.select_errors()
                print(errorListData)
                driver.get(url.url_login)  # ABRE O SITE DO XENTRY
                time.sleep(5)
            else:
                countIndex = countIndex + 1 # ATUALIZA O CONTADOR

        db_queries.insert_into_data(dataListArrays) # COLOCA NO BANCO
        dataList = [] # RESERTA O ARRAY DE DADOS DEPOIS DE COLOCAR NO BANCO
        errorList = [] # RESERTA O ARRAY DE ERROS DEPOIS DE COLOCAR NO BANCO
        dataListArrays = [] # RESERTA OS ARRAYS DEPOIS DE COLOCAR NO BANCO
        whileCount = 0 # RESETA O CONTADOR DO WHILE
        print('Lendo proxima concessionaria...')
    
    try:
        print('Automação completa! Gerando relatório de dados...')
        # IMPRIMINDO O CSV DOS DADOS DO XENTRY
        sql_query = pd.read_sql_query('''select * from xentry_data''',db_connection.db)
        df = pd.DataFrame(sql_query)
        df.to_csv('dados-xentry.csv', sep=';', index=False,
                                    header=['id','Concessionaria','Horario de chegada', 'Ordem de servico', 'Numero do processo', 'FIN/VIN'])
        print('Relatório de dados gerado com sucesso!')
    
    except:
        print('Algo deu errado para imprimir o CSV DE DADOS, verifique se todos os CSV estão fechados, caso o problema persista contate o suporte!')  

    try:
        print('Gerando relatório de erros...')
        # IMPRIME O CSV DE CONCESSIONARIAS COM ERROS
        sql_query2 = pd.read_sql_query('''select * from xentry_errors''',db_connection.db)
        df2 = pd.DataFrame(sql_query2)
        df2.to_csv('erros-xentry.csv', sep=';', index=False,
                                    header=['Concessionaria'])
        print('Relatório de erros gerado com sucesso!')
        
    except:
        print('A automação ocorreu sem erros!')
    
    try:
        # APOS TUDO DER CERTO REINICIA O CONTADOR DA ULTIMA
            db_queries.reset_last_dealership
    except:
        print('')

if __name__ == "main":
    start_scrapping()

# PROGRAMA DESENVOLVIDO POR LUCAS WILLIAM MARTINS LIMA
# LinkedIn: https://www.linkedin.com/in/lucaswmlima
# Github: https://www.github.com/LucaswmLima
# Outros Trabalhos: portfolio-lucaswilliam.vercel.app