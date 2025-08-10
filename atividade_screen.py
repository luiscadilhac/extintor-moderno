from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, ListProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import Database

Builder.load_file('atividade_screen.kv')

class AtividadeScreen(Screen):
    db = ObjectProperty(Database())
    atividades = ListProperty([])
    cargos = ListProperty([])
    current_cargo_id = None
    current_index = 0
    
    def on_enter(self):
        self.load_cargos()
        if self.cargos:
            self.current_cargo_id = self.cargos[0]['id']
            self.ids.spinner_cargo.text = self.cargos[0]['nome']
            self.load_atividades()
            self.display_atividade()
        else:
            self.show_popup("Aviso", "Cadastre primeiro um cargo!")
    
    def load_cargos(self):
        # Carregar todos os cargos de todos os setores
        self.cargos = []
        empresas = self.db.get_empresas()
        for empresa in empresas:
            setores_empresa = self.db.get_setores_by_empresa(empresa['id'])
            for setor in setores_empresa:
                cargos_setor = self.db.get_cargos_by_setor(setor['id'])
                for cargo in cargos_setor:
                    self.cargos.append({
                        'id': cargo['id'],
                        'nome': f"{empresa['nome']} - {setor['nome']} - {cargo['nome']}"
                    })
        
        if self.cargos:
            cargo_names = [cargo['nome'] for cargo in self.cargos]
            self.ids.spinner_cargo.values = cargo_names
    
    def load_atividades(self):
        if not self.current_cargo_id:
            return
        self.atividades = self.db.get_atividades_by_cargo(self.current_cargo_id)
        if not self.atividades:
            self.ids.descricao_atividade.text = ""
            self.ids.frequencia_atividade.text = ""
            return
        self.current_index = 0
        self.display_atividade()
    
    def display_atividade(self):
        if not self.atividades:
            return
            
        atividade = self.atividades[self.current_index]
        self.ids.descricao_atividade.text = atividade['descricao']
        self.ids.frequencia_atividade.text = atividade['frequencia'] or ""
        
        # Atualizar contador
        self.ids.counter.text = f"{self.current_index + 1}/{len(self.atividades)}"
    
    def on_cargo_selected(self, spinner, text):
        for cargo in self.cargos:
            if cargo['nome'] == text:
                self.current_cargo_id = cargo['id']
                break
        self.load_atividades()
        self.display_atividade()
    
    def navigate_first(self):
        if self.atividades:
            self.current_index = 0
            self.display_atividade()
    
    def navigate_previous(self):
        if self.atividades and self.current_index > 0:
            self.current_index -= 1
            self.display_atividade()
    
    def navigate_next(self):
        if self.atividades and self.current_index < len(self.atividades) - 1:
            self.current_index += 1
            self.display_atividade()
    
    def navigate_last(self):
        if self.atividades:
            self.current_index = len(self.atividades) - 1
            self.display_atividade()
    
    def save_atividade(self):
        if not self.current_cargo_id:
            self.show_popup("Erro", "Selecione um cargo!")
            return
            
        descricao = self.ids.descricao_atividade.text.strip()
        if not descricao:
            self.show_popup("Erro", "A descricao da atividade e obrigatoria!")
            return
            
        frequencia = self.ids.frequencia_atividade.text.strip()
        
        if self.atividades and self.current_index < len(self.atividades):
            # Atualizar atividade existente
            atividade_id = self.atividades[self.current_index]['id']
            success = self.db.update_atividade(atividade_id, descricao, frequencia)
            if success:
                self.show_popup("Sucesso", "Atividade atualizada com sucesso!")
                self.load_atividades()
            else:
                self.show_popup("Erro", "Nao foi possivel atualizar a atividade!")
        else:
            # Inserir nova atividade
            atividade_id = self.db.insert_atividade(self.current_cargo_id, descricao, frequencia)
            if atividade_id:
                self.show_popup("Sucesso", "Atividade cadastrada com sucesso!")
                self.load_atividades()
            else:
                self.show_popup("Erro", "Nao foi possivel cadastrar a atividade!")
    
    def new_atividade(self):
        self.ids.descricao_atividade.text = ""
        self.ids.frequencia_atividade.text = ""
        self.current_index = len(self.atividades)  # Posicao para novo registro
        self.ids.counter.text = f"{len(self.atividades) + 1}/{len(self.atividades) + 1}"
    
    def delete_atividade(self):
        if not self.atividades or self.current_index >= len(self.atividades):
            self.show_popup("Erro", "Nenhuma atividade selecionada para exclusao!")
            return
            
        atividade_id = self.atividades[self.current_index]['id']
        success = self.db.delete_atividade(atividade_id)
        if success:
            self.show_popup("Sucesso", "Atividade excluida com sucesso!")
            self.load_atividades()
        else:
            self.show_popup("Erro", "Nao foi possivel excluir a atividade! Existem ambientes vinculados?")
    
    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()