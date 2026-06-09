import csv
import os
from tabulate import tabulate
import pygame
from getpass import getpass

#definição de variaveis globais
admin = "0"
currentUser = ""
#variaveis para direitos editoriais
dicRights = {}
totalAlbuns = int()
totalSoldUnits = int()
totalIncome = float()
totalRights = float()
#Log
logs = []
auxLogs = []
#---------------------- Funcões Auxiliares -------------------------------------------------

#Limpar consola
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

#------------------------------- Ler dados bd --------------------------------------------------------------------

def fetchData(bd):
    bd += ".csv"
    myFile = open(bd, "r", encoding="utf-8")
    dados = csv.reader(myFile, delimiter=";")
    # ------------ Converter dados para dicionarios ---------------------------
    if bd == "autores.csv":
        global dicAuthors
        dicAuthors = {}
        for item in dados:
            dicAuthors[item[0]] = item[1:]
        #Ordenar alfaticamente por keys
        dicAuthors = dict(sorted(dicAuthors.items()))
    elif bd == "albuns.csv":
        global dicAlbuns
        dicAlbuns = {}
        for item in dados:
            dicAlbuns[item[0]] = item[1:]
        #Ordenar alfaticamente por Autores
        dicAlbuns = dict(sorted(dicAlbuns.items() , key=lambda item: item[1][0]))
    elif bd == "musicas.csv":
        global dicMusics
        dicMusics = {}
        for item in dados:
            dicMusics[item[0]] = item[1:]
        #Ordenar alfaticamente por Autores
        dicMusics = dict(sorted(dicMusics.items() , key=lambda item: item[1][0]))
    elif bd == "users.csv":
        global dicUsers
        dicUsers = {}
        for item in dados:
            dicUsers[item[0]] = item[1]
    
    myFile.close()
    #return dados

# ---------------------------------------------------------------------------------------------------------------

def updateFiles(bd):
    file = open(bd , "w", newline="",encoding="utf-8")
    #No meu pc o delimiter é o ';', mudar para ',' caso necessário
    writer = csv.writer(file , delimiter=";")

    match bd:
        case "autores.csv":
            for band, data in dicAuthors.items():
                writer.writerow([band] + data)
        case "albuns.csv":
            for album, data in dicAlbuns.items():
                writer.writerow([album] + data)
        case "musicas.csv":
            for album, data in dicMusics.items():
                writer.writerow([album] + data)
        case _:
            input("⚠️ Erro ao atualizar os dados! Pressionar Enter para continuar...")

    file.close()

#--------------------- Login ------------------------------------------------------------------------------------

def login ():
    global admin
    global currentUser
    
    if admin == "0":
        
        user = input("Introduza o nome de utilizador: ")
        password = getpass("Introduza a password: ")
        for item in dicUsers.items():
            if user == item[0] and password == item[1]:
                admin = "1"
                currentUser = user
                print("\n")
                input("⚠️ Login Efetuado! Pressionar Enter para continuar...")
            else:
                print("\n")
                input("⚠️ Nome de utilizador ou password incorretos! Pressionar Enter para continuar...")
    #Logout
    elif admin == "1":
        admin = "0"
        currentUser = ""
        print("\n")
        input("⚠️ Logout Efetuado! Pressionar Enter para continuar...")

# ---------------------------------------------------------------------------------------------------------------
# -------------------------------- Fim Funções Auxiliares -------------------------------------------------------

# ------------------------------- Func Opcao 1 - Listagem ------------------------------------------------------------------------------

#--------------------------------- Listar Autores ---------------------------------------------------------------
def listAuthors():
    
    #------------------- Mostrar tabela de autores ---------------------------------------
    rows = []
    for key, values in dicAuthors.items():
        if admin == "1":
            rows.append([key] + [values[0],values[1],float(values[2]) * 100])
        elif admin == "0":
            #Esconder Direitos Editoriais para users não logados
            rows.append([key] + values[:-1])   
    headers = ["Nome", "Nacionalidade", "Álbuns", "% Direitos Editoriais"] if admin=="1" else ["Nome", "Nacionalidade", "Álbuns"]
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    print("\n")
    
    # ------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------

