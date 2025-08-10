import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.core.audio import SoundLoader
import json
import datetime
import os
import hashlib

kivy.require('2.0.0')

class UrnaEletronicaCIPA(App):
    def __init__(self):
        super().__init__()
        self.dados_file = 'dados_urna_cipa.json'
        self.dados = self.carregar_dados()
        
    def tocar_som(self, tipo):
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
        sm.add_widget(TelaVotacao(name='votacao'))
        return sm

class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        with layout.canvas.before:
            Color(0.85, 0.9, 1, 1)
            self.rect_bg = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self.atualizar_fundo, pos=self.atualizar_fundo)
        
        titulo = Label(text='URNA ELETRONICA CIPA', font_size='28sp', bold=True, size_hint_y=0.3, color=(0,0,0.8,1))
        layout.add_widget(titulo)
        
        menu = GridLayout(cols=2, spacing=15, size_hint_y=0.7)
        
        btn_empresa = Button(text='EMPRESA\nGerenciar', font_size='12sp', size_hint=(1, 0.6), background_color=(0.6, 0.9, 0.6, 1))
        btn_empresa.bind(on_press=self.ir_empresa)
        
        btn_mesario = Button(text='MESARIO\nAdministrar', font_size='12sp', size_hint=(1, 0.6), background_color=(1, 0.8, 0.5, 1))
        btn_mesario.bind(on_press=self.ir_mesario)
        
        btn_inscricoes = Button(text='INSCRICOES\nCandidatos', font_size='12sp', size_hint=(1, 0.6), background_color=(0.6, 0.8, 1, 1))
        btn_inscricoes.bind(on_press=self.ir_inscricoes)
        
        btn_votacao = Button(text='VOTACAO\nEleitor', font_size='12sp', size_hint=(1, 0.6), background_color=(1, 0.6, 0.9, 1))
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
        self.manager.current = 'votacao'

class TelaEmpresa(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        with layout.canvas.before:
            Color(0.85, 0.9, 1, 1)
            self.rect_bg = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self.atualizar_fundo, pos=self.atualizar_fundo)
        
        header = BoxLayout(orientation='horizontal', size_hint_y=0.12)
        btn_voltar = Button(text='← Voltar', size_hint_x=0.15, size_hint_y=0.6, background_color=(1, 0.7, 0.7, 1))
        btn_voltar.bind(on_press=self.voltar)
        titulo = Label(text='GESTAO DE EMPRESAS', font_size='18sp', bold=True, color=(0,0,0.8,1))
        header.add_widget(btn_voltar)
        header.add_widget(titulo)
        layout.add_widget(header)
        
        form = GridLayout(cols=2, spacing=8, size_hint_y=0.25)
        form.add_widget(Label(text='Nome da Empresa:', size_hint_y=0.7))
        self.input_nome = TextInput(size_hint_y=0.7)
        form.add_widget(self.input_nome)
        
        form.add_widget(Label(text='CNPJ:', size_hint_y=0.7))
        self.input_cnpj = TextInput(size_hint_y=0.7)
        form.add_widget(self.input_cnpj)
        
        layout.add_widget(form)
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.08)
        btn_cadastrar = Button(text='Cadastrar Empresa', background_color=(0.6, 0.9, 0.6, 1))
        btn_cadastrar.bind(on_press=self.cadastrar_empresa)
        btn_listar = Button(text='Listar Empresas', background_color=(0.6, 0.8, 1, 1))
        btn_listar.bind(on_press=self.listar_empresas)
        btn_layout.add_widget(btn_cadastrar)
        btn_layout.add_widget(btn_listar)
        layout.add_widget(btn_layout)
        
        self.lista = Label(text='Empresas aparecerao aqui...', size_hint_y=0.55, text_size=(None, None), valign='top')
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
            self.mostrar_popup('Erro', 'Preencha todos os campos!')
            return
        
        empresa_id = hashlib.md5(self.input_cnpj.text.encode()).hexdigest()[:8].upper()
        app.dados['empresas'][empresa_id] = {
            'nome': self.input_nome.text,
            'cnpj': self.input_cnpj.text,
            'codigo_acesso': empresa_id
        }
        app.salvar_dados()
        self.mostrar_popup('Sucesso', f'Empresa cadastrada!\nCodigo: {empresa_id}')
        self.input_nome.text = ''
        self.input_cnpj.text = ''
        self.listar_empresas(None)
    
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
    
    def mostrar_popup(self, titulo, mensagem):
        popup = Popup(title=titulo, content=Label(text=mensagem), size_hint=(0.6, 0.4))
        popup.open()

