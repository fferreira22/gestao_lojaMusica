from dataclasses import dataclass
from typing import Callable, Dict, Optional
import func

#------------ Ler Dados das bds ------------------

#Ler dados da base de dados 'autores'
func.fetchData("autores")

#Ler dados de albuns da base de dados "albuns"
func.fetchData("albuns")

#Ler dados de musicas da base de dados "musicas"
func.fetchData("musicas")

#Ler dados de users
func.fetchData("users")

#--------------------------------------------------

#------------- Máquina de Estados -------------

class State:
    """Class base para estados (menus)."""

    def __init__(self, state_machine: "StateMachine"):
        self.sm = state_machine

    def enter(self):
        """Chamado quando entra num estado"""
        pass

    def handle_input(self, choice: str):
        """Processa inputs e decide transições"""
        raise NotImplementedError


class MainMenu(State):
    def enter(self):
        func.cls()
        print("-----------------------------------------------------------------\n\t\t\t\tMenu \n-----------------------------------------------------------------\n")
        print("1. Listar")
        print("2. Área Administrativa")
        print("3. Pesquisar")
        print("4. Lista de Samples")
        print("0. Sair\n")
        footer = "-----------------------------------------------------------------\n"
        if func.admin == "0":
            footer += "5 - Login"
        elif func.admin == "1":
            footer += f"Utilizador Logado: {func.currentUser}\n" + "5 - Logout"
        footer += "\n-----------------------------------------------------------------\n"
        print(footer)

    def handle_input(self, choice: str):
        if choice == "1":
            self.sm.change_state("list")
        elif choice == "2":
            self.sm.change_state("admin")
        elif choice == "3":
            func.search()
            self.sm.change_state("main")
        elif choice == "4":
            self.sm.change_state("sample")
        elif choice == "5":
            func.cls()
            print("\n--- Login ---\n")
            func.login()
            self.sm.change_state("main")
        elif choice == "0":
            self.sm.running = False
        else:
            print("Opção Inválida.")

# --------------------- Opcao 1 - Menu Principal -----------------------------------------------------------------------------------------

# ---------------------- Listagem Autores --------------------------

class ListMenu(State):
    def enter(self):
        func.cls()
        print("\n--- Listagem de Autores ---\n")
        func.listAuthors()
        print("-----------------------------------------------------------------\n")
        print("1. Listar Albuns de Autor\t0. Retroceder\n")
        print("-----------------------------------------------------------------\n")

    def handle_input(self, choice: str):
        if choice == "1":
            self.sm.change_state("listAlbuns")
        elif choice == "0":
            self.sm.change_state("main")
        else:
            print("Opção Inválida.")

# -------------------------------------------------------------------

# ---------------------- Listagem Albuns --------------------------

class ListAlbuns(State):
    def enter(self):
        print("\n--- Listagem de Albuns ---\n")
        func.listAlbuns()
        print("-------------------------------------------------------------------------------\n")
        print("1. Listar Músicas de Albuns\t2. Retroceder\t0. Retroceder Menu Inicial\n")
        print("-------------------------------------------------------------------------------\n")

    def handle_input(self, choice: str):
        if choice == "1":
            self.sm.change_state("listMusics")
        elif choice == "2":
            self.sm.change_state("list")
        elif choice == "0":
            self.sm.change_state("main")
        else:
            print("Opção Inválida.")

# -------------------------------------------------------------------

# ---------------------- Listagem Musicas --------------------------

class ListMusics(State):
    def enter(self):
        print("\n--- Listagem de Musicas ---\n")
        func.listMusics()
        print("-----------------------------------------------------------------\n")
        print("1. Retroceder\t0. Retroceder Menu Principal\n")
        print("-----------------------------------------------------------------\n")

    def handle_input(self, choice: str):
        if choice == "1":
            func.cls()
            self.sm.change_state("listAlbuns")
        elif choice == "0":
            self.sm.change_state("main")
        else:
            print("Opção Inválida.")

# -------------------------------------------------------------------

# --------------------------------- Fim Opcao 1 - Menu Principal ------------------------------------------------------------------------------

# --------------------- Opcao 2 - Area Administrativa -----------------------------------------------------------------------------------------

