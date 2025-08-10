import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.widget import Widget
from kivy.lang import Builder
import json
import datetime
import os
import hashlib
import random

kivy.require('2.0.0')

# Popup moderno
def mostrar_popup_moderno(titulo, mensagem):
    content = BoxLayout(orientation='vertical', padding=15, spacing=10)
    
    # Ícone baseado no tipo
    icone = '✅' if 'Sucesso' in titulo else '❌' if 'Erro' in titulo else 'ℹ️'
    
    # Container com ícone e título
    header = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
    icone_label = Label(text=icone, font_size='24sp', size_hint_x=None, width=40)
    titulo_label = Label(text=titulo, font_size='16sp', bold=True, color=(0.2, 0.2, 0.2, 1))
    header.add_widget(icone_label)
    header.add_widget(titulo_label)
    
    # Mensagem
    msg_label = Label(text=mensagem, text_size=(300, None), halign='center', valign='middle', 
                     font_size='14sp', color=(0.3, 0.3, 0.3, 1))
    
    # Botão moderno
    btn_ok = Button(text='OK', size_hint_y=None, height=35, font_size='14sp', 
                   background_normal='', background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1))
    
    content.add_widget(header)
    content.add_widget(msg_label)
    content.add_widget(btn_ok)
    
    popup = Popup(title='', content=content, size_hint=(0.6, 0.4), separator_height=0)
    btn_ok.bind(on_press=popup.dismiss)
    popup.open()

def mostrar_popup_codigo_moderno(titulo, mensagem, codigo):
    content = BoxLayout(orientation='vertical', padding=15, spacing=10)
    
    # Header com ícone
    header = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
    icone_label = Label(text='🔑', font_size='24sp', size_hint_x=None, width=40)
    titulo_label = Label(text=titulo, font_size='16sp', bold=True, color=(0.2, 0.2, 0.2, 1))
    header.add_widget(icone_label)
    header.add_widget(titulo_label)
    
    # Mensagem
    msg_label = Label(text=mensagem, text_size=(300, None), halign='center', valign='middle', 
                     font_size='14sp', color=(0.3, 0.3, 0.3, 1))
    
    # Campo do código
    codigo_input = TextInput(text=codigo, readonly=True, multiline=False, size_hint_y=None, 
                           height=35, font_size='16sp', background_color=(0.95, 0.95, 0.95, 1))
    
    # Botão
    btn_ok = Button(text='OK', size_hint_y=None, height=35, font_size='14sp', 
                   background_normal='', background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1))
    
    content.add_widget(header)
    content.add_widget(msg_label)
    content.add_widget(codigo_input)
    content.add_widget(btn_ok)
    
    popup = Popup(title='', content=content, size_hint=(0.6, 0.5), separator_height=0)
    btn_ok.bind(on_press=popup.dismiss)
    popup.open()

# Carregar arquivo de estilo
if os.path.exists('urna_style.kv'):
    Builder.load_file('urna_style.kv')