#--------------------------------- Listar Albuns ---------------------------------------------------------------

def listAlbuns():
    
    print("\n")
    author = input("Introduza o nome do Autor: ")
    
    #Colocar 1a letra de cada palavra maiuscula
    
    author = author.title()
    
    cls()
    
    print("\n--- Listagem de Albuns ---\n")
    
    rows = []
    for key , values in dicAlbuns.items():
        if values[0] == author:
            rows.append([key] + values)
    if rows:
        headers = ["Nome Album","Nome Banda","Género","Ano Lançamento","Unidades Vendidas", "Preço"]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        print("\n")
    else:
        print("\nNão foi encontrado nenhum registo com os dados inseridos!\n")
    
# ---------------------------------------------------------------------------------------------------------------

#--------------------------------- Listar Musicas ---------------------------------------------------------------

def listMusics():
    
    print("\n")
    album = input("Introduza o nome do Album: ")
    
    #Colocar 1a letra de cada palavra maiuscula
    album = album.title()
    
    #Limpar consola
    
    cls()
    
    # Listar Musicas
    print("\n--- Listagem de Musicas ---\n")
    rows = []
    for key, values in dicMusics.items():
        if key == album:
            header = f"{values[0]} — {key}"
            musics = "\n".join(values[1:])
            rows = [[musics]]
    if rows:
        print(tabulate(rows, headers=[header], tablefmt="grid"))
        print("\n")
    else:
        print("\nNão foi encontrado nenhum registo com os dados inseridos!\n")
    
# ---------------------------------------------------------------------------------------------------------------

# ------------------------------- Fim Func Opcao 1 - Listagem ------------------------------------------------------------------------------         

# ------------------------------- Func Opcao 2 - Admin -------------------------------------------------------------------------------------

# ----------------------------- Consultar Direitos ----------------------------------

def viewRights():
    
    global dicRights
    
    global totalAlbuns
    global totalSoldUnits
    global totalIncome
    global totalRights
    
    totalAlbuns = 0
    totalSoldUnits = 0
    totalIncome = 0
    totalRights = 0
    
    #Buscar dados necessários relativos a cada Autor
    for key , values in dicAuthors.items():
        author = key
        authorAlbuns = int(values[1])
        percentage = float(values[2])
        soldUnits = int()
        authorIncome = float()
        #Buscar dados necessários relativos aos albuns deste Autor
        for item in dicAlbuns.items():
            if item[1][0] == author:
                authorIncome += float(item[1][3]) * float(item[1][4])
                soldUnits += int(item[1][3])
        authorRights = authorIncome * percentage
        
        #Calcular Totais
        totalAlbuns += authorAlbuns
        totalSoldUnits += soldUnits
        totalIncome += authorIncome
        totalRights += authorRights
        #Criar Registo de autor no dicionário
        dicRights[author] = [percentage * 100 , authorAlbuns, soldUnits, authorIncome, authorRights]
        
    #----------------- Print da tabela tabulada com os totais ---------------
    rows = []
    for key , values in dicRights.items():
        rows.append([key] + values)
    rows.append([""] + ["",totalAlbuns,totalSoldUnits,totalIncome,totalRights])
    headers = ["1.Autor","2.% Direitos","3.Nº Álbuns","4.Unid. Vendidas","5.Receita (€)","6.Direitos (€)"]
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    print("\n")
    #-------------------------------------------------------------------------

# ----------------------- Fim Consultar Direitos -------------------------------------------
  
