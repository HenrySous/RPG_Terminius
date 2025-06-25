# ==================== TERMINIUS RPG - COMPLETO ====================
import os
import time
import random
import json
import sys
import string
import glob # <--- NEW: Import glob to find files matching a pattern
from colorama import init, Fore, Style
init(autoreset=True)

 

# ==== Funções Utilitárias ====
def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

def titulo_ascii(texto):
    print(Fore.CYAN + "=" * 60) # Changed '()' to '=' for consistent visual
    print(Fore.MAGENTA + f"{texto}")
    print(Fore.CYAN + "=" * 60) # Changed 'daniel' to '=' for consistent visual

def barra(valor, maximo, tamanho=30, cor=Fore.WHITE):
    proporcao = int((valor / maximo) * tamanho)
    proporcao = min(proporcao, tamanho)
    return cor + "[" + "♥" * proporcao + "\u2661" * (tamanho - proporcao) + f"] {valor}/{maximo}" + Style.RESET_ALL

# ==== Criação de Personagem ====
def criar_personagem(nome_sugestao=None): # <--- MODIFIED: Added nome_sugestao
    limpar()
    titulo_ascii("🎭 CRIAÇÃO DE PERSONAGEM 🎭")

    if nome_sugestao:
        nome = nome_sugestao
        print(Fore.YELLOW + f"\nNome do personagem: {nome}")
    else:
        nome = input(Fore.YELLOW + "\nDigite o nome do seu personagem: ")
        # Add a check to ensure character names are unique for save files
        while True:
            save_file_name = f"personagem_{nome.lower().replace(' ', '_')}.sav"
            if os.path.exists(save_file_name):
                print(Fore.RED + f"❌ Já existe um personagem com o nome '{nome}'. Por favor, escolha outro nome.")
                nome = input(Fore.YELLOW + "Digite um nome diferente para o seu personagem: ")
            else:
                break

    classes = ["Guerreiro", "Mago", "Arqueiro", "Programador", "INSERT_A_TITLE", "Dark Mage", "NULL"]
    print("\nEscolha uma classe:")
    for idx, c in enumerate(classes, 1):
        print(f"{idx}. {c}")

    while True:
        escolha = input("\nDigite o número da classe: ")
        if escolha in [str(i) for i in range(1, len(classes)+1)]:
            classe = classes[int(escolha) - 1]
            break
        else:
            print(Fore.RED + "❌ Escolha inválida.")

    personagem = {
        "nome": nome,
        "classe": classe,
        "nivel": 1,
        "vida": 100,
        "vida_max": 100,
        "mana": 50,
        "mana_max": 50,
        "ataque": 10,
        "defesa": 5,
        "habilidades": [],
        "xp": 0,
        "xp_max": 100,
        "pontos": 0,
        "ouro": 100,
        "inventario": ["Poção de Vida", "Poção de Mana"],
        "progresso_historia": 0,
        "missao_concluidas": [],
        "missao": ""
    }

    # Atributos específicos por classe
    if classe == "Guerreiro":
        personagem.update({
            "vida": 120, "vida_max": 120,
            "ataque": 15, "defesa": 10,
            "habilidades": ["Investida"]
        })
    elif classe == "Mago":
        personagem.update({
            "vida": 80, "vida_max": 80,
            "ataque": 20, "defesa": 3,
            "mana": 80, "mana_max": 80,
            "habilidades": ["Bola de Fogo"]
        })
    elif classe == "Arqueiro":
        personagem.update({
            "vida": 100, "vida_max": 100,
            "ataque": 13, "defesa": 7,
            "habilidades": ["Flecha Rápida"]
        })
    elif classe == "Programador":
        personagem.update({
            "vida": 90, "vida_max": 90,
            "mana": 100, "mana_max": 100,
            "ataque": 8, "defesa": 8,
            "habilidades": ["Debugar Inimigo"]
        })
    elif classe == "INSERT_A_TITLE":
        personagem.update({
            "vida": 110, "vida_max": 110,
            "ataque": 14, "defesa": 6,
            "habilidades": ["Ataque Genérico"]
        })
    elif classe == "Dark Mage":
        personagem.update({
            "vida": 70, "vida_max": 70,
            "mana": 120, "mana_max": 120,
            "ataque": 25, "defesa": 2,
            "habilidades": ["Magia Sombria"]
        })
    elif classe == "NULL":
        personagem.update({
            "vida": 1, "vida_max": 1,
            "mana": 999, "mana_max": 999,
            "ataque": 999, "defesa": 0,
            "habilidades": ["Erro Fatal"]
        })

    print(Fore.GREEN + f"\n{nome} o {classe} foi criado com sucesso!")
    time.sleep(2)
    return personagem

