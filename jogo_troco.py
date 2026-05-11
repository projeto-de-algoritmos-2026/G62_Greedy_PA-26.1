import pygame
import random
import sys

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

pygame.init()
LARGURA, ALTURA = 1000, 800
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo do Troco")

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA_ESCURO = (100, 100, 100)
CINZA_CLARO = (240, 240, 240)
AZUL = (40, 90, 160)
DOURADO = (255, 215, 0)
DOURADO_ESCURO = (218, 165, 32)
VERDE_ESCURO = (34, 139, 34)
VERMELHO = (220, 20, 60)

FONTE_TITULO = pygame.font.SysFont("monospace", 36, bold=True)
FONTE_PADRAO = pygame.font.SysFont("monospace", 24)
FONTE_PEQUENA = pygame.font.SysFont("monospace", 18)
FONTE_TABELA_CABECALHO = pygame.font.SysFont("monospace", 18, bold=True)
FONTE_TABELA_CONTEUDO = pygame.font.SysFont("monospace", 18)

def desenhar_texto(texto, fonte, cor, x, y):
    superficie = fonte.render(texto, True, cor)
    TELA.blit(superficie, (x, y))

def desenhar_texto_centralizado(texto, fonte, cor, x, y):
    superficie = fonte.render(texto, True, cor)
    retangulo = superficie.get_rect(center=(x, y))
    TELA.blit(superficie, retangulo)