# ----------------------- Ordenar Direitos Editoriais -------------------------------------        
def orderRights():
    
        global dicRights
        
        sortType = (input("Introduza o numero da coluna que pretende ordenar (1,2,3,4,5,6): "),input("Qual a ordem que pretende ('1' - 'crescente' ou 2 - 'decrescente') ?"))
        match sortType[0]:
            case "1":
                #Ordenar por Autores
                if sortType[1] == "1":
                    dicRights = dict(sorted(dicRights.items()))
                elif sortType[1] == "2":
                    dicRights = dict(sorted(dicRights.items() , reverse=True))
            case "2":
                #Ordenar por % Direitos
                if sortType[1] == "1":
                    dicRights = dict(sorted(dicRights.items() , key=lambda item: float(item[1][0])))
                elif sortType[1] == "2":
                    dicRights = dict(sorted(dicRights.items() , key=lambda item: float(item[1][0]) , reverse=True))
            case "3":
                #Ordenar por Nº de Albuns
                if sortType[1] == "1":
                    dicRights = dict(sorted(dicRights.items(), key=lambda item: int(item[1][1])))
                elif sortType[1] == "2":
                    dicRights = dict(sorted(dicRights.items() , key=lambda item: int(item[1][1]) , reverse=True))
            case "4":
                #Ordenar por Unidades Vendidas
                if sortType[1] == "1":
                    dicRights = dict(sorted(dicRights.items(), key=lambda item: int(item[1][2])))
                elif sortType[1] == "2":
                    dicRights = dict(sorted(dicRights.items() , key=lambda item: int(item[1][2]) , reverse=True))
            case "5":
                #Ordenar por Receitas
                if sortType[1] == "1":
                    dicRights = dict(sorted(dicRights.items() , key=lambda item: float(item[1][3])))
                elif sortType[1] == "2":
                    dicRights = dict(sorted(dicRights.items() , key=lambda item: float(item[1][3]) , reverse=True))
            case "6":
                #Ordenar por Direitos
                if sortType[1] == "1":
                    dicRights = dict(sorted(dicRights.items() , key=lambda item: float(item[1][4])))
                elif sortType[1] == "2":
                    dicRights = dict(sorted(dicRights.items() , key=lambda item: float(item[1][0]) , reverse = True))
            case _:
                print("Opção Inválida!")
        '''
        rows = []
        for key , values in dicRights.items():
            rows.append([key] + values)
        rows.append([""] + ["",totalAlbuns,totalSoldUnits,totalIncome,totalRights])
        headers = ["Autor","% Direitos","Nº Álbuns","Unid. Vendidas","Receita (€)","Direitos (€)"]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        print("\n") 
        input("⚠️ Dados ordenados com sucesso! Pressionar Enter para continuar...")
        '''
#----------------------------- Fim Ordenar Direitos Editoriais ------------------------------------------------------------

# ----------------------------- Registar Autor e Albuns ----------------------------------

