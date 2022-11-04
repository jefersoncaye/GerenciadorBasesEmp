import pyodbc
import shutil
import os
import time
import lerConexao as lc
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
            if 'CAMINHOBACKUP:' in i:
                caminhoBkp = i
            if 'CAMINHOBANCOS:' in i:
                caminhoBanco = i
            if 'VERSAOBKP:' in i:
                versaoRestaurar = i
        except:
            caminhoBkp = ''
            caminhoBanco = ''
            versaoRestaurar = ''

except:
    raise ValueError('Alguma Variavel não foi encontrada')
arq.close()

server = server[10:].strip()
usuario = usuario[6:].strip()
senha = senha[6:].strip()
caminhoBkp = caminhoBkp[14:].strip()
caminhoBanco = caminhoBanco[14:].strip()
versaoRestaurar = versaoRestaurar[10:].strip()


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


nomeBase = input('Nome da Base: ')
#nomeBase =lc.LerArquivoConexao(nomeBase)

def bancoExiste(base):
    try:
        cursor = cnxn.cursor()
        cursor.execute(f"select name from sys.databases where name = '{base}'")
        resultado = cursor.fetchall()
        return resultado
    except: ValueError('Banco de dados não encontrado')

while len(bancoExiste(nomeBase)) == 0:
    nomeBase = input('Banco de Dados Não Encontrado!\nNome Banco de Dados: ')

nomeBaseHistorico = nomeBase + '_Historico_Dados'

if len(bancoExiste(nomeBaseHistorico)) == 0:
    bancoHistorico = False
    print('Banco de dados Historico_Dados não foi encontrado, o mesmo não será restaurado!')
else: bancoHistorico = True

if len(versaoRestaurar) == 0:
    versaoRestaurar = input('Versão a restaurar: ')

caminhoRestaurar = caminhoBkp + '\\' + versaoRestaurar + '\\' + nomeBase
caminhoRases = caminhoBanco +'\\' + nomeBase
caminhoRestaurarHistorico = caminhoBkp + '\\' + versaoRestaurar + '\\' + nomeBaseHistorico
caminhoRasesHistorico = caminhoBanco +'\\' + nomeBaseHistorico

def transfereArquivos():

    # Arquivos Banco Principal
    if os.path.isfile(caminhoRestaurar + '.mdf') and os.path.isfile(caminhoRases + '.mdf'):
        shutil.copy(caminhoRestaurar + '.mdf', caminhoRases + '.mdf')
        time.sleep(5)
        print(f'Arquivo {caminhoRestaurar}.mdf copiado')
    else:
        print('Não Foi possivel encontrar um dos seguintes arquivos:')
        print(f'{caminhoRestaurar}.mdf')
        print(f'{caminhoRases}.mdf\n')

    if os.path.isfile(caminhoRestaurar + '.ldf') and os.path.isfile(caminhoRases + '.ldf'):
        shutil.copy(caminhoRestaurar + '.ldf', caminhoRases + '.ldf')
        time.sleep(5)
        print(f'Arquivo {caminhoRestaurar}.ldf copiado')
    elif os.path.isfile(caminhoRestaurar + '_Log.ldf') and os.path.isfile(caminhoRases + '_Log.ldf'):
        shutil.copy(caminhoRestaurar + '_Log.ldf', caminhoRases + '_Log.ldf')
        time.sleep(5)
        print(f'Arquivo {caminhoRestaurar}_Log.ldf copiado')
    else:
        print('Não Foi possivel encontrar um dos seguintes arquivos:')
        print(f'{caminhoRestaurar}.ldf')
        print(f'{caminhoRases}.ldf\n')

    # Arquivos Historico_Dados
    if bancoHistorico:
        if os.path.isfile(caminhoRestaurarHistorico + '.mdf')and os.path.isfile(caminhoRasesHistorico + '.mdf'):
            shutil.copy(caminhoRestaurarHistorico + '.mdf', caminhoRasesHistorico + '.mdf')
            time.sleep(5)
            print(f'Arquivo {caminhoRestaurarHistorico}.mdf copiado')
        else:
            print('Não Foi possivel encontrar um dos seguintes arquivos:')
            print(f'{caminhoRestaurarHistorico}.mdf')
            print(f'{caminhoRasesHistorico}.mdf')

        if os.path.isfile(caminhoRestaurarHistorico + '.ldf') and os.path.isfile(caminhoRasesHistorico + '.ldf'):
            shutil.copy(caminhoRestaurarHistorico + '.ldf', caminhoRasesHistorico + '.ldf')
            time.sleep(5)
            print(f'Arquivo {caminhoRestaurarHistorico}.ldf copiado')
        elif os.path.isfile(caminhoRestaurarHistorico + '_Log.ldf') and os.path.isfile(caminhoRasesHistorico + '_Log.ldf'):
            shutil.copy(caminhoRestaurarHistorico + '_Log.ldf', caminhoRasesHistorico + '_Log.ldf')
            time.sleep(5)
            print(f'Arquivo {caminhoRestaurarHistorico}_Log.ldf copiado')
        else:
            print('Não Foi possivel encontrar um dos seguintes arquivos:')
            print(f'{caminhoRestaurarHistorico}.ldf')
            print(f'{caminhoRasesHistorico}.ldf')

try:
    cursor(f'ALTER DATABASE {nomeBase} SET OFFLINE WITH ROLLBACK IMMEDIATE')
except: print(f'Não foi possivel executar o comando para colocar a base {nomeBase} offline')

if bancoHistorico:
    try:
        cursor(f'ALTER DATABASE {nomeBaseHistorico} SET OFFLINE WITH ROLLBACK IMMEDIATE')
    except: print(f'Não foi possivel executar o comando para colocar a base {nomeBaseHistorico} offline')

transfereArquivos()

try:
    cursor(f'ALTER DATABASE {nomeBase} SET ONLINE')
except: print(f'Não foi possivel executar o comando para colocar a base {nomeBase} online')

if bancoHistorico:
    try:
        cursor(f'ALTER DATABASE {nomeBaseHistorico} SET ONLINE')
    except: print(f'Não foi possivel executar o comando para colocar a base {nomeBaseHistorico} online')

input('Aperte [Enter] para sair')