# --------------- Menu Area Administrativa ------------
class AdminMenu(State):
        def enter(self):
            func.cls()
            print("\n--- Área Administrativa ---\n")
            print("1. Consultar Direitos")
            print("2. Criar Registo Autor")
            print("3. Criar Registo Album")
            print("4. Editar Autor")
            print("5. Terminar Contrato Autor")
            print("6. Log Ações")
            print("0. Retroceder\n")

        def handle_input(self, choice: str):
            if choice == "1":
                if func.admin == "1":
                    self.sm.change_state("viewRights")
                elif func.admin == "0":
                    print("\n")
                    input("⚠️ Necessário efetuar login para aceder a esta funcionalidade!Pressionar Enter para continuar...")
                    self.sm.change_state("admin")
            elif choice == "2":
                func.newEntry("author")
                self.sm.change_state("admin")
            elif choice == "3":
                func.newEntry("album")
                self.sm.change_state("admin")
            elif choice == "4":
                func.cls()
                print("\n--- Editar Autores ---\n")
                func.editEntry()
                self.sm.change_state("admin")
            elif choice == "5":
                try:
                    func.deleteEntry()
                except Exception:
                  input("⚠️ Autor Não Encontrado!Pressionar Enter para continuar...")  
                self.sm.change_state("admin")
            elif choice == "6":
                self.sm.change_state("logs")
            elif choice == "0":
                self.sm.change_state("main")
            else:
                print("Opção Inválida.")
# -------------------------------------------------------

# --------------- Consultar Direitos Editoriais ------------
class RightsMenu(State):
    def enter(self):
        func.cls()
        print("\n--- Direitos Editoriais ---\n")
        func.viewRights()
        print("\n---------------------------------------------------------------------------------\n")
        print("1. Ordenar\t2. Retroceder\t0. Retroceder Menu Principal\n")
        print("---------------------------------------------------------------------------------\n")

    def handle_input(self, choice: str):
        if choice == "1":
            func.orderRights()
            self.sm.change_state("viewRights")
        elif choice == "2":
            self.sm.change_state("admin")
        elif choice == "0":
            self.sm.change_state("main")
        else:
            print("Opção Inválida.")
# -------------------------------------------------------

#----------------------- Logs -------------------------------------

class LogsMenu(State):
    def enter(self):
        func.cls()
        print("\n--- Registo de Ações ---\n")
        func.viewLogs()
        print("\n---------------------------------------------------------------------------------\n")
        print("1.Desfazer Última Ação \t2. Retroceder\t0. Retroceder Menu Principal\n")
        print("---------------------------------------------------------------------------------\n")

    def handle_input(self, choice: str):
        if choice == "1":
            func.undoLog()
            self.sm.change_state("logs")
        elif choice == "2":
            self.sm.change_state("admin")
        elif choice == "0":
            self.sm.change_state("main")
        else:
            print("Opção Inválida.")

#------------------------------------------------------------------

# --------------------------------- Fim Opcao 2 - Area Administrativa ------------------------------------------------------------------------------



# --------------- Menu Samples ------------
class SampleMenu(State):
    def enter(self):
        func.cls()
        print("\n--- Lista de Samples Gratuitos ---\n")
        func.listSamples()
        print("---------------------------------------------------------------------------------\n")
        print("1. Reproduzir Música\t2.Parar Música\t0. Retroceder\n")
        print("---------------------------------------------------------------------------------\n")

    def handle_input(self, choice: str):
        if choice == "1":
            func.playMusic("play")
            self.sm.change_state("sample")
        if choice == "2":
            func.playMusic("stop")
            self.sm.change_state("sample")
        elif choice == "0":
            self.sm.change_state("main")
        else:
            print("Opção Inválida.")
# -------------------------------------------------------


class StateMachine:
    def __init__(self):
        self.states: Dict[str, State] = {}
        self.current_state: Optional[State] = None
        self.running = True

    def add_state(self, name: str, state_class: Callable[["StateMachine"], State]):
        self.states[name] = state_class(self)

    def change_state(self, name: str):
        self.current_state = self.states[name]
        self.current_state.enter()

    def run(self):
        self.change_state("main")
        while self.running:
            choice = input("Opção> ")
            if self.current_state:
                self.current_state.handle_input(choice)


if __name__ == "__main__":
    sm = StateMachine()
    sm.add_state("main", MainMenu)
    sm.add_state("list", ListMenu)
    sm.add_state("listAlbuns", ListAlbuns)
    sm.add_state("listMusics", ListMusics)
    sm.add_state("admin", AdminMenu)
    sm.add_state("viewRights", RightsMenu)
    sm.add_state("logs", LogsMenu)
    sm.add_state("sample", SampleMenu)

    sm.run()

# -------------------- Fim Máquina de Estados -----------------