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

    #regex para separar as palavras
    palavras = re.findall(r'\w+', texto.lower())
    #dicionario para contar a frequencia das palavras
    palavras = dict(Counter(palavras))

    probabilidades = {}

    total_palavras = sum(palavras.values())

    for palavra, frequencia in palavras.items():
        probabilidades[palavra] = {
            "p_palavra" : frequencia / total_palavras,
            "verossimilhanca" : palavra.startswith(prefixo)
        }
        #ordena as palavras pela probabilidade
    probabilidades_ordenadas = sorted(probabilidades.items(), key=lambda x: x[1]["p_palavra"], reverse=True)
    
    return probabilidades_ordenadas

calcular_probabilidade("c")