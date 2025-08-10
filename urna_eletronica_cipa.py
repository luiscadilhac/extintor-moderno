import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.widget import Widget
from kivy.animation import Animation
import json
import datetime
import os
import hashlib
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import cv2
import numpy as np
try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False

kivy.require('2.0.0')

class UrnaEletronicaCIPA(App):
    def __init__(self):
        super().__init__()
        self.dados_file = 'dados_urna_cipa.json'
        self.som_tecla = None
        self.som_confirma = None
        self.som_corrige = None
        self.carregar_sons()
        self.dados = self.carregar_dados()
        
    def carregar_sons(self):
        """Carrega os sons da urna eletrônica"""
        try:
            # Sons simulados - você pode adicionar arquivos .wav reais
            self.som_tecla = SoundLoader.load('sons/tecla.wav') if os.path.exists('sons/tecla.wav') else None
            self.som_confirma = SoundLoader.load('sons/confirma.wav') if os.path.exists('sons/confirma.wav') else None
            self.som_corrige = SoundLoader.load('sons/corrige.wav') if os.path.exists('sons/corrige.wav') else None
        except:
            pass
    
    def tocar_som(self, tipo):
        """Toca som específico"""
        try:
            if tipo == 'tecla' and self.som_tecla:
                self.som_tecla.play()
            elif tipo == 'confirma' and self.som_confirma:
                self.som_confirma.play()
            elif tipo == 'corrige' and self.som_corrige:
                self.som_corrige.play()
        except:
            pass
    
    def carregar_dados(self):
        """Carrega dados do arquivo JSON"""
        if os.path.exists(self.dados_file):
            with open(self.dados_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'empresas': {},
            'candidatos': {},
            'votos': {},
            'eleitores': {},
            'configuracoes': {
                'eleicao_ativa': False,
                'data_inicio': '',
                'data_fim': ''
            }
        }
    
    def salvar_dados(self):
        """Salva dados no arquivo JSON"""
        with open(self.dados_file, 'w', encoding='utf-8') as f:
            json.dump(self.dados, f, ensure_ascii=False, indent=2)
    
    def build(self):
        self.title = "Urna Eletrônica CIPA - Sistema Moderno"
        
        # Gerenciador de telas
        sm = ScreenManager(transition=SlideTransition())
        
        # Telas do sistema
        sm.add_widget(TelaInicial(name='inicial'))
        sm.add_widget(TelaEmpresa(name='empresa'))
        sm.add_widget(TelaMesario(name='mesario'))
        sm.add_widget(TelaInscricoes(name='inscricoes'))
        sm.add_widget(TelaVotacao(name='votacao'))
        sm.add_widget(TelaRelatorios(name='relatorios'))
        
        return sm

