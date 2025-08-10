# urna_cipa_completa.py
import kivy
import sys
import json
import os
from datetime import datetime, date
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import random
import traceback

kivy.require('2.0.0')

class SistemaUrnaEletronica:
    def __init__(self):
        self.empresas = {}
        self.candidatos = {}
        self.votos = {}
        self.eleitores = {}
        self.votantes_log = []
        self.empresa_atual = None
        self.data_arquivo = 'urna_cipa.json'
        self.carregar_dados()
        
    def criar_empresa(self, nome, cnpj):
        empresa_id = str(len(self.empresas) + 1)
        self.empresas[empresa_id] = {
            'nome': nome,
            'cnpj': cnpj,
            'candidatos': {},
            'eleitores': {},
            'votos': {},
            'data_criacao': datetime.now().isoformat()
        }
        self.salvar_dados()
        return empresa_id
        
    def adicionar_candidato(self, numero, nome, cargo="Membro CIPA"):
        if self.empresa_atual:
            self.empresas[self.empresa_atual]['candidatos'][str(numero)] = {
                'nome': nome,
                'cargo': cargo,
                'votos': 0
            }
            self.salvar_dados()
            
    def registrar_voto(self, numero_candidato):
        if self.empresa_atual and str(numero_candidato) in self.empresas[self.empresa_atual]['candidatos']:
            self.empresas[self.empresa_atual]['candidatos'][str(numero_candidato)]['votos'] += 1
            
            # Log do voto
            self.votantes_log.append({
                'empresa': self.empresa_atual,
                'candidato': numero_candidato,
                'timestamp': datetime.now().isoformat(),
                'data': datetime.now().strftime('%d/%m/%Y'),
                'hora': datetime.now().strftime('%H:%M:%S')
            })
            self.salvar_dados()
            return True
        return False
        
    def obter_candidatos(self):
        if self.empresa_atual:
            return self.empresas[self.empresa_atual]['candidatos']
        return {}
        
    def obter_resultados(self):
        candidatos = self.obter_candidatos()
        return sorted(candidatos.items(), key=lambda x: x[1]['votos'], reverse=True)
        
    def salvar_dados(self):
        dados = {
            'empresas': self.empresas,
            'votantes_log': self.votantes_log,
            'timestamp': datetime.now().isoformat()
        }
        with open(self.data_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
            
    def carregar_dados(self):
        if os.path.exists(self.data_arquivo):
            try:
                with open(self.data_arquivo, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                self.empresas = dados.get('empresas', {})
                self.votantes_log = dados.get('votantes_log', [])
            except:
                pass

class SomUrna:
    def __init__(self):
        self.som_tecla = None
        self.som_confirma = None
        self.som_corrige = None
        self.carregar_sons()
        
    def carregar_sons(self):
        # Sons simulados - em produção usar arquivos .wav reais
        try:
            # self.som_tecla = SoundLoader.load('beep.wav')
            # self.som_confirma = SoundLoader.load('confirma.wav') 
            # self.som_corrige = SoundLoader.load('corrige.wav')
            pass
        except:
            pass
            
    def tocar_tecla(self):
        if self.som_tecla:
            self.som_tecla.play()
            
    def tocar_confirma(self):
        if self.som_confirma:
            self.som_confirma.play()
            
    def tocar_corrige(self):
        if self.som_corrige:
            self.som_corrige.play()

class EmpresaScreen(Screen):
    def __init__(self, **kwargs):
        super(EmpresaScreen, self).__init__(**kwargs)
        
        with self.canvas.before:
            Color(0.05, 0.05, 0.15, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        title = Label(text='🏢 SISTEMA URNA ELETRÔNICA CIPA', font_size='32sp', bold=True, 
                     color=[1, 0.9, 0, 1])
        layout.add_widget(title)
        
        # Criar nova empresa
        create_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=0.4)
        create_layout.add_widget(Label(text='📝 CRIAR NOVA EMPRESA', font_size='20sp', 
                                      color=[0.8, 1, 0.8, 1]))
        
        self.nome_input = TextInput(hint_text='Nome da Empresa', multiline=False,
                                   background_color=[0.9, 0.9, 0.9, 1])
        create_layout.add_widget(self.nome_input)
        
        self.cnpj_input = TextInput(hint_text='CNPJ', multiline=False,
                                   background_color=[0.9, 0.9, 0.9, 1])
        create_layout.add_widget(self.cnpj_input)
        
        criar_btn = Button(text='➕ CRIAR EMPRESA', font_size='16sp', bold=True,
                          background_color=[0.2, 0.8, 0.2, 1], size_hint_y=None, height=50)
        criar_btn.bind(on_press=self.criar_empresa)
        create_layout.add_widget(criar_btn)
        
        layout.add_widget(create_layout)
        
        # Selecionar empresa existente
        layout.add_widget(Label(text='🏢 EMPRESAS CADASTRADAS', font_size='20sp', 
                               color=[0.8, 1, 0.8, 1]))
        
        self.empresas_scroll = ScrollView(size_hint_y=0.4)
        self.empresas_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.empresas_layout.bind(minimum_height=self.empresas_layout.setter('height'))
        self.empresas_scroll.add_widget(self.empresas_layout)
        layout.add_widget(self.empresas_scroll)
        
        self.message_label = Label(text='', font_size='16sp', bold=True)
        layout.add_widget(self.message_label)
        
        self.add_widget(layout)
        
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
    def on_enter(self):
        self.atualizar_empresas()
        
    def criar_empresa(self, instance):
        nome = self.nome_input.text.strip()
        cnpj = self.cnpj_input.text.strip()
        
        if not nome or not cnpj:
            self.message_label.text = "Preencha todos os campos"
            self.message_label.color = [1, 0, 0, 1]
            return
            
        app = App.get_running_app()
        empresa_id = app.sistema.criar_empresa(nome, cnpj)
        
        self.message_label.text = f"Empresa criada! ID: {empresa_id}"
        self.message_label.color = [0, 0.8, 0, 1]
        
        self.nome_input.text = ''
        self.cnpj_input.text = ''
        self.atualizar_empresas()
        
    def atualizar_empresas(self):
        self.empresas_layout.clear_widgets()
        app = App.get_running_app()
        
        for emp_id, empresa in app.sistema.empresas.items():
            btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
            
            info_label = Label(text=f"🏢 {empresa['nome']} - CNPJ: {empresa['cnpj']}", 
                              size_hint_x=0.7, color=[0.9, 0.9, 0.9, 1])
            btn_layout.add_widget(info_label)
            
            select_btn = Button(text='✅ SELECIONAR', size_hint_x=0.3, font_size='14sp',
                               background_color=[0.2, 0.6, 1, 1])
            select_btn.bind(on_press=lambda x, eid=emp_id: self.selecionar_empresa(eid))
            btn_layout.add_widget(select_btn)
            
            self.empresas_layout.add_widget(btn_layout)
            
    def selecionar_empresa(self, empresa_id):
        app = App.get_running_app()
        app.sistema.empresa_atual = empresa_id
        self.manager.current = 'urna'

class UrnaScreen(Screen):
    def __init__(self, **kwargs):
        super(UrnaScreen, self).__init__(**kwargs)
        
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        self.som = SomUrna()
        self.numero_digitado = ""
        
        main_layout = BoxLayout(orientation='horizontal', padding=20, spacing=20)
        
        # Painel esquerdo - Tela da urna
        left_panel = BoxLayout(orientation='vertical', size_hint_x=0.6, spacing=10)
        
        # Cabeçalho
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=60)
        header.add_widget(Label(text='⚖️ JUSTIÇA ELEITORAL', font_size='20sp', bold=True,
                               color=[1, 1, 1, 1]))
        left_panel.add_widget(header)
        
        # Tela principal
        with self.canvas:
            Color(0.9, 0.9, 0.9, 1)
            self.tela_rect = RoundedRectangle(size=(400, 300), pos=(50, 200), radius=[10])
            
        self.tela_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        self.titulo_label = Label(text='ELEIÇÃO CIPA 2024', font_size='24sp', bold=True,
                                 color=[0, 0, 0, 1])
        self.tela_layout.add_widget(self.titulo_label)
        
        self.instrucao_label = Label(text='Digite o número do candidato', font_size='18sp',
                                    color=[0, 0, 0, 1])
        self.tela_layout.add_widget(self.instrucao_label)
        
        # Display do número
        self.numero_display = Label(text='___', font_size='48sp', bold=True,
                                   color=[0, 0, 0, 1])
        self.tela_layout.add_widget(self.numero_display)
        
        # Info candidato
        self.candidato_info = Label(text='', font_size='16sp', color=[0, 0, 0, 1])
        self.tela_layout.add_widget(self.candidato_info)
        
        left_panel.add_widget(self.tela_layout)
        
        # Painel direito - Teclado
        right_panel = BoxLayout(orientation='vertical', size_hint_x=0.4, spacing=10)
        
        # Teclado numérico
        teclado_grid = GridLayout(cols=3, spacing=5, size_hint_y=0.6)
        
        for i in range(1, 10):
            btn = Button(text=str(i), font_size='24sp', bold=True,
                        background_color=[0.3, 0.3, 0.3, 1])
            btn.bind(on_press=lambda x, num=i: self.digitar_numero(num))
            teclado_grid.add_widget(btn)
            
        # Linha do 0
        teclado_grid.add_widget(Widget())
        btn_0 = Button(text='0', font_size='24sp', bold=True,
                      background_color=[0.3, 0.3, 0.3, 1])
        btn_0.bind(on_press=lambda x: self.digitar_numero(0))
        teclado_grid.add_widget(btn_0)
        teclado_grid.add_widget(Widget())
        
        right_panel.add_widget(teclado_grid)
        
        # Botões de ação
        acoes_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=0.4)
        
        btn_branco = Button(text='BRANCO', font_size='18sp', bold=True,
                           background_color=[0.9, 0.9, 0.9, 1], color=[0, 0, 0, 1])
        btn_branco.bind(on_press=self.votar_branco)
        acoes_layout.add_widget(btn_branco)
        
        btn_corrige = Button(text='CORRIGE', font_size='18sp', bold=True,
                            background_color=[1, 0.5, 0, 1])
        btn_corrige.bind(on_press=self.corrigir)
        acoes_layout.add_widget(btn_corrige)
        
        btn_confirma = Button(text='CONFIRMA', font_size='18sp', bold=True,
                             background_color=[0, 0.8, 0, 1])
        btn_confirma.bind(on_press=self.confirmar_voto)
        acoes_layout.add_widget(btn_confirma)
        
        btn_voltar = Button(text='🏠 VOLTAR', font_size='16sp', bold=True,
                           background_color=[0.6, 0.6, 0.6, 1])
        btn_voltar.bind(on_press=self.voltar)
        acoes_layout.add_widget(btn_voltar)
        
        right_panel.add_widget(acoes_layout)
        
        main_layout.add_widget(left_panel)
        main_layout.add_widget(right_panel)
        
        self.add_widget(main_layout)
        
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
    def digitar_numero(self, numero):
        self.som.tocar_tecla()
        if len(self.numero_digitado) < 3:
            self.numero_digitado += str(numero)
            self.atualizar_display()
            
    def atualizar_display(self):
        display = self.numero_digitado.ljust(3, '_')
        self.numero_display.text = display
        
        # Verificar candidato
        if len(self.numero_digitado) >= 2:
            app = App.get_running_app()
            candidatos = app.sistema.obter_candidatos()
            
            if self.numero_digitado in candidatos:
                candidato = candidatos[self.numero_digitado]
                self.candidato_info.text = f"👤 {candidato['nome']}\n🎯 {candidato['cargo']}"
            else:
                self.candidato_info.text = "❌ CANDIDATO NÃO ENCONTRADO"
        else:
            self.candidato_info.text = ""
            
    def corrigir(self, instance):
        self.som.tocar_corrige()
        self.numero_digitado = ""
        self.numero_display.text = "___"
        self.candidato_info.text = ""
        
    def votar_branco(self, instance):
        self.numero_digitado = "BRANCO"
        self.numero_display.text = "BRANCO"
        self.candidato_info.text = "🗳️ VOTO EM BRANCO"
        
    def confirmar_voto(self, instance):
        if not self.numero_digitado:
            return
            
        self.som.tocar_confirma()
        
        if self.numero_digitado == "BRANCO":
            self.mostrar_confirmacao("Voto em BRANCO confirmado!")
        else:
            app = App.get_running_app()
            if app.sistema.registrar_voto(self.numero_digitado):
                candidatos = app.sistema.obter_candidatos()
                nome = candidatos[self.numero_digitado]['nome']
                self.mostrar_confirmacao(f"Voto confirmado para:\n{nome}")
            else:
                self.mostrar_confirmacao("❌ Erro ao registrar voto")
                
        # Reset após 2 segundos
        Clock.schedule_once(self.reset_urna, 2)
        
    def mostrar_confirmacao(self, mensagem):
        self.titulo_label.text = "✅ VOTO CONFIRMADO"
        self.instrucao_label.text = mensagem
        self.numero_display.text = ""
        self.candidato_info.text = ""
        
    def reset_urna(self, dt):
        self.titulo_label.text = "ELEIÇÃO CIPA 2024"
        self.instrucao_label.text = "Digite o número do candidato"
        self.numero_digitado = ""
        self.numero_display.text = "___"
        self.candidato_info.text = ""
        
    def voltar(self, instance):
        self.manager.current = 'empresa'

