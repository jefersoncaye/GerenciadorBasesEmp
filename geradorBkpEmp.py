import pyodbc
import time
import zipfile
import shutil
import os
from pathlib import Path

arq = open('dados.txt', 'r')
try:
    for i in arq:
        if 'INSTANCIA:' in i:
                server = i
        if 'LOGIN:' in i:
                usuario = i
        if 'SENHA:' in i:
                senha = i
        try:
            if 'CAMINHOGERA:' in i:
                caminhoBkp = i
            if 'CAMINHOENVIA:' in i:
                pastaTarefa = i
        except:
            caminhoBkp = ''
            pastaTarefa = ''

except:
    raise ValueError('Alguma Variavel não foi encontrada')
arq.close()

server = server[10:].strip()
usuario = usuario[6:].strip()
senha = senha[6:].strip()
caminhoBkp = caminhoBkp[12:].strip()
pastaTarefa = pastaTarefa[13:].strip()

try:
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + 'master' +
                          ';UID=' + usuario + ';PWD=' + senha, autocommit=True)
except:
    raise ValueError('Erro ao conectar no Banco de Dados')


def cursor(cmd):
    cursor = cnxn.cursor()
    cursor.execute(cmd)
    cursor.nextset()
    cursor.close()

nomeBase = input('Nome Banco de Dados: ')

def bancoExiste():
    try:
        cursor = cnxn.cursor()
        cursor.execute(f"select name from sys.databases where name = '{nomeBase}'")
        resultado = cursor.fetchall()
        return resultado
    except: ValueError('Banco de dados não encontrado')

while len(bancoExiste()) == 0:
    nomeBase = input('Banco de Dados Não Encontrado!\nNome Banco de Dados: ')

if len(caminhoBkp) == 0:
    caminhoBkp = input(f'Caminho Backup: {caminhoBkp}')

caminhoBkpBak = caminhoBkp + '\\' + nomeBase + '.BAK'

cursor("BACKUP DATABASE [" + nomeBase + "] TO DISK ='" + caminhoBkpBak + "'WITH INIT")

print(f'Gerando Backup {caminhoBkpBak}, Aguarde!')
time.sleep(5)

print(f'Compactando Arquivo {caminhoBkp}\\{nomeBase}.zip Aguarde!')
zip = zipfile.ZipFile(caminhoBkp + '\\' + nomeBase + '.zip', 'w')
zip.write((caminhoBkp + '\\' + nomeBase + '.BAK'), nomeBase + '.BAK', compress_type=zipfile.ZIP_DEFLATED)
zip.close()
time.sleep(5)
print('Backup Gerado e Compactado!')

# Apaga Backup Criado
os.remove(caminhoBkp + '\\' + nomeBase + '.BAK')


if len(pastaTarefa) == 0:
    pastaTarefa = input(f'Pasta Enviar Backup: {pastaTarefa}')

if Path(pastaTarefa).is_dir():
    shutil.move(caminhoBkp + '\\' + nomeBase + '.zip', pastaTarefa +'\\' + nomeBase + '.zip')
else:
    os.mkdir(pastaTarefa)
    time.sleep(3)
    shutil.move(caminhoBkp + '\\' + nomeBase + '.zip', pastaTarefa + '\\' + nomeBase + '.zip')

print(f'Passando Arquivo para {pastaTarefa}\\{nomeBase}.zip, Aguarde!')
time.sleep(5)
print('Base de Dados: ' + pastaTarefa +'\\' + nomeBase + '.zip')

input('Aperte [Enter] para sair')




