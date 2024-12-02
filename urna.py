import pickle  # Importa o módulo pickle para serializar e desserializar objetos (como votos)
import matplotlib.pyplot as plt  # Importa o módulo de gráficos matplotlib para exibir gráficos de barras
import sys  # Importa o módulo sys, usado para terminar o programa

def menu():
    print("1 - Ler arquivo de candidatos")  # Exibe a opção 1 no menu
    print("2 - Ler arquivo de eleitores")  # Exibe a opção 2 no menu
    print("3 - Iniciar votação")  # Exibe a opção 3 no menu
    print("4 - Apurar votos")  # Exibe a opção 4 no menu
    print("5 - Mostrar resultados")  # Exibe a opção 5 no menu
    print("6 - Fechar programa")  # Exibe a opção 6 no menu
    return int(input("Escolha uma opção: "))  # Solicita que o usuário escolha uma opção e a retorna como inteiro

def ler_candidatos():
    candidatos = []  # Lista onde os candidatos serão armazenados
    arquivo = input("Informe o arquivo de candidatos: ")  # Solicita o nome do arquivo de candidatos
    try:
        with open(arquivo, "r") as arq:  # Tenta abrir o arquivo em modo de leitura
            linhas = arq.readlines()  # Lê todas as linhas do arquivo
        for linha in linhas:
            dados = linha.strip().split(", ")  # Divide cada linha em dados com base na vírgula
            if len(dados) != 5:  # Verifica se há exatamente 5 dados por linha
                print(f"Formato inválido na linha: {linha}. Ignorando...")  # Se não houver, avisa que o formato é inválido
                continue  # Pula para a próxima linha

            nome = dados[0]  # Nome do candidato
            try:
                numero = int(dados[1])  # Tenta converter o número do candidato para inteiro
            except ValueError:
                print(f"Erro ao converter número do candidato: {dados[1]}. Linha ignorada.")  # Se falhar, avisa
                continue  # Pula para a próxima linha

            partido = dados[2]  # Partido do candidato
            estado = dados[3]  # Estado do candidato
            cargo = dados[4]  # Cargo do candidato

            candidatos.append({
                "nome": nome,
                "numero": numero,
                "partido": partido,
                "estado": estado,
                "cargo": cargo
            })  # Adiciona o candidato à lista

        print(f"{len(candidatos)} candidatos carregados com sucesso!")  # Informa o número de candidatos carregados
    except FileNotFoundError:
        print(f"Arquivo {arquivo} não encontrado.")  # Se o arquivo não for encontrado, avisa
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")  # Caso ocorra outro erro, exibe o erro

    return candidatos  # Retorna a lista de candidatos

def ler_eleitores():
    eleitores = []  # Lista onde os eleitores serão armazenados
    arquivo = input("Informe o arquivo de eleitores: ")  # Solicita o nome do arquivo de eleitores
    with open(arquivo, "r") as arq:  # Abre o arquivo em modo de leitura
        linhas = arq.readlines()  # Lê todas as linhas do arquivo
    for linha in linhas:
        dados = linha.strip().split(", ")  # Divide cada linha em dados
        eleitores.append({
            "nome": dados[0],  # Nome do eleitor
            "rg": dados[1],  # RG do eleitor
            "titulo": int(dados[2]),  # Título de eleitor (converte para inteiro)
            "cidade": dados[3],  # Cidade do eleitor
            "estado": dados[4]  # Estado do eleitor
        })
    return eleitores  # Retorna a lista de eleitores

def encontrar_eleitor(eleitores, titulo):
    for eleitor in eleitores:
        if eleitor["titulo"] == titulo:  # Procura o eleitor pelo número do título
            return eleitor  # Retorna o eleitor encontrado
    return None  # Retorna None se o eleitor não for encontrado

