import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, Rectangle, RoundedRectangle, Ellipse, Line
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.widget import Widget
from datetime import datetime
import json
import os

kivy.require('2.0.0')

Window.clearcolor = (0.05, 0.05, 0.1, 1)
Window.size = (1200, 800)

class IconWidget(Widget):
    def __init__(self, icon_type, color=[1, 1, 1, 1], **kwargs):
        super().__init__(**kwargs)
        self.icon_type = icon_type
        self.icon_color = color
        self.size_hint = (None, None)
        self.size = (40, 40)
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.update_graphics()
        
    def update_graphics(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(*self.icon_color)
            cx, cy = self.center_x, self.center_y
            
            if self.icon_type == 'fire':
                points = [cx, cy-15, cx-8, cy-5, cx-5, cy+5, cx, cy+15, cx+5, cy+5, cx+8, cy-5]
                Line(points=points, width=3, close=True)
                
            elif self.icon_type == 'add':
                Line(points=[cx-10, cy, cx+10, cy], width=4)
                Line(points=[cx, cy-10, cx, cy+10], width=4)
                
            elif self.icon_type == 'search':
                Line(circle=(cx, cy, 8), width=2)
                Line(points=[cx+6, cy-6, cx+12, cy-12], width=3)
                
            elif self.icon_type == 'chart':
                Line(points=[cx-12, cy-8, cx-4, cy+4, cx+4, cy-2, cx+12, cy+8], width=3)
                Line(points=[cx-15, cy-12, cx+15, cy-12], width=2)
                Line(points=[cx-15, cy-12, cx-15, cy+12], width=2)
                
            elif self.icon_type == 'report':
                Rectangle(pos=(cx-8, cy-12), size=(16, 24))
                Line(points=[cx-5, cy+5, cx+5, cy+5], width=2)
                Line(points=[cx-5, cy, cx+5, cy], width=2)
                Line(points=[cx-5, cy-5, cx+5, cy-5], width=2)
                
            elif self.icon_type == 'ok':
                Line(points=[cx-8, cy, cx-2, cy-6, cx+8, cy+6], width=4)
                
            elif self.icon_type == 'warning':
                points = [cx, cy+10, cx-10, cy-8, cx+10, cy-8]
                Line(points=points, width=3, close=True)
                Ellipse(pos=(cx-2, cy-2), size=(4, 4))
                
            elif self.icon_type == 'total':
                Line(circle=(cx, cy, 12), width=2)
                Line(points=[cx-6, cy, cx+6, cy], width=2)
                Line(points=[cx, cy-6, cx, cy+6], width=2)

class ModernCard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        
        with self.canvas.before:
            Color(0.15, 0.15, 0.25, 0.9)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[15])
        
        self.bind(size=self._update_graphics, pos=self._update_graphics)
        
    def _update_graphics(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class GlowButton(Button):
    def __init__(self, bg_color=(0.2, 0.4, 0.8, 0.8), **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.font_size = '16sp'
        self.bold = True
        self.bg_color = bg_color
        
        # Definir cor do texto
        self.color = (0, 1, 0, 1)  # Verde para todos os botões
        
        with self.canvas.before:
            Color(*self.bg_color)
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[10])
        
        self.bind(size=self._update_graphics, pos=self._update_graphics)
        self.bind(on_press=self._animate_press)
        
    def _update_graphics(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos
        
    def _animate_press(self, *args):
        anim = Animation(size=(self.width * 0.95, self.height * 0.95), duration=0.1)
        anim += Animation(size=(self.width, self.height), duration=0.1)
        anim.start(self)

class ModernInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Transparente
        self.foreground_color = (1, 0.6, 0.2, 1)  # Cor laranja
        self.cursor_color = (1, 0.6, 0.2, 1)      # Cursor laranja
        self.selection_color = (1, 0.6, 0.2, 0.5) # Seleção laranja
        self.font_size = '14sp'
        self.padding = [10, 10, 10, 10]  # left, top, right, bottom
        
        with self.canvas.before:
            Color(0.2, 0.2, 0.3, 0.9)
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[8])
        
        self.bind(size=self._update_graphics, pos=self._update_graphics)
        
    def _update_graphics(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

class ExtintorData:
    def __init__(self):
        self.arquivo = 'extintores_data.json'
        self.extintores = self.carregar_dados()
        
    def carregar_dados(self):
        if os.path.exists(self.arquivo):
            try:
                with open(self.arquivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return self.dados_exemplo()
        
    def salvar_dados(self):
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            json.dump(self.extintores, f, indent=2, ensure_ascii=False)
            
    def dados_exemplo(self):
        return [
            {"id": 1, "numero": "EXT-001", "tipo": "Pó Químico ABC", "capacidade": "6kg", "localizacao": "Recepção Principal", "setor": "Administrativo", "data_fabricacao": "15/03/2022", "data_vencimento": "15/03/2025", "responsavel": "João Silva", "status": "Ativo", "observacoes": "Em perfeito estado"},
            {"id": 2, "numero": "EXT-002", "tipo": "CO2", "capacidade": "5kg", "localizacao": "Sala de Servidores", "setor": "TI", "data_fabricacao": "20/05/2021", "data_vencimento": "20/05/2024", "responsavel": "Maria Santos", "status": "Ativo", "observacoes": "Pressão OK"},
            {"id": 3, "numero": "EXT-003", "tipo": "Água Pressurizada", "capacidade": "10L", "localizacao": "Corredor 1º Andar", "setor": "Administrativo", "data_fabricacao": "10/01/2023", "data_vencimento": "10/01/2026", "responsavel": "Carlos Lima", "status": "Ativo", "observacoes": "Novo"},
            {"id": 4, "numero": "EXT-004", "tipo": "Pó Químico BC", "capacidade": "4kg", "localizacao": "Oficina Mecânica", "setor": "Manutenção", "data_fabricacao": "05/08/2020", "data_vencimento": "05/08/2023", "responsavel": "Pedro Costa", "status": "Vencido", "observacoes": "Necessita recarga"},
            {"id": 5, "numero": "EXT-005", "tipo": "Espuma", "capacidade": "9L", "localizacao": "Cozinha Industrial", "setor": "Alimentação", "data_fabricacao": "22/11/2022", "data_vencimento": "22/11/2025", "responsavel": "Ana Souza", "status": "Ativo", "observacoes": "Inspeção em dia"},
            {"id": 6, "numero": "EXT-006", "tipo": "CO2", "capacidade": "5kg", "localizacao": "Laboratório Química", "setor": "Pesquisa", "data_fabricacao": "18/04/2021", "data_vencimento": "18/04/2024", "responsavel": "Dr. Roberto", "status": "Ativo", "observacoes": "Área sensível"},
            {"id": 7, "numero": "EXT-007", "tipo": "Pó Químico ABC", "capacidade": "6kg", "localizacao": "Almoxarifado", "setor": "Estoque", "data_fabricacao": "30/09/2022", "data_vencimento": "30/09/2025", "responsavel": "Luis Pereira", "status": "Ativo", "observacoes": "OK"},
            {"id": 8, "numero": "EXT-008", "tipo": "Água Pressurizada", "capacidade": "10L", "localizacao": "Sala de Reuniões", "setor": "Administrativo", "data_fabricacao": "12/06/2019", "data_vencimento": "12/06/2022", "responsavel": "Fernanda Dias", "status": "Vencido", "observacoes": "Substituir urgente"},
            {"id": 9, "numero": "EXT-009", "tipo": "Pó Químico BC", "capacidade": "4kg", "localizacao": "Garagem", "setor": "Transporte", "data_fabricacao": "25/02/2023", "data_vencimento": "25/02/2026", "responsavel": "Marcos Auto", "status": "Ativo", "observacoes": "Novo equipamento"},
            {"id": 10, "numero": "EXT-010", "tipo": "CO2", "capacidade": "5kg", "localizacao": "Data Center", "setor": "TI", "data_fabricacao": "08/12/2021", "data_vencimento": "08/12/2024", "responsavel": "Tech Support", "status": "Ativo", "observacoes": "Ambiente controlado"},
            {"id": 11, "numero": "EXT-011", "tipo": "Espuma", "capacidade": "9L", "localizacao": "Refeitório", "setor": "Alimentação", "data_fabricacao": "14/07/2022", "data_vencimento": "14/07/2025", "responsavel": "Chef Maria", "status": "Ativo", "observacoes": "Área de cocção"},
            {"id": 12, "numero": "EXT-012", "tipo": "Pó Químico ABC", "capacidade": "6kg", "localizacao": "Biblioteca", "setor": "Educação", "data_fabricacao": "03/10/2020", "data_vencimento": "03/10/2023", "responsavel": "Bibliotecária", "status": "Vencido", "observacoes": "Área com papel"},
            {"id": 13, "numero": "EXT-013", "tipo": "Água Pressurizada", "capacidade": "10L", "localizacao": "Auditório", "setor": "Eventos", "data_fabricacao": "19/01/2023", "data_vencimento": "19/01/2026", "responsavel": "Coord. Eventos", "status": "Ativo", "observacoes": "Grande público"},
            {"id": 14, "numero": "EXT-014", "tipo": "CO2", "capacidade": "5kg", "localizacao": "Sala Elétrica", "setor": "Elétrica", "data_fabricacao": "27/05/2021", "data_vencimento": "27/05/2024", "responsavel": "Eletricista", "status": "Ativo", "observacoes": "Equipamentos elétricos"},
            {"id": 15, "numero": "EXT-015", "tipo": "Pó Químico BC", "capacidade": "4kg", "localizacao": "Laboratório Física", "setor": "Pesquisa", "data_fabricacao": "11/09/2022", "data_vencimento": "11/09/2025", "responsavel": "Prof. Carlos", "status": "Ativo", "observacoes": "Experimentos"},
            {"id": 16, "numero": "EXT-016", "tipo": "Espuma", "capacidade": "9L", "localizacao": "Posto Combustível", "setor": "Combustível", "data_fabricacao": "06/03/2021", "data_vencimento": "06/03/2024", "responsavel": "Frentista", "status": "Ativo", "observacoes": "Área de risco"},
            {"id": 17, "numero": "EXT-017", "tipo": "Pó Químico ABC", "capacidade": "6kg", "localizacao": "Enfermaria", "setor": "Saúde", "data_fabricacao": "23/08/2019", "data_vencimento": "23/08/2022", "responsavel": "Enfermeira", "status": "Vencido", "observacoes": "Área médica"},
            {"id": 18, "numero": "EXT-018", "tipo": "Água Pressurizada", "capacidade": "10L", "localizacao": "Vestiário Masculino", "setor": "Vestiários", "data_fabricacao": "15/12/2022", "data_vencimento": "15/12/2025", "responsavel": "Zelador", "status": "Ativo", "observacoes": "Área úmida"},
            {"id": 19, "numero": "EXT-019", "tipo": "CO2", "capacidade": "5kg", "localizacao": "Arquivo Morto", "setor": "Arquivo", "data_fabricacao": "09/04/2021", "data_vencimento": "09/04/2024", "responsavel": "Arquivista", "status": "Ativo", "observacoes": "Documentos importantes"},
            {"id": 20, "numero": "EXT-020", "tipo": "Pó Químico BC", "capacidade": "4kg", "localizacao": "Sala Geradores", "setor": "Energia", "data_fabricacao": "28/07/2020", "data_vencimento": "28/07/2023", "responsavel": "Técnico Energia", "status": "Vencido", "observacoes": "Equipamentos pesados"},
            {"id": 21, "numero": "EXT-021", "tipo": "Espuma", "capacidade": "9L", "localizacao": "Lavanderia", "setor": "Limpeza", "data_fabricacao": "17/11/2022", "data_vencimento": "17/11/2025", "responsavel": "Lavadeira", "status": "Ativo", "observacoes": "Produtos químicos"},
            {"id": 22, "numero": "EXT-022", "tipo": "Pó Químico ABC", "capacidade": "6kg", "localizacao": "Recepção Visitantes", "setor": "Recepção", "data_fabricacao": "04/06/2023", "data_vencimento": "04/06/2028", "responsavel": "Recepcionista", "status": "Ativo", "observacoes": "Área pública"},
            {"id": 23, "numero": "EXT-023", "tipo": "Água Pressurizada", "capacidade": "10L", "localizacao": "Corredor 2º Andar", "setor": "Administrativo", "data_fabricacao": "21/01/2021", "data_vencimento": "21/01/2024", "responsavel": "Segurança", "status": "Ativo", "observacoes": "Rota de fuga"},
            {"id": 24, "numero": "EXT-024", "tipo": "CO2", "capacidade": "5kg", "localizacao": "Sala Controle", "setor": "Operações", "data_fabricacao": "13/09/2020", "data_vencimento": "13/09/2023", "responsavel": "Operador", "status": "Vencido", "observacoes": "Centro de controle"},
            {"id": 25, "numero": "EXT-025", "tipo": "Pó Químico BC", "capacidade": "4kg", "localizacao": "Oficina Soldas", "setor": "Soldas", "data_fabricacao": "07/05/2022", "data_vencimento": "07/05/2025", "responsavel": "Soldador", "status": "Ativo", "observacoes": "Trabalho a quente"},
            {"id": 26, "numero": "EXT-026", "tipo": "Espuma", "capacidade": "9L", "localizacao": "Depósito Tintas", "setor": "Pintura", "data_fabricacao": "26/10/2021", "data_vencimento": "26/10/2024", "responsavel": "Pintor", "status": "Ativo", "observacoes": "Materiais inflamáveis"},
            {"id": 27, "numero": "EXT-027", "tipo": "Pó Químico ABC", "capacidade": "6kg", "localizacao": "Sala Treinamento", "setor": "RH", "data_fabricacao": "18/02/2019", "data_vencimento": "18/02/2022", "responsavel": "Instrutor", "status": "Vencido", "observacoes": "Capacitação"},
            {"id": 28, "numero": "EXT-028", "tipo": "Água Pressurizada", "capacidade": "10L", "localizacao": "Vestiário Feminino", "setor": "Vestiários", "data_fabricacao": "12/08/2022", "data_vencimento": "12/08/2025", "responsavel": "Zeladora", "status": "Ativo", "observacoes": "Área feminina"},
            {"id": 29, "numero": "EXT-029", "tipo": "CO2", "capacidade": "5kg", "localizacao": "Sala Reunião VIP", "setor": "Executivo", "data_fabricacao": "01/12/2021", "data_vencimento": "01/12/2024", "responsavel": "Secretária", "status": "Ativo", "observacoes": "Área executiva"},
            {"id": 30, "numero": "EXT-030", "tipo": "Pó Químico BC", "capacidade": "4kg", "localizacao": "Estacionamento", "setor": "Externo", "data_fabricacao": "29/03/2020", "data_vencimento": "29/03/2023", "responsavel": "Porteiro", "status": "Vencido", "observacoes": "Área externa"},
            {"id": 31, "numero": "EXT-031", "tipo": "Pó Químico ABC", "capacidade": "4kg", "localizacao": "Corredor Bloco B", "setor": "Administrativo", "data_fabricacao": "10/01/2024", "data_vencimento": "10/01/2029", "responsavel": "Ana Paula", "status": "Ativo", "observacoes": "Instalado recentemente"},
            {"id": 32, "numero": "EXT-032", "tipo": "Água Pressurizada", "capacidade": "10L", "localizacao": "Pátio Interno", "setor": "Externo", "data_fabricacao": "15/02/2024", "data_vencimento": "15/02/2029", "responsavel": "Segurança Patrimonial", "status": "Ativo", "observacoes": "Verificar abrigo"},
            {"id": 33, "numero": "EXT-033", "tipo": "CO2", "capacidade": "6kg", "localizacao": "Painel Elétrico Central", "setor": "Elétrica", "data_fabricacao": "01/03/2024", "data_vencimento": "01/03/2029", "responsavel": "Eletricista Chefe", "status": "Ativo", "observacoes": "Acesso restrito"},
            {"id": 34, "numero": "EXT-034", "tipo": "Pó Químico BC", "capacidade": "8kg", "localizacao": "Depósito de Inflamáveis", "setor": "Estoque", "data_fabricacao": "20/03/2024", "data_vencimento": "20/03/2029", "responsavel": "Almoxarife", "status": "Ativo", "observacoes": "Sinalização reforçada"},
            {"id": 35, "numero": "EXT-035", "tipo": "Espuma", "capacidade": "10L", "localizacao": "Garagem - Subsolo 1", "setor": "Transporte", "data_fabricacao": "05/04/2024", "data_vencimento": "05/04/2029", "responsavel": "Manobrista", "status": "Ativo", "observacoes": "Próximo à rampa"},
            {"id": 36, "numero": "EXT-036", "tipo": "Pó Químico ABC", "capacidade": "2kg", "localizacao": "Veículo de Transporte 1", "setor": "Transporte", "data_fabricacao": "10/04/2024", "data_vencimento": "10/04/2025", "responsavel": "Motorista A", "status": "Ativo", "observacoes": "Extintor veicular"},
            {"id": 37, "numero": "EXT-037", "tipo": "Água Pressurizada", "capacidade": "10L", "localizacao": "Entrada de Serviço", "setor": "Serviços Gerais", "data_fabricacao": "25/04/2024", "data_vencimento": "25/04/2029", "responsavel": "Portaria", "status": "Ativo", "observacoes": ""},
            {"id": 38, "numero": "EXT-038", "tipo": "CO2", "capacidade": "6kg", "localizacao": "Sala de Projeção", "setor": "Eventos", "data_fabricacao": "02/05/2024", "data_vencimento": "02/05/2029", "responsavel": "Técnico de Som", "status": "Ativo", "observacoes": "Equipamento sensível"},
            {"id": 39, "numero": "EXT-039", "tipo": "Pó Químico BC", "capacidade": "4kg", "localizacao": "Casa de Bombas", "setor": "Manutenção", "data_fabricacao": "15/05/2024", "data_vencimento": "15/05/2029", "responsavel": "Bombeiro Hidráulico", "status": "Ativo", "observacoes": "Verificar umidade"},
            {"id": 40, "numero": "EXT-040", "tipo": "Espuma", "capacidade": "50L", "localizacao": "Hangar", "setor": "Aviação", "data_fabricacao": "20/05/2024", "data_vencimento": "20/05/2029", "responsavel": "Mecânico de Aeronaves", "status": "Ativo", "observacoes": "Extintor sobre rodas"},
            {"id": 41, "numero": "EXT-041", "tipo": "Pó Químico ABC", "capacidade": "12kg", "localizacao": "Depósito Central", "setor": "Estoque", "data_fabricacao": "01/06/2024", "data_vencimento": "01/06/2029", "responsavel": "Chefe de Estoque", "status": "Ativo", "observacoes": "Próximo ao portão 3"},
            {"id": 42, "numero": "EXT-042", "tipo": "Água Pressurizada", "capacidade": "10L", "localizacao": "Ginásio de Esportes", "setor": "Lazer", "data_fabricacao": "10/06/2024", "data_vencimento": "10/06/2029", "responsavel": "Professor Ed. Física", "status": "Ativo", "observacoes": ""},
            {"id": 43, "numero": "EXT-043", "tipo": "CO2", "capacidade": "2kg", "localizacao": "Bancada Eletrônica", "setor": "Manutenção", "data_fabricacao": "15/06/2024", "data_vencimento": "15/06/2029", "responsavel": "Técnico Eletrônico", "status": "Ativo", "observacoes": "Para pequenos focos"},
            {"id": 44, "numero": "EXT-044", "tipo": "Pó Químico BC", "capacidade": "6kg", "localizacao": "Estação de Gás", "setor": "Energia", "data_fabricacao": "20/06/2024", "data_vencimento": "20/06/2029", "responsavel": "Técnico de Gás", "status": "Ativo", "observacoes": "Área de alta periculosidade"},
            {"id": 45, "numero": "EXT-045", "tipo": "Pó Químico ABC", "capacidade": "4kg", "localizacao": "Ambulatório", "setor": "Saúde", "data_fabricacao": "01/07/2024", "data_vencimento": "01/07/2029", "responsavel": "Enfermeiro Chefe", "status": "Ativo", "observacoes": "Próximo à farmácia"}
        ]

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        with self.canvas.before:
            Color(0.4, 0.8, 0.67, 1)
            self.bg = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)
        
        layout = BoxLayout(orientation='vertical', padding=40, spacing=30)
        
        # Header
        header = BoxLayout(orientation='vertical', size_hint_y=0.3, spacing=20)
        
        title_layout = BoxLayout(orientation='horizontal', spacing=15)
        title_icon = IconWidget('fire', color=[1, 0.8, 0.2, 1])
        title_icon.size = (60, 60)
        title_label = Label(text='EXTINTOR MANAGER', font_size='48sp', bold=True,
                           color=[1, 0.8, 0.2, 1])
        title_layout.add_widget(title_icon)
        title_layout.add_widget(title_label)
        
        subtitle = Label(text='Sistema Moderno de Gerenciamento de Extintores',
                        font_size='18sp', color=[1, 0.27, 0, 1])
        
        header.add_widget(title_layout)
        header.add_widget(subtitle)
        layout.add_widget(header)
        
        # Cards de navegação
        cards_layout = GridLayout(cols=2, spacing=30, size_hint_y=0.7)
        
        # Card Cadastro
        cadastro_card = ModernCard(size_hint=(1, 1))
        cadastro_icon = IconWidget('add', color=[0.4, 0.8, 1, 1])
        cadastro_icon.size = (64, 64)
        cadastro_title = Label(text='CADASTRO', font_size='24sp', bold=True, color=[0.4, 0.8, 1, 1])
        cadastro_desc = Label(text='Cadastrar novos extintores\nGerenciar informações',
                             font_size='14sp', color=[0.8, 0.8, 0.9, 1])
        cadastro_btn = GlowButton(text='ACESSAR', size_hint_y=None, height=50, bg_color=(1, 0.84, 0, 0.8))
        cadastro_btn.bind(on_press=self.go_cadastro)
        
        cadastro_card.add_widget(cadastro_icon)
        cadastro_card.add_widget(cadastro_title)
        cadastro_card.add_widget(cadastro_desc)
        cadastro_card.add_widget(cadastro_btn)
        
        # Card Consulta
        consulta_card = ModernCard(size_hint=(1, 1))
        consulta_icon = IconWidget('search', color=[0.2, 0.8, 0.2, 1])
        consulta_icon.size = (64, 64)
        consulta_title = Label(text='CONSULTA', font_size='24sp', bold=True, color=[0.2, 0.8, 0.2, 1])
        consulta_desc = Label(text='Consultar e filtrar\nExtintores cadastrados',
                             font_size='14sp', color=[0.8, 0.8, 0.9, 1])
        consulta_btn = GlowButton(text='ACESSAR', size_hint_y=None, height=50, bg_color=(0.2, 0.8, 0.2, 0.8))
        consulta_btn.bind(on_press=self.go_consulta)
        
        consulta_card.add_widget(consulta_icon)
        consulta_card.add_widget(consulta_title)
        consulta_card.add_widget(consulta_desc)
        consulta_card.add_widget(consulta_btn)
        
        # Card Dashboard
        dashboard_card = ModernCard(size_hint=(1, 1))
        dashboard_icon = IconWidget('chart', color=[0.8, 0.4, 1, 1])
        dashboard_icon.size = (64, 64)
        dashboard_title = Label(text='DASHBOARD', font_size='24sp', bold=True, color=[0.8, 0.4, 1, 1])
        dashboard_desc = Label(text='Visão geral do sistema\nIndicadores e estatísticas',
                              font_size='14sp', color=[0.8, 0.8, 0.9, 1])
        dashboard_btn = GlowButton(text='ACESSAR', size_hint_y=None, height=50, bg_color=(0.8, 0.4, 1, 0.8))
        dashboard_btn.bind(on_press=self.go_dashboard)
        
        dashboard_card.add_widget(dashboard_icon)
        dashboard_card.add_widget(dashboard_title)
        dashboard_card.add_widget(dashboard_desc)
        dashboard_card.add_widget(dashboard_btn)
        
        # Card Relatórios
        relatorio_card = ModernCard(size_hint=(1, 1))
        relatorio_icon = IconWidget('report', color=[1, 0.6, 0.2, 1])
        relatorio_icon.size = (64, 64)
        relatorio_title = Label(text='RELATÓRIOS', font_size='24sp', bold=True, color=[1, 0.6, 0.2, 1])
        relatorio_desc = Label(text='Gerar relatórios\nAnálises e estatísticas',
                              font_size='14sp', color=[0.8, 0.8, 0.9, 1])
        relatorio_btn = GlowButton(text='ACESSAR', size_hint_y=None, height=50, bg_color=(1, 0.6, 0.2, 0.8))
        relatorio_btn.bind(on_press=self.go_relatorio)
        
        relatorio_card.add_widget(relatorio_icon)
        relatorio_card.add_widget(relatorio_title)
        relatorio_card.add_widget(relatorio_desc)
        relatorio_card.add_widget(relatorio_btn)
        
        cards_layout.add_widget(cadastro_card)
        cards_layout.add_widget(consulta_card)
        cards_layout.add_widget(dashboard_card)
        cards_layout.add_widget(relatorio_card)
        
        layout.add_widget(cards_layout)
        self.add_widget(layout)
        
        Clock.schedule_once(self.animate_entrance, 0.1)
        
    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos
        
    def animate_entrance(self, dt):
        for child in self.children[0].children:
            child.opacity = 0
            anim = Animation(opacity=1, duration=0.8)
            anim.start(child)
            
    def go_cadastro(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'cadastro'
        
    def go_consulta(self, instance):
        self.manager.transition = SlideTransition(direction='up')
        self.manager.current = 'consulta'
        
    def go_relatorio(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'relatorio'
        
    def go_dashboard(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'dashboard'

class CadastroScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_index = 0
        
        with self.canvas.before:
            Color(0.5, 1, 0.83, 1)
            self.bg = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)
        
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=80)
        
        back_btn = GlowButton(text='VOLTAR', size_hint_x=None, width=120, bg_color=(0.4, 0.8, 0.67, 1))
        back_btn.bind(on_press=self.go_back)
        
        title = Label(text='[+] CADASTRO DE EXTINTORES', font_size='32sp', bold=True,
                     color=[1, 0.8, 0.2, 1])
        
        header.add_widget(back_btn)
        header.add_widget(title)
        main_layout.add_widget(header)
        
        # Barra de navegação
        nav_card = ModernCard(size_hint_y=None, height=80)
        nav_layout = BoxLayout(orientation='horizontal', spacing=15, padding=10)
        
        # Botão primeiro
        first_btn = GlowButton(text='|<<', size_hint_x=None, width=60, bg_color=(1, 0.84, 0, 0.8))
        first_btn.bind(on_press=self.primeiro_registro)
        
        # Botão anterior
        prev_btn = GlowButton(text='<<', size_hint_x=None, width=60, bg_color=(1, 0.84, 0, 0.8))
        prev_btn.bind(on_press=self.registro_anterior)
        
        # Indicador de posição
        self.position_label = Label(text='0 / 0', font_size='16sp', bold=True, 
                                   color=[1, 0.8, 0.2, 1], size_hint_x=None, width=100)
        
        # Botão próximo
        next_btn = GlowButton(text='>>', size_hint_x=None, width=60, bg_color=(1, 0.84, 0, 0.8))
        next_btn.bind(on_press=self.proximo_registro)
        
        # Botão último
        last_btn = GlowButton(text='>>|', size_hint_x=None, width=60, bg_color=(1, 0.84, 0, 0.8))
        last_btn.bind(on_press=self.ultimo_registro)
        
        # Espaçadores para centralizar
        nav_layout.add_widget(Label())
        nav_layout.add_widget(Label())
        
        nav_layout.add_widget(first_btn)
        nav_layout.add_widget(prev_btn)
        nav_layout.add_widget(self.position_label)
        nav_layout.add_widget(next_btn)
        nav_layout.add_widget(last_btn)
        
        nav_layout.add_widget(Label())
        nav_layout.add_widget(Label())
        
        nav_card.add_widget(nav_layout)
        main_layout.add_widget(nav_card)
        
        # Formulário em card
        form_card = ModernCard()
        form_layout = GridLayout(cols=2, spacing=20, size_hint_y=None)
        form_layout.bind(minimum_height=form_layout.setter('height'))
        
        # Campos do formulário
        campos = [
            ('[#] Número:', 'numero'),
            ('[T] Tipo:', 'tipo'),
            ('[C] Capacidade:', 'capacidade'),
            ('[L] Localização:', 'localizacao'),
            ('[S] Setor:', 'setor'),
            ('[F] Data Fabricação:', 'data_fabricacao'),
            ('[V] Data Vencimento:', 'data_vencimento'),
            ('[D] Data Validade:', 'data_validade'),
            ('[I] Data Inspeção:', 'data_inspecao'),
            ('[M] Data Manutenção:', 'data_manutencao'),
            ('[R] Responsável:', 'responsavel')
        ]
        
        self.inputs = {}
        
        for label_text, field_name in campos:
            label = Label(text=label_text, font_size='16sp', bold=True,
                         color=[1, 0.7, 0.3, 1], size_hint_y=None, height=40,
                         halign='left', text_size=(None, None))
            label.bind(size=label.setter('text_size'))
            
            if field_name == 'tipo':
                input_widget = Spinner(
                    text='Selecione o tipo',
                    values=['Pó Químico ABC', 'Pó Químico BC', 'CO2', 'Água Pressurizada', 'Espuma'],
                    size_hint_y=None, height=40
                )
                form_layout.add_widget(label)
                form_layout.add_widget(input_widget)
                self.inputs[field_name] = input_widget
            elif field_name in ['data_fabricacao', 'data_vencimento', 'data_validade', 'data_inspecao', 'data_manutencao']:
                date_layout = BoxLayout(orientation='horizontal', spacing=5, size_hint_y=None, height=40)
                
                input_widget = TextInput(multiline=False,
                                        background_color=(0.2, 0.2, 0.3, 0.9),
                                        foreground_color=(1, 0.6, 0.2, 1),
                                        cursor_color=(1, 0.6, 0.2, 1),
                                        font_size='14sp',
                                        hint_text='dd/mm/aaaa',
                                        padding=[10, 5, 5, 5])
                
                cal_btn = GlowButton(text='📅', size_hint_x=None, width=50)
                cal_btn.bind(on_press=lambda x, field=field_name: self.show_date_picker(field))
                
                date_layout.add_widget(input_widget)
                date_layout.add_widget(cal_btn)
                
                form_layout.add_widget(label)
                form_layout.add_widget(date_layout)
                self.inputs[field_name] = input_widget
            else:
                input_widget = TextInput(size_hint_y=None, height=40, multiline=False,
                                        background_color=(0.2, 0.2, 0.3, 0.9),
                                        foreground_color=(1, 0.6, 0.2, 1),
                                        cursor_color=(1, 0.6, 0.2, 1),
                                        font_size='14sp',
                                        padding=[10, 5, 5, 5])
                form_layout.add_widget(label)
                form_layout.add_widget(input_widget)
                self.inputs[field_name] = input_widget
            
        # Observações
        obs_label = Label(text='[O] Observações:', font_size='16sp', bold=True,
                         color=[1, 0.7, 0.3, 1], size_hint_y=None, height=40,
                         halign='left', text_size=(None, None))
        obs_label.bind(size=obs_label.setter('text_size'))
        obs_input = TextInput(size_hint_y=None, height=100,
                             background_color=(0.2, 0.2, 0.3, 0.9),
                             foreground_color=(1, 0.6, 0.2, 1),
                             cursor_color=(1, 0.6, 0.2, 1),
                             font_size='14sp',
                             padding=[10, 5, 5, 5])
        
        form_layout.add_widget(obs_label)
        form_layout.add_widget(obs_input)
        self.inputs['observacoes'] = obs_input
        
        scroll = ScrollView()
        scroll.add_widget(form_layout)
        form_card.add_widget(scroll)
        
        # Botões
        btn_layout = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=None, height=60)
        
        new_btn = GlowButton(text='[+] NOVO', bg_color=(0.2, 0.8, 0.2, 0.8))
        new_btn.bind(on_press=self.novo_extintor)
        
        save_btn = GlowButton(text='[S] SALVAR', bg_color=(1, 0.84, 0, 0.8))
        save_btn.bind(on_press=self.salvar_extintor)
        
        delete_btn = GlowButton(text='[X] EXCLUIR', bg_color=(0.8, 0.2, 0.2, 0.8))
        delete_btn.bind(on_press=self.excluir_extintor)
        
        clear_btn = GlowButton(text='[C] LIMPAR', bg_color=(0.8, 0.4, 1, 0.8))
        clear_btn.bind(on_press=self.limpar_campos)
        
        btn_layout.add_widget(new_btn)
        btn_layout.add_widget(save_btn)
        btn_layout.add_widget(delete_btn)
        btn_layout.add_widget(clear_btn)
        
        main_layout.add_widget(form_card)
        main_layout.add_widget(btn_layout)
        
        self.add_widget(main_layout)
        
        # Carregar dados iniciais
        Clock.schedule_once(self.carregar_dados_iniciais, 0.1)
        
    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos
        
    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'home'
        
    def salvar_extintor(self, instance):
        data = {}
        for field, widget in self.inputs.items():
            if hasattr(widget, 'text'):
                data[field] = widget.text
            else:
                data[field] = widget.text if widget.text != 'Selecione o tipo' else ''
                
        required = ['numero', 'tipo', 'capacidade', 'localizacao']
        for field in required:
            if not data.get(field):
                self.show_popup('Erro', f'Campo {field} é obrigatório!')
                return
                
        app = App.get_running_app()
        
        # Verificar se está editando um registro existente
        if app.data.extintores and self.current_index < len(app.data.extintores):
            # Editando registro existente
            extintor_atual = app.data.extintores[self.current_index]
            data['id'] = extintor_atual['id']
            data['data_cadastro'] = extintor_atual.get('data_cadastro', datetime.now().strftime('%d/%m/%Y %H:%M'))
            data['status'] = extintor_atual.get('status', 'Ativo')
            app.data.extintores[self.current_index] = data
            self.show_popup('Sucesso', 'Extintor atualizado com sucesso!')
        else:
            # Criando novo registro
            data['id'] = len(app.data.extintores) + 1
            data['data_cadastro'] = datetime.now().strftime('%d/%m/%Y %H:%M')
            data['status'] = 'Ativo'
            app.data.extintores.append(data)
            self.current_index = len(app.data.extintores) - 1
            self.show_popup('Sucesso', 'Extintor cadastrado com sucesso!')
        
        app.data.salvar_dados()
        self.atualizar_posicao()
        
    def novo_extintor(self, instance):
        self.limpar_campos(None)
        

        
    def excluir_extintor(self, instance):
        app = App.get_running_app()
        if not app.data.extintores or self.current_index >= len(app.data.extintores):
            self.show_popup('Info', 'Nenhum extintor selecionado para excluir')
            return
            
        extintor = app.data.extintores[self.current_index]
        
        # Popup de confirmação
        content = BoxLayout(orientation='vertical', spacing=20, padding=20)
        content.add_widget(Label(text=f'Confirma exclusão do extintor:\n{extintor["numero"]} - {extintor["tipo"]}?', 
                                font_size='16sp', text_size=(400, None), halign='center'))
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        
        sim_btn = GlowButton(text='SIM', bg_color=(0.8, 0.2, 0.2, 0.8))
        nao_btn = GlowButton(text='NÃO', bg_color=(0.2, 0.8, 0.2, 0.8))
        
        btn_layout.add_widget(sim_btn)
        btn_layout.add_widget(nao_btn)
        content.add_widget(btn_layout)
        
        popup = Popup(title='Confirmar Exclusão', content=content, size_hint=(0.6, 0.4))
        
        def confirmar_exclusao(instance):
            app.data.extintores.pop(self.current_index)
            app.data.salvar_dados()
            
            # Ajustar índice se necessário
            if self.current_index >= len(app.data.extintores) and len(app.data.extintores) > 0:
                self.current_index = len(app.data.extintores) - 1
            elif len(app.data.extintores) == 0:
                self.current_index = 0
                
            self.carregar_extintor_atual()
            self.show_popup('Sucesso', 'Extintor excluído com sucesso!')
            popup.dismiss()
            
        sim_btn.bind(on_press=confirmar_exclusao)
        nao_btn.bind(on_press=popup.dismiss)
        popup.open()
        
    def show_date_picker(self, field_name):
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        today = datetime.now()
        
        date_layout = GridLayout(cols=3, spacing=10, size_hint_y=None, height=100)
        
        day_spinner = Spinner(text=str(today.day), values=[str(i) for i in range(1, 32)])
        month_spinner = Spinner(text=str(today.month), values=[str(i) for i in range(1, 13)])
        year_spinner = Spinner(text=str(today.year), values=[str(i) for i in range(2020, 2030)])
        
        date_layout.add_widget(Label(text='Dia', size_hint_y=None, height=30))
        date_layout.add_widget(Label(text='Mês', size_hint_y=None, height=30))
        date_layout.add_widget(Label(text='Ano', size_hint_y=None, height=30))
        
        date_layout.add_widget(day_spinner)
        date_layout.add_widget(month_spinner)
        date_layout.add_widget(year_spinner)
        
        content.add_widget(Label(text='Selecione a data:', font_size='16sp'))
        content.add_widget(date_layout)
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        
        ok_btn = GlowButton(text='OK')
        cancel_btn = GlowButton(text='Cancelar')
        
        btn_layout.add_widget(ok_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)
        
        popup = Popup(title='Selecionar Data', content=content, size_hint=(0.6, 0.5))
        
        def set_date(instance):
            day = day_spinner.text.zfill(2)
            month = month_spinner.text.zfill(2)
            year = year_spinner.text
            date_str = f"{day}/{month}/{year}"
            self.inputs[field_name].text = date_str
            popup.dismiss()
            
        ok_btn.bind(on_press=set_date)
        cancel_btn.bind(on_press=popup.dismiss)
        popup.open()
        
    def limpar_campos(self, instance):
        for widget in self.inputs.values():
            if hasattr(widget, 'text'):
                widget.text = ''
            else:
                widget.text = 'Selecione o tipo'
        # Resetar para modo de novo registro
        self.current_index = -1
        self.atualizar_posicao()
        
    def carregar_dados_iniciais(self, dt):
        app = App.get_running_app()
        if app.data.extintores:
            self.current_index = 0
            self.carregar_extintor_atual()
        self.atualizar_posicao()
        
    def carregar_extintor_atual(self):
        app = App.get_running_app()
        if not app.data.extintores or self.current_index >= len(app.data.extintores):
            self.limpar_campos(None)
            return
            
        extintor = app.data.extintores[self.current_index]
        
        # Preencher campos
        for field, widget in self.inputs.items():
            valor = extintor.get(field, '')
            if hasattr(widget, 'text'):
                widget.text = str(valor)
            else:  # Spinner
                if valor and valor in widget.values:
                    widget.text = valor
                else:
                    widget.text = 'Selecione o tipo'
                    
    def atualizar_posicao(self):
        app = App.get_running_app()
        total = len(app.data.extintores)
        if self.current_index == -1:
            self.position_label.text = f'NOVO / {total}'
        else:
            atual = self.current_index + 1 if total > 0 and self.current_index < total else 0
            self.position_label.text = f'{atual} / {total}'
        
    def primeiro_registro(self, instance):
        app = App.get_running_app()
        if app.data.extintores:
            self.current_index = 0
            self.carregar_extintor_atual()
            self.atualizar_posicao()
            
    def ultimo_registro(self, instance):
        app = App.get_running_app()
        if app.data.extintores:
            self.current_index = len(app.data.extintores) - 1
            self.carregar_extintor_atual()
            self.atualizar_posicao()
            
    def registro_anterior(self, instance):
        app = App.get_running_app()
        if app.data.extintores and self.current_index > 0:
            self.current_index -= 1
            self.carregar_extintor_atual()
            self.atualizar_posicao()
            
    def proximo_registro(self, instance):
        app = App.get_running_app()
        if app.data.extintores and self.current_index < len(app.data.extintores) - 1:
            self.current_index += 1
            self.carregar_extintor_atual()
            self.atualizar_posicao()
                
    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', spacing=20, padding=20)
        content.add_widget(Label(text=message, font_size='16sp'))
        
        btn = GlowButton(text='OK', size_hint_y=None, height=50)
        content.add_widget(btn)
        
        popup = Popup(title=title, content=content, size_hint=(0.6, 0.4))
        btn.bind(on_press=popup.dismiss)
        popup.open()

class ConsultaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        with self.canvas.before:
            Color(0.93, 0.98, 0.68, 1)
            self.bg = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)
        
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=80)
        
        back_btn = GlowButton(text='VOLTAR', size_hint_x=None, width=120, bg_color=(0.4, 0.8, 0.67, 1))
        back_btn.bind(on_press=self.go_back)
        
        title = Label(text='[?] CONSULTA DE EXTINTORES', font_size='32sp', bold=True,
                     color=[1, 0.8, 0.2, 1])
        
        header.add_widget(back_btn)
        header.add_widget(title)
        main_layout.add_widget(header)
        
        # Filtros
        filter_card = ModernCard(size_hint_y=None, height=100)
        filter_layout = BoxLayout(orientation='horizontal', spacing=20)
        
        self.type_filter = Spinner(
            text='Todos os tipos',
            values=['Todos os tipos', 'Pó Químico ABC', 'Pó Químico BC', 'CO2', 'Água Pressurizada', 'Espuma'],
            size_hint_x=0.3,
            background_color=(0.8, 0.4, 1, 0.8)
        )
        
        self.status_filter = Spinner(
            text='Todos os estatus',
            values=['Todos os estatus', 'Ativo', 'Vencido'],
            size_hint_x=0.3,
            background_color=(1, 0.84, 0, 0.8)
        )
        
        filter_btn = GlowButton(text='FILTRAR', size_hint_x=0.2, bg_color=(0.2, 0.8, 0.2, 0.8))
        filter_btn.bind(on_press=self.filtrar_dados)
        
        filter_layout.add_widget(self.type_filter)
        filter_layout.add_widget(self.status_filter)
        filter_layout.add_widget(filter_btn)
        filter_card.add_widget(filter_layout)
        
        # Lista de resultados
        results_card = ModernCard()
        self.results_layout = BoxLayout(orientation='vertical', spacing=10)
        
        scroll = ScrollView()
        scroll.add_widget(self.results_layout)
        results_card.add_widget(scroll)
        
        main_layout.add_widget(filter_card)
        main_layout.add_widget(results_card)
        self.add_widget(main_layout)
        
        Clock.schedule_once(self.load_data, 0.1)
        
    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos
        
    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='down')
        self.manager.current = 'home'
        
    def load_data(self, dt):
        app = App.get_running_app()
        self.display_extintores(app.data.extintores)
        
    def filtrar_dados(self, instance):
        app = App.get_running_app()
        extintores = app.data.extintores
        
        # Aplicar filtro de tipo
        if self.type_filter.text != 'Todos os tipos':
            extintores = [e for e in extintores if e.get('tipo', '') == self.type_filter.text]
            
        # Aplicar filtro de status
        if self.status_filter.text != 'Todos os estatus':
            extintores = [e for e in extintores if e.get('status', '') == self.status_filter.text]
            
        self.display_extintores(extintores)
        
    def display_extintores(self, extintores):
        self.results_layout.clear_widgets()
        
        for extintor in extintores:
            item_card = ModernCard(size_hint_y=None, height=120)
            item_layout = BoxLayout(orientation='horizontal', spacing=20)
            
            info_layout = BoxLayout(orientation='vertical')
            
            numero_label = Label(text=f"[*] {extintor.get('numero', 'N/A')}", 
                               font_size='18sp', bold=True, color=[1, 0.8, 0.2, 1])
            tipo_label = Label(text=f"[T] {extintor.get('tipo', 'N/A')}", 
                             font_size='14sp', color=[1, 0.7, 0.3, 1])
            local_label = Label(text=f"[L] {extintor.get('localizacao', 'N/A')}", 
                              font_size='14sp', color=[1, 0.7, 0.3, 1])
            
            info_layout.add_widget(numero_label)
            info_layout.add_widget(tipo_label)
            info_layout.add_widget(local_label)
            
            status_layout = BoxLayout(orientation='vertical', size_hint_x=0.3)
            
            status = extintor.get('status', 'N/A')
            status_color = [0.2, 0.8, 0.2, 1] if status == 'Ativo' else [0.8, 0.2, 0.2, 1]
            
            status_label = Label(text=f"[OK] {status}" if status == 'Ativo' else f"[X] {status}", 
                               font_size='14sp', bold=True, color=status_color)
            venc_label = Label(text=f"[V] {extintor.get('data_vencimento', 'N/A')}", 
                             font_size='12sp', color=[1, 0.7, 0.3, 1])
            
            status_layout.add_widget(status_label)
            status_layout.add_widget(venc_label)
            
            item_layout.add_widget(info_layout)
            item_layout.add_widget(status_layout)
            item_card.add_widget(item_layout)
            
            self.results_layout.add_widget(item_card)

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        with self.canvas.before:
            Color(0.68, 1, 0.18, 1)
            self.bg = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)
        
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=80)
        
        back_btn = GlowButton(text='VOLTAR', size_hint_x=None, width=120, bg_color=(0.4, 0.8, 0.67, 1))
        back_btn.bind(on_press=self.go_back)
        
        title = Label(text='[#] DASHBOARD', font_size='32sp', bold=True,
                     color=[1, 0.8, 0.2, 1])
        
        header.add_widget(back_btn)
        header.add_widget(title)
        main_layout.add_widget(header)
        
        # Cards linha 1
        stats1_layout = GridLayout(cols=3, spacing=20, size_hint_y=0.4)
        
        total_card = ModernCard()
        total_layout = BoxLayout(orientation='vertical')
        total_icon = IconWidget('total', color=[0.4, 0.8, 1, 1])
        total_icon.size = (36, 36)
        total_layout.add_widget(total_icon)
        total_layout.add_widget(Label(text='TOTAL', font_size='16sp', bold=True, color=[0.4, 0.8, 1, 1]))
        self.total_label = Label(text='0', font_size='28sp', bold=True, color=[1, 1, 1, 1])
        total_layout.add_widget(self.total_label)
        total_card.add_widget(total_layout)
        
        ativo_card = ModernCard()
        ativo_layout = BoxLayout(orientation='vertical')
        ativo_icon = IconWidget('ok', color=[0.2, 0.8, 0.2, 1])
        ativo_icon.size = (36, 36)
        ativo_layout.add_widget(ativo_icon)
        ativo_layout.add_widget(Label(text='ATIVOS', font_size='16sp', bold=True, color=[0.2, 0.8, 0.2, 1]))
        self.ativo_label = Label(text='0', font_size='28sp', bold=True, color=[1, 1, 1, 1])
        ativo_layout.add_widget(self.ativo_label)
        ativo_card.add_widget(ativo_layout)
        
        vencido_card = ModernCard()
        vencido_layout = BoxLayout(orientation='vertical')
        vencido_icon = IconWidget('warning', color=[0.8, 0.2, 0.2, 1])
        vencido_icon.size = (36, 36)
        vencido_layout.add_widget(vencido_icon)
        vencido_layout.add_widget(Label(text='VENCIDOS', font_size='16sp', bold=True, color=[0.8, 0.2, 0.2, 1]))
        self.vencido_label = Label(text='0', font_size='28sp', bold=True, color=[1, 1, 1, 1])
        vencido_layout.add_widget(self.vencido_label)
        vencido_card.add_widget(vencido_layout)
        
        stats1_layout.add_widget(total_card)
        stats1_layout.add_widget(ativo_card)
        stats1_layout.add_widget(vencido_card)
        
        # Cards linha 2
        stats2_layout = GridLayout(cols=3, spacing=20, size_hint_y=0.4)
        
        tipos_card = ModernCard()
        tipos_layout = BoxLayout(orientation='vertical')
        tipos_icon = IconWidget('fire', color=[0.8, 0.4, 1, 1])
        tipos_icon.size = (36, 36)
        tipos_layout.add_widget(tipos_icon)
        tipos_layout.add_widget(Label(text='TIPOS', font_size='16sp', bold=True, color=[0.8, 0.4, 1, 1]))
        self.tipos_label = Label(text='0', font_size='28sp', bold=True, color=[1, 1, 1, 1])
        tipos_layout.add_widget(self.tipos_label)
        tipos_card.add_widget(tipos_layout)
        
        setores_card = ModernCard()
        setores_layout = BoxLayout(orientation='vertical')
        setores_icon = IconWidget('chart', color=[1, 0.6, 0.2, 1])
        setores_icon.size = (36, 36)
        setores_layout.add_widget(setores_icon)
        setores_layout.add_widget(Label(text='SETORES', font_size='16sp', bold=True, color=[1, 0.6, 0.2, 1]))
        self.setores_label = Label(text='0', font_size='28sp', bold=True, color=[1, 1, 1, 1])
        setores_layout.add_widget(self.setores_label)
        setores_card.add_widget(setores_layout)
        
        resp_card = ModernCard()
        resp_layout = BoxLayout(orientation='vertical')
        resp_icon = IconWidget('ok', color=[0.2, 0.8, 0.8, 1])
        resp_icon.size = (36, 36)
        resp_layout.add_widget(resp_icon)
        resp_layout.add_widget(Label(text='RESPONSÁVEIS', font_size='16sp', bold=True, color=[0.2, 0.8, 0.8, 1]))
        self.resp_label = Label(text='0', font_size='28sp', bold=True, color=[1, 1, 1, 1])
        resp_layout.add_widget(self.resp_label)
        resp_card.add_widget(resp_layout)
        
        stats2_layout.add_widget(tipos_card)
        stats2_layout.add_widget(setores_card)
        stats2_layout.add_widget(resp_card)
        
        # Cards linha 3 - Extintores por Tipo
        tipos_detail_layout = GridLayout(cols=5, spacing=15, size_hint_y=0.3)
        
        # Pó Químico ABC
        abc_card = ModernCard()
        abc_layout = BoxLayout(orientation='vertical')
        abc_icon = IconWidget('fire', color=[1, 0.4, 0.2, 1])
        abc_icon.size = (24, 24)
        abc_layout.add_widget(abc_icon)
        abc_layout.add_widget(Label(text='PÓ ABC', font_size='12sp', bold=True, color=[1, 0.4, 0.2, 1]))
        self.abc_label = Label(text='0', font_size='20sp', bold=True, color=[1, 1, 1, 1])
        abc_layout.add_widget(self.abc_label)
        abc_card.add_widget(abc_layout)
        
        # Pó Químico BC
        bc_card = ModernCard()
        bc_layout = BoxLayout(orientation='vertical')
        bc_icon = IconWidget('fire', color=[1, 0.6, 0.2, 1])
        bc_icon.size = (24, 24)
        bc_layout.add_widget(bc_icon)
        bc_layout.add_widget(Label(text='PÓ BC', font_size='12sp', bold=True, color=[1, 0.6, 0.2, 1]))
        self.bc_label = Label(text='0', font_size='20sp', bold=True, color=[1, 1, 1, 1])
        bc_layout.add_widget(self.bc_label)
        bc_card.add_widget(bc_layout)
        
        # CO2
        co2_card = ModernCard()
        co2_layout = BoxLayout(orientation='vertical')
        co2_icon = IconWidget('ok', color=[0.4, 0.8, 1, 1])
        co2_icon.size = (24, 24)
        co2_layout.add_widget(co2_icon)
        co2_layout.add_widget(Label(text='CO2', font_size='12sp', bold=True, color=[0.4, 0.8, 1, 1]))
        self.co2_label = Label(text='0', font_size='20sp', bold=True, color=[1, 1, 1, 1])
        co2_layout.add_widget(self.co2_label)
        co2_card.add_widget(co2_layout)
        
        # Água Pressurizada
        agua_card = ModernCard()
        agua_layout = BoxLayout(orientation='vertical')
        agua_icon = IconWidget('total', color=[0.2, 0.8, 1, 1])
        agua_icon.size = (24, 24)
        agua_layout.add_widget(agua_icon)
        agua_layout.add_widget(Label(text='ÁGUA', font_size='12sp', bold=True, color=[0.2, 0.8, 1, 1]))
        self.agua_label = Label(text='0', font_size='20sp', bold=True, color=[1, 1, 1, 1])
        agua_layout.add_widget(self.agua_label)
        agua_card.add_widget(agua_layout)
        
        # Espuma
        espuma_card = ModernCard()
        espuma_layout = BoxLayout(orientation='vertical')
        espuma_icon = IconWidget('warning', color=[0.8, 0.2, 0.8, 1])
        espuma_icon.size = (24, 24)
        espuma_layout.add_widget(espuma_icon)
        espuma_layout.add_widget(Label(text='ESPUMA', font_size='12sp', bold=True, color=[0.8, 0.2, 0.8, 1]))
        self.espuma_label = Label(text='0', font_size='20sp', bold=True, color=[1, 1, 1, 1])
        espuma_layout.add_widget(self.espuma_label)
        espuma_card.add_widget(espuma_layout)
        
        tipos_detail_layout.add_widget(abc_card)
        tipos_detail_layout.add_widget(bc_card)
        tipos_detail_layout.add_widget(co2_card)
        tipos_detail_layout.add_widget(agua_card)
        tipos_detail_layout.add_widget(espuma_card)
        
        main_layout.add_widget(stats1_layout)
        main_layout.add_widget(stats2_layout)
        main_layout.add_widget(tipos_detail_layout)
        self.add_widget(main_layout)
        
        Clock.schedule_once(self.update_stats, 0.1)
        
    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos
        
    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'home'
        
    def update_stats(self, dt):
        app = App.get_running_app()
        extintores = app.data.extintores
        
        total = len(extintores)
        ativos = len([e for e in extintores if e.get('status') == 'Ativo'])
        vencidos = total - ativos
        tipos_unicos = len(set(e.get('tipo', '') for e in extintores))
        setores_unicos = len(set(e.get('setor', '') for e in extintores))
        resp_unicos = len(set(e.get('responsavel', '') for e in extintores))
        
        # Contar extintores por tipo
        abc_count = len([e for e in extintores if e.get('tipo', '') == 'Pó Químico ABC'])
        bc_count = len([e for e in extintores if e.get('tipo', '') == 'Pó Químico BC'])
        co2_count = len([e for e in extintores if e.get('tipo', '') == 'CO2'])
        agua_count = len([e for e in extintores if e.get('tipo', '') == 'Água Pressurizada'])
        espuma_count = len([e for e in extintores if e.get('tipo', '') == 'Espuma'])
        
        self.total_label.text = str(total)
        self.ativo_label.text = str(ativos)
        self.vencido_label.text = str(vencidos)
        self.tipos_label.text = str(tipos_unicos)
        self.setores_label.text = str(setores_unicos)
        self.resp_label.text = str(resp_unicos)
        
        # Atualizar contadores por tipo
        self.abc_label.text = str(abc_count)
        self.bc_label.text = str(bc_count)
        self.co2_label.text = str(co2_count)
        self.agua_label.text = str(agua_count)
        self.espuma_label.text = str(espuma_count)

class RelatorioScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        with self.canvas.before:
            Color(0.9, 0.9, 0.98, 1)
            self.bg = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)
        
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=80)
        
        back_btn = GlowButton(text='VOLTAR', size_hint_x=None, width=120, bg_color=(0.4, 0.8, 0.67, 1))
        back_btn.bind(on_press=self.go_back)
        
        title = Label(text='[@] RELATÓRIOS', font_size='32sp', bold=True,
                     color=[1, 0.8, 0.2, 1])
        
        header.add_widget(back_btn)
        header.add_widget(title)
        main_layout.add_widget(header)
        
        # Opções de relatório
        options_layout = GridLayout(cols=2, spacing=30)
        
        # Relatório Geral
        geral_card = ModernCard()
        geral_layout = BoxLayout(orientation='vertical', spacing=15)
        geral_icon = IconWidget('report', color=[0.4, 0.8, 1, 1])
        geral_icon.size = (48, 48)
        geral_layout.add_widget(geral_icon)
        geral_layout.add_widget(Label(text='RELATÓRIO GERAL', font_size='18sp', bold=True, color=[0.4, 0.8, 1, 1]))
        geral_layout.add_widget(Label(text='= Lista completa de todos\n* os extintores cadastrados', 
                                     font_size='14sp', color=[0.8, 0.8, 0.9, 1]))
        geral_btn = GlowButton(text='[PDF] GERAR PDF', size_hint_y=None, height=50, bg_color=(1, 0.84, 0, 0.8))
        geral_btn.bind(on_press=self.gerar_relatorio_geral)
        geral_layout.add_widget(geral_btn)
        geral_card.add_widget(geral_layout)
        
        # Relatório de Vencimentos
        venc_card = ModernCard()
        venc_layout = BoxLayout(orientation='vertical', spacing=15)
        venc_icon = IconWidget('warning', color=[0.8, 0.4, 0.2, 1])
        venc_icon.size = (48, 48)
        venc_layout.add_widget(venc_icon)
        venc_layout.add_widget(Label(text='VENCIMENTOS', font_size='18sp', bold=True, color=[0.8, 0.4, 0.2, 1]))
        venc_layout.add_widget(Label(text='! Extintores próximos\n> ao vencimento', 
                                    font_size='14sp', color=[0.8, 0.8, 0.9, 1]))
        venc_btn = GlowButton(text='[PDF] GERAR PDF', size_hint_y=None, height=50, bg_color=(0.8, 0.4, 0.2, 0.8))
        venc_btn.bind(on_press=self.gerar_relatorio_vencimentos)
        venc_layout.add_widget(venc_btn)
        venc_card.add_widget(venc_layout)
        
        options_layout.add_widget(geral_card)
        options_layout.add_widget(venc_card)
        
        main_layout.add_widget(options_layout)
        self.add_widget(main_layout)
        
    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos
        
    def go_back(self, instance):
        self.manager.transition = FadeTransition()
        self.manager.current = 'home'
        
    def gerar_relatorio_geral(self, instance):
        app = App.get_running_app()
        extintores = app.data.extintores
        
        relatorio = "📋 RELATÓRIO GERAL DE EXTINTORES\n"
        relatorio += "=" * 50 + "\n\n"
        relatorio += f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        relatorio += f"📊 Total de Extintores: {len(extintores)}\n\n"
        
        for ext in extintores:
            relatorio += f"🔥 {ext['numero']} - {ext['tipo']}\n"
            relatorio += f"   📍 Local: {ext['localizacao']}\n"
            relatorio += f"   🏢 Setor: {ext['setor']}\n"
            relatorio += f"   📏 Capacidade: {ext['capacidade']}\n"
            relatorio += f"   👤 Responsável: {ext['responsavel']}\n"
            relatorio += f"   📅 Vencimento: {ext['data_vencimento']}\n"
            status_icon = "✅" if ext['status'] == 'Ativo' else "❌"
            relatorio += f"   {status_icon} Status: {ext['status']}\n"
            relatorio += f"   💬 Obs: {ext['observacoes']}\n\n"
            
        self.mostrar_relatorio("Relatório Geral", relatorio)
        
    def gerar_relatorio_vencimentos(self, instance):
        app = App.get_running_app()
        extintores = app.data.extintores
        
        vencidos = [e for e in extintores if e['status'] == 'Vencido']
        
        relatorio = "⚠️ RELATÓRIO DE VENCIMENTOS\n"
        relatorio += "=" * 50 + "\n\n"
        relatorio += f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        relatorio += f"⚠️ Extintores Vencidos: {len(vencidos)}\n\n"
        
        if not vencidos:
            relatorio += "✅ Nenhum extintor vencido encontrado!\n"
        else:
            for ext in vencidos:
                relatorio += f"❌ {ext['numero']} - {ext['tipo']}\n"
                relatorio += f"   📍 Local: {ext['localizacao']}\n"
                relatorio += f"   🏢 Setor: {ext['setor']}\n"
                relatorio += f"   📅 Venceu em: {ext['data_vencimento']}\n"
                relatorio += f"   👤 Responsável: {ext['responsavel']}\n"
                relatorio += f"   🚨 Ação: SUBSTITUIR URGENTE\n\n"
                
        self.mostrar_relatorio("Relatório de Vencimentos", relatorio)
        
    def mostrar_relatorio(self, titulo, conteudo):
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        scroll = ScrollView()
        label = Label(text=conteudo, font_size='12sp', text_size=(None, None),
                     halign='left', valign='top', color=[0.9, 0.9, 0.9, 1])
        label.bind(texture_size=label.setter('size'))
        scroll.add_widget(label)
        content.add_widget(scroll)
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        
        save_btn = GlowButton(text='💾 SALVAR PDF')
        save_btn.bind(on_press=lambda x: [self.salvar_relatorio(conteudo, titulo), popup.dismiss()])
        
        close_btn = GlowButton(text='❌ FECHAR')
        
        btn_layout.add_widget(save_btn)
        btn_layout.add_widget(close_btn)
        content.add_widget(btn_layout)
        
        popup = Popup(title=titulo, content=content, size_hint=(0.9, 0.8))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
        
    def salvar_relatorio(self, conteudo, titulo):
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib.colors import HexColor
            import os
            import subprocess
            import platform
            
            filename = f"{titulo.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
            
            doc = SimpleDocTemplate(filename, pagesize=A4)
            styles = getSampleStyleSheet()
            
            # Criar estilos personalizados
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Title'],
                textColor=HexColor('#ff0000'),  # Vermelho para título
                fontSize=18,
                spaceAfter=20
            )
            
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                textColor=HexColor('#191970'),  # Azul escuro para texto
                fontSize=12
            )
            
            story = []
            
            story.append(Paragraph(titulo, title_style))
            story.append(Spacer(1, 0.2*inch))
            
            linhas = conteudo.split('\n')
            for linha in linhas:
                if linha.strip():
                    story.append(Paragraph(linha, normal_style))
                else:
                    story.append(Spacer(1, 0.1*inch))
            
            doc.build(story)
            
            # Abrir o arquivo PDF automaticamente
            try:
                if platform.system() == 'Windows':
                    os.startfile(filename)
                elif platform.system() == 'Darwin':  # macOS
                    subprocess.run(['open', filename])
                else:  # Linux
                    subprocess.run(['xdg-open', filename])
            except:
                pass  # Se não conseguir abrir, continua normalmente
                
            self.show_popup("✅ Sucesso", f"Relatório PDF salvo e aberto:\n{filename}")
        except ImportError:
            filename = f"{titulo.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(conteudo)
            self.show_popup("✅ Sucesso", f"Relatório TXT salvo:\n{filename}")
        except Exception as e:
            self.show_popup("❌ Erro", f"Erro ao salvar:\n{str(e)}")
            
    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', spacing=20, padding=20)
        content.add_widget(Label(text=message, font_size='16sp'))
        
        btn = GlowButton(text='OK', size_hint_y=None, height=50)
        content.add_widget(btn)
        
        popup = Popup(title=title, content=content, size_hint=(0.6, 0.4))
        btn.bind(on_press=popup.dismiss)
        popup.open()

class ExtintorApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = ExtintorData()
        
    def build(self):
        sm = ScreenManager()
        
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(CadastroScreen(name='cadastro'))
        sm.add_widget(ConsultaScreen(name='consulta'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(RelatorioScreen(name='relatorio'))
        
        return sm

if __name__ == '__main__':
    ExtintorApp().run()