def main():
    rodadas_max = 3
    rodada_atual = 1
    historico = []
    estado = "JOGANDO"
    
    def iniciar_rodada():
        moedas = gerar_sistema_moedas()
        troco_alvo = random.randint(moedas[0], moedas[0] * 5)
        valor_compra = random.randint(50, 500)
        valor_pago = valor_compra + troco_alvo
        selecao = {m: 0 for m in moedas}
        return moedas, troco_alvo, valor_compra, valor_pago, selecao

    moedas, troco_alvo, valor_compra, valor_pago, selecao = iniciar_rodada()
    
    botoes = {}
    btn_confirmar = pygame.Rect(LARGURA // 2 - 300, 500, 600, 60)

    rodando = True
    while rodando:
        TELA.fill(BRANCO)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos = pygame.mouse.get_pos()
                
                if estado == "JOGANDO":
                    for moeda, rects in botoes.items():
                        if rects['mais'].collidepoint(pos):
                            selecao[moeda] += 1
                        if rects['menos'].collidepoint(pos) and selecao[moeda] > 0:
                            selecao[moeda] -= 1
                            
                    if btn_confirmar.collidepoint(pos):
                        valor_jogador = sum(m * q for m, q in selecao.items())
                        moedas_jogador = sum(selecao.values())
                        ideal = algoritmo_guloso(troco_alvo, moedas)
                        
                        historico.append({
                            "rodada": rodada_atual,
                            "compra": valor_compra,
                            "pago": valor_pago,
                            "troco": troco_alvo,
                            "entrega": valor_jogador,
                            "suas_moedas": moedas_jogador,
                            "moedas_ideais": ideal
                        })
                        
                        rodada_atual += 1
                        if rodada_atual > rodadas_max:
                            estado = "RESULTADOS"
                        else:
                            moedas, troco_alvo, valor_compra, valor_pago, selecao = iniciar_rodada()
                            
        if estado == "JOGANDO":
            desenhar_texto(f"RODADA {rodada_atual} / {rodadas_max}", FONTE_TITULO, PRETO, 50, 30)
            desenhar_texto(f"Valor da compra: {valor_compra}", FONTE_PADRAO, PRETO, 50, 90)
            desenhar_texto(f"Valor pago:      {valor_pago}", FONTE_PADRAO, PRETO, 50, 130)
            desenhar_texto(f"Troco alvo:      {troco_alvo}", FONTE_PADRAO, AZUL, 50, 170)
            
            x_instrucoes = 650
            y_instrucoes = 50
            desenhar_texto("INSTRUCOES:", FONTE_PADRAO, PRETO, x_instrucoes, y_instrucoes)
            instrucoes = [
                "1. Observe o troco alvo",
                "   no lado esquerdo.",
                "2. Clique no [+] e [-]",
                "   para escolher as moedas.",
                "3. Use a MENOR quantidade",
                "   possivel de moedas.",
                "4. Clique em CONFIRMAR."
            ]
            for i, inst in enumerate(instrucoes):
                desenhar_texto(inst, FONTE_PEQUENA, CINZA_ESCURO, x_instrucoes, y_instrucoes + 40 + (i * 30))
            
            pygame.draw.rect(TELA, AZUL, btn_confirmar, border_radius=15)
            desenhar_texto_centralizado("CONFIRMAR TROCO", FONTE_TITULO, BRANCO, btn_confirmar.centerx, btn_confirmar.centery)
            
            y_moeda = 650
            espacamento = LARGURA // (len(moedas) + 1)
            botoes.clear()
            
            for i, moeda in enumerate(moedas):
                x_centro = espacamento * (i + 1)
                
                pygame.draw.circle(TELA, DOURADO, (x_centro, y_moeda), 45)
                pygame.draw.circle(TELA, DOURADO_ESCURO, (x_centro, y_moeda), 45, 4)
                desenhar_texto_centralizado(str(moeda), FONTE_PADRAO, PRETO, x_centro, y_moeda)
                
                btn_menos = pygame.Rect(x_centro - 60, y_moeda + 65, 35, 35)
                pygame.draw.rect(TELA, CINZA_ESCURO, btn_menos, border_radius=5)
                desenhar_texto_centralizado("-", FONTE_TITULO, BRANCO, btn_menos.centerx, btn_menos.centery - 2)
                
                texto_qtd = str(selecao[moeda])
                desenhar_texto_centralizado(texto_qtd, FONTE_TITULO, PRETO, x_centro, y_moeda + 82)
                
                btn_mais = pygame.Rect(x_centro + 25, y_moeda + 65, 35, 35)
                pygame.draw.rect(TELA, CINZA_ESCURO, btn_mais, border_radius=5)
                desenhar_texto_centralizado("+", FONTE_TITULO, BRANCO, btn_mais.centerx, btn_mais.centery - 2)
                
                botoes[moeda] = {'menos': btn_menos, 'mais': btn_mais}
                
        elif estado == "RESULTADOS":
            desenhar_texto_centralizado("RELATORIO FINAL DA PARTIDA", FONTE_TITULO, PRETO, LARGURA // 2, 50)
            
            colunas = [
                ("RD", 50),
                ("COMPRA", 120),
                ("PAGO", 240),
                ("TROCO", 340),
                ("ENTREGA", 440),
                ("SUAS MOEDAS", 560),
                ("IDEAL", 720),
                ("STATUS", 820)
            ]
            
            y_cabecalho = 140
            pygame.draw.rect(TELA, AZUL, (30, y_cabecalho - 20, LARGURA - 60, 40), border_radius=5)
            
            for nome, x in colunas:
                desenhar_texto(nome, FONTE_TABELA_CABECALHO, BRANCO, x, y_cabecalho - 10)
            
            y_pos = 190
            pontos_totais = 0
            
            for idx, h in enumerate(historico):
                cor_fundo = CINZA_CLARO if idx % 2 == 0 else BRANCO
                pygame.draw.rect(TELA, cor_fundo, (30, y_pos - 15, LARGURA - 60, 50))
                
                correto = h["entrega"] == h["troco"]
                otimizado = h["suas_moedas"] == h["moedas_ideais"]
                
                status = "ERRO"
                pontos = 0
                cor_status = VERMELHO
                
                if correto and otimizado:
                    status = "PERFEITO"
                    pontos = 100
                    cor_status = VERDE_ESCURO
                elif correto:
                    status = "NAO OTIMO"
                    pontos = 50
                    cor_status = DOURADO_ESCURO
                    
                valores = [
                    (str(h["rodada"]), 50, PRETO),
                    (str(h["compra"]), 120, PRETO),
                    (str(h["pago"]), 240, PRETO),
                    (str(h["troco"]), 340, PRETO),
                    (str(h["entrega"]), 440, PRETO),
                    (str(h["suas_moedas"]), 560, PRETO),
                    (str(h["moedas_ideais"]), 720, PRETO),
                    (status, 820, cor_status)
                ]
                
                for val, x, cor in valores:
                    desenhar_texto(val, FONTE_TABELA_CONTEUDO, cor, x, y_pos)
                
                pontos_totais += pontos
                y_pos += 50
                
            pygame.draw.rect(TELA, CINZA_ESCURO, (30, y_pos + 20, LARGURA - 60, 60), border_radius=5)
            texto_pontuacao = f"PONTUACAO TOTAL: {pontos_totais} / {rodadas_max * 100}"
            desenhar_texto_centralizado(texto_pontuacao, FONTE_TITULO, BRANCO, LARGURA // 2, y_pos + 50)
            
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()