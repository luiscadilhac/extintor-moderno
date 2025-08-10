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
from kivy.graphics import Color, Rectangle
import json
import datetime
import os
import hashlib
import random

kivy.require('2.0.0')

def criar_botao_com_icone(texto, icone_path, cor):
    layout = BoxLayout(orientation='horizontal', spacing=10)
    
    if os.path.exists(icone_path):
        icone = Image(source=icone_path, size_hint_x=0.3)
        layout.add_widget(icone)
    
    label = Label(text=texto, font_size='14sp', size_hint_x=0.7, color=(0, 0, 0, 1))
    layout.add_widget(label)
    
    btn = Button(size_hint=(1, 0.6), background_color=cor)
    btn.add_widget(layout)
    return btn

def criar_botao_pequeno(texto, icone_path, cor):
    layout = BoxLayout(orientation='horizontal', spacing=5)
    
    if os.path.exists(icone_path):
        icone = Image(source=icone_path, size_hint_x=0.2)
        layout.add_widget(icone)
    
    label = Label(text=texto, font_size='12sp', size_hint_x=0.8, color=(0, 0, 0, 1))
    layout.add_widget(label)
    
    btn = Button(background_color=cor)
    btn.add_widget(layout)
    return btn

class UrnaEletronicaCIPA(App):
    def __init__(self):
        super().__init__()
        self.dados_file = 'dados_urna_cipa.json'
        self.dados = self.carregar_dados()
        self.empresa_atual = None
    
    def tocar_som(self, tipo):
        try:
            import winsound
            if tipo == 'tecla':
                winsound.Beep(800, 100)
            elif tipo == 'confirma':
                winsound.Beep(1000, 200)
            elif tipo == 'corrige':
                winsound.Beep(600, 150)
            elif tipo == 'erro':
                winsound.Beep(400, 300)
        except:
            print(f"[SOM] {tipo}")
        
    def carregar_dados(self):
        if os.path.exists(self.dados_file):
            with open(self.dados_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'empresas': {},
            'candidatos': {},
            'votos': {},
            'eleitores': {},
            'configuracoes': {'eleicao_ativa': False}
        }
    
    def salvar_dados(self):
        with open(self.dados_file, 'w', encoding='utf-8') as f:
            json.dump(self.dados, f, ensure_ascii=False, indent=2)
    
    def build(self):
        self.title = "Urna Eletronica CIPA"
        sm = ScreenManager()
        sm.add_widget(TelaInicial(name='inicial'))
        sm.add_widget(TelaEmpresa(name='empresa'))
        sm.add_widget(TelaMesario(name='mesario'))
        sm.add_widget(TelaInscricoes(name='inscricoes'))
        sm.add_widget(TelaCodigoEmpresa(name='codigo_empresa'))
        sm.add_widget(TelaVotacao(name='votacao'))
        return sm

class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        with layout.canvas.before:
            Color(0.9, 0.95, 1, 1)
            self.rect_bg = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self.atualizar_fundo, pos=self.atualizar_fundo)
        
        if os.path.exists('logo_urna.png'):
            logo = Image(source='logo_urna.png', size_hint_y=0.15)
            layout.add_widget(logo)
        
        titulo = Label(text='URNA ELETRONICA CIPA', font_size='28sp', bold=True, size_hint_y=0.15, color=(1, 0.6, 0.2, 1))
        layout.add_widget(titulo)
        
        menu = GridLayout(cols=2, spacing=15, size_hint_y=0.7)
        
        btn_empresa = criar_botao_com_icone('EMPRESA\nGerenciar', 'icones/empresa.png', (0.7, 1, 0.7, 1))
        btn_empresa.bind(on_press=self.ir_empresa)
        
        btn_mesario = criar_botao_com_icone('MESARIO\nAdministrar', 'icones/mesario.png', (1, 0.9, 0.6, 1))
        btn_mesario.bind(on_press=self.ir_mesario)
        
        btn_inscricoes = criar_botao_com_icone('INSCRICOES\nCandidatos', 'icones/inscricoes.png', (0.7, 0.9, 1, 1))
        btn_inscricoes.bind(on_press=self.ir_inscricoes)
        
        btn_votacao = criar_botao_com_icone('VOTACAO\nEleitor', 'icones/votacao.png', (1, 0.8, 1, 1))
        btn_votacao.bind(on_press=self.ir_votacao)
        
        menu.add_widget(btn_empresa)
        menu.add_widget(btn_mesario)
        menu.add_widget(btn_inscricoes)
        menu.add_widget(btn_votacao)
        
        layout.add_widget(menu)
        self.add_widget(layout)
    
    def atualizar_fundo(self, instance, value):
        self.rect_bg.size = instance.size
        self.rect_bg.pos = instance.pos
    
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
        self.manager.current = 'codigo_empresa'