def coletar_voto(candidatos, eleitor, estado_urna):
    voto = {"UF": estado_urna}  # Inicializa o voto com o estado da urna
    cargos = ["F", "E", "S", "G", "P"]  # Define os cargos disponíveis (Federal, Estadual, Senador, Governador, Presidente)
    nomes_cargos = ["Deputado Federal", "Deputado Estadual", "Senador", "Governador", "Presidente"]  # Nomes dos cargos

    for i, cargo in enumerate(cargos):  # Itera sobre os cargos
        while True:  # Laço para repetir até o voto ser válido
            print(f"Informe o voto para {nomes_cargos[i]}: ", end="")  # Solicita o voto para o cargo
            numero = input().strip().upper()  # Lê o número do voto

            if numero == "B":  # Verifica se o voto foi em branco
                confirmacao = input("Confirma voto em branco (S ou N)? ").strip().upper()  # Confirma o voto em branco
                if confirmacao == "S":
                    voto[cargo] = "B"  # Marca o voto como branco
                    break  # Sai do loop
                else:
                    print("Voto em branco não confirmado. Tente novamente.")  # Se não confirmar, tenta novamente
                    continue

            if numero.isdigit():  # Se a entrada for um número
                numero = int(numero)  # Converte para inteiro
            else:
                print("Entrada inválida. Digite um número ou 'B' para votar em branco.")  # Se não for número, avisa
                continue

            if cargo != "P":  # Para todos os cargos, exceto presidente, verifica o estado do candidato
                candidato = next((c for c in candidatos if c["numero"] == numero and c["estado"] == eleitor["estado"] and c["cargo"] == cargo), None)
            else:
                candidato = next((c for c in candidatos if c["numero"] == numero and c["cargo"] == cargo), None)  # Para presidente, não importa o estado

            if candidato:  # Se o candidato for encontrado
                print(f"Candidato {candidato['nome']} | {candidato['partido']}")  # Exibe o nome e o partido do candidato
                confirmacao = input("Confirma (S ou N)? ").strip().upper()  # Confirma o voto
                if confirmacao == "S":
                    voto[cargo] = candidato["numero"]  # Registra o número do candidato
                    break  # Sai do loop
                else:
                    print("Voto não confirmado. Tente novamente.")  # Se não confirmar, tenta novamente
            else:
                print("Candidato não encontrado!")  # Se o candidato não for encontrado
                confirmacao = input("Digite 'N' para voto nulo, 'B' para branco ou qualquer outra tecla para tentar novamente: ").strip().upper()  # Opções para voto nulo ou branco
                if confirmacao == "N":
                    voto[cargo] = "N"  # Marca como nulo
                    break  # Sai do loop
                elif confirmacao == "B":
                    voto[cargo] = "B"  # Marca como branco
                    break  # Sai do loop
                else:
                    print("Tentando novamente...")  # Tenta novamente

    return voto  # Retorna o voto registrado

def salvar_voto(voto, arquivo_votos="votos.bin"):
    with open(arquivo_votos, "ab") as arq:  # Abre o arquivo de votos em modo de append binário
        pickle.dump(voto, arq)  # Serializa o voto e salva no arquivo

def apurar_votos(arquivo_votos, candidatos):
    votos_por_candidato = {"F": {}, "E": {}, "S": {}, "G": {}, "P": {}}  # Dicionário para armazenar votos por cargo
    total_votos = {"F": 0, "E": 0, "S": 0, "G": 0, "P": 0}  # Dicionário para contar o total de votos por cargo
    brancos = 0  # Contador de votos brancos
    nulos = 0  # Contador de votos nulos

    with open(arquivo_votos, "rb") as arq:  # Abre o arquivo de votos em modo de leitura binária
        while True:
            try:
                voto = pickle.load(arq)  # Deserializa e lê um voto
                for cargo, numero in voto.items():  # Itera sobre os cargos do voto
                    if cargo == "UF":  # Ignora o campo "UF"
                        continue
                    if numero == "B":
                        brancos += 1  # Conta votos brancos
                    elif numero == "N":
                        nulos += 1  # Conta votos nulos
                    else:
                        # Organiza votos por cargo
                        if numero not in votos_por_candidato[cargo]:
                            votos_por_candidato[cargo][numero] = 0  # Se o candidato ainda não recebeu votos, inicializa com 0
                        votos_por_candidato[cargo][numero] += 1  # Incrementa o número de votos para o candidato
                        total_votos[cargo] += 1  # Incrementa o total de votos para o cargo
            except EOFError:
                break  # Sai do loop quando todos os votos forem lidos (fim do arquivo)

    # Exibindo resultados por cargo
    for cargo in votos_por_candidato:
        print(f"\nResultado para {cargo}:")  # Exibe o cargo para o qual está mostrando os resultados
        for candidato in candidatos:
            if candidato["numero"] in votos_por_candidato[cargo]:  # Se o candidato recebeu votos para esse cargo
                votos = votos_por_candidato[cargo][candidato["numero"]]  # Obtém o número de votos
                porcentagem = (votos / total_votos[cargo]) * 100 if total_votos[cargo] > 0 else 0  # Calcula a porcentagem de votos
                print(f"Candidato: {candidato['nome']} | Cargo: {candidato['cargo']} | Estado: {candidato['estado']} | Votos: {votos} ({porcentagem:.2f}%)")
    
    # Exibe o total de votos, votos brancos e nulos
    print(f"\nTotal de Votos: {sum(total_votos.values())}")
    print(f"Brancos: {brancos}")
    print(f"Nulos: {nulos}")

    # Gerar gráfico para cada cargo
    for cargo in votos_por_candidato:
        gera_grafico(cargo, votos_por_candidato[cargo], candidatos)  # Chama a função que gera o gráfico para o cargo