class AdminScreen(Screen):
    def __init__(self, **kwargs):
        super(AdminScreen, self).__init__(**kwargs)
        
        with self.canvas.before:
            Color(0.2, 0.1, 0.2, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        title = Label(text='⚙️ ADMINISTRAÇÃO CIPA', font_size='28sp', bold=True,
                     color=[1, 0.8, 1, 1])
        layout.add_widget(title)
        
        # Adicionar candidato
        add_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        self.numero_input = TextInput(hint_text='Nº', size_hint_x=0.2,
                                     background_color=[0.9, 0.9, 0.9, 1])
        self.nome_input = TextInput(hint_text='Nome', size_hint_x=0.5,
                                   background_color=[0.9, 0.9, 0.9, 1])
        self.cargo_input = TextInput(hint_text='Cargo', size_hint_x=0.3,
                                    background_color=[0.9, 0.9, 0.9, 1])
        
        add_btn = Button(text='➕ ADICIONAR', size_hint_x=0.2, font_size='14sp',
                        background_color=[0.2, 0.8, 0.2, 1])
        add_btn.bind(on_press=self.adicionar_candidato)
        
        add_layout.add_widget(self.numero_input)
        add_layout.add_widget(self.nome_input)
        add_layout.add_widget(self.cargo_input)
        add_layout.add_widget(add_btn)
        layout.add_widget(add_layout)
        
        # Lista candidatos
        layout.add_widget(Label(text='👥 CANDIDATOS CADASTRADOS', font_size='18sp',
                               color=[1, 0.8, 1, 1]))
        
        self.candidatos_scroll = ScrollView(size_hint_y=0.5)
        self.candidatos_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.candidatos_layout.bind(minimum_height=self.candidatos_layout.setter('height'))
        self.candidatos_scroll.add_widget(self.candidatos_layout)
        layout.add_widget(self.candidatos_scroll)
        
        # Botões
        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        btn_relatorio = Button(text='📊 RELATÓRIO', font_size='16sp',
                              background_color=[0.2, 0.6, 1, 1])
        btn_relatorio.bind(on_press=self.mostrar_relatorio)
        
        btn_urna = Button(text='🗳️ URNA', font_size='16sp',
                         background_color=[0.8, 0.2, 0.8, 1])
        btn_urna.bind(on_press=lambda x: setattr(self.manager, 'current', 'urna'))
        
        btn_voltar = Button(text='🏠 VOLTAR', font_size='16sp',
                           background_color=[0.6, 0.6, 0.6, 1])
        btn_voltar.bind(on_press=lambda x: setattr(self.manager, 'current', 'empresa'))
        
        btn_layout.add_widget(btn_relatorio)
        btn_layout.add_widget(btn_urna)
        btn_layout.add_widget(btn_voltar)
        layout.add_widget(btn_layout)
        
        self.message_label = Label(text='', font_size='16sp', bold=True)
        layout.add_widget(self.message_label)
        
        self.add_widget(layout)
        
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
    def on_enter(self):
        self.atualizar_candidatos()
        
    def adicionar_candidato(self, instance):
        numero = self.numero_input.text.strip()
        nome = self.nome_input.text.strip()
        cargo = self.cargo_input.text.strip() or "Membro CIPA"
        
        if not numero or not nome:
            self.message_label.text = "Preencha número e nome"
            self.message_label.color = [1, 0, 0, 1]
            return
            
        app = App.get_running_app()
        app.sistema.adicionar_candidato(numero, nome, cargo)
        
        self.message_label.text = f"Candidato {nome} adicionado"
        self.message_label.color = [0, 0.8, 0, 1]
        
        self.numero_input.text = ''
        self.nome_input.text = ''
        self.cargo_input.text = ''
        
        self.atualizar_candidatos()
        
    def atualizar_candidatos(self):
        self.candidatos_layout.clear_widgets()
        app = App.get_running_app()
        candidatos = app.sistema.obter_candidatos()
        
        for num, candidato in candidatos.items():
            item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
            
            info_label = Label(text=f"🔢 {num} - 👤 {candidato['nome']} - 🎯 {candidato['cargo']} - 🗳️ {candidato['votos']} votos",
                              size_hint_x=0.8, color=[0.9, 0.9, 0.9, 1])
            item_layout.add_widget(info_label)
            
            self.candidatos_layout.add_widget(item_layout)
            
    def mostrar_relatorio(self, instance):
        app = App.get_running_app()
        resultados = app.sistema.obter_resultados()
        
        relatorio = "📊 RELATÓRIO DE VOTAÇÃO\n\n"
        relatorio += f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        
        total_votos = sum(candidato['votos'] for _, candidato in resultados)
        relatorio += f"🗳️ Total de votos: {total_votos}\n\n"
        
        for i, (num, candidato) in enumerate(resultados, 1):
            percentual = (candidato['votos'] / total_votos * 100) if total_votos > 0 else 0
            relatorio += f"{i}º - {candidato['nome']}\n"
            relatorio += f"    Votos: {candidato['votos']} ({percentual:.1f}%)\n\n"
            
        # Log de votantes
        relatorio += "\n📋 LOG DE VOTAÇÃO:\n"
        for voto in app.sistema.votantes_log[-10:]:  # Últimos 10 votos
            relatorio += f"🕐 {voto['data']} {voto['hora']} - Candidato {voto['candidato']}\n"
        
        popup = Popup(title='Relatório de Votação',
                     content=Label(text=relatorio, text_size=(400, None)),
                     size_hint=(0.8, 0.8))
        popup.open()

class UrnaApp(App):
    def __init__(self, **kwargs):
        super(UrnaApp, self).__init__(**kwargs)
        self.sistema = SistemaUrnaEletronica()
        
    def build(self):
        sm = ScreenManager()
        sm.add_widget(EmpresaScreen(name='empresa'))
        sm.add_widget(UrnaScreen(name='urna'))
        sm.add_widget(AdminScreen(name='admin'))
        return sm

if __name__ == '__main__':
    try:
        UrnaApp().run()
    except Exception as e:
        print(f"ERRO: {e}")
        traceback.print_exc()
        sys.exit(1)