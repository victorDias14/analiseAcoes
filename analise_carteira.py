import requests 
from bs4 import BeautifulSoup

listaAcoes = []

while True:
    acao = input('Informe um código de ação: ')

    if acao != '':
        listaAcoes.append(acao)

    else:
        break

link = 'https://www.fundamentus.com.br/detalhes.php?papel='
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                         '/50.0.2661.102 Safari/537.36'}

while len(listaAcoes) > 0:
    acao = listaAcoes.pop(0)
    url = link + acao
    pagina = requests.get(url, headers=headers)
    codhtml = BeautifulSoup(pagina.content, 'html.parser')

    # CÁLCULO DA MARGEM LÍQUIDA #
    try:
        margLiq = codhtml.find_all('td')[59].get_text()

    except IndexError:
        continue
        
    margLiq = margLiq.strip()

    if margLiq == '-':
        notaMargLiq = 0

    else:
        margLiq = margLiq.strip('%')
        
        if len(margLiq) < 4:
            margLiq = margLiq.replace(',', '.')

        else:
            margLiq = margLiq.replace('.', '')
            margLiq = margLiq.replace(',', '.')

        margLiq = float(str(margLiq))

        if margLiq >= 15:
            notaMargLiq = 10

        elif 0 < margLiq < 15:
            notaMargLiq = 10 / 15 * margLiq

        else:
            notaMargLiq = 0

    # CÁLCULO ROE
    roe = codhtml.find_all('td')[77].get_text()
    roe = roe.strip()

    if roe == '-':
        notaRoe = 0
        
    else:
        roe = roe.strip('%')
        
        if len(roe) < 4:
            roe = roe.replace(',', '.')

        else:
            roe = roe.replace('.', '')
            roe = roe.replace(',', '.')

        roe = float(str(roe))

        if roe >= 15:
            notaRoe = 10

        elif 0 < roe < 15:
            notaRoe = 10 / 15 * roe

        else:
            notaRoe = 0

    # CÁLCULO DIVIDEND YIELD
    dy = codhtml.find_all('td')[75].get_text()
    dy = dy.strip()

    if dy == '-':
        notaDy = 0

    else:
        dy = dy.strip('%')
        
        if len(dy) < 4:
            dy = dy.replace(',', '.')
        
        else:
            dy = dy.replace('.', '')
            dy = dy.replace(',', '.')
            
        dy = float(str(dy))
        
        if dy >= 5:
            notaDy = 10

        elif 0 < dy < 5:
            notaDy = 10 / 5 * dy

        else:
            notaDy = 0

    # CÁLCULO DÍVIDA
    divLiq = codhtml.find_all('td')[104].get_text()
    ebit = codhtml.find_all('td')[119].get_text()
    divLiq = float(str(divLiq.replace('.', '')))
    ebit = float(str(ebit.replace('.', '')))

    if ebit == 0 or ebit == '-':
        notaDivida = 0
        
    else:
        divida = divLiq / ebit

        if divida <= 3:
            notaDivida = 10

        else:
            notaDivida = 10 / divida * 3

    # CÁLCULO LUCRO
    cresc = codhtml.find_all('td')[93].get_text()
    cresc = cresc.strip()

    if cresc == '-':
        notaLucro = 0

    else:
        cresc = cresc.strip('%')
        
        if len(cresc) < 4:
            cresc = cresc.replace(',', '.')
            
        else:
            cresc = cresc.replace('.', '')
            cresc = cresc.replace(',', '.')
            
        cresc = float(str(cresc))

        if cresc > 0:
            notaLucro = 10

        else:
            notaLucro = 0

    # COLETA PREÇO
    preco = str(codhtml.find_all('td')[3].get_text())
    preco = preco.replace(',', '.')

    # COLETA O NÚMERO DO SETOR
    setor = str(codhtml.find_all('a')[17])
    setor = setor[9:31]

    pagina = requests.get('https://www.fundamentus.com.br/' + setor, headers=headers)
    sopa = BeautifulSoup(pagina.content, 'html.parser')

    maiorZero = []
    menorZero = []
    posicao = 20
    
    while True:
        try:
            valor = sopa.find_all('td')[posicao].get_text()
            valor = valor.strip('%')

            if len(valor) > 5:
                valor = valor.replace('.', '')
                valor = valor.replace(',', '.')
                valor = float(str(valor))
            else:
                valor = valor.replace(',', '.')
                valor = float(str(valor))

            posicao += 21
            
            if valor > 0:
                maiorZero.append(valor)
                
            elif valor < 0:
                menorZero.append(valor)
            
            else:
                continue
        
        except IndexError:
            break
        
    if len(maiorZero) > len(menorZero):
        notaSetor = 10
    
    elif len(maiorZero) < len(menorZero):
        notaSetor = 0
        
    else:
        notaSetor = 5

    fatorSetor = 0.5
    fatorLucro = 0.1
    fatorMargLiq = 0.1
    fatorRoe = 0.1
    fatorDy = 0.15
    fatorDivida = 0.05

    notaEmpresa = round(notaSetor * fatorSetor + notaLucro * fatorLucro + notaMargLiq * fatorMargLiq + notaRoe *
                        fatorRoe + notaDy * fatorDy + notaDivida * fatorDivida, 2)
    print(acao)
    notaEmpresa = str(float(notaEmpresa))
    print(notaEmpresa)
