import random

def gerar_sistema_moedas():
    moedas = [1]
    for _ in range(5):
        multiplicador = random.randint(2, 5)
        nova_moeda = moedas[-1] * multiplicador
        moedas.append(nova_moeda)
    return sorted(moedas, reverse=True)

def algoritmo_guloso(alvo, moedas_desc):
    qtd_total = 0
    for moeda in moedas_desc:
        qtd_moedas = alvo // moeda
        qtd_total += qtd_moedas
        alvo %= moeda
    return qtd_total

def jogar():
    rodadas = 3
    historico = []
    
    for r in range(1, rodadas + 1):
        moedas = gerar_sistema_moedas()
        troco_alvo = random.randint(moedas[0], moedas[0] * 5)
        valor_compra = random.randint(50, 500)
        valor_pago = valor_compra + troco_alvo
        
        print(f"RODADA {r}")
        print(f"Valor da compra: {valor_compra}")
        print(f"Valor pago: {valor_pago}")
        print(f"Troco a ser devolvido: {troco_alvo}")
        print(f"Moedas disponiveis: {sorted(moedas)}")
        print("Digite a quantidade de moedas para devolver o troco.")
        
        valor_jogador = 0
        moedas_jogador = 0
        
        for moeda in moedas:
            while True:
                try:
                    texto = f"Quantidade de moedas de {moeda}: "
                    qtd = int(input(texto))
                    if qtd >= 0:
                        valor_jogador += (qtd * moeda)
                        moedas_jogador += qtd
                        break
                except ValueError:
                    pass
        
        ideal = algoritmo_guloso(troco_alvo, moedas)
        
        historico.append({
            "rodada": r,
            "compra": valor_compra,
            "pago": valor_pago,
            "troco": troco_alvo,
            "entrega": valor_jogador,
            "suas_moedas": moedas_jogador,
            "moedas_ideais": ideal
        })
        print("\n" + "-"*40 + "\n")

    print("RESULTADOS FINAIS")
    print(f"{'RD':<4} | {'COMPRA':<7} | {'PAGO':<7} | {'TROCO':<7} | {'SOMA':<7} | {'SUAS':<5} | {'IDEAL':<5} | {'STATUS'}")
    
    pontos_totais = 0
    for h in historico:
        correto = h["entrega"] == h["troco"]
        otimizado = h["suas_moedas"] == h["moedas_ideais"]
        
        status = "ERRO TOTAL"
        pontos = 0
        
        if correto and otimizado:
            status = "PERFEITO"
            pontos = 100
        elif correto:
            status = "NAO OTIMO"
            pontos = 50
            
        print(f"{h['rodada']:<4} | {h['compra']:<7} | {h['pago']:<7} | {h['troco']:<7} | {h['entrega']:<7} | {h['suas_moedas']:<5} | {h['moedas_ideais']:<5} | {status}")
        pontos_totais += pontos
        
    print("-" * 75)
    print(f"PONTUACAO FINAL: {pontos_totais}")

if __name__ == "__main__":
    jogar()