# ==== Subir de Nível ====
def subir_nivel(personagem):
    while personagem['xp'] >= personagem['xp_max']:
        personagem['xp'] -= personagem['xp_max']
        personagem['nivel'] += 1
        personagem['pontos'] += 3
        personagem['xp_max'] = 100 * personagem['nivel']
        personagem['vida'] = personagem['vida_max']
        personagem['mana'] = personagem['mana_max']
        print(Fore.YELLOW + f"\n⭐ {personagem['nome']} subiu para o nível {personagem['nivel']}! 3 pontos disponíveis para distribuir!")
        time.sleep(2)

# ==== Distribuir Pontos ====
def distribuir_pontos(personagem):
    while True:
        limpar()
        titulo_ascii("📈 DISTRIBUIR PONTOS 📈")
        print(f"Pontos disponíveis: {personagem['pontos']}")
        print(f"1. Vida ({personagem['vida_max']})")
        print(f"2. Mana ({personagem['mana_max']})")
        print(f"3. Ataque ({personagem['ataque']})")
        print(f"4. Defesa ({personagem['defesa']})")
        print("5. Voltar")

        escolha = input("\nEscolha um atributo para aumentar: ")
        if escolha == "1" and personagem['pontos'] > 0:
            personagem['vida_max'] += 10
            personagem['pontos'] -= 1
        elif escolha == "2" and personagem['pontos'] > 0:
            personagem['mana_max'] += 5
            personagem['pontos'] -= 1
        elif escolha == "3" and personagem['pontos'] > 0:
            personagem['ataque'] += 1
            personagem['pontos'] -= 1
        elif escolha == "4" and personagem['pontos'] > 0:
            personagem['defesa'] += 1
            personagem['pontos'] -= 1
        elif escolha == "5":
            break
        else:
            print(Fore.RED + "\n❌ Opção inválida ou pontos insuficientes.")
            time.sleep(1)

# ==== Missões e História ====
def mostrar_missao(personagem):
    limpar()
    titulo_ascii("📜 MISSÃO ATUAL 📜")
    missao = personagem.get('missao', "Nenhuma missão ativa.")
    print(Fore.CYAN + missao)
    input("\nPressione Enter para voltar ao menu.")

# ==== Menu Principal ====
def menu_principal(personagem):
    while True:
        limpar()
        titulo_ascii("⚔️ TERMINIUS RPG - MENU PRINCIPAL ⚔️")

        print(f"{Fore.GREEN}{personagem['nome']} o {personagem['classe']} - Nv {personagem['nivel']}")
        print(barra(personagem['vida'], personagem['vida_max'], cor=Fore.RED))
        print(barra(personagem['mana'], personagem['mana_max'], cor=Fore.BLUE))
        print(barra(personagem['xp'], personagem['xp_max'], cor=Fore.YELLOW))
        print(f"Ouro: {personagem['ouro']}")

        print("\nEscolha uma opção:")
        print("1. Ver história")
        print("2. Gerenciar habilidades")
        print("3. Iniciar uma batalha")
        print("4. Distribuir pontos")
        print("5. Ver missão atual")
        print("6. Salvar e sair do jogo")
        print("7. Voltar ao menu de seleção de personagem") # <--- NEW: Option to return to character selection

        escolha = input("\nDigite o número da opção: ")

        if escolha == "1":
            avancar_historia(personagem, personagem.get('progresso_historia', 0))
        elif escolha == "2":
            gerenciar_habilidades(personagem)
        elif escolha == "3":
            inimigo = gerar_inimigo()
            batalha(personagem, inimigo)
            subir_nivel(personagem)
        elif escolha == "4":
            distribuir_pontos(personagem)
        elif escolha == "5":
            mostrar_missao(personagem)
        elif escolha == "6":
            salvar_personagem_hex(personagem, f"personagem_{personagem['nome'].lower().replace(' ', '_')}.sav") # <--- MODIFIED
            print(Fore.YELLOW + "\nAté logo, aventureiro!")
            time.sleep(2)
            sys.exit() # <--- NEW: Exit the game entirely
        elif escolha == "7": # <--- NEW: Handle return to character selection
            salvar_personagem_hex(personagem, f"personagem_{personagem['nome'].lower().replace(' ', '_')}.sav")
            print(Fore.YELLOW + "\nRetornando ao menu de seleção...")
            time.sleep(1.5)
            return # Exit menu_principal to go back to main()
        else:
            print(Fore.RED + "\n❌ Opção inválida.")
            time.sleep(1.5)