def newEntry(entryType):
    
    if entryType == "author":
        author = input("\nIntroduza o nome do Autor: ")
        nation = input("\nIntroduza a nacionalidade do Autor: ")
        nrAlbuns = input("\nIntroduza o número de albúns do Autor: ")
        percent = input("\nIntroduza a percentagem do Autor: ")
        
        #Colocar 1a letra de cada palavra das strings Maiuscula
        
        author = author.title()
        nation = nation.title()
        
        #Verificar se Autor já existe
        
        authorExist = False
        for key in dicAuthors.keys():
            if author == key:
                authorExist = True
        if authorExist == True:
            input("⚠️ Autor que Pretende Inserir Já Existe! Pressionar Enter para continuar...")
        elif authorExist == False:
            #Adicionar entrada no dicionário
            
            dicAuthors[author] = [nation,nrAlbuns,str(float(percent)/100)]
            
            #Adicionar ação nos logs
            
            logs.append(["create","autor",author,nation, nrAlbuns, percent])
            
            #Adicionar entrada no ficheiro
            file = open("autores.csv","a",newline="", encoding="utf-8")
            writer = csv.writer(file, delimiter=";")
            writer.writerow([author,nation,nrAlbuns,float(percent)/100])
            file.close()
            print("\n")
            input("⚠️  Autor adicionado com sucesso! Pressionar Enter para continuar...")
        
    elif entryType == "album":
        author = input("\nIntroduza o nome do Autor: ")
        nameAlbum = input("\nIntroduza o nome do Album: ")
        genre = input("\nIntroduza o género do Album: ")
        year = input("\nIntroduza o ano de lançamento do Album: ")
        sold = input("\nIntroduza o número de cópias vendidas do Album: ")
        price = input("\nIntroduza o preço do Album: ")
        
        #Verificar se autor existe

        authorExist = False
        for key in dicAuthors.keys():
            if author == key:
                authorExist = True
        if authorExist == False:
            print("\n")
            input("⚠️  Autor Não Existe! Pressionar Enter para continuar...")
        elif authorExist == True:
        
            #Colocar 1a letra de cada palavra das strings Maiuscula
            
            author = author.title()
            nameAlbum = nameAlbum.title()
            genre = genre.title()
            
            nmbMusics = input("\nQuantas músicas pretende inserir no Album: ")
            countMusics = 0
            musicsList = []
            while countMusics < int(nmbMusics):
                music = input("\nIntroduza o nome da música: ")
                music = music.title()
                musicsList.append(music)
                countMusics += 1
            # ------------------ Gravar dados ------------------------------
            
            #Adicionar entrada no dicionário Albuns
            
            dicAlbuns[nameAlbum] = [author,genre,year,sold,price]
            
            #Adicionar ação nos logs
            
            logs.append(["create","album",nameAlbum,author,genre,year,sold,price])
            
            #Adicionar entrada no ficheiro albuns
            
            file = open("albuns.csv","a",newline="", encoding="utf-8")
            writer = csv.writer(file,delimiter=";")
            writer.writerow([nameAlbum,author,genre,year,sold,price])
            file.close()
            
            #Adicionar entrada no dicionário Musicas
            
            dicMusics[nameAlbum] = [author,musicsList]
            
            #Adicionar entrada no ficheiro musicas
            
            file = open("musicas.csv","a",newline="", encoding="utf-8")
            writer = csv.writer(file,delimiter=";")
            writer.writerow([nameAlbum,author,*musicsList])
            file.close()
                
            #----------------------------------------------------------------
            print("\n")
            input("⚠️  Album adicionado com sucesso! Pressionar Enter para continuar...")
#--------------------------------------------------------------------------------

#------------------------------- Editar Autor --------------------------------------------

def editEntry():
    
    listAuthors()
    
    author = input("\nIntroduza o nome do Autor: ")
    
    #Coolocar 1a letra de cada palavra maiuscula
    author = author.title()
    
    #Verificar se Autor já existe
        
    authorExist = False
    for key in dicAuthors.keys():
        if author == key:
            authorExist = True

    if authorExist == False:
        input("⚠️ Autor que Pretende Editar Não Existe! Pressionar Enter para continuar...")
    elif authorExist == True:
        
        nation = input("\nIntroduza a nacionalidade do Autor: ")
        nrAlbuns = input("\nIntroduza o número de albúns do Autor: ")
        percent = input("\nIntroduza a percentagem do Autor: ")
        
        #Colocar 1a letra de cada palavra das strings Maiuscula
        nation = nation.title()
        
        #Adicionar ação nos logs
            
        logs.append(["edit","autor",author,dicAuthors[author][0], dicAuthors[author][1], dicAuthors[author][2]])
        
        #Adicionar entrada no dicionário
        dicAuthors[author] = [nation,nrAlbuns,str(float(percent)/100)]
        
        #Atualizar ficheiro
        updateFiles("autores.csv")
        
        print("\n")
        input("⚠️ Autor Editado com Sucesso! Pressionar Enter para continuar...")
        
#-----------------------------------------------------------------------------------------

# ----------------------------- Terminar Contrato com Autor ----------------------------------