class UrnaEletronicaCIPA(App):
    def __init__(self):
        super().__init__()
        self.dados_file = 'dados_urna_cipa.json'
        self.dados = self.carregar_dados()
        self.empresa_atual = None
    
    def criar_botao_com_icone(self, texto, icone_path, cor, tamanho_icone=(20, 20)):
        # Container horizontal para ícone e botão
        container = BoxLayout(orientation='horizontal', spacing=5)
        
        # Ícone
        if os.path.exists(icone_path):
            icone = Image(source=icone_path, size_hint=(None, None), size=tamanho_icone)
            container.add_widget(icone)
        
        # Botão com cantos arredondados
        btn = Button(text=texto, background_normal='', background_color=cor, color=(0.5, 0.8, 1, 1))
        
        def desenhar_botao_arredondado(instance, *args):
            instance.canvas.before.clear()
            with instance.canvas.before:
                Color(*cor)
                RoundedRectangle(pos=instance.pos, size=instance.size, radius=[15])
        
        btn.bind(pos=desenhar_botao_arredondado, size=desenhar_botao_arredondado)
        desenhar_botao_arredondado(btn)
        
        container.add_widget(btn)
        
        return container, btn
    
    def tocar_som(self, tipo):
        try:
            import pygame
            
            # Inicializar pygame mixer se não estiver inicializado
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            
            # Tentar tocar arquivo de som
            arquivo_som = f'sons/{tipo}.wav'
            if os.path.exists(arquivo_som):
                som = pygame.mixer.Sound(arquivo_som)
                som.play()
            else:
                # Fallback para winsound se arquivo não existir
                import winsound
                if tipo == 'tecla':
                    winsound.Beep(800, 100)
                elif tipo == 'confirma':
                    winsound.Beep(659, 150)
                    winsound.Beep(784, 150)
                    winsound.Beep(1047, 300)
                elif tipo == 'corrige':
                    winsound.Beep(1047, 120)
                    winsound.Beep(523, 180)
                elif tipo == 'erro':
                    winsound.Beep(400, 500)
        except:
            print(f"[SOM] {tipo}")
        
    def carregar_dados(self):
        if os.path.exists(self.dados_file):
            with open(self.dados_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Dados iniciais para teste
        dados_teste = {
            'auth': {'email': '', 'senha': ''},
            'empresas': {
                'emp001': {'nome': 'Empresa Teste LTDA', 'cnpj': '12.345.678/0001-90', 'codigo_acesso': '1234'}
            },
            'candidatos': {
                'cand01': {'nome': 'João Silva', 'cpf': '111.111.111-11', 'empresa': '1234', 'numero': 1},
                'cand02': {'nome': 'Maria Santos', 'cpf': '222.222.222-22', 'empresa': '1234', 'numero': 2},
                'cand03': {'nome': 'Pedro Costa', 'cpf': '333.333.333-33', 'empresa': '1234', 'numero': 3},
                'cand04': {'nome': 'Ana Oliveira', 'cpf': '444.444.444-44', 'empresa': '1234', 'numero': 4},
                'cand05': {'nome': 'Carlos Pereira', 'cpf': '555.555.555-55', 'empresa': '1234', 'numero': 5},
                'cand06': {'nome': 'Lucia Ferreira', 'cpf': '666.666.666-66', 'empresa': '1234', 'numero': 6},
                'cand07': {'nome': 'Roberto Lima', 'cpf': '777.777.777-77', 'empresa': '1234', 'numero': 7},
                'cand08': {'nome': 'Fernanda Souza', 'cpf': '888.888.888-88', 'empresa': '1234', 'numero': 8}
            },
            'votos': {},
            'eleitores': {},
            'configuracoes': {'eleicao_ativa': True}
        }
        
        # Salva os dados de teste
        with open(self.dados_file, 'w', encoding='utf-8') as f:
            json.dump(dados_teste, f, ensure_ascii=False, indent=2)
        
        return dados_teste
    
    def salvar_dados(self):
        with open(self.dados_file, 'w', encoding='utf-8') as f:
            json.dump(self.dados, f, ensure_ascii=False, indent=2)
    
    def enviar_email(self, email, senha):
        # Simula envio de email
        print(f"EMAIL ENVIADO PARA: {email}")
        print(f"Login: {email}")
        print(f"Senha: {senha}")
        return True
    
    def build(self):
        self.title = "Urna Eletronica CIPA"
        sm = ScreenManager()
        sm.add_widget(TelaInicial(name='inicial'))
        sm.add_widget(TelaAuth(name='auth'))
        return sm

class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from kivy.uix.floatlayout import FloatLayout
        
        layout = FloatLayout()
        
        with layout.canvas.before:
            Color(0.9, 0.95, 1, 1)
            self.rect_bg = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self.atualizar_fundo, pos=self.atualizar_fundo)
        
        # Logos institucionais
        logos_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(None, None), size=(500, 80), pos_hint={'center_x': 0.5, 'center_y': 0.8})
        
        if os.path.exists('logos/ministerio_trabalho.png'):
            logo_mt = Image(source='logos/ministerio_trabalho.png', size_hint=(None, None), size=(120, 80))
            logos_layout.add_widget(logo_mt)
        
        if os.path.exists('logos/fundacentro.png'):
            logo_fund = Image(source='logos/fundacentro.png', size_hint=(None, None), size=(120, 80))
            logos_layout.add_widget(logo_fund)
        
        if os.path.exists('logos/cipa.png'):
            logo_cipa = Image(source='logos/cipa.png', size_hint=(None, None), size=(120, 80))
            logos_layout.add_widget(logo_cipa)
        
        if os.path.exists('logos/sesmt.png'):
            logo_sesmt = Image(source='logos/sesmt.png', size_hint=(None, None), size=(120, 80))
            logos_layout.add_widget(logo_sesmt)
        
        layout.add_widget(logos_layout)
        
        titulo = Label(text='URNA ELETRONICA CIPA', font_size='28sp', bold=True, size_hint=(None, None), size=(500, 60), pos_hint={'center_x': 0.5, 'center_y': 0.7}, color=(1, 0.6, 0.2, 1))
        layout.add_widget(titulo)
        
        menu = GridLayout(cols=2, spacing=30, size_hint=(None, None), size=(450, 220), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        # Botões com ícones
        app = App.get_running_app()
        container_empresa, btn_empresa = app.criar_botao_com_icone('EMPRESA\nGerenciar', 'icones/empresa.png', (0.7, 1, 0.7, 1), (50, 50))
        container_empresa.spacing = 8
        btn_empresa.size_hint = (None, None)
        btn_empresa.size = (140, 80)
        btn_empresa.bind(on_press=self.ir_empresa)
        
        container_mesario, btn_mesario = app.criar_botao_com_icone('MESARIO\nAdministrar', 'icones/mesario.png', (1, 0.9, 0.6, 1), (50, 50))
        container_mesario.spacing = 8
        btn_mesario.size_hint = (None, None)
        btn_mesario.size = (140, 80)
        btn_mesario.bind(on_press=self.ir_mesario)
        
        container_inscricoes, btn_inscricoes = app.criar_botao_com_icone('INSCRICOES\nCandidatos', 'icones/inscricoes.png', (0.7, 0.9, 1, 1), (50, 50))
        container_inscricoes.spacing = 8
        btn_inscricoes.size_hint = (None, None)
        btn_inscricoes.size = (140, 80)
        btn_inscricoes.bind(on_press=self.ir_inscricoes)
        
        container_votacao, btn_votacao = app.criar_botao_com_icone('VOTACAO\nEleitor', 'icones/votacao.png', (1, 0.8, 1, 1), (50, 50))
        container_votacao.spacing = 8
        btn_votacao.size_hint = (None, None)
        btn_votacao.size = (140, 80)
        btn_votacao.bind(on_press=self.ir_votacao)
        
        menu.add_widget(container_empresa)
        menu.add_widget(container_mesario)
        menu.add_widget(container_inscricoes)
        menu.add_widget(container_votacao)
        
        layout.add_widget(menu)
        self.add_widget(layout)
    
    def atualizar_fundo(self, instance, value):
        self.rect_bg.size = instance.size
        self.rect_bg.pos = instance.pos
    
    def ir_empresa(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.manager.current = 'auth'
    
    def ir_mesario(self, instance):
        App.get_running_app().tocar_som('tecla')
        mostrar_popup_moderno('Info', 'Tela em desenvolvimento!')
    
    def ir_inscricoes(self, instance):
        App.get_running_app().tocar_som('tecla')
        mostrar_popup_moderno('Info', 'Tela em desenvolvimento!')
    
    def ir_votacao(self, instance):
        App.get_running_app().tocar_som('tecla')
        mostrar_popup_moderno('Info', 'Tela em desenvolvimento!')

class TelaAuth(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from kivy.uix.floatlayout import FloatLayout
        
        layout = FloatLayout()
        
        with layout.canvas.before:
            Color(0.9, 0.95, 1, 1)
            self.rect_bg = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self.atualizar_fundo, pos=self.atualizar_fundo)
        
        # Título
        titulo = Label(text='ACESSO GESTAO EMPRESAS', font_size='20sp', bold=True, size_hint=(None, None), size=(400, 40), pos_hint={'center_x': 0.5, 'center_y': 0.85}, color=(1, 0.6, 0.2, 1))
        layout.add_widget(titulo)
        
        # Formulário
        form = GridLayout(cols=2, spacing=10, size_hint=(None, None), size=(500, 200), pos_hint={'center_x': 0.5, 'center_y': 0.6})
        
        form.add_widget(Label(text='Email:', color=(1, 0.6, 0.2, 1)))
        self.input_email = TextInput(size_hint=(None, None), size=(300, 40), font_size='14sp')
        form.add_widget(self.input_email)
        
        form.add_widget(Label(text='Senha:', color=(1, 0.6, 0.2, 1)))
        senha_container = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(300, 40))
        self.input_senha = TextInput(password=True, size_hint=(None, None), size=(260, 40), font_size='14sp')
        self.btn_mostrar = Button(text='👁', size_hint=(None, None), size=(40, 40), color=(0.5, 0.8, 1, 1))
        self.btn_mostrar.bind(on_press=self.toggle_senha)
        senha_container.add_widget(self.input_senha)
        senha_container.add_widget(self.btn_mostrar)
        form.add_widget(senha_container)
        
        # Verificar se é primeiro acesso
        app = App.get_running_app()
        self.primeiro_acesso = 'auth' not in app.dados or not app.dados['auth']['email']
        
        # Campo confirmar senha (sempre no primeiro acesso)
        if self.primeiro_acesso:
            form.add_widget(Label(text='Confirmar Senha:', color=(1, 0.6, 0.2, 1)))
            confirma_container = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(300, 40))
            self.input_confirma = TextInput(password=True, size_hint=(None, None), size=(260, 40), font_size='14sp')
            self.btn_mostrar2 = Button(text='👁', size_hint=(None, None), size=(40, 40), color=(0.5, 0.8, 1, 1))
            self.btn_mostrar2.bind(on_press=self.toggle_confirma)
            confirma_container.add_widget(self.input_confirma)
            confirma_container.add_widget(self.btn_mostrar2)
            form.add_widget(confirma_container)
        else:
            form.add_widget(Label(text='', color=(1, 0.6, 0.2, 1)))  # Espaço vazio
            form.add_widget(Label(text='', color=(1, 0.6, 0.2, 1)))  # Espaço vazio
        
        layout.add_widget(form)
        
        # Orientações
        orientacao = Label(text='Senha: mínimo 6 caracteres\nPode conter letras, números e símbolos', font_size='12sp', size_hint=(None, None), size=(400, 40), pos_hint={'center_x': 0.5, 'center_y': 0.42}, color=(0.6, 0.6, 0.6, 1))
        layout.add_widget(orientacao)
        
        # Botões
        btn_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint=(None, None), size=(300, 50), pos_hint={'center_x': 0.5, 'center_y': 0.32})
        
        app = App.get_running_app()
        container_entrar, btn_entrar = app.criar_botao_com_icone('ENTRAR', 'icones/confirmar.png', (0.7, 1, 0.7, 1), (30, 30))
        btn_entrar.size_hint = (None, None)
        btn_entrar.size = (120, 40)
        btn_entrar.bind(on_press=self.entrar)
        
        container_voltar, btn_voltar = app.criar_botao_com_icone('VOLTAR', 'icones/voltar.png', (1, 0.8, 0.8, 1), (30, 30))
        btn_voltar.size_hint = (None, None)
        btn_voltar.size = (120, 40)
        btn_voltar.bind(on_press=self.voltar)
        
        btn_layout.add_widget(container_entrar)
        btn_layout.add_widget(container_voltar)
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
    
    def atualizar_fundo(self, instance, value):
        self.rect_bg.size = instance.size
        self.rect_bg.pos = instance.pos
    
    def toggle_senha(self, instance):
        self.input_senha.password = not self.input_senha.password
        self.btn_mostrar.text = '👁' if self.input_senha.password else '👀'
    
    def toggle_confirma(self, instance):
        if hasattr(self, 'input_confirma'):
            self.input_confirma.password = not self.input_confirma.password
            self.btn_mostrar2.text = '👁' if self.input_confirma.password else '👀'
    
    def entrar(self, instance):
        App.get_running_app().tocar_som('confirma')
        app = App.get_running_app()
        
        # Primeiro acesso - cadastrar email e senha
        if self.primeiro_acesso:
            if not self.input_email.text or not self.input_senha.text:
                mostrar_popup_moderno('Erro', 'Preencha email e senha!')
                return
            
            if hasattr(self, 'input_confirma') and not self.input_confirma.text:
                mostrar_popup_moderno('Erro', 'Confirme a senha!')
                return
            
            if len(self.input_senha.text) < 6:
                mostrar_popup_moderno('Erro', 'Senha deve ter no minimo 6 caracteres!')
                return
            
            if hasattr(self, 'input_confirma') and self.input_senha.text != self.input_confirma.text:
                mostrar_popup_moderno('Erro', 'Senhas nao coincidem!')
                return
            
            if 'auth' not in app.dados:
                app.dados['auth'] = {'email': '', 'senha': ''}
            app.dados['auth']['email'] = self.input_email.text
            app.dados['auth']['senha'] = self.input_senha.text
            app.salvar_dados()
            
            app.enviar_email(self.input_email.text, self.input_senha.text)
            mostrar_popup_moderno('Sucesso', f'Dados de login enviados para:\n{self.input_email.text}')
            mostrar_popup_moderno('Info', 'Tela de empresa em desenvolvimento!')
        else:
            # Segundo acesso - só pede senha
            if not self.input_senha.text:
                mostrar_popup_moderno('Erro', 'Digite a senha!')
                return
            
            if self.input_senha.text == app.dados['auth']['senha']:
                mostrar_popup_moderno('Info', 'Tela de empresa em desenvolvimento!')
            else:
                mostrar_popup_moderno('Erro', 'Senha incorreta!')
    
    def voltar(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.input_email.text = ''
        self.input_senha.text = ''
        if hasattr(self, 'input_confirma'):
            self.input_confirma.text = ''
        self.manager.current = 'inicial'

if __name__ == '__main__':
    UrnaEletronicaCIPA().run()