# ==== Funções de Jogo ====
def navegar_mapa(personagem):
    print(Fore.CYAN + "\nVocê explora uma floresta misteriosa...")
    time.sleep(2)

def gerenciar_habilidades(personagem):
    if personagem["habilidades"]:
        print(Fore.CYAN + "\nSuas habilidades:")
        for hab in personagem["habilidades"]:
            print(f" - {hab}")
    else:
        print(Fore.CYAN + "\nVocê não possui habilidades no momento.")
    time.sleep(2)

def gerar_inimigo():
    inimigos = [
        {"nome": "Goblin", "vida": 30, "vida_max": 30, "ataque": 5, "defesa": 2},
        {"nome": "Esqueleto", "vida": 40, "vida_max": 40, "ataque": 7, "defesa": 3},
        {"nome": "Orc", "vida": 60, "vida_max": 60, "ataque": 10, "defesa": 4},
        {"nome": "Feiticeiro", "vida": 50, "vida_max": 50, "ataque": 12, "defesa": 2},
        {"nome": "Lobos Gigantes", "vida": 30, "vida_max": 30, "ataque": 20, "defesa": 10},
        {"nome": "Slime verde", "vida": 10, "vida_max": 10, "ataque": 5, "defesa": 0},
        {"nome": "Mumia", "vida": 30, "vida_max": 30, "ataque": 12, "defesa": 2},
        {"nome": "Observador", "vida": 50, "vida_max": 50, "ataque": 20, "defesa": 5},
        {"nome": "Mimico", "vida": 30, "vida_max": 30, "ataque": 20, "defesa": 2},
        {"nome": "Bandido", "vida": 50, "vida_max": 50, "ataque": 12, "defesa": 2},
        {"nome": "Aranha Gigante", "vida": 20, "vida_max": 20, "ataque": 10, "defesa": 2},
        {"nome": "Arvore Amaldiçoada", "vida": 50, "vida_max": 50, "ataque": 20, "defesa": 7},
    ]
    return random.choice(inimigos)