class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_interface()
    
    def build_interface(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Cabeçalho com logo
        header = BoxLayout(orientation='horizontal', size_hint_y=0.3)
        
        # Logo da urna
        logo_layout = BoxLayout(orientation='vertical')
        logo = Label(
            text='🗳️',
            font_size='80sp',
            size_hint_y=0.6
        )
        titulo = Label(
            text='URNA ELETRÔNICA CIPA',
            font_size='24sp',
            bold=True,
            color=(0.2, 0.4, 0.8, 1)
        )
        logo_layout.add_widget(logo)
        logo_layout.add_widget(titulo)
        header.add_widget(logo_layout)
        
        layout.add_widget(header)
        
        # Menu principal
        menu_layout = GridLayout(cols=2, spacing=20, size_hint_y=0.7)
        
        # Botões do menu
        btn_empresa = self.criar_botao_menu('👔 EMPRESA\nGerenciar', self.ir_empresa)
        btn_mesario = self.criar_botao_menu('👨‍💼 MESÁRIO\nAdministrar', self.ir_mesario)
        btn_inscricoes = self.criar_botao_menu('📝 INSCRIÇÕES\nCandidatos', self.ir_inscricoes)
        btn_votacao = self.criar_botao_menu('🗳️ VOTAÇÃO\nEleitor', self.ir_votacao)
        
        menu_layout.add_widget(btn_empresa)
        menu_layout.add_widget(btn_mesario)
        menu_layout.add_widget(btn_inscricoes)
        menu_layout.add_widget(btn_votacao)
        
        layout.add_widget(menu_layout)
        
        # Rodapé
        rodape = Label(
            text='Sistema de Eleição CIPA - Versão 2024',
            size_hint_y=0.1,
            color=(0.5, 0.5, 0.5, 1)
        )
        layout.add_widget(rodape)
        
        self.add_widget(layout)
    
    def criar_botao_menu(self, texto, callback):
        btn = Button(
            text=texto,
            font_size='18sp',
            bold=True,
            background_color=(0.2, 0.6, 0.9, 1)
        )
        btn.bind(on_press=callback)
        return btn
    
    def ir_empresa(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.manager.current = 'empresa'
    
    def ir_mesario(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.manager.current = 'mesario'
    
    def ir_inscricoes(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.manager.current = 'inscricoes'
    
    def ir_votacao(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.manager.current = 'votacao'

class TelaEmpresa(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_interface()
    
    def build_interface(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Cabeçalho
        header = BoxLayout(orientation='horizontal', size_hint_y=0.15)
        btn_voltar = Button(
            text='← Voltar',
            size_hint_x=0.2,
            background_color=(0.8, 0.3, 0.3, 1)
        )
        btn_voltar.bind(on_press=self.voltar)
        
        titulo = Label(
            text='GESTÃO DE EMPRESAS',
            font_size='24sp',
            bold=True,
            color=(0.2, 0.4, 0.8, 1)
        )
        
        header.add_widget(btn_voltar)
        header.add_widget(titulo)
        layout.add_widget(header)
        
        # Formulário de empresa
        form_layout = GridLayout(cols=2, spacing=10, size_hint_y=0.6)
        
        form_layout.add_widget(Label(text='Nome da Empresa:', halign='right'))
        self.input_nome = TextInput(multiline=False)
        form_layout.add_widget(self.input_nome)
        
        form_layout.add_widget(Label(text='CNPJ:', halign='right'))
        self.input_cnpj = TextInput(multiline=False)
        form_layout.add_widget(self.input_cnpj)
        
        form_layout.add_widget(Label(text='Endereço:', halign='right'))
        self.input_endereco = TextInput(multiline=False)
        form_layout.add_widget(self.input_endereco)
        
        form_layout.add_widget(Label(text='Responsável:', halign='right'))
        self.input_responsavel = TextInput(multiline=False)
        form_layout.add_widget(self.input_responsavel)
        
        layout.add_widget(form_layout)
        
        # Botões de ação
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.15)
        
        btn_cadastrar = Button(
            text='💾 Cadastrar Empresa',
            background_color=(0.2, 0.8, 0.2, 1)
        )
        btn_cadastrar.bind(on_press=self.cadastrar_empresa)
        
        btn_listar = Button(
            text='📋 Listar Empresas',
            background_color=(0.2, 0.6, 0.9, 1)
        )
        btn_listar.bind(on_press=self.listar_empresas)
        
        btn_layout.add_widget(btn_cadastrar)
        btn_layout.add_widget(btn_listar)
        layout.add_widget(btn_layout)
        
        # Lista de empresas
        self.lista_empresas = Label(
            text='Empresas cadastradas aparecerão aqui...',
            text_size=(None, None),
            valign='top',
            size_hint_y=0.1
        )
        layout.add_widget(self.lista_empresas)
        
        self.add_widget(layout)
    
    def cadastrar_empresa(self, instance):
        app = App.get_running_app()
        app.tocar_som('confirma')
        
        if not all([self.input_nome.text, self.input_cnpj.text]):
            self.mostrar_popup('Erro', 'Nome e CNPJ são obrigatórios!')
            return
        
        empresa_id = hashlib.md5(self.input_cnpj.text.encode()).hexdigest()[:8]
        
        app.dados['empresas'][empresa_id] = {
            'nome': self.input_nome.text,
            'cnpj': self.input_cnpj.text,
            'endereco': self.input_endereco.text,
            'responsavel': self.input_responsavel.text,
            'data_cadastro': datetime.datetime.now().isoformat(),
            'codigo_acesso': empresa_id.upper()
        }
        
        app.salvar_dados()
        self.limpar_campos()
        self.mostrar_popup('Sucesso', f'Empresa cadastrada!\nCódigo de acesso: {empresa_id.upper()}')
    
    def listar_empresas(self, instance):
        app = App.get_running_app()
        empresas = app.dados['empresas']
        
        if not empresas:
            self.lista_empresas.text = 'Nenhuma empresa cadastrada.'
            return
        
        texto = 'EMPRESAS CADASTRADAS:\n\n'
        for emp_id, dados in empresas.items():
            texto += f"• {dados['nome']} - Código: {dados['codigo_acesso']}\n"
        
        self.lista_empresas.text = texto
        self.lista_empresas.text_size = (self.width - 40, None)
    
    def limpar_campos(self):
        self.input_nome.text = ''
        self.input_cnpj.text = ''
        self.input_endereco.text = ''
        self.input_responsavel.text = ''
    
    def mostrar_popup(self, titulo, mensagem):
        popup = Popup(
            title=titulo,
            content=Label(text=mensagem),
            size_hint=(0.6, 0.4)
        )
        popup.open()
    
    def voltar(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.manager.current = 'inicial'

class TelaMesario(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_interface()
    
    def build_interface(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Cabeçalho
        header = BoxLayout(orientation='horizontal', size_hint_y=0.15)
        btn_voltar = Button(
            text='← Voltar',
            size_hint_x=0.2,
            background_color=(0.8, 0.3, 0.3, 1)
        )
        btn_voltar.bind(on_press=self.voltar)
        
        titulo = Label(
            text='PAINEL DO MESÁRIO',
            font_size='24sp',
            bold=True,
            color=(0.2, 0.4, 0.8, 1)
        )
        
        header.add_widget(btn_voltar)
        header.add_widget(titulo)
        layout.add_widget(header)
        
        # Menu de opções do mesário
        menu_layout = GridLayout(cols=2, spacing=15, size_hint_y=0.7)
        
        btn_iniciar = self.criar_botao_mesario('🚀 INICIAR\nEleição', self.iniciar_eleicao)
        btn_finalizar = self.criar_botao_mesario('🛑 FINALIZAR\nEleição', self.finalizar_eleicao)
        btn_relatorios = self.criar_botao_mesario('📊 RELATÓRIOS\nResultados', self.ver_relatorios)
        btn_backup = self.criar_botao_mesario('💾 BACKUP\nDados', self.fazer_backup)
        
        menu_layout.add_widget(btn_iniciar)
        menu_layout.add_widget(btn_finalizar)
        menu_layout.add_widget(btn_relatorios)
        menu_layout.add_widget(btn_backup)
        
        layout.add_widget(menu_layout)
        
        # Status da eleição
        self.status_label = Label(
            text='Status: Eleição não iniciada',
            size_hint_y=0.15,
            font_size='18sp',
            color=(0.8, 0.4, 0.2, 1)
        )
        layout.add_widget(self.status_label)
        
        self.add_widget(layout)
        self.atualizar_status()
    
    def criar_botao_mesario(self, texto, callback):
        btn = Button(
            text=texto,
            font_size='16sp',
            bold=True,
            background_color=(0.3, 0.7, 0.3, 1)
        )
        btn.bind(on_press=callback)
        return btn
    
    def iniciar_eleicao(self, instance):
        app = App.get_running_app()
        app.tocar_som('confirma')
        
        app.dados['configuracoes']['eleicao_ativa'] = True
        app.dados['configuracoes']['data_inicio'] = datetime.datetime.now().isoformat()
        app.salvar_dados()
        
        self.atualizar_status()
        self.mostrar_popup('Sucesso', 'Eleição iniciada com sucesso!')
    
    def finalizar_eleicao(self, instance):
        app = App.get_running_app()
        app.tocar_som('confirma')
        
        app.dados['configuracoes']['eleicao_ativa'] = False
        app.dados['configuracoes']['data_fim'] = datetime.datetime.now().isoformat()
        app.salvar_dados()
        
        self.atualizar_status()
        self.mostrar_popup('Sucesso', 'Eleição finalizada com sucesso!')
    
    def ver_relatorios(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.manager.current = 'relatorios'
    
    def fazer_backup(self, instance):
        app = App.get_running_app()
        app.tocar_som('confirma')
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'backup_urna_{timestamp}.json'
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(app.dados, f, ensure_ascii=False, indent=2)
        
        self.mostrar_popup('Sucesso', f'Backup criado: {backup_file}')
    
    def atualizar_status(self):
        app = App.get_running_app()
        config = app.dados['configuracoes']
        
        if config['eleicao_ativa']:
            self.status_label.text = f"Status: Eleição ATIVA desde {config.get('data_inicio', 'N/A')}"
            self.status_label.color = (0.2, 0.8, 0.2, 1)
        else:
            self.status_label.text = "Status: Eleição INATIVA"
            self.status_label.color = (0.8, 0.4, 0.2, 1)
    
    def mostrar_popup(self, titulo, mensagem):
        popup = Popup(
            title=titulo,
            content=Label(text=mensagem),
            size_hint=(0.6, 0.4)
        )
        popup.open()
    
    def voltar(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.manager.current = 'inicial'

class TelaInscricoes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_interface()
    
    def build_interface(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Cabeçalho
        header = BoxLayout(orientation='horizontal', size_hint_y=0.15)
        btn_voltar = Button(
            text='← Voltar',
            size_hint_x=0.2,
            background_color=(0.8, 0.3, 0.3, 1)
        )
        btn_voltar.bind(on_press=self.voltar)
        
        titulo = Label(
            text='INSCRIÇÕES DE CANDIDATOS',
            font_size='24sp',
            bold=True,
            color=(0.2, 0.4, 0.8, 1)
        )
        
        header.add_widget(btn_voltar)
        header.add_widget(titulo)
        layout.add_widget(header)
        
        # Formulário de inscrição
        form_layout = GridLayout(cols=2, spacing=10, size_hint_y=0.6)
        
        form_layout.add_widget(Label(text='Nome Completo:', halign='right'))
        self.input_nome = TextInput(multiline=False)
        form_layout.add_widget(self.input_nome)
        
        form_layout.add_widget(Label(text='CPF:', halign='right'))
        self.input_cpf = TextInput(multiline=False)
        form_layout.add_widget(self.input_cpf)
        
        form_layout.add_widget(Label(text='Cargo/Função:', halign='right'))
        self.input_cargo = TextInput(multiline=False)
        form_layout.add_widget(self.input_cargo)
        
        form_layout.add_widget(Label(text='Código da Empresa:', halign='right'))
        self.input_empresa = TextInput(multiline=False)
        form_layout.add_widget(self.input_empresa)
        
        form_layout.add_widget(Label(text='Foto:', halign='right'))
        btn_foto = Button(text='📷 Capturar Foto')
        btn_foto.bind(on_press=self.capturar_foto)
        form_layout.add_widget(btn_foto)
        
        layout.add_widget(form_layout)
        
        # Botões de ação
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.15)
        
        btn_inscrever = Button(
            text='✅ Inscrever Candidato',
            background_color=(0.2, 0.8, 0.2, 1)
        )
        btn_inscrever.bind(on_press=self.inscrever_candidato)
        
        btn_comprovante = Button(
            text='🖨️ Gerar Comprovante',
            background_color=(0.2, 0.6, 0.9, 1)
        )
        btn_comprovante.bind(on_press=self.gerar_comprovante)
        
        btn_layout.add_widget(btn_inscrever)
        btn_layout.add_widget(btn_comprovante)
        layout.add_widget(btn_layout)
        
        # Lista de candidatos
        self.lista_candidatos = Label(
            text='Candidatos inscritos aparecerão aqui...',
            text_size=(None, None),
            valign='top',
            size_hint_y=0.1
        )
        layout.add_widget(self.lista_candidatos)
        
        self.add_widget(layout)
        self.foto_path = None
    
    def capturar_foto(self, instance):
        # Simulação de captura de foto
        App.get_running_app().tocar_som('tecla')
        self.mostrar_popup('Info', 'Funcionalidade de foto será implementada com câmera')
    
    def inscrever_candidato(self, instance):
        app = App.get_running_app()
        app.tocar_som('confirma')
        
        if not all([self.input_nome.text, self.input_cpf.text, self.input_empresa.text]):
            self.mostrar_popup('Erro', 'Todos os campos são obrigatórios!')
            return
        
        # Verificar se empresa existe
        if self.input_empresa.text.upper() not in [emp['codigo_acesso'] for emp in app.dados['empresas'].values()]:
            self.mostrar_popup('Erro', 'Código da empresa inválido!')
            return
        
        candidato_id = hashlib.md5(self.input_cpf.text.encode()).hexdigest()[:8]
        
        app.dados['candidatos'][candidato_id] = {
            'nome': self.input_nome.text,
            'cpf': self.input_cpf.text,
            'cargo': self.input_cargo.text,
            'empresa': self.input_empresa.text.upper(),
            'data_inscricao': datetime.datetime.now().isoformat(),
            'numero': len(app.dados['candidatos']) + 1,
            'foto': self.foto_path
        }
        
        app.salvar_dados()
        self.limpar_campos()
        self.mostrar_popup('Sucesso', f'Candidato inscrito!\nNúmero: {len(app.dados["candidatos"])}')
        self.listar_candidatos()
    
    def gerar_comprovante(self, instance):
        if not self.input_nome.text:
            self.mostrar_popup('Erro', 'Preencha o nome para gerar comprovante!')
            return
        
        # Gerar PDF de comprovante
        filename = f'comprovante_inscricao_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        c = canvas.Canvas(filename, pagesize=letter)
        
        c.drawString(100, 750, "COMPROVANTE DE INSCRIÇÃO - ELEIÇÃO CIPA")
        c.drawString(100, 700, f"Nome: {self.input_nome.text}")
        c.drawString(100, 680, f"CPF: {self.input_cpf.text}")
        c.drawString(100, 660, f"Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
        
        c.save()
        self.mostrar_popup('Sucesso', f'Comprovante gerado: {filename}')
    
    def listar_candidatos(self):
        app = App.get_running_app()
        candidatos = app.dados['candidatos']
        
        if not candidatos:
            self.lista_candidatos.text = 'Nenhum candidato inscrito.'
            return
        
        texto = 'CANDIDATOS INSCRITOS:\n\n'
        for cand_id, dados in candidatos.items():
            texto += f"• {dados['numero']:02d} - {dados['nome']} ({dados['empresa']})\n"
        
        self.lista_candidatos.text = texto
        self.lista_candidatos.text_size = (self.width - 40, None)
    
    def limpar_campos(self):
        self.input_nome.text = ''
        self.input_cpf.text = ''
        self.input_cargo.text = ''
        self.input_empresa.text = ''
        self.foto_path = None
    
    def mostrar_popup(self, titulo, mensagem):
        popup = Popup(
            title=titulo,
            content=Label(text=mensagem),
            size_hint=(0.6, 0.4)
        )
        popup.open()
    
    def voltar(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.manager.current = 'inicial'

class TelaVotacao(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.numero_digitado = ''
        self.build_interface()
    
    def build_interface(self):
        layout = BoxLayout(orientation='horizontal', padding=20, spacing=20)
        
        # Painel esquerdo - Tela da urna
        painel_esquerdo = BoxLayout(orientation='vertical', size_hint_x=0.6)
        
        # Tela da urna
        tela_urna = BoxLayout(orientation='vertical', padding=20)
        with tela_urna.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.rect_tela = Rectangle(size=tela_urna.size, pos=tela_urna.pos)
        
        # Cabeçalho da votação
        header_votacao = Label(
            text='ELEIÇÃO CIPA 2024',
            font_size='24sp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=0.2
        )
        tela_urna.add_widget(header_votacao)
        
        # Área de exibição do candidato
        self.area_candidato = BoxLayout(orientation='vertical', size_hint_y=0.6)
        
        self.label_numero = Label(
            text='Digite o número do candidato:',
            font_size='18sp',
            color=(1, 1, 1, 1)
        )
        
        self.display_numero = Label(
            text='_ _',
            font_size='48sp',
            bold=True,
            color=(1, 1, 0, 1)
        )
        
        self.info_candidato = Label(
            text='',
            font_size='16sp',
            color=(1, 1, 1, 1),
            text_size=(None, None)
        )
        
        self.area_candidato.add_widget(self.label_numero)
        self.area_candidato.add_widget(self.display_numero)
        self.area_candidato.add_widget(self.info_candidato)
        
        tela_urna.add_widget(self.area_candidato)
        
        # Instruções
        instrucoes = Label(
            text='Digite o número e pressione CONFIRMA\nPara corrigir, pressione CORRIGE',
            font_size='14sp',
            color=(0.8, 0.8, 0.8, 1),
            size_hint_y=0.2
        )
        tela_urna.add_widget(instrucoes)
        
        painel_esquerdo.add_widget(tela_urna)
        
        # Painel direito - Teclado
        painel_direito = BoxLayout(orientation='vertical', size_hint_x=0.4)
        
        # Código da empresa
        codigo_layout = BoxLayout(orientation='horizontal', size_hint_y=0.15)
        codigo_layout.add_widget(Label(text='Código da Empresa:'))
        self.input_codigo = TextInput(multiline=False, size_hint_x=0.6)
        codigo_layout.add_widget(self.input_codigo)
        painel_direito.add_widget(codigo_layout)
        
        # Teclado numérico
        teclado = GridLayout(cols=3, spacing=5, size_hint_y=0.6)
        
        # Números 1-9
        for i in range(1, 10):
            btn = self.criar_botao_numero(str(i))
            teclado.add_widget(btn)
        
        # Linha inferior: CORRIGE, 0, CONFIRMA
        btn_corrige = Button(
            text='CORRIGE',
            background_color=(1, 0.5, 0, 1),
            font_size='14sp',
            bold=True
        )
        btn_corrige.bind(on_press=self.corrigir)
        
        btn_zero = self.criar_botao_numero('0')
        
        btn_confirma = Button(
            text='CONFIRMA',
            background_color=(0, 0.8, 0, 1),
            font_size='14sp',
            bold=True
        )
        btn_confirma.bind(on_press=self.confirmar_voto)
        
        teclado.add_widget(btn_corrige)
        teclado.add_widget(btn_zero)
        teclado.add_widget(btn_confirma)
        
        painel_direito.add_widget(teclado)
        
        # Botão voltar
        btn_voltar = Button(
            text='← Voltar ao Menu',
            size_hint_y=0.15,
            background_color=(0.8, 0.3, 0.3, 1)
        )
        btn_voltar.bind(on_press=self.voltar)
        painel_direito.add_widget(btn_voltar)
        
        layout.add_widget(painel_esquerdo)
        layout.add_widget(painel_direito)
        
        self.add_widget(layout)
        
        # Bind para redimensionar o retângulo da tela
        tela_urna.bind(size=self.atualizar_tela, pos=self.atualizar_tela)
    
    def atualizar_tela(self, instance, value):
        self.rect_tela.size = instance.size
        self.rect_tela.pos = instance.pos
    
    def criar_botao_numero(self, numero):
        btn = Button(
            text=numero,
            font_size='24sp',
            bold=True,
            background_color=(0.2, 0.2, 0.8, 1)
        )
        btn.bind(on_press=lambda x: self.digitar_numero(numero))
        return btn
    
    def digitar_numero(self, numero):
        app = App.get_running_app()
        app.tocar_som('tecla')
        
        if len(self.numero_digitado) < 2:
            self.numero_digitado += numero
            self.atualizar_display()
            
            if len(self.numero_digitado) == 2:
                self.buscar_candidato()
    
    def atualizar_display(self):
        display = ''
        for i in range(2):
            if i < len(self.numero_digitado):
                display += self.numero_digitado[i] + ' '
            else:
                display += '_ '
        self.display_numero.text = display.strip()
    
    def buscar_candidato(self):
        app = App.get_running_app()
        numero = int(self.numero_digitado)
        
        # Buscar candidato pelo número
        candidato_encontrado = None
        for cand_id, dados in app.dados['candidatos'].items():
            if dados['numero'] == numero:
                candidato_encontrado = dados
                break
        
        if candidato_encontrado:
            self.info_candidato.text = f"Nome: {candidato_encontrado['nome']}\nCargo: {candidato_encontrado['cargo']}\nEmpresa: {candidato_encontrado['empresa']}"
        else:
            self.info_candidato.text = "CANDIDATO NÃO ENCONTRADO"
    
    def corrigir(self, instance):
        app = App.get_running_app()
        app.tocar_som('corrige')
        
        self.numero_digitado = ''
        self.atualizar_display()
        self.info_candidato.text = ''
    
    def confirmar_voto(self, instance):
        app = App.get_running_app()
        
        # Verificar se eleição está ativa
        if not app.dados['configuracoes']['eleicao_ativa']:
            self.mostrar_popup('Erro', 'Eleição não está ativa!')
            return
        
        # Verificar código da empresa
        if not self.input_codigo.text:
            self.mostrar_popup('Erro', 'Digite o código da empresa!')
            return
        
        codigo_valido = False
        for emp_id, dados in app.dados['empresas'].items():
            if dados['codigo_acesso'] == self.input_codigo.text.upper():
                codigo_valido = True
                break
        
        if not codigo_valido:
            self.mostrar_popup('Erro', 'Código da empresa inválido!')
            return
        
        if len(self.numero_digitado) != 2:
            self.mostrar_popup('Erro', 'Digite um número válido!')
            return
        
        app.tocar_som('confirma')
        
        # Registrar voto
        numero = int(self.numero_digitado)
        empresa = self.input_codigo.text.upper()
        
        if empresa not in app.dados['votos']:
            app.dados['votos'][empresa] = {}
        
        if str(numero) not in app.dados['votos'][empresa]:
            app.dados['votos'][empresa][str(numero)] = 0
        
        app.dados['votos'][empresa][str(numero)] += 1
        
        # Registrar eleitor
        eleitor_id = hashlib.md5(f"{empresa}_{datetime.datetime.now().isoformat()}".encode()).hexdigest()[:8]
        app.dados['eleitores'][eleitor_id] = {
            'empresa': empresa,
            'data_voto': datetime.datetime.now().isoformat(),
            'numero_votado': numero
        }
        
        app.salvar_dados()
        
        # Gerar comprovante
        self.gerar_comprovante_votacao(eleitor_id)
        
        # Limpar tela
        self.numero_digitado = ''
        self.input_codigo.text = ''
        self.atualizar_display()
        self.info_candidato.text = ''
        
        self.mostrar_popup('Sucesso', 'Voto registrado com sucesso!\nComprovante gerado.')
    
    def gerar_comprovante_votacao(self, eleitor_id):
        filename = f'comprovante_votacao_{eleitor_id}.pdf'
        c = canvas.Canvas(filename, pagesize=letter)
        
        c.drawString(100, 750, "COMPROVANTE DE VOTAÇÃO - ELEIÇÃO CIPA")
        c.drawString(100, 700, f"Código do Eleitor: {eleitor_id}")
        c.drawString(100, 680, f"Data/Hora: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        c.drawString(100, 660, "Voto registrado com sucesso!")
        
        c.save()
    
    def mostrar_popup(self, titulo, mensagem):
        popup = Popup(
            title=titulo,
            content=Label(text=mensagem),
            size_hint=(0.6, 0.4)
        )
        popup.open()
    
    def voltar(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.manager.current = 'inicial'

class TelaRelatorios(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_interface()
    
    def build_interface(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Cabeçalho
        header = BoxLayout(orientation='horizontal', size_hint_y=0.15)
        btn_voltar = Button(
            text='← Voltar',
            size_hint_x=0.2,
            background_color=(0.8, 0.3, 0.3, 1)
        )
        btn_voltar.bind(on_press=self.voltar)
        
        titulo = Label(
            text='RELATÓRIOS E RESULTADOS',
            font_size='24sp',
            bold=True,
            color=(0.2, 0.4, 0.8, 1)
        )
        
        header.add_widget(btn_voltar)
        header.add_widget(titulo)
        layout.add_widget(header)
        
        # Botões de relatórios
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.15)
        
        btn_resultados = Button(
            text='📊 Ver Resultados',
            background_color=(0.2, 0.6, 0.9, 1)
        )
        btn_resultados.bind(on_press=self.ver_resultados)
        
        btn_eleitores = Button(
            text='👥 Lista Eleitores',
            background_color=(0.3, 0.7, 0.3, 1)
        )
        btn_eleitores.bind(on_press=self.ver_eleitores)
        
        btn_pdf = Button(
            text='📄 Gerar PDF',
            background_color=(0.8, 0.4, 0.2, 1)
        )
        btn_pdf.bind(on_press=self.gerar_pdf)
        
        btn_layout.add_widget(btn_resultados)
        btn_layout.add_widget(btn_eleitores)
        btn_layout.add_widget(btn_pdf)
        layout.add_widget(btn_layout)
        
        # Área de exibição dos relatórios
        self.area_relatorio = Label(
            text='Selecione um relatório acima...',
            text_size=(None, None),
            valign='top',
            size_hint_y=0.7
        )
        layout.add_widget(self.area_relatorio)
        
        self.add_widget(layout)
    
    def ver_resultados(self, instance):
        app = App.get_running_app()
        app.tocar_som('tecla')
        
        texto = 'RESULTADOS DA ELEIÇÃO CIPA\n\n'
        
        for empresa, votos in app.dados['votos'].items():
            texto += f"EMPRESA: {empresa}\n"
            texto += "-" * 30 + "\n"
            
            total_votos = sum(votos.values())
            
            # Ordenar por número de votos
            votos_ordenados = sorted(votos.items(), key=lambda x: x[1], reverse=True)
            
            for numero, qtd_votos in votos_ordenados:
                # Buscar nome do candidato
                nome_candidato = "Candidato não encontrado"
                for cand_id, dados in app.dados['candidatos'].items():
                    if dados['numero'] == int(numero):
                        nome_candidato = dados['nome']
                        break
                
                percentual = (qtd_votos / total_votos * 100) if total_votos > 0 else 0
                texto += f"{numero:02d} - {nome_candidato}: {qtd_votos} votos ({percentual:.1f}%)\n"
            
            texto += f"\nTotal de votos: {total_votos}\n\n"
        
        self.area_relatorio.text = texto
        self.area_relatorio.text_size = (self.width - 40, None)
    
    def ver_eleitores(self, instance):
        app = App.get_running_app()
        app.tocar_som('tecla')
        
        texto = 'LISTA DE ELEITORES\n\n'
        
        for eleitor_id, dados in app.dados['eleitores'].items():
            data_voto = datetime.datetime.fromisoformat(dados['data_voto'])
            texto += f"ID: {eleitor_id}\n"
            texto += f"Empresa: {dados['empresa']}\n"
            texto += f"Data/Hora: {data_voto.strftime('%d/%m/%Y %H:%M:%S')}\n"
            texto += f"Número votado: {dados['numero_votado']:02d}\n"
            texto += "-" * 40 + "\n"
        
        total_eleitores = len(app.dados['eleitores'])
        texto += f"\nTotal de eleitores: {total_eleitores}"
        
        self.area_relatorio.text = texto
        self.area_relatorio.text_size = (self.width - 40, None)
    
    def gerar_pdf(self, instance):
        app = App.get_running_app()
        app.tocar_som('confirma')
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'relatorio_eleicao_cipa_{timestamp}.pdf'
        
        c = canvas.Canvas(filename, pagesize=letter)
        y_position = 750
        
        c.drawString(100, y_position, "RELATÓRIO FINAL - ELEIÇÃO CIPA")
        y_position -= 40
        
        c.drawString(100, y_position, f"Data do relatório: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        y_position -= 30
        
        # Resultados por empresa
        for empresa, votos in app.dados['votos'].items():
            c.drawString(100, y_position, f"EMPRESA: {empresa}")
            y_position -= 20
            
            total_votos = sum(votos.values())
            votos_ordenados = sorted(votos.items(), key=lambda x: x[1], reverse=True)
            
            for numero, qtd_votos in votos_ordenados:
                nome_candidato = "Candidato não encontrado"
                for cand_id, dados in app.dados['candidatos'].items():
                    if dados['numero'] == int(numero):
                        nome_candidato = dados['nome']
                        break
                
                percentual = (qtd_votos / total_votos * 100) if total_votos > 0 else 0
                c.drawString(120, y_position, f"{numero:02d} - {nome_candidato}: {qtd_votos} votos ({percentual:.1f}%)")
                y_position -= 15
            
            c.drawString(100, y_position, f"Total de votos: {total_votos}")
            y_position -= 30
            
            if y_position < 100:
                c.showPage()
                y_position = 750
        
        c.save()
        self.mostrar_popup('Sucesso', f'Relatório PDF gerado: {filename}')
    
    def mostrar_popup(self, titulo, mensagem):
        popup = Popup(
            title=titulo,
            content=Label(text=mensagem),
            size_hint=(0.6, 0.4)
        )
        popup.open()
    
    def voltar(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.manager.current = 'mesario'

if __name__ == '__main__':
    # Criar diretório de sons se não existir
    if not os.path.exists('sons'):
        os.makedirs('sons')
    
    UrnaEletronicaCIPA().run()