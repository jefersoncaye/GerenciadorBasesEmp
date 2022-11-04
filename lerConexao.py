
def LerArquivoConexao(conexao):
    arqConexao = open('D:\workspace\Empresarial.TC\Testes_Empresarial\conexao.xml', 'r')
    conexao = 'conection_' + conexao
    texto = []
    try:
        for i in arqConexao:
            if conexao in i:
                texto.append(arqConexao.readline())
                texto.append(arqConexao.readline())
        print('Base: ' + texto[1].strip().replace('<bd>', '').replace('</bd>', ''))
        return texto[1].strip().replace('<bd>', '').replace('</bd>', '')

    except:
        raise ValueError('Erro ao Ler arquivo')
    arqConexao.close()
