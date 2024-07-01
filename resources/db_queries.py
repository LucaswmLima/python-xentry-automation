import db_connection

# PROGRAMA DESENVOLVIDO POR LUCAS WILLIAM MARTINS LIMA
# LinkedIn: https://www.linkedin.com/in/lucaswmlima
# Github: https://www.github.com/LucaswmLima
# Outros Trabalhos: portfolio-lucaswilliam.vercel.app

# COLETA OS DADOS DA TABELA USER
def get_db_user(index):
    db_connection.cursor.execute('SELECT * from user')
    username = db_connection.cursor.fetchall()
    # print(f'Usuario: {username[0][index]}')
    return username[0][index]

# COLETA OS DADOS DA TABELA CSS
def get_db_dealership(id, index):
    db_connection.cursor.execute(f'SELECT * from dealerships WHERE id = {id}')
    dealership = db_connection.cursor.fetchall()
    print(f'Concessionaria atual: Numero {id}, ID {((dealership[0][index]).split())[0]}')
    return (((dealership[0][index]).split())[0])

# PEGA O INDEX DA ULTIMA CSS DO BANCO
def get_max_dealership_index():
    db_connection.cursor.execute('SELECT MAX(Id) FROM dealerships')
    maxDealershipIndex = db_connection.cursor.fetchall()
    # print(f'Ultimo index da tabela de concessionarias: {maxDealershipIndex[0][0]}')
    return maxDealershipIndex[0][0]

# ATUALIZADA O USUARIO
def update_user(username,password):
    db_connection.cursor.execute(f'UPDATE user SET username = "{username}", password = "{password}"')
    db_connection.db.commit()
    print("Dados de usuario atualizados com sucesso!")

# PEGA O INDEX DA PRIMEIRA CSS DO BANCO
def get_min_dealership_index():
    db_connection.cursor.execute('SELECT id FROM dealerships ORDER BY ROWID ASC LIMIT 1')
    minDealershipIndex = db_connection.cursor.fetchall()
    # print(f'Primeiro index da tabela de concessionarias: {minDealershipIndex[0][0]}')
    return minDealershipIndex[0][0]

# COLOCA TODOS OS DADOS COLETADOS DA CSS NO BANCO
def insert_into_data(data):
    db_connection.cursor.executemany('''INSERT INTO xentry_data(css_code, arrival_time, process_number, service_order, FIN) VALUES(?,?,?,?,?)''',data)
    db_connection.db.commit()

# COLOCA TODOS OS ERROS COLETADOS NO BANCO
def insert_into_errors(error):
    errorList = zip(error)
    db_connection.cursor.executemany('INSERT INTO xentry_errors(name) VALUES(?)',errorList)
    db_connection.db.commit()

# DELETA TODOS OS ERROS DO BANCO
def delete_all_errors():
    db_connection.cursor.execute('delete from xentry_errors')
    db_connection.db.commit()
    print('Erros apagados com sucesso!')

# SELECIONA OS ERROS
def select_errors():
    db_connection.cursor.execute('SELECT * from xentry_errors')
    errorList = db_connection.cursor.fetchall()    
    def Extract(lst):
        return [item[0] for item in lst]    

    return Extract(errorList)

# DELETA TODOS OS DADOS DO BANCO
def delete_all():
    db_connection.cursor.execute('delete from xentry_data')
    db_connection.db.commit()
    db_connection.cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'xentry_data'")
    db_connection.db.commit()
    print('Dados apagados com sucesso!')
    
# ATUALIZADA A ULTIMA CSS QUE DEU CERTO
def update_last_dealership(lastDealership):
    db_connection.cursor.execute(f'UPDATE last_dealership SET last_dealership = {lastDealership}')
    db_connection.db.commit()

# SELECIONA A ULTIMA CSS QUE DEU CERTO
def select_last_dealership():
    db_connection.cursor.execute('SELECT * from last_dealership')
    last_dealership = db_connection.cursor.fetchall()
    return last_dealership[0][0]

# RESETA A ULTIMA CSS QUE DEU CERTO
def reset_last_dealership():
    db_connection.cursor.execute('SELECT * from last_dealership')
    last_dealership = db_connection.cursor.fetchall()
    return last_dealership[0][0]

# RESETA A ULTIMA CSS QUE DEU CERTO PARA 0 DENOVO
def reset_last_dealership():
    db_connection.cursor.execute('SELECT id FROM dealerships ORDER BY ROWID ASC LIMIT 1')
    minDealership = db_connection.cursor.fetchall()
    db_connection.cursor.execute(f'UPDATE last_dealership SET last_dealership = {minDealership[0][0]}')
    db_connection.db.commit()
    
try:
    minDealdershipIndex = get_min_dealership_index()
except:
    minDealdershipIndex = 0

maxDealershipIndex = get_max_dealership_index()

def set_index():
    try:
        global minDealdershipIndex
        minDealdershipIndex = get_min_dealership_index()
    except:
        minDealdershipIndex = 0
    global maxDealershipIndex
    maxDealershipIndex = get_max_dealership_index()

def max_sequence_set():
    newMax = get_max_dealership_index()
    db_connection.cursor.execute(f"UPDATE sqlite_sequence SET seq = {newMax} WHERE name = 'dealerships'")
    db_connection.db.commit()

def att_user():
    global dbUsername
    global dbPassword
    dbUsername = get_db_user(0)
    dbPassword = get_db_user(1)
    print(f'Usuario atual: {dbUsername}')

print('Programa desenvolvido por Lucas Lima')
print('LinkedIn: http://www.linkedin.com/in/lucaswmlima')
print('Github: http://www.github.com/LucaswmLima\n')

print('Colaboração de Leonardo Oliveira')
print('https://www.linkedin.com/in/leonardo-raphael\n')

att_user()


# countIndex = 1
# currentDealership = 0
