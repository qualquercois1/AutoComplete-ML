from collections import Counter
import re

def calcular_probabilidade(prefixo):
    #Texto de exemplo como dataset
    texto = """A ciencia da computacao é fantastica. A ciencia de dados tambem é incrivel.
        Eu gosto de programar em python. Eu gosto de programar em c++. 
        Inteligencia artificial vai mudar o mundo. Inteligencia artificial aprende com dados.
        O desenvolvimento de software e a engenharia de software sao pilares da ciencia da computacao.
        Programar em python facilita a analise de dados e a criacao de modelos de inteligencia artificial.
        Programar em c++ garante alta performance e velocidade no desenvolvimento de sistemas robustos e arquiteturas complexas.
        Eu gosto de estudar algoritmos de machine learning e eu gosto de testar novas logicas.
        A ciencia de dados utiliza python para organizar os grandes volumes de dados brutos.
        A inteligencia artificial usa esses dados processados para treinar redes neurais e gerar previsoes.
        Quem trabalha com ciencia da computacao sempre busca programar de forma eficiente.
        Se voce quer aprender a programar, python é uma excelente escolha inicial.
        Se voce busca otimizacao extrema de memoria e hardware, c++ é o caminho ideal.
        Muitos modelos de inteligencia artificial sao escritos inicialmente em python e depois reescritos em c++ para executar de forma mais rapida.
        No fim das contas, a ciencia da computacao une a logica, a matematica e os dados para transformar o mundo."""

    #calculo de A
    #regex para separar as palavras
    palavras = re.findall(r'\w+', texto.lower())
    #dicionario para contar a frequencia das palavras
    palavras = dict(Counter(palavras))

    #calculo de B
    B = [b for b in palavras if b.startswith(palavra_teste)]
    B_tam = len(B)

    probabilidades = {}
    #calculo de n
    total_palavras = sum(palavras.values())

    #calculo de P(B)
    p_prefixo = B_tam / total_palavras if total_palavras > 0 else 0.0

    for palavra, frequencia in palavras.items():
        #calculo de P(A)
        p_palavra = frequencia / total_palavras
        #calculo de P(B|A)
        verossimilhanca = 1.0 if palavra.startswith(palavra_teste) else 0.0
        
        if p_prefixo > 0 and verossimilhanca > 0:
            #calculo de P(A|B)
            probabilidade_final = (verossimilhanca * p_palavra) / p_prefixo
        else:
            probabilidade_final = 0.0

        probabilidades[palavra] = {
            "p_palavra": p_palavra,
            "verossimilhanca": verossimilhanca,
            "p_prefixo": p_prefixo,
            "probabilidade_final": probabilidade_final
        }

    probabilidades_ordenadas = sorted(
        probabilidades.items(), 
        key=lambda x: x[1]["probabilidade_final"], 
        reverse=True
    )
    
    return probabilidades_ordenadas

