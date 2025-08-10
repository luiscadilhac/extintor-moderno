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
            import winsound
            if tipo == 'tecla':
                # Som oficial TSE - digitação de números
                winsound.Beep(784, 100)  # Sol agudo, curto e seco
            elif tipo == 'confirma':
                # Som oficial TSE - confirmação (sequência melódica característica)
                winsound.Beep(659, 150)   # Mi
                winsound.Beep(784, 150)   # Sol  
                winsound.Beep(1047, 300)  # Dó agudo (finalização)
            elif tipo == 'corrige':
                # Som oficial TSE - correção (dois tons descendentes)
                winsound.Beep(1047, 120)  # Dó agudo
                winsound.Beep(523, 180)   # Dó médio
            elif tipo == 'erro':
                # Som oficial TSE - erro/alerta
                winsound.Beep(392, 500)   # Sol grave, longo
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
        sm.add_widget(TelaEmpresa(name='empresa'))
        sm.add_widget(TelaMesario(name='mesario'))
        sm.add_widget(TelaInscricoes(name='inscricoes'))
        sm.add_widget(TelaCodigoEmpresa(name='codigo_empresa'))
        sm.add_widget(TelaCodigoInscricoes(name='codigo_inscricoes'))
        sm.add_widget(TelaVotacao(name='votacao'))
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
        self.manager.current = 'mesario'
    
    def ir_inscricoes(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.manager.current = 'codigo_inscricoes'
    
    def ir_votacao(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.manager.current = 'codigo_empresa'

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
        self.input_email = TextInput(size_hint=(None, None), size=(300, 40))
        form.add_widget(self.input_email)
        
        form.add_widget(Label(text='Senha:', color=(1, 0.6, 0.2, 1)))
        senha_container = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(300, 40))
        self.input_senha = TextInput(password=True, size_hint=(None, None), size=(260, 40))
        self.btn_mostrar = Button(text='👁', size_hint=(None, None), size=(40, 40), color=(0.5, 0.8, 1, 1))
        self.btn_mostrar.bind(on_press=self.toggle_senha)
        senha_container.add_widget(self.input_senha)
        senha_container.add_widget(self.btn_mostrar)
        form.add_widget(senha_container)
        
        # Campo confirmar senha (só no primeiro acesso)
        self.label_confirma = Label(text='Confirmar Senha:', color=(1, 0.6, 0.2, 1))
        confirma_container = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(300, 40))
        self.input_confirma = TextInput(password=True, size_hint=(None, None), size=(260, 40))
        self.btn_mostrar2 = Button(text='👁', size_hint=(None, None), size=(40, 40), color=(0.5, 0.8, 1, 1))
        self.btn_mostrar2.bind(on_press=self.toggle_confirma)
        confirma_container.add_widget(self.input_confirma)
        confirma_container.add_widget(self.btn_mostrar2)
        
        # Adicionar campos condicionalmente
        app = App.get_running_app()
        if 'auth' not in app.dados or not app.dados['auth']['email']:  # Primeiro acesso
            form.add_widget(self.label_confirma)
            form.add_widget(confirma_container)
        else:  # Segundo acesso
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
        self.input_confirma.password = not self.input_confirma.password
        self.btn_mostrar2.text = '👁' if self.input_confirma.password else '👀'
    
    def entrar(self, instance):
        App.get_running_app().tocar_som('confirma')
        app = App.get_running_app()
        
        # Primeiro acesso - cadastrar email e senha
        if 'auth' not in app.dados or not app.dados['auth']['email']:
            if not self.input_email.text or not self.input_senha.text:
                self.mostrar_popup('Erro', 'Preencha email e senha!')
                return
            
            if hasattr(self, 'input_confirma') and not self.input_confirma.text:
                self.mostrar_popup('Erro', 'Confirme a senha!')
                return
            
            if len(self.input_senha.text) < 6:
                self.mostrar_popup('Erro', 'Senha deve ter no minimo 6 caracteres!')
                return
            
            if hasattr(self, 'input_confirma') and self.input_senha.text != self.input_confirma.text:
                self.mostrar_popup('Erro', 'Senhas nao coincidem!')
                return
            
            if 'auth' not in app.dados:
                app.dados['auth'] = {'email': '', 'senha': ''}
            app.dados['auth']['email'] = self.input_email.text
            app.dados['auth']['senha'] = self.input_senha.text
            app.salvar_dados()
            
            app.enviar_email(self.input_email.text, self.input_senha.text)
            self.mostrar_popup('Sucesso', f'Dados de login enviados para:\n{self.input_email.text}')
            self.manager.current = 'empresa'
        else:
            # Segundo acesso - só pede senha
            if not self.input_senha.text:
                self.mostrar_popup('Erro', 'Digite a senha!')
                return
            
            if self.input_senha.text == app.dados['auth']['senha']:
                self.manager.current = 'empresa'
            else:
                self.mostrar_popup('Erro', 'Senha incorreta!')
    
    def voltar(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.input_email.text = ''
        self.input_senha.text = ''
        if hasattr(self, 'input_confirma'):
            self.input_confirma.text = ''
        self.manager.current = 'inicial'
    
    def mostrar_popup(self, titulo, mensagem):
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        label = Label(text=mensagem, text_size=(450, None), halign='center', valign='middle', font_size='18sp', color=(0, 0, 0, 1))
        btn_ok = Button(text='OK', size_hint_y=None, height=50, font_size='16sp', color=(0.5, 0.8, 1, 1))
        content.add_widget(label)
        content.add_widget(btn_ok)
        popup = Popup(title=titulo, content=content, size_hint=(0.9, 0.6), title_size='20sp')
        btn_ok.bind(on_press=popup.dismiss)
        popup.open()

class TelaEmpresa(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from kivy.uix.floatlayout import FloatLayout
        
        self.indice_atual = 0
        self.empresas_lista = []
        
        layout = FloatLayout()
        
        with layout.canvas.before:
            Color(0.9, 0.95, 1, 1)
            self.rect_bg = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self.atualizar_fundo, pos=self.atualizar_fundo)
        
        # Botão voltar no topo
        app = App.get_running_app()
        container_voltar, btn_voltar = app.criar_botao_com_icone('<< Voltar', 'icones/voltar.png', (1, 0.8, 0.8, 1), (50, 50))
        container_voltar.size_hint = (None, None)
        container_voltar.size = (130, 40)
        container_voltar.spacing = 5
        container_voltar.pos_hint = {'x': 0.02, 'top': 0.95}
        btn_voltar.size_hint = (None, None)
        btn_voltar.size = (100, 40)
        btn_voltar.bind(on_press=self.voltar)
        layout.add_widget(container_voltar)
        
        # Título
        titulo = Label(text='GESTAO DE EMPRESAS', font_size='18sp', bold=True, size_hint=(None, None), size=(400, 40), pos_hint={'center_x': 0.5, 'center_y': 0.85}, color=(1, 0.6, 0.2, 1))
        layout.add_widget(titulo)
        
        # Formulário centralizado com campos 3x maiores
        form = GridLayout(cols=2, spacing=8, size_hint=(None, None), size=(800, 160), pos_hint={'center_x': 0.5, 'center_y': 0.65})
        form.add_widget(Label(text='Nome da Empresa:', color=(1, 0.6, 0.2, 1)))
        self.input_nome = TextInput(size_hint=(None, None), size=(600, 60))
        form.add_widget(self.input_nome)
        
        form.add_widget(Label(text='CNPJ:', color=(1, 0.6, 0.2, 1)))
        self.input_cnpj = TextInput(size_hint=(None, None), size=(600, 60))
        form.add_widget(self.input_cnpj)
        
        layout.add_widget(form)
        
        # Botões de ação
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(None, None), size=(520, 50), pos_hint={'center_x': 0.5, 'center_y': 0.48})
        container_nova, btn_nova = app.criar_botao_com_icone('Nova', 'icones/empresa.png', (0.8, 0.9, 1, 1), (25, 25))
        btn_nova.size_hint = (None, None)
        btn_nova.size = (70, 40)
        btn_nova.bind(on_press=self.nova_empresa)
        container_cadastrar, btn_cadastrar = app.criar_botao_com_icone('Cadastrar', 'icones/salvar.png', (0.7, 1, 0.7, 1), (25, 25))
        btn_cadastrar.size_hint = (None, None)
        btn_cadastrar.size = (80, 40)
        btn_cadastrar.bind(on_press=self.cadastrar_empresa)
        container_alterar, btn_alterar = app.criar_botao_com_icone('Alterar', 'icones/alterar.png', (1, 1, 0.7, 1), (25, 25))
        btn_alterar.size_hint = (None, None)
        btn_alterar.size = (80, 40)
        btn_alterar.bind(on_press=self.alterar_empresa)
        container_excluir, btn_excluir = app.criar_botao_com_icone('Excluir', 'icones/excluir.png', (1, 0.8, 0.8, 1), (25, 25))
        btn_excluir.size_hint = (None, None)
        btn_excluir.size = (80, 40)
        btn_excluir.bind(on_press=self.excluir_empresa)
        btn_layout.add_widget(container_nova)
        btn_layout.add_widget(container_cadastrar)
        btn_layout.add_widget(container_alterar)
        btn_layout.add_widget(container_excluir)
        layout.add_widget(btn_layout)
        
        # Botões de navegação abaixo dos botões de ação
        nav_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(None, None), size=(300, 40), pos_hint={'center_x': 0.5, 'center_y': 0.38})
        def criar_botao_arredondado(texto, cor, callback):
            btn = Button(text=texto, size_hint=(None, None), size=(50, 40), background_normal='', background_color=cor, color=(0.5, 0.8, 1, 1))
            def desenhar(instance, *args):
                instance.canvas.before.clear()
                with instance.canvas.before:
                    Color(*cor)
                    RoundedRectangle(pos=instance.pos, size=instance.size, radius=[10])
            btn.bind(pos=desenhar, size=desenhar, on_press=callback)
            desenhar(btn)
            return btn
        
        btn_inicio = criar_botao_arredondado('<<', (0.7, 0.9, 1, 1), self.ir_inicio)
        btn_anterior = criar_botao_arredondado('<', (0.7, 0.9, 1, 1), self.anterior)
        btn_proximo = criar_botao_arredondado('>', (0.7, 0.9, 1, 1), self.proximo)
        btn_fim = criar_botao_arredondado('>>', (0.7, 0.9, 1, 1), self.ir_fim)
        nav_layout.add_widget(btn_inicio)
        nav_layout.add_widget(btn_anterior)
        nav_layout.add_widget(btn_proximo)
        nav_layout.add_widget(btn_fim)
        layout.add_widget(nav_layout)
        
        # Lista de empresas alinhada à esquerda com fonte laranja escuro
        self.lista = Label(text='', size_hint=(None, None), size=(600, 120), pos_hint={'x': 0.05, 'center_y': 0.2}, text_size=(580, None), halign='left', valign='top', color=(0.8, 0.4, 0, 1))
        layout.add_widget(self.lista)
        
        self.add_widget(layout)
        self.atualizar_lista()
    
    def atualizar_fundo(self, instance, value):
        self.rect_bg.size = instance.size
        self.rect_bg.pos = instance.pos
    
    def voltar(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.manager.current = 'inicial'
    
    def nova_empresa(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.input_nome.text = ''
        self.input_cnpj.text = ''
        self.indice_atual = 0
        self.atualizar_lista()
    
    def cadastrar_empresa(self, instance):
        App.get_running_app().tocar_som('confirma')
        app = App.get_running_app()
        if not self.input_nome.text or not self.input_cnpj.text:
            App.get_running_app().tocar_som('erro')
            self.mostrar_popup('Erro', 'Preencha todos os campos!')
            return
        
        codigo = str(random.randint(1000, 9999))
        while codigo in [emp['codigo_acesso'] for emp in app.dados['empresas'].values()]:
            codigo = str(random.randint(1000, 9999))
        
        empresa_id = hashlib.md5(self.input_cnpj.text.encode()).hexdigest()[:8]
        app.dados['empresas'][empresa_id] = {
            'nome': self.input_nome.text,
            'cnpj': self.input_cnpj.text,
            'codigo_acesso': codigo
        }
        app.salvar_dados()
        self.mostrar_popup_codigo('Sucesso', f'Empresa cadastrada!\nCodigo: {codigo}', codigo)
        self.input_nome.text = ''
        self.input_cnpj.text = ''
        self.atualizar_lista()
    
    def excluir_empresa(self, instance):
        App.get_running_app().tocar_som('tecla')
        app = App.get_running_app()
        
        if not self.empresas_lista:
            App.get_running_app().tocar_som('erro')
            self.mostrar_popup('Erro', 'Nenhuma empresa para excluir!')
            return
        
        emp_id, dados = self.empresas_lista[self.indice_atual]
        del app.dados['empresas'][emp_id]
        app.salvar_dados()
        
        self.mostrar_popup('Sucesso', 'Empresa excluida!')
        self.input_nome.text = ''
        self.input_cnpj.text = ''
        
        if self.indice_atual >= len(app.dados['empresas']):
            self.indice_atual = max(0, len(app.dados['empresas']) - 1)
        
        self.atualizar_lista()
    
    def atualizar_lista(self):
        app = App.get_running_app()
        self.empresas_lista = list(app.dados['empresas'].items())
        
        if not self.empresas_lista:
            self.lista.text = 'Nenhuma empresa cadastrada.'
            self.input_nome.text = ''
            self.input_cnpj.text = ''
            return
        
        if self.indice_atual >= len(self.empresas_lista):
            self.indice_atual = 0
        
        # Lista todas as empresas com bolinha verde para atual
        texto = 'EMPRESAS CADASTRADAS:\n\n'
        for i, (emp_id, dados) in enumerate(self.empresas_lista):
            marcador = '● ' if i == self.indice_atual else '○ '
            texto += f"{marcador}{dados['nome']} - Código: {dados['codigo_acesso']}\n"
        
        self.lista.text = texto
        
        # Preenche campos da empresa atual para edição
        emp_id, dados = self.empresas_lista[self.indice_atual]
        self.input_nome.text = dados['nome']
        self.input_cnpj.text = dados['cnpj']
    
    def ir_inicio(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.indice_atual = 0
        self.atualizar_lista()
    
    def anterior(self, instance):
        App.get_running_app().tocar_som('tecla')
        if self.indice_atual > 0:
            self.indice_atual -= 1
            self.atualizar_lista()
    
    def proximo(self, instance):
        App.get_running_app().tocar_som('tecla')
        if self.indice_atual < len(self.empresas_lista) - 1:
            self.indice_atual += 1
            self.atualizar_lista()
    
    def ir_fim(self, instance):
        App.get_running_app().tocar_som('tecla')
        if self.empresas_lista:
            self.indice_atual = len(self.empresas_lista) - 1
            self.atualizar_lista()
    
    def alterar_empresa(self, instance):
        App.get_running_app().tocar_som('confirma')
        app = App.get_running_app()
        
        if not self.empresas_lista or not self.input_nome.text or not self.input_cnpj.text:
            App.get_running_app().tocar_som('erro')
            self.mostrar_popup('Erro', 'Preencha todos os campos!')
            return
        
        emp_id, dados_antigos = self.empresas_lista[self.indice_atual]
        app.dados['empresas'][emp_id]['nome'] = self.input_nome.text
        app.dados['empresas'][emp_id]['cnpj'] = self.input_cnpj.text
        app.salvar_dados()
        
        self.mostrar_popup('Sucesso', 'Empresa alterada com sucesso!')
        self.atualizar_lista()
    
    def mostrar_popup_codigo(self, titulo, mensagem, codigo):
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)
        label = Label(text=mensagem, text_size=(350, None), halign='center', valign='middle')
        codigo_input = TextInput(text=codigo, readonly=True, multiline=False, size_hint_y=None, height=40)
        btn_ok = Button(text='OK', size_hint_y=None, height=40, color=(0.5, 0.8, 1, 1))
        content.add_widget(label)
        content.add_widget(codigo_input)
        content.add_widget(btn_ok)
        popup = Popup(title=titulo, content=content, size_hint=(0.8, 0.6))
        btn_ok.bind(on_press=popup.dismiss)
        popup.open()
    
    def mostrar_popup(self, titulo, mensagem):
        content = BoxLayout(orientation='vertical', padding=10)
        label = Label(text=mensagem, text_size=(350, None), halign='center', valign='middle')
        btn_ok = Button(text='OK', size_hint_y=None, height=40, color=(0.5, 0.8, 1, 1))
        content.add_widget(label)
        content.add_widget(btn_ok)
        popup = Popup(title=titulo, content=content, size_hint=(0.8, 0.5))
        btn_ok.bind(on_press=popup.dismiss)
        popup.open()

class TelaMesario(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from kivy.uix.floatlayout import FloatLayout
        
        layout = FloatLayout()
        
        with layout.canvas.before:
            Color(0.9, 0.95, 1, 1)
            self.rect_bg = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self.atualizar_fundo, pos=self.atualizar_fundo)
        
        # Botão voltar
        app = App.get_running_app()
        container_voltar, btn_voltar = app.criar_botao_com_icone('<< Voltar', 'icones/voltar.png', (1, 0.8, 0.8, 1), (50, 50))
        container_voltar.size_hint = (None, None)
        container_voltar.size = (130, 40)
        container_voltar.spacing = 5
        container_voltar.pos_hint = {'x': 0.02, 'top': 0.95}
        btn_voltar.size_hint = (None, None)
        btn_voltar.size = (100, 40)
        btn_voltar.bind(on_press=self.voltar)
        layout.add_widget(container_voltar)
        
        # Título
        titulo = Label(text='PAINEL DO MESARIO', font_size='18sp', bold=True, size_hint=(None, None), size=(400, 40), pos_hint={'center_x': 0.5, 'center_y': 0.8}, color=(1, 0.6, 0.2, 1))
        layout.add_widget(titulo)
        
        # Menu centralizado
        menu = GridLayout(cols=2, spacing=20, size_hint=(None, None), size=(450, 150), pos_hint={'center_x': 0.5, 'center_y': 0.55})
        
        app = App.get_running_app()
        container_iniciar, btn_iniciar = app.criar_botao_com_icone('INICIAR\nEleicao', 'icones/confirmar.png', (0.7, 1, 0.7, 1), (50, 50))
        container_iniciar.spacing = 8
        btn_iniciar.size_hint = (None, None)
        btn_iniciar.size = (140, 60)
        btn_iniciar.bind(on_press=self.iniciar_eleicao)
        
        container_finalizar, btn_finalizar = app.criar_botao_com_icone('FINALIZAR\nEleicao', 'icones/excluir.png', (1, 0.8, 0.8, 1), (50, 50))
        container_finalizar.spacing = 8
        btn_finalizar.size_hint = (None, None)
        btn_finalizar.size = (140, 60)
        btn_finalizar.bind(on_press=self.finalizar_eleicao)
        
        container_relatorios, btn_relatorios = app.criar_botao_com_icone('RELATORIOS\nResultados', 'icones/listar.png', (0.7, 0.9, 1, 1), (50, 50))
        container_relatorios.spacing = 8
        btn_relatorios.size_hint = (None, None)
        btn_relatorios.size = (140, 60)
        btn_relatorios.bind(on_press=self.ver_relatorios)
        
        container_backup, btn_backup = app.criar_botao_com_icone('BACKUP\nDados', 'icones/salvar.png', (0.9, 0.8, 1, 1), (50, 50))
        container_backup.spacing = 8
        btn_backup.size_hint = (None, None)
        btn_backup.size = (140, 60)
        btn_backup.bind(on_press=self.fazer_backup)
        
        menu.add_widget(container_iniciar)
        menu.add_widget(container_finalizar)
        menu.add_widget(container_relatorios)
        menu.add_widget(container_backup)
        
        layout.add_widget(menu)
        
        # Status centralizado
        self.status = Label(text='Status: Eleicao nao iniciada', size_hint=(None, None), size=(400, 50), pos_hint={'center_x': 0.5, 'center_y': 0.3}, color=(1, 0.6, 0.2, 1))
        layout.add_widget(self.status)
        
        self.add_widget(layout)
    
    def atualizar_fundo(self, instance, value):
        self.rect_bg.size = instance.size
        self.rect_bg.pos = instance.pos
    
    def voltar(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.manager.current = 'inicial'
    
    def iniciar_eleicao(self, instance):
        App.get_running_app().tocar_som('confirma')
        app = App.get_running_app()
        app.dados['configuracoes']['eleicao_ativa'] = True
        app.salvar_dados()
        self.status.text = 'Status: Eleicao ATIVA'
        self.mostrar_popup('Sucesso', 'Eleicao iniciada!')
    
    def finalizar_eleicao(self, instance):
        App.get_running_app().tocar_som('confirma')
        app = App.get_running_app()
        app.dados['configuracoes']['eleicao_ativa'] = False
        app.salvar_dados()
        self.status.text = 'Status: Eleicao FINALIZADA'
        self.mostrar_popup('Sucesso', 'Eleicao finalizada!')
    
    def ver_relatorios(self, instance):
        App.get_running_app().tocar_som('tecla')
        app = App.get_running_app()
        texto = 'RESULTADOS:\n\n'
        for empresa, votos in app.dados['votos'].items():
            texto += f'Empresa {empresa}:\n'
            for numero, qtd in votos.items():
                texto += f'  Candidato {numero}: {qtd} votos\n'
            texto += '\n'
        self.mostrar_popup('Relatorios', texto)
    
    def fazer_backup(self, instance):
        App.get_running_app().tocar_som('confirma')
        app = App.get_running_app()
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'backup_{timestamp}.json'
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(app.dados, f, ensure_ascii=False, indent=2)
        self.mostrar_popup('Sucesso', f'Backup criado: {backup_file}')
    
    def mostrar_popup(self, titulo, mensagem):
        content = Label(text=mensagem, text_size=(500, None), halign='center', valign='middle')
        popup = Popup(title=titulo, content=content, size_hint=(0.9, 0.7))
        popup.open()

class TelaInscricoes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        with layout.canvas.before:
            Color(0.9, 0.95, 1, 1)
            self.rect_bg = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self.atualizar_fundo, pos=self.atualizar_fundo)
        
        header = BoxLayout(orientation='horizontal', size_hint_y=0.12)
        app = App.get_running_app()
        container_voltar, btn_voltar = app.criar_botao_com_icone('<< Voltar', 'icones/voltar.png', (1, 0.8, 0.8, 1), (50, 50))
        container_voltar.size_hint = (None, None)
        container_voltar.size = (130, 40)
        container_voltar.spacing = 5
        btn_voltar.size_hint = (None, None)
        btn_voltar.size = (100, 40)
        btn_voltar.bind(on_press=self.voltar)
        titulo = Label(text='INSCRICOES DE CANDIDATOS', font_size='16sp', bold=True, color=(1, 0.6, 0.2, 1))
        header.add_widget(container_voltar)
        header.add_widget(titulo)
        layout.add_widget(header)
        
        form = GridLayout(cols=2, spacing=8, size_hint=(None, None), size=(400, 120), pos_hint={'center_x': 0.5})
        
        form.add_widget(Label(text='Nome:', color=(1, 0.6, 0.2, 1)))
        self.input_nome = TextInput()
        form.add_widget(self.input_nome)
        
        form.add_widget(Label(text='CPF:', color=(1, 0.6, 0.2, 1)))
        self.input_cpf = TextInput()
        form.add_widget(self.input_cpf)
        
        form.add_widget(Label(text='Codigo da Empresa:', color=(1, 0.6, 0.2, 1)))
        self.input_empresa = TextInput()
        form.add_widget(self.input_empresa)
        
        layout.add_widget(form)
        
        btn_container = BoxLayout(size_hint=(None, None), size=(250, 50), pos_hint={'center_x': 0.5})
        app = App.get_running_app()
        container_inscrever, btn_inscrever = app.criar_botao_com_icone('Inscrever Candidato', 'icones/salvar.png', (0.7, 1, 0.7, 1), (50, 50))
        container_inscrever.spacing = 8
        btn_inscrever.size_hint = (None, None)
        btn_inscrever.size = (180, 40)
        btn_inscrever.bind(on_press=self.inscrever_candidato)
        btn_container.add_widget(container_inscrever)
        layout.add_widget(btn_container)
        
        self.lista = Label(text='Candidatos aparecerao aqui...', size_hint_y=0.45, text_size=(None, None), valign='top', color=(1, 0.6, 0.2, 1))
        layout.add_widget(self.lista)
        
        self.add_widget(layout)
    
    def atualizar_fundo(self, instance, value):
        self.rect_bg.size = instance.size
        self.rect_bg.pos = instance.pos
    
    def voltar(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.manager.current = 'inicial'
    
    def inscrever_candidato(self, instance):
        App.get_running_app().tocar_som('confirma')
        app = App.get_running_app()
        if not all([self.input_nome.text, self.input_cpf.text, self.input_empresa.text]):
            App.get_running_app().tocar_som('erro')
            self.mostrar_popup('Erro', 'Preencha todos os campos!')
            return
        
        codigo_valido = False
        for emp_id, dados in app.dados['empresas'].items():
            if dados['codigo_acesso'] == self.input_empresa.text:
                codigo_valido = True
                break
        
        if not codigo_valido:
            App.get_running_app().tocar_som('erro')
            self.mostrar_popup('Erro', 'Codigo da empresa invalido!')
            return
        
        candidato_id = hashlib.md5(self.input_cpf.text.encode()).hexdigest()[:8]
        numero = len(app.dados['candidatos']) + 1
        
        app.dados['candidatos'][candidato_id] = {
            'nome': self.input_nome.text,
            'cpf': self.input_cpf.text,
            'empresa': self.input_empresa.text,
            'numero': numero
        }
        app.salvar_dados()
        self.mostrar_popup('Sucesso', f'Candidato inscrito!\nNumero: {numero:02d}')
        self.limpar_campos()
        self.listar_candidatos()
    
    def listar_candidatos(self):
        app = App.get_running_app()
        if not app.dados['candidatos']:
            self.lista.text = 'Nenhum candidato inscrito.'
            return
        
        texto = 'CANDIDATOS INSCRITOS:\n\n'
        for cand_id, dados in app.dados['candidatos'].items():
            texto += f"• {dados['numero']:02d} - {dados['nome']} ({dados['empresa']})\n"
        
        self.lista.text = texto
        self.lista.text_size = (self.width - 40, None)
    
    def limpar_campos(self):
        self.input_nome.text = ''
        self.input_cpf.text = ''
        self.input_empresa.text = ''
    
    def mostrar_popup(self, titulo, mensagem):
        content = Label(text=mensagem, text_size=(400, None), halign='center', valign='middle')
        popup = Popup(title=titulo, content=content, size_hint=(0.8, 0.6))
        popup.open()

class TelaCodigoEmpresa(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from kivy.uix.floatlayout import FloatLayout
        
        layout = FloatLayout()
        
        with layout.canvas.before:
            Color(0.9, 0.95, 1, 1)
            self.rect_bg = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self.atualizar_fundo, pos=self.atualizar_fundo)
        
        # Título centralizado
        titulo = Label(text='DIGITE O CODIGO DA EMPRESA', font_size='24sp', bold=True, size_hint=(None, None), size=(500, 60), pos_hint={'center_x': 0.5, 'center_y': 0.7}, color=(1, 0.6, 0.2, 1))
        layout.add_widget(titulo)
        
        # Input centralizado
        self.input_codigo = TextInput(font_size='32sp', halign='center', multiline=False, size_hint=(None, None), size=(300, 60), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(self.input_codigo)
        
        # Botões centralizados
        btn_layout = BoxLayout(orientation='horizontal', spacing=40, size_hint=(None, None), size=(400, 60), pos_hint={'center_x': 0.5, 'center_y': 0.3})
        
        app = App.get_running_app()
        container_confirmar, btn_confirmar = app.criar_botao_com_icone('CONFIRMAR', 'icones/confirmar.png', (0.7, 1, 0.7, 1), (50, 50))
        container_confirmar.spacing = 8
        btn_confirmar.size_hint = (None, None)
        btn_confirmar.size = (130, 50)
        btn_confirmar.bind(on_press=self.confirmar_codigo)
        
        container_voltar, btn_voltar = app.criar_botao_com_icone('VOLTAR', 'icones/voltar.png', (1, 0.8, 0.8, 1), (50, 50))
        container_voltar.spacing = 8
        btn_voltar.size_hint = (None, None)
        btn_voltar.size = (130, 50)
        btn_voltar.bind(on_press=self.voltar)
        
        btn_layout.add_widget(container_confirmar)
        btn_layout.add_widget(container_voltar)
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
    
    def atualizar_fundo(self, instance, value):
        self.rect_bg.size = instance.size
        self.rect_bg.pos = instance.pos
    
    def confirmar_codigo(self, instance):
        App.get_running_app().tocar_som('confirma')
        app = App.get_running_app()
        
        if not self.input_codigo.text:
            App.get_running_app().tocar_som('erro')
            self.mostrar_popup('Erro', 'Digite o codigo da empresa!')
            return
        
        codigo_valido = False
        for emp_id, dados in app.dados['empresas'].items():
            if dados['codigo_acesso'] == self.input_codigo.text:
                codigo_valido = True
                app.empresa_atual = self.input_codigo.text
                break
        
        if codigo_valido:
            self.input_codigo.text = ''
            self.manager.current = 'votacao'
        else:
            App.get_running_app().tocar_som('erro')
            self.mostrar_popup('Erro', 'Codigo da empresa invalido!')
    
    def voltar(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.input_codigo.text = ''
        self.manager.current = 'inicial'
    
    def mostrar_popup(self, titulo, mensagem):
        content = Label(text=mensagem, text_size=(400, None), halign='center', valign='middle')
        popup = Popup(title=titulo, content=content, size_hint=(0.8, 0.6))
        popup.open()

class TelaVotacao(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.numero_digitado = ''
        layout = BoxLayout(orientation='horizontal', padding=20, spacing=20)
        
        with layout.canvas.before:
            Color(0.9, 0.95, 1, 1)
            self.rect_bg = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self.atualizar_fundo, pos=self.atualizar_fundo)
        
        painel_esquerdo = BoxLayout(orientation='vertical', size_hint_x=0.6)
        tela_urna = BoxLayout(orientation='vertical', padding=20)
        
        with tela_urna.canvas.before:
            Color(0.8, 1, 0.8, 1)
            self.rect = Rectangle(size=tela_urna.size, pos=tela_urna.pos)
        
        tela_urna.bind(size=self.atualizar_rect, pos=self.atualizar_rect)
        
        header = Label(text='ELEICAO CIPA 2024', font_size='24sp', color=(1, 0.6, 0.2, 1), size_hint_y=0.15)
        tela_urna.add_widget(header)
        
        instrucao = Label(text='Digite o numero de seu candidato:', font_size='18sp', color=(1, 0.6, 0.2, 1), size_hint_y=0.1)
        tela_urna.add_widget(instrucao)
        
        self.display_numero = Label(text='_ _', font_size='48sp', color=(1, 0.6, 0.2, 1), bold=True, size_hint_y=0.15)
        tela_urna.add_widget(self.display_numero)
        
        self.info_candidato = Label(text='', font_size='16sp', color=(1, 0.6, 0.2, 1), text_size=(None, None), size_hint_y=0.2)
        tela_urna.add_widget(self.info_candidato)
        
        self.lista_candidatos = Label(text='', font_size='12sp', color=(1, 0.6, 0.2, 1), text_size=(None, None), valign='top', size_hint_y=0.4)
        tela_urna.add_widget(self.lista_candidatos)
        
        painel_esquerdo.add_widget(tela_urna)
        
        painel_direito = BoxLayout(orientation='vertical', size_hint_x=0.4)
        
        teclado = GridLayout(cols=3, spacing=2, size_hint_y=0.8)
        
        def criar_tecla(texto, cor_fundo, callback):
            btn = Button(text=texto, font_size='20sp', background_normal='', background_color=cor_fundo, color=(0.5, 0.8, 1, 1))
            def desenhar(instance, *args):
                instance.canvas.before.clear()
                with instance.canvas.before:
                    Color(*cor_fundo)
                    RoundedRectangle(pos=instance.pos, size=instance.size, radius=[8])
            btn.bind(pos=desenhar, size=desenhar, on_press=callback)
            desenhar(btn)
            return btn
        
        for i in range(1, 10):
            btn = criar_tecla(str(i), (0.1, 0.1, 0.1, 1), lambda x, num=str(i): self.digitar_numero(num))
            teclado.add_widget(btn)
        
        btn_corrige = criar_tecla('CORRIGE', (1, 0, 0, 1), self.corrigir)
        btn_corrige.color = (0.5, 0.8, 1, 1)
        btn_corrige.font_size = '12sp'
        
        btn_zero = criar_tecla('0', (0.1, 0.1, 0.1, 1), lambda x: self.digitar_numero('0'))
        
        btn_confirma = criar_tecla('CONFIRMA', (0.133, 0.545, 0.133, 1), self.confirmar_voto)
        btn_confirma.color = (0.5, 0.8, 1, 1)
        btn_confirma.font_size = '12sp'
        
        teclado.add_widget(btn_corrige)
        teclado.add_widget(btn_zero)
        teclado.add_widget(btn_confirma)
        
        btn_branco = criar_tecla('BRANCO', (1, 1, 1, 1), self.votar_branco)
        btn_branco.color = (0.5, 0.8, 1, 1)
        btn_branco.font_size = '12sp'
        
        espaco1 = Label(text='')
        espaco2 = Label(text='')
        
        teclado.add_widget(btn_branco)
        teclado.add_widget(espaco1)
        teclado.add_widget(espaco2)
        
        painel_direito.add_widget(teclado)
        
        app = App.get_running_app()
        container_voltar, btn_voltar = app.criar_botao_com_icone('<< Voltar', 'icones/voltar.png', (1, 0.8, 0.8, 1), (50, 50))
        container_voltar.size_hint_y = 0.1
        container_voltar.spacing = 5
        btn_voltar.size_hint = (None, None)
        btn_voltar.size = (100, 40)
        btn_voltar.bind(on_press=self.voltar)
        painel_direito.add_widget(container_voltar)
        
        layout.add_widget(painel_esquerdo)
        layout.add_widget(painel_direito)
        self.add_widget(layout)
    
    def on_enter(self):
        self.mostrar_lista_candidatos()
    
    def atualizar_fundo(self, instance, value):
        self.rect_bg.size = instance.size
        self.rect_bg.pos = instance.pos
    
    def atualizar_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
    
    def mostrar_lista_candidatos(self):
        app = App.get_running_app()
        if not app.dados['candidatos']:
            self.lista_candidatos.text = 'Nenhum candidato cadastrado.'
            return
        
        texto = 'CANDIDATOS:\n\n'
        candidatos_empresa = []
        
        for cand_id, dados in app.dados['candidatos'].items():
            if dados['empresa'] == app.empresa_atual:
                candidatos_empresa.append(dados)
        
        candidatos_empresa.sort(key=lambda x: x['numero'])
        
        for dados in candidatos_empresa:
            texto += f"{dados['numero']:02d} - {dados['nome']}\n"
        
        self.lista_candidatos.text = texto
        self.lista_candidatos.text_size = (300, None)
    
    def voltar(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.numero_digitado = ''
        self.atualizar_display()
        self.info_candidato.text = ''
        self.manager.current = 'inicial'
    
    def digitar_numero(self, numero):
        App.get_running_app().tocar_som('tecla')
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
        
        candidato_encontrado = None
        for dados in app.dados['candidatos'].values():
            if dados['numero'] == numero and dados['empresa'] == app.empresa_atual:
                candidato_encontrado = dados
                break
        
        if candidato_encontrado:
            self.info_candidato.text = f"Nome: {candidato_encontrado['nome']}"
            self.info_candidato.text_size = (400, None)
        else:
            self.info_candidato.text = "CANDIDATO NAO ENCONTRADO"
            self.info_candidato.text_size = (400, None)
    
    def corrigir(self, instance):
        App.get_running_app().tocar_som('corrige')
        self.numero_digitado = ''
        self.atualizar_display()
        self.info_candidato.text = ''
    
    def votar_branco(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.numero_digitado = '00'
        self.display_numero.text = 'BRANCO'
        self.info_candidato.text = 'VOTO EM BRANCO'
    
    def confirmar_voto(self, instance):
        app = App.get_running_app()
        app.tocar_som('confirma')
        
        if not app.dados['configuracoes']['eleicao_ativa']:
            App.get_running_app().tocar_som('erro')
            self.mostrar_popup('Erro', 'Eleicao nao esta ativa!')
            return
        
        if not self.numero_digitado:
            App.get_running_app().tocar_som('erro')
            self.mostrar_popup('Erro', 'Digite um numero ou BRANCO!')
            return
        
        if self.numero_digitado == '00':
            numero = 'BRANCO'
        else:
            if len(self.numero_digitado) != 2:
                App.get_running_app().tocar_som('erro')
                self.mostrar_popup('Erro', 'Digite um numero valido!')
                return
            numero = int(self.numero_digitado)
        
        empresa = app.empresa_atual
        
        if empresa not in app.dados['votos']:
            app.dados['votos'][empresa] = {}
        
        voto_key = str(numero)
        if voto_key not in app.dados['votos'][empresa]:
            app.dados['votos'][empresa][voto_key] = 0
        
        app.dados['votos'][empresa][voto_key] += 1
        
        eleitor_id = hashlib.md5(f"{empresa}_{datetime.datetime.now().isoformat()}".encode()).hexdigest()[:8]
        app.dados['eleitores'][eleitor_id] = {
            'empresa': empresa,
            'data_voto': datetime.datetime.now().isoformat(),
            'numero_votado': str(numero)
        }
        
        app.salvar_dados()
        
        self.numero_digitado = ''
        self.atualizar_display()
        self.info_candidato.text = ''
        
        if numero == 'BRANCO':
            self.mostrar_popup('Sucesso', 'Voto em BRANCO registrado!')
        else:
            self.mostrar_popup('Sucesso', 'Voto registrado com sucesso!')
    
    def mostrar_popup(self, titulo, mensagem):
        content = Label(text=mensagem, text_size=(400, None), halign='center', valign='middle')
        popup = Popup(title=titulo, content=content, size_hint=(0.8, 0.6))
        popup.open()

class TelaCodigoInscricoes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from kivy.uix.floatlayout import FloatLayout
        
        layout = FloatLayout()
        
        with layout.canvas.before:
            Color(0.9, 0.95, 1, 1)
            self.rect_bg = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self.atualizar_fundo, pos=self.atualizar_fundo)
        
        # Título centralizado
        titulo = Label(text='DIGITE O CODIGO DA EMPRESA\nPARA INSCRICOES', font_size='24sp', bold=True, size_hint=(None, None), size=(500, 80), pos_hint={'center_x': 0.5, 'center_y': 0.7}, color=(1, 0.6, 0.2, 1))
        layout.add_widget(titulo)
        
        # Input centralizado
        self.input_codigo = TextInput(font_size='32sp', halign='center', multiline=False, size_hint=(None, None), size=(300, 60), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(self.input_codigo)
        
        # Botões centralizados
        btn_layout = BoxLayout(orientation='horizontal', spacing=40, size_hint=(None, None), size=(400, 60), pos_hint={'center_x': 0.5, 'center_y': 0.3})
        
        app = App.get_running_app()
        container_confirmar, btn_confirmar = app.criar_botao_com_icone('CONFIRMAR', 'icones/confirmar.png', (0.7, 1, 0.7, 1), (50, 50))
        container_confirmar.spacing = 8
        btn_confirmar.size_hint = (None, None)
        btn_confirmar.size = (130, 50)
        btn_confirmar.bind(on_press=self.confirmar_codigo)
        
        container_voltar, btn_voltar = app.criar_botao_com_icone('VOLTAR', 'icones/voltar.png', (1, 0.8, 0.8, 1), (50, 50))
        container_voltar.spacing = 8
        btn_voltar.size_hint = (None, None)
        btn_voltar.size = (130, 50)
        btn_voltar.bind(on_press=self.voltar)
        
        btn_layout.add_widget(container_confirmar)
        btn_layout.add_widget(container_voltar)
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
    
    def atualizar_fundo(self, instance, value):
        self.rect_bg.size = instance.size
        self.rect_bg.pos = instance.pos
    
    def confirmar_codigo(self, instance):
        App.get_running_app().tocar_som('confirma')
        app = App.get_running_app()
        
        if not self.input_codigo.text:
            App.get_running_app().tocar_som('erro')
            self.mostrar_popup('Erro', 'Digite o codigo da empresa!')
            return
        
        codigo_valido = False
        for emp_id, dados in app.dados['empresas'].items():
            if dados['codigo_acesso'] == self.input_codigo.text:
                codigo_valido = True
                app.empresa_atual = self.input_codigo.text
                break
        
        if codigo_valido:
            self.input_codigo.text = ''
            self.manager.current = 'inscricoes'
        else:
            App.get_running_app().tocar_som('erro')
            self.mostrar_popup('Erro', 'Codigo da empresa invalido!')
    
    def voltar(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.input_codigo.text = ''
        self.manager.current = 'inicial'
    
    def mostrar_popup(self, titulo, mensagem):
        content = Label(text=mensagem, text_size=(400, None), halign='center', valign='middle')
        popup = Popup(title=titulo, content=content, size_hint=(0.8, 0.6))
        popup.open()

if __name__ == '__main__':
    UrnaEletronicaCIPA().run()