def deleteEntry():
    
    author = input("\nIntroduza o nome do Autor: ")
    
    #Coloca 1a letra de cada palavra em maiusculas
    author.title()
    
    #------- Guardar dados nos logs ---------------
    logs.append(["delete","autor",author,dicAuthors[author][0],dicAuthors[author][1],dicAuthors[author][2]])
    #----------------------------------------------
    
    del dicAuthors[author]
    
    deleteAlbuns = []
    for item in dicAlbuns.items():
        if item[1][0] == author:
            deleteAlbuns.append(item[0])
            #Guardar dados dos albuns num array auxiliar
            auxLogs.append(["album",item])
   
    for item in deleteAlbuns:
        del dicAlbuns[item]
    
    deleteMusics = []
    for item in dicMusics.items():
        if item[1][0] == author:
            deleteMusics.append(item[0])
            #Guardar dados dos albuns num array auxiliar
            auxLogs.append(["musicas",item])
    
    for item in deleteMusics:
        del dicMusics[item]
    
    #----------- Atualizar ficheiros --------------
    #------------ Autores -------------------------
    
    updateFiles("autores.csv")
    
    #----------------------------------------------
    #------------ Albuns --------------------------
    
    updateFiles("albuns.csv")
    
    #----------------------------------------------
    #------------ Musicas -------------------------
    
    updateFiles("musicas.csv")
    
    #----------------------------------------------
    #----------------------------------------------
    
    print("\n")
    input("⚠️ Autor Removido com Sucesso! Pressionar Enter para continuar...")

#--------------------------------------------------------------------------------

# ---------------------------- Logs ----------------------------------------------

def viewLogs():
    if logs:
        #----------------- Print da tabela tabulada de logs ---------------
        logsViewer = logs
        rows = []
        aux = ""
        for item in logsViewer:
            if item[0] == "delete":
                aux = "Contrato Cessado com o autor " + item[2] + " !"
                rows.append([aux])
            elif item[0] == "create":
                if item[1] == "autor":
                    aux = "Autor " + item[2] + " criado!"
                    rows.append([aux])
                elif item[1] == "album":
                    aux = "Album " + item[2] + " de " + item[3] + " criado!"
                    rows.append([aux])
            elif item[0] == "edit":
                aux = "Dados do Autor " + item[2] + " alterados!"
                rows.append([aux])
        rows.reverse()
        headers = ["Ação"]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        print("\n")
        #-------------------------------------------------------------------------
    else:
        input("⚠️ Sem logs para apresentar! Pressionar Enter para continuar...")

def undoLog():
    if not logs:
        input("⚠️ Sem logs para apresentar! Pressionar Enter para continuar...")
        return
    
    lastAction = logs.pop()

    if lastAction[0] == "edit":
        #Desfazer ação de edição do autor
        dicAuthors[lastAction[2]] = [lastAction[3],lastAction[4],lastAction[5]]
        
        #Atualizar bd
        updateFiles("autores.csv")
        
        
    elif lastAction[0] == "create":
        #Desfazer ação de criação de autor
        if lastAction[1] == "autor":
            del dicAuthors[lastAction[2]]
            #Atualizar bd
            updateFiles("autores.csv")
        #Desfazer ação de criação de album
        elif lastAction[1] == "album":
            del dicAlbuns[lastAction[2]]
            del dicMusics[lastAction[2]]
            #Atualizar bd
            updateFiles("albuns.csv")
            updateFiles("musicas.csv")  
    
    elif lastAction[0] == "delete":
        dicAuthors[lastAction[2]] = [lastAction[3],lastAction[4],lastAction[5]]
        i = 0
        popsList = []
        for item in auxLogs:
            if item[0] == "album" and item[1][1][0] == lastAction[2]:
                popsList.append(i)
                dicAlbuns[item[1][0]] = [item[1][1][0],item[1][1][1],item[1][1][2],item[1][1][3],item[1][1][4]]
                i += 1
            elif item[0] == "musicas" and item[1][1][0] == lastAction[2]:
                popsList.append(i)
                dicMusics[item[1][0]] = [item[1][1][0]] + item[1][1][1:]
                i += 1
        popsList.reverse()
        for item in popsList:
            auxLogs.pop(item)
        #Atualizar dicionários
        updateFiles("autores.csv")
        updateFiles("albuns.csv")
        updateFiles("musicas.csv")
        #----------------------
    print("\n")
    input("⚠️ Ação Desfeita com Sucesso! Pressionar Enter para continuar...")
        
        

#---------------------------------------------------------------------------------

# ------------------------------- Fim Func Opcao 2 - Admin ------------------------------------------------------------------------------ 