def batalha(personagem, inimigo):
    limpar()
    titulo_ascii(f"⚔️ Batalha contra {inimigo['nome']} ⚔️")
    time.sleep(1) # Reduced sleep time
    while personagem['vida'] > 0 and inimigo['vida'] > 0:
        print(f"\n{Fore.GREEN}{personagem['nome']}{Style.RESET_ALL}")
        print(barra(personagem['vida'], personagem['vida_max'], cor=Fore.RED))
        print(barra(personagem['mana'], personagem['mana_max'], cor=Fore.BLUE))
        print(f"==================Vida do {inimigo['nome']}===================")
        print(barra(inimigo['vida'], inimigo['vida_max'], cor=Fore.MAGENTA))
        print("\n1. Atacar\n2. Usar Poção\n3. Fugir\n4. Usar habilidade\n")
        acao = input("Escolha sua ação: ")

        if acao == "1":
            dano_jogador = max(0, personagem['ataque'] + random.randint(-3, 3) - inimigo['defesa'])
            inimigo['vida'] -= dano_jogador
            print(Fore.CYAN + f"\nVocê causou {dano_jogador} de dano!")
        elif acao == "2":
            if "Poção de Vida" in personagem['inventario']:
                personagem['vida'] = min(personagem['vida_max'], personagem['vida'] + 30)
                personagem['inventario'].remove("Poção de Vida")
                print(Fore.GREEN + "\nVocê usou uma Poção de Vida.")
            elif "Poção de Mana" in personagem['inventario']: # Added Mana Potion usage
                personagem['mana'] = min(personagem['mana_max'], personagem['mana'] + 20)
                personagem['inventario'].remove("Poção de Mana")
                print(Fore.GREEN + "\nVocê usou uma Poção de Mana.")
            else:
                print(Fore.RED + "\nVocê não tem poções para usar!")
        elif acao == "3":
            print(Fore.YELLOW + "\nVocê fugiu da batalha!")
            return
        elif acao == "4":
            usar_habilidade(personagem, inimigo)
        else:
            print(Fore.RED + "\nAção inválida.")
            time.sleep(1)
            continue

        time.sleep(1)

        if inimigo['vida'] <= 0:
            xp = random.randint(1,50)
            print(Fore.GREEN + f"\nVocê derrotou o {inimigo['nome']} e ganhou {xp} de XP!")
            time.sleep(3)
            personagem['xp'] += xp
            return

        dano_inimigo = max(0, inimigo['ataque'] + random.randint(-2, 2) - personagem['defesa'])
        personagem['vida'] -= dano_inimigo
        print(Fore.RED + f"\nO {inimigo['nome']} atacou e causou {dano_inimigo} de dano!")
        time.sleep(1)

def usar_habilidade(jogador, inimigo):
    if not jogador["habilidades"]:
        print(Fore.RED + "❌ Você não tem habilidades para usar.")
        return

    # Let the player choose which ability to use
    print(Fore.YELLOW + "\nSuas habilidades disponíveis:")
    for i, hab in enumerate(jogador["habilidades"], 1):
        print(f"{i}. {hab}")

    while True:
        try:
            escolha_hab = int(input(Fore.YELLOW + "Escolha o número da habilidade a usar: "))
            if 1 <= escolha_hab <= len(jogador["habilidades"]):
                habilidade = jogador["habilidades"][escolha_hab - 1]
                break
            else:
                print(Fore.RED + "Escolha inválida.")
        except ValueError:
            print(Fore.RED + "Entrada inválida. Digite um número.")

    mana_custo = 0
    dano = 0

    if habilidade == "Investida":
        dano = jogador["ataque"] + 10
        mana_custo = 0
    elif habilidade == "Bola de Fogo":
        dano = jogador["ataque"] + 20
        mana_custo = 10
    elif habilidade == "Flecha Rápida":
        dano = jogador["ataque"] + 15
        mana_custo = 5
    elif habilidade == "Debugar Inimigo":
        dano = jogador["ataque"] + 25
        mana_custo = 15
    elif habilidade == "Ataque Genérico":
        dano = jogador["ataque"] + 10
        mana_custo = 0
    elif habilidade == "Magia Sombria":
        dano = jogador["ataque"] + 30
        mana_custo = 20
    elif habilidade == "Erro Fatal":
        dano = 999
        mana_custo = 0
    else:
        print(Fore.RED + "Habilidade desconhecida!")
        return

    if jogador['mana'] < mana_custo:
        print(Fore.RED + "Mana insuficiente!")
        return

    jogador['mana'] -= mana_custo
    inimigo['vida'] -= dano
    print(Fore.MAGENTA + f"Você usou {habilidade} causando {dano} de dano!")

