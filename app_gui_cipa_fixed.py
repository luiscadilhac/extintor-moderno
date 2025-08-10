# app_gui_cipa.py
import kivy
import sys
import json
import os
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
import random
import traceback

kivy.require('2.0.0')

class SistemaVotacaoCIPA:
    def __init__(self):
        self.candidatos = {}
        self.votos = {}
        self.eleitores_habilitados = {}
        self.codigos_ativos = set()
        self.total_votantes = 0
        self.eleitores_votaram = set()
        self.data_arquivo = 'dados_cipa.json'
        self.carregar_dados()

    def adicionar_candidato(self, numero, nome):
        self.candidatos[str(numero)] = nome
        self.votos[str(numero)] = 0
        self.salvar_dados()

    def _gerar_codigo_validacao(self):
        while True:
            codigo = str(random.randint(100000, 999999))
            if codigo not in self.codigos_ativos:
                self.codigos_ativos.add(codigo)
                return codigo

    def habilitar_eleitor(self, id_eleitor_interno):
        if id_eleitor_interno in self.eleitores_habilitados:
            return False, "Eleitor já foi habilitado."
        codigo = self._gerar_codigo_validacao()
        self.eleitores_habilitados[id_eleitor_interno] = codigo
        return True, codigo

    def registrar_voto(self, id_eleitor_interno, codigo_informado, numero_candidato):
        if id_eleitor_interno not in self.eleitores_habilitados:
            return False, "Erro: Eleitor não habilitado."
        if self.eleitores_habilitados[id_eleitor_interno] != codigo_informado:
            return False, "Erro: Código de validação incorreto."
        if codigo_informado not in self.codigos_ativos:
            return False, "Este código já foi usado ou é inválido."
        
        num_candidato_str = str(numero_candidato)
        if num_candidato_str not in self.candidatos:
            return False, "Número de candidato inválido."

        self.votos[num_candidato_str] += 1
        self.total_votantes += 1
        self.eleitores_votaram.add(id_eleitor_interno)
        self.codigos_ativos.remove(codigo_informado)
        del self.eleitores_habilitados[id_eleitor_interno]
        self.salvar_dados()
        return True, "Voto registrado com sucesso!"

    def salvar_dados(self):
        dados = {
            'candidatos': self.candidatos,
            'votos': self.votos,
            'total_votantes': self.total_votantes,
            'eleitores_votaram': list(self.eleitores_votaram),
            'timestamp': datetime.now().isoformat()
        }
        with open(self.data_arquivo, 'w') as f:
            json.dump(dados, f, indent=2)

    def carregar_dados(self):
        if os.path.exists(self.data_arquivo):
            try:
                with open(self.data_arquivo, 'r') as f:
                    dados = json.load(f)
                self.candidatos = dados.get('candidatos', {})
                self.votos = dados.get('votos', {})
                self.total_votantes = dados.get('total_votantes', 0)
                self.eleitores_votaram = set(dados.get('eleitores_votaram', []))
            except:
                pass

    def remover_candidato(self, numero):
        numero_str = str(numero)
        if numero_str in self.candidatos:
            del self.candidatos[numero_str]
            del self.votos[numero_str]
            self.salvar_dados()
            return True
        return False

    def resetar_eleicao(self):
        self.votos = {num: 0 for num in self.candidatos.keys()}
        self.total_votantes = 0
        self.eleitores_votaram.clear()
        self.eleitores_habilitados.clear()
        self.codigos_ativos.clear()
        self.salvar_dados()

    def obter_resultados(self):
        return sorted(self.votos.items(), key=lambda item: item[1], reverse=True)

    def obter_estatisticas(self):
        total_candidatos = len(self.candidatos)
        percentuais = {}
        for num, votos in self.votos.items():
            if self.total_votantes > 0:
                percentuais[num] = (votos / self.total_votantes) * 100
            else:
                percentuais[num] = 0
        return {
            'total_candidatos': total_candidatos,
            'total_votantes': self.total_votantes,
            'percentuais': percentuais
        }

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        
        with self.canvas.before:
            Color(0.1, 0.1, 0.2, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        layout = BoxLayout(orientation='vertical', padding=40, spacing=25)
        
        title = Label(text='🗳️ ELEIÇÃO CIPA', font_size='40sp', bold=True, color=[1, 0.8, 0, 1])
        layout.add_widget(title)
        
        layout.add_widget(Widget(size_hint_y=0.1))
        
        admin_btn = Button(text='⚙️ ADMIN', font_size='18sp', bold=True, 
                          background_color=[0.8, 0.2, 0.8, 1], size_hint_y=None, height=50, on_press=self.go_admin)
        layout.add_widget(admin_btn)
        
        mesario_btn = Button(text='👨‍💼 MESÁRIO', font_size='18sp', bold=True,
                            background_color=[0.2, 0.8, 0.2, 1], size_hint_y=None, height=50, on_press=self.go_mesario)
        layout.add_widget(mesario_btn)
        
        eleitor_btn = Button(text='🗳️ ELEITOR', font_size='18sp', bold=True,
                            background_color=[0.2, 0.6, 1, 1], size_hint_y=None, height=50, on_press=self.go_eleitor)
        layout.add_widget(eleitor_btn)
        
        result_btn = Button(text='📊 RESULTADOS', font_size='18sp', bold=True,
                           background_color=[1, 0.5, 0.2, 1], size_hint_y=None, height=50, on_press=self.go_resultados)
        layout.add_widget(result_btn)
        
        self.add_widget(layout)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def go_mesario(self, instance):
        self.manager.current = 'mesario'

    def go_eleitor(self, instance):
        self.manager.current = 'eleitor'

    def go_admin(self, instance):
        self.manager.current = 'admin'

    def go_resultados(self, instance):
        self.manager.get_screen('resultados').update_results()
        self.manager.current = 'resultados'

class AdminScreen(Screen):
    def __init__(self, **kwargs):
        super(AdminScreen, self).__init__(**kwargs)
        
        with self.canvas.before:
            Color(0.3, 0.1, 0.3, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        title = Label(text='⚙️ ADMINISTRAÇÃO CIPA', font_size='28sp', bold=True, color=[1, 0.8, 1, 1])
        layout.add_widget(title)

        add_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        self.numero_input = TextInput(hint_text='Nº', size_hint_x=0.2, background_color=[0.9, 0.9, 0.9, 1])
        self.nome_input = TextInput(hint_text='Nome do Candidato', size_hint_x=0.6, background_color=[0.9, 0.9, 0.9, 1])
        add_btn = Button(text='➕ ADICIONAR', size_hint_x=0.2, font_size='14sp', bold=True,
                        background_color=[0.2, 0.8, 0.2, 1], on_press=self.adicionar_candidato)
        add_layout.add_widget(self.numero_input)
        add_layout.add_widget(self.nome_input)
        add_layout.add_widget(add_btn)
        layout.add_widget(add_layout)

        layout.add_widget(Label(text='👥 CANDIDATOS CADASTRADOS:', font_size='20sp', bold=True, color=[1, 0.8, 1, 1]))
        
        self.candidatos_scroll = ScrollView(size_hint_y=0.4)
        self.candidatos_grid = GridLayout(cols=3, size_hint_y=None, spacing=5)
        self.candidatos_grid.bind(minimum_height=self.candidatos_grid.setter('height'))
        self.candidatos_scroll.add_widget(self.candidatos_grid)
        layout.add_widget(self.candidatos_scroll)

        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)
        reset_btn = Button(text='🔄 RESETAR', font_size='16sp', bold=True,
                          background_color=[1, 0.3, 0.3, 1], on_press=self.resetar_eleicao)
        update_btn = Button(text='🔄 ATUALIZAR', font_size='16sp', bold=True,
                           background_color=[0.3, 0.7, 1, 1], on_press=self.atualizar_lista)
        back_btn = Button(text='🏠 VOLTAR', font_size='16sp', bold=True,
                         background_color=[0.6, 0.6, 0.6, 1], on_press=self.go_home)
        btn_layout.add_widget(reset_btn)
        btn_layout.add_widget(update_btn)
        btn_layout.add_widget(back_btn)
        layout.add_widget(btn_layout)

        self.message_label = Label(text='', font_size='16sp', bold=True)
        layout.add_widget(self.message_label)
        
        self.add_widget(layout)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_enter(self):
        self.atualizar_lista()

    def adicionar_candidato(self, instance):
        numero = self.numero_input.text.strip()
        nome = self.nome_input.text.strip()
        
        if not numero or not nome:
            self.message_label.text = "Preencha número e nome"
            self.message_label.color = [1,0,0,1]
            return

        app_instance = App.get_running_app()
        if numero in app_instance.sistema_votacao.candidatos:
            self.message_label.text = "Número já existe"
            self.message_label.color = [1,0,0,1]
            return

        app_instance.sistema_votacao.adicionar_candidato(numero, nome)
        self.message_label.text = f"Candidato {nome} adicionado"
        self.message_label.color = [0,0.5,0,1]
        self.numero_input.text = ''
        self.nome_input.text = ''
        self.atualizar_lista()

    def remover_candidato(self, numero):
        app_instance = App.get_running_app()
        if app_instance.sistema_votacao.remover_candidato(numero):
            self.message_label.text = f"Candidato {numero} removido"
            self.message_label.color = [0,0.5,0,1]
            self.atualizar_lista()

    def atualizar_lista(self, instance=None):
        self.candidatos_grid.clear_widgets()
        app_instance = App.get_running_app()
        
        for num, nome in app_instance.sistema_votacao.candidatos.items():
            votos = app_instance.sistema_votacao.votos.get(num, 0)
            
            self.candidatos_grid.add_widget(Label(text=f"🔢 {num}", size_hint_y=None, height=45,
                                                  font_size='16sp', bold=True, color=[1, 1, 0.8, 1]))
            self.candidatos_grid.add_widget(Label(text=f"👤 {nome} ({votos} votos)", size_hint_y=None, height=45,
                                                  font_size='14sp', color=[0.9, 0.9, 0.9, 1]))
            
            remove_btn = Button(text='❌ REMOVER', size_hint_y=None, height=45, font_size='12sp', bold=True,
                               background_color=[1, 0.3, 0.3, 1])
            remove_btn.bind(on_press=lambda x, n=num: self.remover_candidato(n))
            self.candidatos_grid.add_widget(remove_btn)

    def resetar_eleicao(self, instance):
        app_instance = App.get_running_app()
        app_instance.sistema_votacao.resetar_eleicao()
        self.message_label.text = "Eleição resetada"
        self.message_label.color = [0,0.5,0,1]
        self.atualizar_lista()

    def go_home(self, instance):
        self.manager.current = 'home'
        self.message_label.text = ''

class CIPAApp(App):
    def __init__(self, **kwargs):
        super(CIPAApp, self).__init__(**kwargs)
        self.sistema_votacao = SistemaVotacaoCIPA()

    def build(self):
        self.sistema_votacao.adicionar_candidato(1, "Maria Silva")
        self.sistema_votacao.adicionar_candidato(2, "João Pereira")
        self.sistema_votacao.adicionar_candidato(3, "Ana Costa")

        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(AdminScreen(name='admin'))
        return sm

if __name__ == '__main__':
    try:
        CIPAApp().run()
    except Exception as e:
        print(f"\nERRO CRÍTICO: {e}")
        traceback.print_exc()
        sys.exit(1)