# ------------------------------- Func Opcao 3 - Pesquisa -------------------------------------------------------------------------------------

def search():
    
    #Limpar consola
    cls()
    
    searchType = input("Introduza o tipo de pesquisa a efetuar ('autor' , 'album' ou 'musica') (Case Sensitive): ")
    searchElement = input("\nPesquisar: ")
    print("\n")
    
    match searchType:
        case "autor":
            searchOutput = {}
            for item in dicAuthors.items():
                if searchElement in item[0]:
                    searchOutput[item[0]] = [item[1][0],item[1][1],item[1][2]]
            # ----------- Mostrar lista de Resultados --------------
            rows = []
            for key, values in searchOutput.items():
                if admin == "1":
                    rows.append([key] + [values[0] , values[1] , str(float(values[2]) * 100)])
                elif admin == "0":
                    #Esconder Direitos Editoriais para users não logados
                    rows.append([key] + values[:-1])   
            headers = ["Nome", "Nacionalidade", "Álbuns", "% Direitos Editoriais"] if admin=="1" else ["Nome", "Nacionalidade", "Álbuns"]
            print(tabulate(rows, headers=headers, tablefmt="grid"))
            # ----------------------------------------------------------
        case "album":
            searchOutput = {}
            for item in dicAlbuns.items():
                if searchElement in item[0]:
                    searchOutput[item[0]] = [item[1][0],item[1][1],item[1][2],item[1][3],item[1][4]]
            # ----------- Mostrar lista de Resultados --------------
            rows = []
            for key , values in searchOutput.items():
                rows.append([key] + values)
            headers = ["Nome Album","Nome Banda","Género","Ano Lançamento","Unidades Vendidas", "Preço"]
            print(tabulate(rows, headers=headers, tablefmt="grid"))
            # ----------------------------------------------------------
        case "musica":
            searchOutput = {}
            for item in dicMusics.items():
                for music in item[1]:
                    if searchElement in music:
                        searchOutput[music] = [item[0],item[1][0]]
            # ----------- Mostrar lista de Resultados --------------
            rows = []
            for key , values in searchOutput.items():
                rows.append([key] + values)
            headers = ["Musica","Nome Album","Nome Banda"]
            print(tabulate(rows, headers=headers, tablefmt="grid"))
            # ----------------------------------------------------------
        case _:
            print("O tipo de pesquisa selecionado não é válido! Tipos de pesquisa válidos - 'autor'")
    
    print("\n")
    if searchType == "album" or searchType == "autor" or searchType == "musica":
        del searchOutput
    input("⚠️ Pressionar Enter para continuar...")
# ------------------------------- Fim Func Opcao 3 - Pesquisa ------------------------------------------------------------------------------
# ------------------------------- Func Opcao 4 - Lista Samples -----------------------------------------------------------------------------
def listSamples():
    rows = [["Jonas Blakewood","electronic","Eletronica"],["Audiogreen","sport","Rock"],["ArtEffectAudio","lady","Hip Hop Beat"],["Psychronic","hyperspace","Electro"]]
    if rows:
        headers = ["Nome Autor","Nome Música","Género"]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        print("\n")
def playMusic(action):
    match action:
        case "play":
            print("\n")
            samplesList = ["electronic","sport","lady","hyperspace"]
            music = input("Introduza o nome da musica que pretende ouvir: ")
            if music in samplesList:
                pygame.mixer.init()
                pygame.mixer.music.load("samples/" + music + ".mp3")
                pygame.mixer.music.play()
                input("⚠️ Música em Reprodução! Pressionar Enter para continuar...")
            else:
                input("⚠️ Nome Música Não Encontrado! Pressionar Enter para continuar...")
        case "stop":
            pygame.mixer.music.stop()
            print("\n")
            input("⚠️ Música Pausada! Pressionar Enter para continuar...")
        case _:
            print("\n")
            input("⚠️ Erro! Pressionar Enter para continuar...")
# ------------------------------- Fim Func Opcao 4 - Lista Samples -------------------------------------------------------------------------   