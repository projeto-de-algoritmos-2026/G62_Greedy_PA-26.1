import random

def gerar_sistema_moedas():
    moedas = [1] 
    for _ in range(3): 
        multiplicador = random.randint(2, 4)
        nova_moeda = moedas[-1] * multiplicador
        moedas.append(nova_moeda)
    return sorted(moedas, reverse=True)

def algoritmo_guloso(alvo, moedas_desc):
    qtd_total = 0
    distribuicao = {}
    
    for moeda in moedas_desc:
        qtd_moedas = alvo // moeda
        if qtd_moedas > 0:
            distribuicao[moeda] = qtd_moedas
            qtd_total += qtd_moedas
            alvo %= moeda
            
    return qtd_total, distribuicao

def jogar():
    print("=" * 40)
    print("JOGO DO ALGORITMO GULOSO (TROCO)")
    print("=" * 40)
    print("Objetivo: Entregar o troco exato usando a MENOR quantidade de moedas possível.\n")
    
    rodadas = 3
    resultados = []
    
    for r in range(1, rodadas + 1):
        print(f"--- RODADA {r} ---")
        moedas = gerar_sistema_moedas()
        moedas_asc = sorted(moedas)
        
        
        alvo = random.randint(moedas[0], moedas[0] * 4)
        
        print(f"Moedas disponíveis nesta rodada: {moedas_asc}")
        print(f"Troco Alvo: {alvo}\n")
        
        
        qtd_ideal, _ = algoritmo_guloso(alvo, moedas)
        
        
        total_valor_jogador = 0
        total_moedas_jogador = 0
        
        print("Quantas moedas de cada valor você vai usar?")
        for moeda in moedas:
            while True:
                try:
                    qtd = int(input(f" -> Moedas de {moeda}: "))
                    if qtd < 0:
                        print("    Por favor, insira um valor positivo.")
                        continue
                    total_valor_jogador += (qtd * moeda)
                    total_moedas_jogador += qtd
                    break
                except ValueError:
                    print("    Entrada inválida. Digite um número inteiro.")
        
        
        valido = (total_valor_jogador == alvo)
        if not valido:
            print(f"\nERROU O VALOR! Você entregou {total_valor_jogador}, mas o troco era {alvo}.")
            pontos = 0
        else:
            if total_moedas_jogador == qtd_ideal:
                print(f"\nPERFEITO! Você usou a quantidade mínima ({qtd_ideal} moedas).")
                pontos = 100
            else:
                print(f"\nVALOR CORRETO, MAS NÃO OTIMIZADO. Você usou {total_moedas_jogador} moedas. O ideal era {qtd_ideal}.")
                pontos = 50
                
        resultados.append({
            'rodada': r,
            'alvo': alvo,
            'valido': valido,
            'suas_moedas': total_moedas_jogador,
            'moedas_ideais': qtd_ideal,
            'pontos': pontos
        })
        print("-" * 40 + "\n")
        
    
    print("=" * 40)
    print("RESULTADO FINAL")
    print("=" * 40)
    
    pontuacao_total = 0
    for res in resultados:
        status = "Correto" if res['valido'] else "Incorreto"
        print(f"Rodada {res['rodada']} | Alvo: {res['alvo']:3} | Status: {status:9} | Suas Moedas: {res['suas_moedas']:2} | Ideais: {res['moedas_ideais']:2} | Pontos: {res['pontos']}")
        pontuacao_total += res['pontos']
        
    print("-" * 40)
    print(f"Pontuação Total: {pontuacao_total} / {rodadas * 100}")

if __name__ == "__main__":
    jogar()