# ==== Avançar História ====
def avancar_historia(personagem, progresso):
    limpar()
    titulo_ascii("📖 HISTÓRIA 📖")

    textos = [
        "Você acorda em um mundo estranho, sem memórias...",
        "O vilarejo próximo foi atacado por monstros...",
        "Você encontra um sábio que fala sobre uma antiga relíquia...",
        "Sua missão é recuperar a relíquia e salvar o mundo!",
        "Você parte em sua aventura, enfrentando perigos desconhecidos..."
    ]

    if progresso < len(textos):
        print(Fore.WHITE + textos[progresso])
        personagem['progresso_historia'] = progresso + 1
    else:
        print(Fore.WHITE + "Você já completou toda a história disponível.")

    input("\nPressione Enter para voltar ao menu.")

# ==== Salvar e Carregar Personagem em Hexadecimal ====
def salvar_personagem_hex(personagem, nome_arquivo): # <--- MODIFIED: nome_arquivo now passed as argument
    try:
        json_str = json.dumps(personagem)
        hex_str = json_str.encode().hex()
        with open(nome_arquivo, 'w') as f:
            f.write(hex_str)
        print(Fore.GREEN + f"✅ Dados do personagem salvos em {nome_arquivo} (formato hexadecimal)")
    except Exception as e:
        print(Fore.RED + f"Erro ao salvar personagem: {e}")
    time.sleep(1) # Reduced sleep time

def carregar_personagem_hex(nome_arquivo): # <--- MODIFIED: nome_arquivo now passed as argument
    try:
        with open(nome_arquivo, 'r') as f:
            hex_str = f.read()
        json_str = bytes.fromhex(hex_str).decode()
        personagem = json.loads(json_str)
        print(Fore.GREEN + f"✅ Personagem '{personagem['nome']}' carregado com sucesso!")
        time.sleep(1) # Reduced sleep time
        return personagem
    except Exception as e:
        print(Fore.RED + f"Erro ao carregar personagem de '{nome_arquivo}': {e}")
        return None

def verificar_ou_criar_personagem():
    limpar()
    titulo_ascii("🎮 TERMINIUS RPG - INÍCIO 🎮")

    # Find all existing save files
    # We'll use a pattern like "personagem_*.sav"
    # This assumes save files are named 'personagem_NOME.sav'
    save_files = glob.glob("personagem_*.sav")
    personagem = None

    if save_files:
        print(Fore.CYAN + "Saves de personagem encontrados! Escolha uma opção:\n" + Style.RESET_ALL)
        for i, file_path in enumerate(save_files):
            # Extract just the character name from the filename for display
            char_name = file_path.replace("personagem_", "").replace(".sav", "").replace("_", " ").title()
            print(f"{i + 1}. Carregar: {char_name}")
        print(f"{len(save_files) + 1}. Criar novo personagem")

        while True:
            try:
                escolha = input(Fore.YELLOW + "\nDigite o número da sua escolha: " + Style.RESET_ALL)
                if escolha.isdigit():
                    escolha_int = int(escolha)
                    if 1 <= escolha_int <= len(save_files):
                        selected_file = save_files[escolha_int - 1]
                        print(Fore.CYAN + f"Carregando {selected_file}...\n" + Style.RESET_ALL)
                        personagem = carregar_personagem_hex(selected_file)
                        if personagem:
                            return personagem
                        else:
                            print(Fore.RED + f"Erro ao carregar {selected_file}, por favor tente novamente ou crie um novo." + Style.RESET_ALL)
                            # If loading fails, go back to the selection loop
                            continue
                    elif escolha_int == len(save_files) + 1:
                        return criar_personagem()
                    else:
                        print(Fore.RED + "Escolha inválida. Por favor, digite um número da lista." + Style.RESET_ALL)
                else:
                    print(Fore.RED + "Entrada inválida. Por favor, digite um número." + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "Entrada inválida. Por favor, digite um número." + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "Nenhum save encontrado. Criando novo personagem...\n" + Style.RESET_ALL)
        # Directly create a character if no saves exist
        return criar_personagem()

# ==== Início do Jogo ====
def main():
    while True: # Keep looping until the player chooses to exit the game entirely
        personagem = verificar_ou_criar_personagem()
        if personagem:
            menu_principal(personagem)
        # If menu_principal returns, it means the player chose to go back to character selection
        # Or if character creation/loading failed, we loop back to re-verify/create.

if __name__ == "__main__":
    main()