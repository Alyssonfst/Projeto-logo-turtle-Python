import curses


def modo_livre(stdscr):
    stdscr.clear()
    altura, largura = stdscr.getmaxyx() #pega o tamanho máximo da tela
    altura -= 1 #ajuste para que caiba na tela
    largura -= 1

    x = largura // 2 #posição inicial do caractere
    y = altura // 2

    while True:
        try:
            stdscr.addstr(y, x, "#", curses.A_BOLD) # desenha o símbolo na nova posição
        except curses.error: #erro que dá ao passar da borda da tela
            pass

        tecla = stdscr.getch()

        if tecla == curses.KEY_UP:
            y -= 1
        elif tecla == curses.KEY_DOWN:
            y += 1
        elif tecla == curses.KEY_LEFT:
            x -= 1
        elif tecla == curses.KEY_RIGHT:
            x += 1
        elif tecla == 27:  # ESC
            curses.endwin()
            exit()
        elif tecla == ord('q'):
            stdscr.clear()  #limpa a tela
            x = largura // 2  #reinicia a posição do símbolo
            y = altura // 2
            continue #retorna o loop

        if x < 0: #não permite que saia da tela
            x = 0
        elif x >= largura:
            x = largura - 1
        if y < 0:
            y = 0
        elif y >= altura:
            y = altura - 1

def iniciar_jogo(stdscr): #semelhante ao modo livre, inclui a matriz
    stdscr.clear()
    altura, largura = stdscr.getmaxyx()
    altura -= 1
    largura -= 1
    tela = [[' ' for c in range(largura)] for c in range(altura)]
    x = largura // 2
    y = altura // 2

    while True:
        for i in range(altura):
            for j in range(largura):
                stdscr.addstr(i, j, tela[i][j])
        curses.echo()

        if stdscr.getch() == ord('q'): #limpa a tela e reinicia
            tela = [[' ' for c in range(largura)] for c in range(altura)]
            x = largura // 2
            y = altura // 2
            continue

        while True:
            comando = stdscr.getstr(0, 0, 8 ).decode("utf-8") #lê o comando do usuário
            if comando in ["cima", "baixo", "esquerda", "direita"]:
                break
            stdscr.addstr( 2, 0, "Comando inválido. Tente novamente.")
            stdscr.clrtoeol()

        while True:
            try:
                num_movimentos = int(stdscr.getstr(1, 0, 8).decode("utf-8")) #lê o número de vezes que vai andar
                break
            except ValueError:
                stdscr.addstr(y + 2, 0, "Valor inválido. Tente novamente.")
                stdscr.clrtoeol()

        for i in range(num_movimentos): # Move o símbolo de acordo com o comando e o número de movimentos
            tela[y][x] = '*' #atualiza a matriz

            if comando == "cima":
                y -= 1
            elif comando == "baixo":
                y += 1
            elif comando == "esquerda":
                x -= 1
            elif comando == "direita":
                x += 1
            elif comando == 27:  #tecla ESC
                curses.endwin()  #encerra o programa
                exit()
            elif comando == "q":
                tela = [[' ' for c in range(largura)] for c in range(altura)]
                x = largura // 2
                y = altura // 2
                continue

            if x < 0:
                x = 0
            elif x >= largura:
                x = largura - 1
            if y < 0:
                y = 0
            elif y >= altura:
                y = altura - 1

def mostrar_creditos(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Criadores: Vinicius Ferreira e Alysson Fernandes")
    stdscr.addstr(1, 1, "Pressione qualquer tecla para voltar")
    stdscr.getch()

def menu_principal(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Menu Principal")
    stdscr.addstr(2, 0, "1 - Iniciar Jogo")
    stdscr.addstr(3, 0, "2 - Criadores")
    stdscr.addstr(4, 0, "3 - Sair")
    stdscr.addstr(5, 0, "4 - Modo Livre")
    stdscr.refresh()

    while True: #loop de escolha, espera até que uma dessas teclas seja pressionada
        key = stdscr.getch()
        if key == ord('1'):
            curses.wrapper(iniciar_jogo)
        elif key == ord('2'):
            curses.wrapper(mostrar_creditos)
            menu_principal(stdscr)
        elif key == ord('3'):
            curses.endwin()
            exit()
        elif key == ord('4'):
            curses.wrapper(modo_livre)
            break

curses.wrapper(menu_principal)