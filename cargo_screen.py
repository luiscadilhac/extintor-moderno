from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, ListProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import Database

Builder.load_file('cargo_screen.kv')

class CargoScreen(Screen):
    db = ObjectProperty(Database())
    cargos = ListProperty([])
    setores = ListProperty([])
    current_setor_id = None
    current_index = 0
    
    def on_enter(self):
        self.load_setores()
        if self.setores:
            self.current_setor_id = self.setores[0]['id']
            self.ids.spinner_setor.text = self.setores[0]['nome']
            self.load_cargos()
            self.display_cargo()
        else:
            self.show_popup("Aviso", "Cadastre primeiro um setor!")
    
    def load_setores(self):
        # Carregar todos os setores de todas as empresas
        self.setores = []
        empresas = self.db.get_empresas()
        for empresa in empresas:
            setores_empresa = self.db.get_setores_by_empresa(empresa['id'])
            for setor in setores_empresa:
                self.setores.append({
                    'id': setor['id'],
                    'nome': f"{empresa['nome']} - {setor['nome']}"
                })
        
        if self.setores:
            setor_names = [setor['nome'] for setor in self.setores]
            self.ids.spinner_setor.values = setor_names
    
    def load_cargos(self):
        if not self.current_setor_id:
            return
        self.cargos = self.db.get_cargos_by_setor(self.current_setor_id)
        if not self.cargos:
            self.ids.nome_cargo.text = ""
            self.ids.descricao_cargo.text = ""
            return
        self.current_index = 0
        self.display_cargo()
    
    def display_cargo(self):
        if not self.cargos:
            return
            
        cargo = self.cargos[self.current_index]
        self.ids.nome_cargo.text = cargo['nome']
        self.ids.descricao_cargo.text = cargo['descricao'] or ""
        
        # Atualizar contador
        self.ids.counter.text = f"{self.current_index + 1}/{len(self.cargos)}"
    
    def on_setor_selected(self, spinner, text):
        for setor in self.setores:
            if setor['nome'] == text:
                self.current_setor_id = setor['id']
                break
        self.load_cargos()
        self.display_cargo()
    
    def navigate_first(self):
        if self.cargos:
            self.current_index = 0
            self.display_cargo()
    
    def navigate_previous(self):
        if self.cargos and self.current_index > 0:
            self.current_index -= 1
            self.display_cargo()
    
    def navigate_next(self):
        if self.cargos and self.current_index < len(self.cargos) - 1:
            self.current_index += 1
            self.display_cargo()
    
    def navigate_last(self):
        if self.cargos:
            self.current_index = len(self.cargos) - 1
            self.display_cargo()
    
    def save_cargo(self):
        if not self.current_setor_id:
            self.show_popup("Erro", "Selecione um setor!")
            return
            
        nome = self.ids.nome_cargo.text.strip()
        if not nome:
            self.show_popup("Erro", "O nome do cargo e obrigatorio!")
            return
            
        descricao = self.ids.descricao_cargo.text.strip()
        
        if self.cargos and self.current_index < len(self.cargos):
            # Atualizar cargo existente
            cargo_id = self.cargos[self.current_index]['id']
            success = self.db.update_cargo(cargo_id, nome, descricao)
            if success:
                self.show_popup("Sucesso", "Cargo atualizado com sucesso!")
                self.load_cargos()
            else:
                self.show_popup("Erro", "Nao foi possivel atualizar o cargo!")
        else:
            # Inserir novo cargo
            cargo_id = self.db.insert_cargo(self.current_setor_id, nome, descricao)
            if cargo_id:
                self.show_popup("Sucesso", "Cargo cadastrado com sucesso!")
                self.load_cargos()
            else:
                self.show_popup("Erro", "Nao foi possivel cadastrar o cargo!")
    
    def new_cargo(self):
        self.ids.nome_cargo.text = ""
        self.ids.descricao_cargo.text = ""
        self.current_index = len(self.cargos)  # Posicao para novo registro
        self.ids.counter.text = f"{len(self.cargos) + 1}/{len(self.cargos) + 1}"
    
    def delete_cargo(self):
        if not self.cargos or self.current_index >= len(self.cargos):
            self.show_popup("Erro", "Nenhum cargo selecionado para exclusao!")
            return
            
        cargo_id = self.cargos[self.current_index]['id']
        success = self.db.delete_cargo(cargo_id)
        if success:
            self.show_popup("Sucesso", "Cargo excluido com sucesso!")
            self.load_cargos()
        else:
            self.show_popup("Erro", "Nao foi possivel excluir o cargo! Existem atividades vinculadas?")
    
    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()