class TelaEmpresa(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        with layout.canvas.before:
            Color(0.9, 0.95, 1, 1)
            self.rect_bg = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self.atualizar_fundo, pos=self.atualizar_fundo)
        
        header = BoxLayout(orientation='horizontal', size_hint_y=0.12)
        btn_voltar = criar_botao_pequeno('<< Voltar', 'icones/voltar.png', (1, 0.8, 0.8, 1))
        btn_voltar.size_hint_x = 0.15
        btn_voltar.size_hint_y = 0.6
        btn_voltar.bind(on_press=self.voltar)
        titulo = Label(text='GESTAO DE EMPRESAS', font_size='18sp', bold=True, color=(1, 0.6, 0.2, 1))
        header.add_widget(btn_voltar)
        header.add_widget(titulo)
        layout.add_widget(header)
        
        form = GridLayout(cols=2, spacing=8, size_hint_y=0.25)
        form.add_widget(Label(text='Nome da Empresa:', size_hint_y=0.7, color=(1, 0.6, 0.2, 1)))
        self.input_nome = TextInput(size_hint_y=0.7)
        form.add_widget(self.input_nome)
        
        form.add_widget(Label(text='CNPJ:', size_hint_y=0.7, color=(1, 0.6, 0.2, 1)))
        self.input_cnpj = TextInput(size_hint_y=0.7)
        form.add_widget(self.input_cnpj)
        
        layout.add_widget(form)
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.08)
        btn_cadastrar = criar_botao_pequeno('Cadastrar', 'icones/salvar.png', (0.7, 1, 0.7, 1))
        btn_cadastrar.bind(on_press=self.cadastrar_empresa)
        btn_listar = criar_botao_pequeno('Listar', 'icones/listar.png', (0.7, 0.9, 1, 1))
        btn_listar.bind(on_press=self.listar_empresas)
        btn_excluir = criar_botao_pequeno('Excluir', 'icones/excluir.png', (1, 0.8, 0.8, 1))
        btn_excluir.bind(on_press=self.excluir_empresa)
        btn_layout.add_widget(btn_cadastrar)
        btn_layout.add_widget(btn_listar)
        btn_layout.add_widget(btn_excluir)
        layout.add_widget(btn_layout)
        
        self.lista = Label(text='Empresas aparecerao aqui...', size_hint_y=0.55, text_size=(None, None), valign='top', color=(1, 0.6, 0.2, 1))
        layout.add_widget(self.lista)
        
        self.add_widget(layout)
    
    def atualizar_fundo(self, instance, value):
        self.rect_bg.size = instance.size
        self.rect_bg.pos = instance.pos
    
    def voltar(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.manager.current = 'inicial'
    
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
        self.listar_empresas(None)
    
    def excluir_empresa(self, instance):
        App.get_running_app().tocar_som('tecla')
        if not self.input_nome.text:
            App.get_running_app().tocar_som('erro')
            self.mostrar_popup('Erro', 'Digite o nome da empresa para excluir!')
            return
        
        app = App.get_running_app()
        empresa_encontrada = None
        for emp_id, dados in app.dados['empresas'].items():
            if dados['nome'].lower() == self.input_nome.text.lower():
                empresa_encontrada = emp_id
                break
        
        if empresa_encontrada:
            del app.dados['empresas'][empresa_encontrada]
            app.salvar_dados()
            self.mostrar_popup('Sucesso', 'Empresa excluida!')
            self.input_nome.text = ''
            self.input_cnpj.text = ''
            self.listar_empresas(None)
        else:
            App.get_running_app().tocar_som('erro')
            self.mostrar_popup('Erro', 'Empresa nao encontrada!')
    
    def listar_empresas(self, instance):
        if instance:
            App.get_running_app().tocar_som('tecla')
        app = App.get_running_app()
        if not app.dados['empresas']:
            self.lista.text = 'Nenhuma empresa cadastrada.'
            return
        
        texto = 'EMPRESAS CADASTRADAS:\n\n'
        for emp_id, dados in app.dados['empresas'].items():
            texto += f"• {dados['nome']} - Codigo: {dados['codigo_acesso']}\n"
        
        self.lista.text = texto
        self.lista.text_size = (self.width - 40, None)
    
    def mostrar_popup_codigo(self, titulo, mensagem, codigo):
        content = BoxLayout(orientation='vertical', spacing=10)
        label = Label(text=mensagem)
        codigo_input = TextInput(text=codigo, readonly=True, multiline=False)
        content.add_widget(label)
        content.add_widget(codigo_input)
        popup = Popup(title=titulo, content=content, size_hint=(0.6, 0.4))
        popup.open()
    
    def mostrar_popup(self, titulo, mensagem):
        popup = Popup(title=titulo, content=Label(text=mensagem), size_hint=(0.6, 0.4))
        popup.open()

class TelaMesario(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        with layout.canvas.before:
            Color(0.9, 0.95, 1, 1)
            self.rect_bg = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self.atualizar_fundo, pos=self.atualizar_fundo)
        
        header = BoxLayout(orientation='horizontal', size_hint_y=0.12)
        btn_voltar = criar_botao_pequeno('<< Voltar', 'icones/voltar.png', (1, 0.8, 0.8, 1))
        btn_voltar.size_hint_x = 0.15
        btn_voltar.size_hint_y = 0.6
        btn_voltar.bind(on_press=self.voltar)
        titulo = Label(text='PAINEL DO MESARIO', font_size='18sp', bold=True, color=(1, 0.6, 0.2, 1))
        header.add_widget(btn_voltar)
        header.add_widget(titulo)
        layout.add_widget(header)
        
        menu = GridLayout(cols=2, spacing=12, size_hint_y=0.6)
        
        btn_iniciar = Button(text='INICIAR\nEleicao', size_hint=(1, 0.6), background_color=(0.7, 1, 0.7, 1))
        btn_iniciar.bind(on_press=self.iniciar_eleicao)
        
        btn_finalizar = Button(text='FINALIZAR\nEleicao', size_hint=(1, 0.6), background_color=(1, 0.8, 0.8, 1))
        btn_finalizar.bind(on_press=self.finalizar_eleicao)
        
        btn_relatorios = Button(text='RELATORIOS\nResultados', size_hint=(1, 0.6), background_color=(0.7, 0.9, 1, 1))
        btn_relatorios.bind(on_press=self.ver_relatorios)
        
        btn_backup = Button(text='BACKUP\nDados', size_hint=(1, 0.6), background_color=(0.9, 0.8, 1, 1))
        btn_backup.bind(on_press=self.fazer_backup)
        
        menu.add_widget(btn_iniciar)
        menu.add_widget(btn_finalizar)
        menu.add_widget(btn_relatorios)
        menu.add_widget(btn_backup)
        
        layout.add_widget(menu)
        
        self.status = Label(text='Status: Eleicao nao iniciada', size_hint_y=0.28, color=(1, 0.6, 0.2, 1))
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
        popup = Popup(title=titulo, content=Label(text=mensagem), size_hint=(0.8, 0.6))
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
        btn_voltar = criar_botao_pequeno('<< Voltar', 'icones/voltar.png', (1, 0.8, 0.8, 1))
        btn_voltar.size_hint_x = 0.15
        btn_voltar.size_hint_y = 0.6
        btn_voltar.bind(on_press=self.voltar)
        titulo = Label(text='INSCRICOES DE CANDIDATOS', font_size='16sp', bold=True, color=(1, 0.6, 0.2, 1))
        header.add_widget(btn_voltar)
        header.add_widget(titulo)
        layout.add_widget(header)
        
        form = GridLayout(cols=2, spacing=8, size_hint_y=0.35)
        
        form.add_widget(Label(text='Nome:', size_hint_y=0.7, color=(1, 0.6, 0.2, 1)))
        self.input_nome = TextInput(size_hint_y=0.7)
        form.add_widget(self.input_nome)
        
        form.add_widget(Label(text='CPF:', size_hint_y=0.7, color=(1, 0.6, 0.2, 1)))
        self.input_cpf = TextInput(size_hint_y=0.7)
        form.add_widget(self.input_cpf)
        
        form.add_widget(Label(text='Codigo da Empresa:', size_hint_y=0.7, color=(1, 0.6, 0.2, 1)))
        self.input_empresa = TextInput(size_hint_y=0.7)
        form.add_widget(self.input_empresa)
        
        layout.add_widget(form)
        
        btn_inscrever = criar_botao_pequeno('Inscrever Candidato', 'icones/confirmar.png', (0.7, 1, 0.7, 1))
        btn_inscrever.size_hint_y = 0.08
        btn_inscrever.bind(on_press=self.inscrever_candidato)
        layout.add_widget(btn_inscrever)
        
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
        popup = Popup(title=titulo, content=Label(text=mensagem), size_hint=(0.6, 0.4))
        popup.open()

class TelaCodigoEmpresa(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=30)
        
        with layout.canvas.before:
            Color(0.9, 0.95, 1, 1)
            self.rect_bg = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self.atualizar_fundo, pos=self.atualizar_fundo)
        
        titulo = Label(text='DIGITE O CODIGO DA EMPRESA', font_size='24sp', bold=True, size_hint_y=0.3, color=(1, 0.6, 0.2, 1))
        layout.add_widget(titulo)
        
        self.input_codigo = TextInput(font_size='32sp', size_hint_y=0.2, halign='center', multiline=False)
        layout.add_widget(self.input_codigo)
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint_y=0.2)
        
        btn_confirmar = criar_botao_pequeno('CONFIRMAR', 'icones/confirmar.png', (0.7, 1, 0.7, 1))
        btn_confirmar.bind(on_press=self.confirmar_codigo)
        
        btn_voltar = criar_botao_pequeno('VOLTAR', 'icones/voltar.png', (1, 0.8, 0.8, 1))
        btn_voltar.bind(on_press=self.voltar)
        
        btn_layout.add_widget(btn_confirmar)
        btn_layout.add_widget(btn_voltar)
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
        popup = Popup(title=titulo, content=Label(text=mensagem), size_hint=(0.6, 0.4))
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
        
        for i in range(1, 10):
            btn = Button(text=str(i), font_size='20sp', background_color=(0.1, 0.1, 0.1, 1), color=(1,1,1,1))
            btn.bind(on_press=lambda x, num=str(i): self.digitar_numero(num))
            teclado.add_widget(btn)
        
        btn_corrige = Button(text='CORRIGE', font_size='12sp', background_color=(1, 0.6, 0.2, 1), color=(0,0,0,1))
        btn_corrige.bind(on_press=self.corrigir)
        
        btn_zero = Button(text='0', font_size='20sp', background_color=(0.1, 0.1, 0.1, 1), color=(1,1,1,1))
        btn_zero.bind(on_press=lambda x: self.digitar_numero('0'))
        
        btn_confirma = Button(text='CONFIRMA', font_size='12sp', background_color=(0.3, 0.9, 0.3, 1), color=(0,0,0,1))
        btn_confirma.bind(on_press=self.confirmar_voto)
        
        teclado.add_widget(btn_corrige)
        teclado.add_widget(btn_zero)
        teclado.add_widget(btn_confirma)
        
        btn_branco = Button(text='BRANCO', font_size='12sp', background_color=(1, 1, 1, 1), color=(0,0,0,1))
        btn_branco.bind(on_press=self.votar_branco)
        
        espaco1 = Label(text='')
        espaco2 = Label(text='')
        
        teclado.add_widget(btn_branco)
        teclado.add_widget(espaco1)
        teclado.add_widget(espaco2)
        
        painel_direito.add_widget(teclado)
        
        btn_voltar = criar_botao_pequeno('<< Voltar', 'icones/voltar.png', (1, 0.8, 0.8, 1))
        btn_voltar.size_hint_y = 0.1
        btn_voltar.bind(on_press=self.voltar)
        painel_direito.add_widget(btn_voltar)
        
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
        self.manager.current = 'codigo_empresa'
    
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
        popup = Popup(title=titulo, content=Label(text=mensagem), size_hint=(0.6, 0.4))
        popup.open()

if __name__ == '__main__':
    UrnaEletronicaCIPA().run()