class TelaMesario(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        with layout.canvas.before:
            Color(0.85, 0.9, 1, 1)
            self.rect_bg = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self.atualizar_fundo, pos=self.atualizar_fundo)
        
        header = BoxLayout(orientation='horizontal', size_hint_y=0.12)
        btn_voltar = Button(text='← Voltar', size_hint_x=0.15, size_hint_y=0.6, background_color=(1, 0.7, 0.7, 1))
        btn_voltar.bind(on_press=self.voltar)
        titulo = Label(text='PAINEL DO MESARIO', font_size='18sp', bold=True, color=(0,0,0.8,1))
        header.add_widget(btn_voltar)
        header.add_widget(titulo)
        layout.add_widget(header)
        
        menu = GridLayout(cols=2, spacing=12, size_hint_y=0.6)
        
        btn_iniciar = Button(text='INICIAR\nEleicao', size_hint=(1, 0.6), background_color=(0.6, 0.9, 0.6, 1))
        btn_iniciar.bind(on_press=self.iniciar_eleicao)
        
        btn_finalizar = Button(text='FINALIZAR\nEleicao', size_hint=(1, 0.6), background_color=(1, 0.7, 0.7, 1))
        btn_finalizar.bind(on_press=self.finalizar_eleicao)
        
        btn_relatorios = Button(text='RELATORIOS\nResultados', size_hint=(1, 0.6), background_color=(0.6, 0.8, 1, 1))
        btn_relatorios.bind(on_press=self.ver_relatorios)
        
        btn_backup = Button(text='BACKUP\nDados', size_hint=(1, 0.6), background_color=(0.8, 0.7, 1, 1))
        btn_backup.bind(on_press=self.fazer_backup)
        
        menu.add_widget(btn_iniciar)
        menu.add_widget(btn_finalizar)
        menu.add_widget(btn_relatorios)
        menu.add_widget(btn_backup)
        
        layout.add_widget(menu)
        
        self.status = Label(text='Status: Eleicao nao iniciada', size_hint_y=0.28)
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
            Color(0.85, 0.9, 1, 1)
            self.rect_bg = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self.atualizar_fundo, pos=self.atualizar_fundo)
        
        header = BoxLayout(orientation='horizontal', size_hint_y=0.12)
        btn_voltar = Button(text='← Voltar', size_hint_x=0.15, size_hint_y=0.6, background_color=(1, 0.7, 0.7, 1))
        btn_voltar.bind(on_press=self.voltar)
        titulo = Label(text='INSCRICOES DE CANDIDATOS', font_size='16sp', bold=True, color=(0,0,0.8,1))
        header.add_widget(btn_voltar)
        header.add_widget(titulo)
        layout.add_widget(header)
        
        form = GridLayout(cols=2, spacing=8, size_hint_y=0.35)
        
        form.add_widget(Label(text='Nome:', size_hint_y=0.7))
        self.input_nome = TextInput(size_hint_y=0.7)
        form.add_widget(self.input_nome)
        
        form.add_widget(Label(text='CPF:', size_hint_y=0.7))
        self.input_cpf = TextInput(size_hint_y=0.7)
        form.add_widget(self.input_cpf)
        
        form.add_widget(Label(text='Codigo da Empresa:', size_hint_y=0.7))
        self.input_empresa = TextInput(size_hint_y=0.7)
        form.add_widget(self.input_empresa)
        
        layout.add_widget(form)
        
        btn_inscrever = Button(text='Inscrever Candidato', size_hint_y=0.08, background_color=(0.6, 0.9, 0.6, 1))
        btn_inscrever.bind(on_press=self.inscrever_candidato)
        layout.add_widget(btn_inscrever)
        
        self.lista = Label(text='Candidatos aparecerao aqui...', size_hint_y=0.45, text_size=(None, None), valign='top')
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
            self.mostrar_popup('Erro', 'Preencha todos os campos!')
            return
        
        codigo_valido = False
        for emp_id, dados in app.dados['empresas'].items():
            if dados['codigo_acesso'] == self.input_empresa.text.upper():
                codigo_valido = True
                break
        
        if not codigo_valido:
            self.mostrar_popup('Erro', 'Codigo da empresa invalido!')
            return
        
        candidato_id = hashlib.md5(self.input_cpf.text.encode()).hexdigest()[:8]
        numero = len(app.dados['candidatos']) + 1
        
        app.dados['candidatos'][candidato_id] = {
            'nome': self.input_nome.text,
            'cpf': self.input_cpf.text,
            'empresa': self.input_empresa.text.upper(),
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

class TelaVotacao(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.numero_digitado = ''
        layout = BoxLayout(orientation='horizontal', padding=20, spacing=20)
        
        with layout.canvas.before:
            Color(0.85, 0.9, 1, 1)
            self.rect_bg = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self.atualizar_fundo, pos=self.atualizar_fundo)
        
        painel_esquerdo = BoxLayout(orientation='vertical', size_hint_x=0.6)
        tela_urna = BoxLayout(orientation='vertical', padding=20)
        
        with tela_urna.canvas.before:
            Color(0.05, 0.05, 0.05, 1)
            self.rect = Rectangle(size=tela_urna.size, pos=tela_urna.pos)
        
        tela_urna.bind(size=self.atualizar_rect, pos=self.atualizar_rect)
        
        header = Label(text='ELEICAO CIPA 2024', font_size='24sp', color=(1,1,1,1), size_hint_y=0.2)
        tela_urna.add_widget(header)
        
        self.area_candidato = BoxLayout(orientation='vertical', size_hint_y=0.5)
        self.label_numero = Label(text='Digite o numero do candidato:', font_size='16sp', color=(1,1,1,1))
        self.display_numero = Label(text='_ _', font_size='42sp', color=(1,1,0,1), bold=True)
        self.info_candidato = Label(text='', font_size='14sp', color=(1,1,1,1), text_size=(None, None))
        
        self.area_candidato.add_widget(self.label_numero)
        self.area_candidato.add_widget(self.display_numero)
        self.area_candidato.add_widget(self.info_candidato)
        tela_urna.add_widget(self.area_candidato)
        
        instrucoes = Label(text='Digite o numero, BRANCO, NULO ou CONFIRMA', font_size='12sp', color=(0.8,0.8,0.8,1), size_hint_y=0.3)
        tela_urna.add_widget(instrucoes)
        
        painel_esquerdo.add_widget(tela_urna)
        
        painel_direito = BoxLayout(orientation='vertical', size_hint_x=0.4)
        
        codigo_layout = BoxLayout(orientation='horizontal', size_hint_y=0.08)
        codigo_layout.add_widget(Label(text='Codigo da Empresa:', color=(0,0,0.8,1), font_size='12sp'))
        self.input_codigo = TextInput(size_hint_x=0.5, size_hint_y=0.8)
        codigo_layout.add_widget(self.input_codigo)
        painel_direito.add_widget(codigo_layout)
        
        teclado = GridLayout(cols=3, spacing=2, size_hint_y=0.7)
        
        for i in range(1, 10):
            btn = Button(text=str(i), font_size='16sp', background_color=(0.1, 0.1, 0.1, 1), color=(1,1,1,1))
            btn.bind(on_press=lambda x, num=str(i): self.digitar_numero(num))
            teclado.add_widget(btn)
        
        btn_corrige = Button(text='CORRIGE', font_size='10sp', background_color=(1, 0.5, 0, 1), color=(0,0,0,1))
        btn_corrige.bind(on_press=self.corrigir)
        
        btn_zero = Button(text='0', font_size='16sp', background_color=(0.1, 0.1, 0.1, 1), color=(1,1,1,1))
        btn_zero.bind(on_press=lambda x: self.digitar_numero('0'))
        
        btn_confirma = Button(text='CONFIRMA', font_size='10sp', background_color=(0.2, 0.8, 0.2, 1), color=(0,0,0,1))
        btn_confirma.bind(on_press=self.confirmar_voto)
        
        teclado.add_widget(btn_corrige)
        teclado.add_widget(btn_zero)
        teclado.add_widget(btn_confirma)
        
        btn_branco = Button(text='BRANCO', font_size='10sp', background_color=(1, 1, 1, 1), color=(0,0,0,1))
        btn_branco.bind(on_press=self.votar_branco)
        
        btn_nulo = Button(text='NULO', font_size='10sp', background_color=(0.5, 0.5, 0.5, 1), color=(1,1,1,1))
        btn_nulo.bind(on_press=self.votar_nulo)
        
        espaco = Label(text='')
        
        teclado.add_widget(btn_branco)
        teclado.add_widget(espaco)
        teclado.add_widget(btn_nulo)
        
        painel_direito.add_widget(teclado)
        
        btn_voltar = Button(text='← Voltar', size_hint_y=0.08, background_color=(1, 0.7, 0.7, 1))
        btn_voltar.bind(on_press=self.voltar)
        painel_direito.add_widget(btn_voltar)
        
        layout.add_widget(painel_esquerdo)
        layout.add_widget(painel_direito)
        self.add_widget(layout)
    
    def atualizar_fundo(self, instance, value):
        self.rect_bg.size = instance.size
        self.rect_bg.pos = instance.pos
    
    def atualizar_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
    
    def voltar(self, instance):
        App.get_running_app().tocar_som('tecla')
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
            if dados['numero'] == numero:
                candidato_encontrado = dados
                break
        
        if candidato_encontrado:
            self.info_candidato.text = f"Nome: {candidato_encontrado['nome']}\nEmpresa: {candidato_encontrado['empresa']}"
            self.info_candidato.text_size = (300, None)
        else:
            self.info_candidato.text = "CANDIDATO NAO ENCONTRADO"
            self.info_candidato.text_size = (300, None)
    
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
    
    def votar_nulo(self, instance):
        App.get_running_app().tocar_som('tecla')
        self.numero_digitado = '99'
        self.display_numero.text = 'NULO'
        self.info_candidato.text = 'VOTO NULO'
    
    def confirmar_voto(self, instance):
        app = App.get_running_app()
        app.tocar_som('confirma')
        
        if not app.dados['configuracoes']['eleicao_ativa']:
            self.mostrar_popup('Erro', 'Eleicao nao esta ativa!')
            return
        
        if not self.input_codigo.text:
            self.mostrar_popup('Erro', 'Digite o codigo da empresa!')
            return
        
        if not self.numero_digitado:
            self.mostrar_popup('Erro', 'Digite um numero, BRANCO ou NULO!')
            return
        
        if self.numero_digitado == '00':
            numero = 'BRANCO'
        elif self.numero_digitado == '99':
            numero = 'NULO'
        else:
            if len(self.numero_digitado) != 2:
                self.mostrar_popup('Erro', 'Digite um numero valido!')
                return
            numero = int(self.numero_digitado)
        
        empresa = self.input_codigo.text.upper()
        
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
        self.input_codigo.text = ''
        self.atualizar_display()
        self.info_candidato.text = ''
        
        if numero == 'BRANCO':
            self.mostrar_popup('Sucesso', 'Voto em BRANCO registrado!')
        elif numero == 'NULO':
            self.mostrar_popup('Sucesso', 'Voto NULO registrado!')
        else:
            self.mostrar_popup('Sucesso', 'Voto registrado com sucesso!')
    
    def mostrar_popup(self, titulo, mensagem):
        popup = Popup(title=titulo, content=Label(text=mensagem), size_hint=(0.6, 0.4))
        popup.open()

if __name__ == '__main__':
    UrnaEletronicaCIPA().run()