def gera_grafico(cargo, votos, candidatos):
    # Cria um gráfico de barras para o cargo específico
    nomes_candidatos = [candidato['nome'] for candidato in candidatos if candidato['numero'] in votos]  # Filtra os candidatos que receberam votos
    qtd_votos = [votos[candidato['numero']] for candidato in candidatos if candidato['numero'] in votos]  # Obtém a quantidade de votos

    # Criação e configuração do gráfico
    plt.figure(figsize=(12, 8))  # Aumenta o tamanho do gráfico
    bars = plt.bar(nomes_candidatos, qtd_votos, color='skyblue', edgecolor='black')  # Cria as barras verticais com bordas pretas

    # Adiciona os valores de votos sobre as barras
    for bar in bars:
        yval = bar.get_height()  # Pega a altura da barra (que é o número de votos)
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 1,  # Coloca o texto um pouco acima da barra
                 str(yval), ha='center', va='bottom', fontsize=10, color='black')

    # Personaliza o gráfico com título, rótulos e eixos
    plt.title(f'Votos para {cargo}', fontsize=16)
    plt.xlabel('Candidatos', fontsize=14)
    plt.ylabel('Quantidade de Votos', fontsize=14)

    # Ajusta os nomes dos candidatos no eixo X para que não se sobreponham
    plt.xticks(rotation=45, ha="right")  # Rotaciona os nomes dos candidatos para a direita

    # Adiciona a porcentagem nos eixos Y
    total_votos = sum(qtd_votos)  # Total de votos para o cargo
    if total_votos > 0:
        for i, voto in enumerate(qtd_votos):
            porcentagem = (voto / total_votos) * 100  # Calcula a porcentagem
            plt.text(i, qtd_votos[i] + 0.5, f'{porcentagem:.2f}%', ha='center', va='bottom', fontsize=10)  # Coloca a porcentagem acima da barra

    plt.tight_layout()  # Ajusta o layout para garantir que tudo caiba bem
    plt.show()  # Exibe o gráfico

def main():
    candidatos = []  # Lista de candidatos
    eleitores = []  # Lista de eleitores
    arquivo_votos = "votos.bin"  # Nome do arquivo onde os votos serão armazenados
    votacao_iniciada = False  # Flag para verificar se a votação foi iniciada

    while True:
        opcao = menu()  # Exibe o menu e obtém a opção do usuário

        if opcao == 1:
            # Ler arquivo de candidatos
            candidatos = ler_candidatos()  # Chama a função para ler os candidatos
            print(f"{len(candidatos)} candidatos carregados com sucesso!")  # Informa quantos candidatos foram carregados

        elif opcao == 2:
            # Ler arquivo de eleitores
            eleitores = ler_eleitores()  # Chama a função para ler os eleitores
            print(f"{len(eleitores)} eleitores carregados com sucesso!")  # Informa quantos eleitores foram carregados

        elif opcao == 3:
            # Iniciar votação
            if not candidatos or not eleitores:
                print("Erro: Você precisa carregar os arquivos de candidatos e eleitores antes de iniciar a votação!")  # Verifica se os arquivos foram carregados
            else:
                estado_urna = input("Informe a UF onde a urna está localizada: ").strip().upper()  # Solicita o estado da urna
                while True:
                    titulo = input("\nInforme o Título de Eleitor: ")  # Solicita o título de eleitor
                    eleitor = encontrar_eleitor(eleitores, int(titulo))  # Busca o eleitor pelo título

                    if not eleitor:
                        print("Título de eleitor não encontrado! Tente novamente.")  # Se o eleitor não for encontrado
                        continue

                    print(f"Eleitor: {eleitor['nome']}")  # Exibe o nome do eleitor
                    print(f"Estado: {eleitor['estado']}")  # Exibe o estado do eleitor

                    voto = coletar_voto(candidatos, eleitor, estado_urna)  # Coleta o voto do eleitor
                    salvar_voto(voto, arquivo_votos)  # Salva o voto no arquivo
                    print("Voto registrado com sucesso!")  # Confirma o registro do voto

                    votacao_iniciada = True  # Marca que a votação foi iniciada
                    continuar = input("\nRegistrar outro voto? (S ou N): ").strip().upper()  # Pergunta se deve continuar
                    if continuar == "N":
                        break  # Sai do loop caso o usuário não queira continuar

        elif opcao == 4:
            # Apurar votos
            if not votacao_iniciada:
                print("Erro: A votação ainda não foi iniciada! Inicie a votação antes de apurar os votos.")  # Verifica se a votação foi iniciada
            elif not candidatos:
                print("Erro: Arquivo de candidatos deve ser carregado antes de apurar os votos!")  # Verifica se os candidatos foram carregados
            else:
                print("Apurando votos...")  # Inicia o processo de apuração
                apurar_votos(arquivo_votos, candidatos)  # Chama a função para apurar os votos

        elif opcao == 5:
            # Mostrar resultados
            if not votacao_iniciada:
                print("Erro: A votação ainda não foi iniciada! Inicie a votação antes de mostrar os resultados.")  # Verifica se a votação foi iniciada
            elif not candidatos:
                print("Erro: Arquivo de candidatos deve ser carregado antes de mostrar os resultados!")  # Verifica se os candidatos foram carregados
            else:
                print("Mostrando resultados...")  # Inicia a exibição dos resultados
                apurar_votos(arquivo_votos, candidatos)  # Chama a função para apurar e exibir os resultados

        elif opcao == 6:
            # Fechar programa
            print("Encerrando o programa...")  # Exibe mensagem de encerramento
            sys.exit()  # Encerra o programa

        else:
            print("Opção inválida! Tente novamente.")  # Exibe mensagem caso a opção escolhida seja inválida

# Chamada da função principal
if __name__ == "__main__":
    main()  # Inicia a execução do programa
