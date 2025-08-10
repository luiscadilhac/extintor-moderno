# main.py - Sistema de Gerenciamento de Extintores
import os
import sys
import json
import sqlite3
from datetime import datetime, timedelta
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
import webbrowser
import subprocess

# Configuração de cores
CORES = {
    'fundo_principal': get_color_from_hex('#FF8C00'),  # Laranja
    'fundo_input': get_color_from_hex('#FFFFE0'),     # Amarelo claro
    'botao_vermelho': get_color_from_hex('#DC143C'),   # Vermelho
    'texto_azul': get_color_from_hex('#000080'),       # Azul marinho
    'branco': get_color_from_hex('#FFFFFF'),
    'cinza_claro': get_color_from_hex('#F5F5F5')
}

class MaskedTextInput(TextInput):
    """TextInput personalizado com máscara"""
    def __init__(self, mask='', **kwargs):
        super().__init__(**kwargs)
        self.mask = mask
        self.background_color = CORES['fundo_input']
        self.foreground_color = CORES['texto_azul']
        
    def insert_text(self, substring, from_undo=False):
        if self.mask == 'data':
            # Máscara para data DD/MM/AAAA
            current_text = self.text
            if len(current_text) == 2 and len(current_text + substring) == 3:
                substring = '/' + substring
            elif len(current_text) == 5 and len(current_text + substring) == 6:
                substring = '/' + substring
            elif len(current_text) >= 10:
                return
        elif self.mask == 'decimal':
            # Máscara para valores decimais
            if not (substring.isdigit() or substring == ',' or substring == '.'):
                return
        elif self.mask == 'numero':
            # Apenas números
            if not substring.isdigit():
                return
                
        return super().insert_text(substring, from_undo)

class Extintor:
    def __init__(self, numero_serie, localizacao, tipo, capacidade, 
                 data_fabricacao, data_validade, data_recarga, 
                 data_manutencao, empresa_manutencao, observacoes=''):
        self.numero_serie = numero_serie
        self.localizacao = localizacao
        self.tipo = tipo
        self.capacidade = capacidade
        self.data_fabricacao = data_fabricacao
        self.data_validade = data_validade
        self.data_recarga = data_recarga
        self.data_manutencao = data_manutencao
        self.empresa_manutencao = empresa_manutencao
        self.observacoes = observacoes
        self.status = self.calcular_status()
    
    def calcular_status(self):
        """Calcula o status do extintor baseado nas datas"""
        try:
            data_val = datetime.strptime(self.data_validade, '%d/%m/%Y')
            hoje = datetime.now()
            
            if data_val < hoje:
                return 'VENCIDO'
            elif (data_val - hoje).days <= 30:
                return 'VENCE EM 30 DIAS'
            else:
                return 'OK'
        except:
            return 'DATA INVÁLIDA'
    
    def to_dict(self):
        return {
            'numero_serie': self.numero_serie,
            'localizacao': self.localizacao,
            'tipo': self.tipo,
            'capacidade': self.capacidade,
            'data_fabricacao': self.data_fabricacao,
            'data_validade': self.data_validade,
            'data_recarga': self.data_recarga,
            'data_manutencao': self.data_manutencao,
            'empresa_manutencao': self.empresa_manutencao,
            'observacoes': self.observacoes,
            'status': self.status
        }

class DatabaseManager:
    def __init__(self):
        # VERMELHO: Altere o caminho do banco de dados conforme necessário
        self.db_path = os.path.join(os.path.expanduser('~'), 'Documents', 'extintores.db')
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS extintores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_serie TEXT UNIQUE NOT NULL,
                localizacao TEXT NOT NULL,
                tipo TEXT NOT NULL,
                capacidade TEXT NOT NULL,
                data_fabricacao TEXT NOT NULL,
                data_validade TEXT NOT NULL,
                data_recarga TEXT NOT NULL,
                data_manutencao TEXT NOT NULL,
                empresa_manutencao TEXT NOT NULL,
                observacoes TEXT,
                data_cadastro TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def salvar_extintor(self, extintor):
        """Salva um extintor no banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO extintores 
                (numero_serie, localizacao, tipo, capacidade, data_fabricacao,
                 data_validade, data_recarga, data_manutencao, empresa_manutencao,
                 observacoes, data_cadastro)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                extintor.numero_serie, extintor.localizacao, extintor.tipo,
                extintor.capacidade, extintor.data_fabricacao, extintor.data_validade,
                extintor.data_recarga, extintor.data_manutencao, extintor.empresa_manutencao,
                extintor.observacoes, datetime.now().strftime('%d/%m/%Y %H:%M')
            ))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def listar_extintores(self):
        """Lista todos os extintores"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM extintores ORDER BY numero_serie')
        registros = cursor.fetchall()
        conn.close()
        
        extintores = []
        for reg in registros:
            extintor = Extintor(
                reg[1], reg[2], reg[3], reg[4], reg[5],
                reg[6], reg[7], reg[8], reg[9], reg[10]
            )
            extintores.append(extintor)
        
        return extintores
    
    def remover_extintor(self, numero_serie):
        """Remove um extintor do banco"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM extintores WHERE numero_serie = ?', (numero_serie,))
        conn.commit()
        conn.close()

class TelaCadastro(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'cadastro'
        self.build_interface()
    
    def build_interface(self):
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        main_layout.canvas.before.add(Color(*CORES['fundo_principal']))
        main_layout.canvas.before.add(Rectangle(pos=self.pos, size=self.size))
        
        # Título
        titulo = Label(
            text='CADASTRO DE EXTINTORES',
            size_hint_y=None,
            height=dp(60),
            font_size=sp(20),
            bold=True,
            color=CORES['texto_azul']
        )
        main_layout.add_widget(titulo)
        
        # Scroll para o formulário
        scroll = ScrollView()
        form_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, padding=dp(10))
        form_layout.bind(minimum_height=form_layout.setter('height'))
        
        # Campos do formulário
        campos = [
            ('Número de Série:', 'input_serie', ''),
            ('Localização:', 'input_localizacao', ''),
            ('Tipo:', 'spinner_tipo', ''),
            ('Capacidade:', 'input_capacidade', ''),
            ('Data Fabricação:', 'input_data_fab', 'data'),
            ('Data Validade:', 'input_data_val', 'data'),
            ('Data Recarga:', 'input_data_rec', 'data'),
            ('Data Manutenção:', 'input_data_man', 'data'),
            ('Empresa Manutenção:', 'input_empresa', ''),
            ('Observações:', 'input_obs', '')
        ]
        
        self.inputs = {}
        
        for label_text, input_name, mask in campos:
            # Label
            label = Label(
                text=label_text,
                size_hint_y=None,
                height=dp(40),
                color=CORES['texto_azul'],
                bold=True,
                text_size=(dp(150), None),
                halign='left',
                valign='middle'
            )
            form_layout.add_widget(label)
            
            # Input
            if input_name == 'spinner_tipo':
                input_widget = Spinner(
                    text='Selecione o tipo',
                    values=['Água', 'Espuma', 'Pó Químico', 'CO2', 'Halon'],
                    size_hint_y=None,
                    height=dp(40),
                    background_color=CORES['fundo_input']
                )
            elif input_name == 'input_obs':
                input_widget = MaskedTextInput(
                    multiline=True,
                    size_hint_y=None,
                    height=dp(80),
                    mask=mask
                )
            else:
                input_widget = MaskedTextInput(
                    size_hint_y=None,
                    height=dp(40),
                    mask=mask
                )
            
            self.inputs[input_name] = input_widget
            form_layout.add_widget(input_widget)
        
        scroll.add_widget(form_layout)
        main_layout.add_widget(scroll)
        
        # Botões
        botoes_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), spacing=dp(10))
        
        btn_salvar = Button(
            text='SALVAR EXTINTOR',
            background_color=CORES['botao_vermelho'],
            color=CORES['branco'],
            bold=True,
            font_size=sp(16)
        )
        btn_salvar.bind(on_press=self.salvar_extintor)
        
        btn_limpar = Button(
            text='LIMPAR CAMPOS',
            background_color=CORES['botao_vermelho'],
            color=CORES['branco'],
            bold=True,
            font_size=sp(16)
        )
        btn_limpar.bind(on_press=self.limpar_campos)
        
        botoes_layout.add_widget(btn_salvar)
        botoes_layout.add_widget(btn_limpar)
        main_layout.add_widget(botoes_layout)
        
        self.add_widget(main_layout)
    
    def salvar_extintor(self, instance):
        """Salva o extintor no banco de dados"""
        try:
            # Validação dos campos obrigatórios
            if not self.inputs['input_serie'].text.strip():
                self.mostrar_popup('Erro', 'Número de série é obrigatório!')
                return
            
            if not self.inputs['input_localizacao'].text.strip():
                self.mostrar_popup('Erro', 'Localização é obrigatória!')
                return
            
            if self.inputs['spinner_tipo'].text == 'Selecione o tipo':
                self.mostrar_popup('Erro', 'Tipo do extintor é obrigatório!')
                return
            
            # Validação das datas
            datas = ['input_data_fab', 'input_data_val', 'input_data_rec', 'input_data_man']
            for data_field in datas:
                if not self.validar_data(self.inputs[data_field].text):
                    self.mostrar_popup('Erro', f'Data inválida no campo {data_field}!')
                    return
            
            # Criar objeto extintor
            extintor = Extintor(
                self.inputs['input_serie'].text.strip(),
                self.inputs['input_localizacao'].text.strip(),
                self.inputs['spinner_tipo'].text,
                self.inputs['input_capacidade'].text.strip(),
                self.inputs['input_data_fab'].text.strip(),
                self.inputs['input_data_val'].text.strip(),
                self.inputs['input_data_rec'].text.strip(),
                self.inputs['input_data_man'].text.strip(),
                self.inputs['input_empresa'].text.strip(),
                self.inputs['input_obs'].text.strip()
            )
            
            # Salvar no banco
            db = DatabaseManager()
            if db.salvar_extintor(extintor):
                self.mostrar_popup('Sucesso', 'Extintor cadastrado com sucesso!')
                self.limpar_campos(None)
            else:
                self.mostrar_popup('Erro', 'Número de série já existe!')
                
        except Exception as e:
            self.mostrar_popup('Erro', f'Erro ao salvar: {str(e)}')
    
    def validar_data(self, data_str):
        """Valida se a data está no formato correto"""
        try:
            datetime.strptime(data_str, '%d/%m/%Y')
            return True
        except:
            return False
    
    def limpar_campos(self, instance):
        """Limpa todos os campos do formulário"""
        for key, input_widget in self.inputs.items():
            if key == 'spinner_tipo':
                input_widget.text = 'Selecione o tipo'
            else:
                input_widget.text = ''
    
    def mostrar_popup(self, titulo, mensagem):
        """Mostra popup com mensagem"""
        content = Label(text=mensagem, color=CORES['texto_azul'])
        popup = Popup(
            title=titulo,
            content=content,
            size_hint=(0.8, 0.4),
            title_color=CORES['texto_azul']
        )
        popup.open()

class TelaListagem(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'listagem'
        self.build_interface()
    
    def build_interface(self):
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        main_layout.canvas.before.add(Color(*CORES['fundo_principal']))
        main_layout.canvas.before.add(Rectangle(pos=self.pos, size=self.size))
        
        # Título
        titulo = Label(
            text='LISTAGEM DE EXTINTORES',
            size_hint_y=None,
            height=dp(60),
            font_size=sp(20),
            bold=True,
            color=CORES['texto_azul']
        )
        main_layout.add_widget(titulo)
        
        # Botões de ação
        botoes_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
        
        btn_atualizar = Button(
            text='ATUALIZAR LISTA',
            background_color=CORES['botao_vermelho'],
            color=CORES['branco'],
            bold=True
        )
        btn_atualizar.bind(on_press=self.atualizar_lista)
        
        btn_relatorio = Button(
            text='GERAR RELATÓRIO PDF',
            background_color=CORES['botao_vermelho'],
            color=CORES['branco'],
            bold=True
        )
        btn_relatorio.bind(on_press=self.gerar_relatorio_pdf)
        
        botoes_layout.add_widget(btn_atualizar)
        botoes_layout.add_widget(btn_relatorio)
        main_layout.add_widget(botoes_layout)
        
        # Lista de extintores
        self.scroll = ScrollView()
        self.lista_layout = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_y=None)
        self.lista_layout.bind(minimum_height=self.lista_layout.setter('height'))
        self.scroll.add_widget(self.lista_layout)
        main_layout.add_widget(self.scroll)
        
        self.add_widget(main_layout)
        self.atualizar_lista(None)
    
    def atualizar_lista(self, instance):
        """Atualiza a lista de extintores"""
        self.lista_layout.clear_widgets()
        
        db = DatabaseManager()
        extintores = db.listar_extintores()
        
        if not extintores:
            sem_dados = Label(
                text='Nenhum extintor cadastrado',
                size_hint_y=None,
                height=dp(40),
                color=CORES['texto_azul']
            )
            self.lista_layout.add_widget(sem_dados)
            return
        
        for extintor in extintores:
            item_layout = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(120),
                spacing=dp(5)
            )
            
            # Cor de fundo baseada no status
            cor_status = CORES['cinza_claro']
            if extintor.status == 'VENCIDO':
                cor_status = get_color_from_hex('#FFB6C1')
            elif 'VENCE' in extintor.status:
                cor_status = get_color_from_hex('#FFFFE0')
            
            with item_layout.canvas.before:
                Color(*cor_status)
                Rectangle(pos=item_layout.pos, size=item_layout.size)
            
            # Informações do extintor
            info_text = f"Série: {extintor.numero_serie} | Local: {extintor.localizacao}\n"
            info_text += f"Tipo: {extintor.tipo} | Capacidade: {extintor.capacidade}\n"
            info_text += f"Validade: {extintor.data_validade} | Status: {extintor.status}"
            
            info_label = Label(
                text=info_text,
                text_size=(dp(280), None),
                halign='left',
                valign='middle',
                color=CORES['texto_azul'],
                size_hint_y=None,
                height=dp(80)
            )
            
            # Botão remover
            btn_remover = Button(
                text='REMOVER',
                size_hint_y=None,
                height=dp(35),
                background_color=CORES['botao_vermelho'],
                color=CORES['branco']
            )
            btn_remover.bind(on_press=lambda x, serie=extintor.numero_serie: self.confirmar_remocao(serie))
            
            item_layout.add_widget(info_label)
            item_layout.add_widget(btn_remover)
            self.lista_layout.add_widget(item_layout)
    
    def confirmar_remocao(self, numero_serie):
        """Confirma a remoção do extintor"""
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        content.add_widget(Label(text=f'Remover extintor {numero_serie}?', color=CORES['texto_azul']))
        
        botoes = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(40))
        
        btn_sim = Button(text='SIM', background_color=CORES['botao_vermelho'], color=CORES['branco'])
        btn_nao = Button(text='NÃO', background_color=CORES['botao_vermelho'], color=CORES['branco'])
        
        botoes.add_widget(btn_sim)
        botoes.add_widget(btn_nao)
        content.add_widget(botoes)
        
        popup = Popup(title='Confirmação', content=content, size_hint=(0.8, 0.3))
        
        btn_sim.bind(on_press=lambda x: self.remover_extintor(numero_serie, popup))
        btn_nao.bind(on_press=popup.dismiss)
        
        popup.open()
    
    def remover_extintor(self, numero_serie, popup):
        """Remove o extintor do banco"""
        db = DatabaseManager()
        db.remover_extintor(numero_serie)
        popup.dismiss()
        self.atualizar_lista(None)
        self.mostrar_popup('Sucesso', f'Extintor {numero_serie} removido!')
    
    def gerar_relatorio_pdf(self, instance):
        """Gera relatório em PDF"""
        try:
            # VERMELHO: Instale a biblioteca reportlab primeiro
            # pip install reportlab
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors
            from reportlab.lib.units import inch
            
            db = DatabaseManager()
            extintores = db.listar_extintores()
            
            if not extintores:
                self.mostrar_popup('Aviso', 'Nenhum extintor para gerar relatório!')
                return
            
            # VERMELHO: Altere o caminho do arquivo PDF conforme necessário
            filename = os.path.join(os.path.expanduser('~'), 'Desktop', f'relatorio_extintores_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf')
            
            doc = SimpleDocTemplate(filename, pagesize=A4)
            elementos = []
            
            # Título
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1,  # Centro
                textColor=colors.darkblue
            )
            
            titulo = Paragraph("RELATÓRIO DE EXTINTORES DE INCÊNDIO", title_style)
            elementos.append(titulo)
            elementos.append(Spacer(1, 20))
            
            # Data do relatório
            data_relatorio = Paragraph(f"Data do Relatório: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal'])
            elementos.append(data_relatorio)
            elementos.append(Spacer(1, 20))
            
            # Tabela com dados
            dados = [['Série', 'Localização', 'Tipo', 'Validade', 'Status']]
            
            for extintor in extintores:
                dados.append([
                    extintor.numero_serie,
                    extintor.localizacao,
                    extintor.tipo,
                    extintor.data_validade,
                    extintor.status
                ])
            
            tabela = Table(dados, colWidths=[1*inch, 2*inch, 1*inch, 1*inch, 1.5*inch])
            tabela.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elementos.append(tabela)
            elementos.append(Spacer(1, 20))
            
            # Estatísticas
            total = len(extintores)
            vencidos = len([e for e in extintores if e.status == 'VENCIDO'])
            vencendo = len([e for e in extintores if 'VENCE' in e.status])
            ok = total - vencidos - vencendo
            
            stats_text = f"""
            <b>ESTATÍSTICAS:</b><br/>
            Total de Extintores: {total}<br/>
            Extintores OK: {ok}<br/>
            Vencendo em 30 dias: {vencendo}<br/>
            Vencidos: {vencidos}
            """
            
            stats = Paragraph(stats_text, styles['Normal'])
            elementos.append(stats)
            
            # Gerar PDF
            doc.build(elementos)
            
            self.mostrar_popup('Sucesso', f'Relatório gerado:\n{filename}')
            
            # VERMELHO: Abrir o PDF automaticamente (Windows)
            # Altere conforme seu sistema operacional
            try:
                os.startfile(filename)  # Windows
                # subprocess.call(['open', filename])  # macOS
                # subprocess.call(['xdg-open', filename])  # Linux
            except:
                pass
                
        except ImportError:
            self.mostrar_popup('Erro', 'Biblioteca reportlab não instalada!\nExecute: pip install reportlab')
        except Exception as e:
            self.mostrar_popup('Erro', f'Erro ao gerar relatório: {str(e)}')
    
    def mostrar_popup(self, titulo, mensagem):
        """Mostra popup com mensagem"""
        content = Label(text=mensagem, color=CORES['texto_azul'])
        popup = Popup(title=titulo, content=content, size_hint=(0.8, 0.4))
        popup.open()

class GerenciadorExtintoresApp(App):
    def build(self):
        # Configurar janela
        Window.clearcolor = CORES['fundo_principal']
        Window.size = (400, 700)  # Tamanho para simular celular
        
        # Gerenciador de telas
        sm = ScreenManager()
        
        # Adicionar telas
        sm.add_widget(TelaCadastro())
        sm.add_widget(TelaListagem())
        
        # Layout principal com navegação
        main_layout = BoxLayout(orientation='vertical')
        
        # Botões de navegação
        nav_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), spacing=dp(5))
        
        btn_cadastro = Button(
            text='CADASTRO',
            background_color=CORES['botao_vermelho'],
            color=CORES['branco'],
            bold=True,
            font_size=sp(14)
        )
        btn_cadastro.bind(on_press=lambda x: setattr(sm, 'current', 'cadastro'))
        
        btn_listagem = Button(
            text='LISTAGEM',
            background_color=CORES['botao_vermelho'],
            color=CORES['branco'],
            bold=True,
            font_size=sp(14)
        )
        btn_listagem.bind(on_press=lambda x: setattr(sm, 'current', 'listagem'))
        
        nav_layout.add_widget(btn_cadastro)
        nav_layout.add_widget(btn_listagem)
        
        main_layout.add_widget(nav_layout)
        main_layout.add_widget(sm)
        
        return main_layout

# Classe para importar módulos necessários
from kivy.graphics import Color, Rectangle

# Arquivos de configuração necessários
def criar_arquivos_config():
    """Cria arquivos de configuração necessários"""
    
    # requirements.txt
    requirements_content = """kivy>=2.1.0
kivymd>=1.1.1
reportlab>=3.6.0
sqlite3
"""
    
    # buildozer.spec
    buildozer_content = """[app]
title = Gerenciador de Extintores
package.name = gerenciadorextintores
package.domain = com.empresa.extintores

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,db

version = 1.0
requirements = python3,kivy,kivymd,reportlab

[buildozer]
log_level = 2

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET

[app]
android.api = 30
android.minapi = 21
android.sdk = 30
android.ndk = 21b
android.private_storage = True
android.arch = armeabi-v7a

# VERMELHO: Configure estes caminhos conforme sua instalação do Android SDK
# android.sdk_path = C:\\Users\\SEU_USUARIO\\AppData\\Local\\Android\\Sdk
# android.ndk_path = C:\\Users\\SEU_USUARIO\\AppData\\Local\\Android\\Sdk\\ndk\\21.4.7075529
"""
    
    # Salvar arquivos
    with open('requirements.txt', 'w') as f:
        f.write(requirements_content)
    
    with open('buildozer.spec', 'w') as f:
        f.write(buildozer_content)

def instalar_dependencias():
    """Instala as dependências necessárias"""
    import subprocess
    import sys
    
    dependencias = [
        'kivy>=2.1.0',
        'kivymd>=1.1.1', 
        'reportlab>=3.6.0'
    ]
    
    print("Instalando dependências...")
    for dep in dependencias:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
            print(f"✓ {dep} instalado com sucesso")
        except subprocess.CalledProcessError:
            print(f"✗ Erro ao instalar {dep}")

# VERMELHO: Configurações específicas do Windows/VS Code
def configurar_vscode():
    """Cria configurações para VS Code"""
    
    # Criar pasta .vscode se não existir
    if not os.path.exists('.vscode'):
        os.makedirs('.vscode')
    
    # settings.json para VS Code
    vscode_settings = {
        "python.defaultInterpreterPath": "python.exe",
        "python.terminal.activateEnvironment": True,
        "files.associations": {
            "*.kv": "yaml"
        },
        "python.analysis.extraPaths": [
            "./",
            "${workspaceFolder}"
        ],
        "terminal.integrated.shell.windows": "cmd.exe"
    }
    
    # launch.json para debug
    vscode_launch = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Gerenciador Extintores",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/main.py",
                "console": "integratedTerminal",
                "args": []
            }
        ]
    }
    
    # tasks.json para automação
    vscode_tasks = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Instalar Dependências",
                "type": "shell",
                "command": "pip",
                "args": ["install", "-r", "requirements.txt"],
                "group": "build",
                "presentation": {
                    "echo": True,
                    "reveal": "always",
                    "focus": False,
                    "panel": "shared"
                }
            },
            {
                "label": "Executar App",
                "type": "shell",
                "command": "python",
                "args": ["main.py"],
                "group": {
                    "kind": "build",
                    "isDefault": True
                }
            },
            {
                "label": "Gerar APK Debug",
                "type": "shell",
                "command": "buildozer",
                "args": ["android", "debug"],
                "group": "build"
            }
        ]
    }
    
    try:
        with open('.vscode/settings.json', 'w') as f:
            json.dump(vscode_settings, f, indent=4)
        
        with open('.vscode/launch.json', 'w') as f:
            json.dump(vscode_launch, f, indent=4)
            
        with open('.vscode/tasks.json', 'w') as f:
            json.dump(vscode_tasks, f, indent=4)
            
        print("✓ Configurações do VS Code criadas")
    except Exception as e:
        print(f"✗ Erro ao criar configurações do VS Code: {e}")

# Script de inicialização
def setup_projeto():
    """Configura o projeto inicial"""
    print("=== CONFIGURAÇÃO DO PROJETO GERENCIADOR DE EXTINTORES ===")
    print()
    
    # Criar arquivos de configuração
    print("1. Criando arquivos de configuração...")
    criar_arquivos_config()
    print("✓ Arquivos criados: requirements.txt, buildozer.spec")
    
    # Configurar VS Code
    print("\n2. Configurando VS Code...")
    configurar_vscode()
    
    # Verificar Python
    print(f"\n3. Versão do Python: {sys.version}")
    
    # VERMELHO: Verificar caminhos importantes
    print("\n4. VERIFICAÇÕES IMPORTANTES (VERMELHO - CONFIGURE MANUALMENTE):")
    print(f"   - Pasta do usuário: {os.path.expanduser('~')}")
    print(f"   - Pasta Documents: {os.path.join(os.path.expanduser('~'), 'Documents')}")
    print(f"   - Pasta Desktop: {os.path.join(os.path.expanduser('~'), 'Desktop')}")
    print("   - ALTERE os caminhos no código se necessário!")
    
    print("\n5. DEPENDÊNCIAS A INSTALAR:")
    print("   Execute no terminal do VS Code:")
    print("   pip install kivy kivymd reportlab")
    
    print("\n6. CONFIGURAÇÕES ANDROID (se quiser gerar APK):")
    print("   - Instale Android Studio")
    print("   - Configure Android SDK")
    print("   - Instale Buildozer: pip install buildozer")
    print("   - Configure os caminhos no buildozer.spec")
    
    print("\n=== PROJETO CONFIGURADO! ===")
    print("Execute 'python main.py' para iniciar o aplicativo")

class TelaRelatorios(Screen):
    """Tela adicional para relatórios avançados"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'relatorios'
        self.build_interface()
    
    def build_interface(self):
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Título
        titulo = Label(
            text='RELATÓRIOS AVANÇADOS',
            size_hint_y=None,
            height=dp(60),
            font_size=sp(20),
            bold=True,
            color=CORES['texto_azul']
        )
        main_layout.add_widget(titulo)
        
        # Botões de relatórios
        botoes_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(200))
        
        btn_completo = Button(
            text='RELATÓRIO\nCOMPLETO',
            background_color=CORES['botao_vermelho'],
            color=CORES['branco'],
            bold=True,
            font_size=sp(14)
        )
        btn_completo.bind(on_press=self.relatorio_completo)
        
        btn_vencidos = Button(
            text='EXTINTORES\nVENCIDOS',
            background_color=CORES['botao_vermelho'],
            color=CORES['branco'],
            bold=True,
            font_size=sp(14)
        )
        btn_vencidos.bind(on_press=self.relatorio_vencidos)
        
        btn_vencendo = Button(
            text='VENCENDO EM\n30 DIAS',
            background_color=CORES['botao_vermelho'],
            color=CORES['branco'],
            bold=True,
            font_size=sp(14)
        )
        btn_vencendo.bind(on_press=self.relatorio_vencendo)
        
        btn_por_tipo = Button(
            text='RELATÓRIO\nPOR TIPO',
            background_color=CORES['botao_vermelho'],
            color=CORES['branco'],
            bold=True,
            font_size=sp(14)
        )
        btn_por_tipo.bind(on_press=self.relatorio_por_tipo)
        
        botoes_layout.add_widget(btn_completo)
        botoes_layout.add_widget(btn_vencidos)
        botoes_layout.add_widget(btn_vencendo)
        botoes_layout.add_widget(btn_por_tipo)
        
        main_layout.add_widget(botoes_layout)
        
        # Estatísticas em tempo real
        stats_label = Label(
            text='ESTATÍSTICAS EM TEMPO REAL',
            size_hint_y=None,
            height=dp(40),
            font_size=sp(16),
            bold=True,
            color=CORES['texto_azul']
        )
        main_layout.add_widget(stats_label)
        
        self.stats_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(200))
        main_layout.add_widget(self.stats_layout)
        
        self.add_widget(main_layout)
        self.atualizar_estatisticas()
    
    def atualizar_estatisticas(self):
        """Atualiza as estatísticas em tempo real"""
        self.stats_layout.clear_widgets()
        
        db = DatabaseManager()
        extintores = db.listar_extintores()
        
        if not extintores:
            sem_dados = Label(text='Nenhum extintor cadastrado', color=CORES['texto_azul'])
            self.stats_layout.add_widget(sem_dados)
            return
        
        # Calcular estatísticas
        total = len(extintores)
        vencidos = len([e for e in extintores if e.status == 'VENCIDO'])
        vencendo = len([e for e in extintores if 'VENCE' in e.status])
        ok = total - vencidos - vencendo
        
        # Estatísticas por tipo
        tipos = {}
        for extintor in extintores:
            tipos[extintor.tipo] = tipos.get(extintor.tipo, 0) + 1
        
        # Exibir estatísticas
        stats_text = f"""TOTAL DE EXTINTORES: {total}
SITUAÇÃO OK: {ok}
VENCENDO EM 30 DIAS: {vencendo}
VENCIDOS: {vencidos}

EXTINTORES POR TIPO:"""
        
        for tipo, quantidade in tipos.items():
            stats_text += f"\n{tipo}: {quantidade}"
        
        stats_display = Label(
            text=stats_text,
            color=CORES['texto_azul'],
            font_size=sp(14),
            text_size=(dp(300), None),
            halign='left'
        )
        
        self.stats_layout.add_widget(stats_display)
    
    def relatorio_completo(self, instance):
        """Gera relatório completo detalhado"""
        self.gerar_relatorio_personalizado('completo')
    
    def relatorio_vencidos(self, instance):
        """Gera relatório apenas dos vencidos"""
        self.gerar_relatorio_personalizado('vencidos')
    
    def relatorio_vencendo(self, instance):
        """Gera relatório dos que vencem em 30 dias"""
        self.gerar_relatorio_personalizado('vencendo')
    
    def relatorio_por_tipo(self, instance):
        """Gera relatório agrupado por tipo"""
        self.gerar_relatorio_personalizado('por_tipo')
    
    def gerar_relatorio_personalizado(self, tipo_relatorio):
        """Gera relatório personalizado baseado no tipo"""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors
            from reportlab.lib.units import inch
            
            db = DatabaseManager()
            extintores = db.listar_extintores()
            
            if not extintores:
                self.mostrar_popup('Aviso', 'Nenhum extintor cadastrado!')
                return
            
            # Filtrar extintores baseado no tipo de relatório
            if tipo_relatorio == 'vencidos':
                extintores = [e for e in extintores if e.status == 'VENCIDO']
                titulo_relatorio = "RELATÓRIO DE EXTINTORES VENCIDOS"
            elif tipo_relatorio == 'vencendo':
                extintores = [e for e in extintores if 'VENCE' in e.status]
                titulo_relatorio = "RELATÓRIO DE EXTINTORES VENCENDO EM 30 DIAS"
            elif tipo_relatorio == 'por_tipo':
                titulo_relatorio = "RELATÓRIO DE EXTINTORES POR TIPO"
            else:
                titulo_relatorio = "RELATÓRIO COMPLETO DE EXTINTORES"
            
            if not extintores and tipo_relatorio in ['vencidos', 'vencendo']:
                self.mostrar_popup('Aviso', 'Nenhum extintor encontrado para este filtro!')
                return
            
            # VERMELHO: Altere o caminho conforme necessário
            filename = os.path.join(
                os.path.expanduser('~'), 
                'Desktop', 
                f'relatorio_{tipo_relatorio}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
            )
            
            doc = SimpleDocTemplate(filename, pagesize=A4)
            elementos = []
            
            # Estilos
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1,
                textColor=colors.darkblue
            )
            
            # Título
            titulo = Paragraph(titulo_relatorio, title_style)
            elementos.append(titulo)
            elementos.append(Spacer(1, 20))
            
            # Data e hora
            data_relatorio = Paragraph(
                f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}", 
                styles['Normal']
            )
            elementos.append(data_relatorio)
            elementos.append(Spacer(1, 20))
            
            if tipo_relatorio == 'por_tipo':
                # Agrupar por tipo
                tipos = {}
                for extintor in extintores:
                    if extintor.tipo not in tipos:
                        tipos[extintor.tipo] = []
                    tipos[extintor.tipo].append(extintor)
                
                for tipo, lista_extintores in tipos.items():
                    # Subtítulo por tipo
                    subtitulo = Paragraph(f"TIPO: {tipo} ({len(lista_extintores)} extintores)", styles['Heading2'])
                    elementos.append(subtitulo)
                    elementos.append(Spacer(1, 10))
                    
                    # Tabela para este tipo
                    dados = [['Série', 'Localização', 'Capacidade', 'Validade', 'Status']]
                    for extintor in lista_extintores:
                        dados.append([
                            extintor.numero_serie,
                            extintor.localizacao,
                            extintor.capacidade,
                            extintor.data_validade,
                            extintor.status
                        ])
                    
                    tabela = Table(dados, colWidths=[1*inch, 2*inch, 1*inch, 1*inch, 1.5*inch])
                    tabela.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    
                    elementos.append(tabela)
                    elementos.append(Spacer(1, 20))
            
            else:
                # Tabela padrão
                if tipo_relatorio == 'completo':
                    dados = [['Série', 'Local', 'Tipo', 'Capacidade', 'Fabricação', 'Validade', 'Recarga', 'Manutenção', 'Status']]
                    col_widths = [0.8*inch, 1.2*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 1*inch]
                    
                    for extintor in extintores:
                        dados.append([
                            extintor.numero_serie,
                            extintor.localizacao,
                            extintor.tipo,
                            extintor.capacidade,
                            extintor.data_fabricacao,
                            extintor.data_validade,
                            extintor.data_recarga,
                            extintor.data_manutencao,
                            extintor.status
                        ])
                else:
                    dados = [['Série', 'Localização', 'Tipo', 'Validade', 'Status']]
                    col_widths = [1*inch, 2*inch, 1*inch, 1*inch, 1.5*inch]
                    
                    for extintor in extintores:
                        dados.append([
                            extintor.numero_serie,
                            extintor.localizacao,
                            extintor.tipo,
                            extintor.data_validade,
                            extintor.status
                        ])
                
                tabela = Table(dados, colWidths=col_widths)
                tabela.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                elementos.append(tabela)
                elementos.append(Spacer(1, 20))
            
            # Resumo estatístico
            total = len(extintores)
            if tipo_relatorio not in ['vencidos', 'vencendo']:
                vencidos = len([e for e in extintores if e.status == 'VENCIDO'])
                vencendo = len([e for e in extintores if 'VENCE' in e.status])
                ok = total - vencidos - vencendo
                
                resumo_text = f"""
                <b>RESUMO ESTATÍSTICO:</b><br/>
                Total de Extintores: {total}<br/>
                Extintores OK: {ok}<br/>
                Vencendo em 30 dias: {vencendo}<br/>
                Vencidos: {vencidos}<br/>
                Percentual OK: {(ok/total*100):.1f}%
                """
            else:
                resumo_text = f"""
                <b>RESUMO:</b><br/>
                Total de Extintores Filtrados: {total}
                """
            
            resumo = Paragraph(resumo_text, styles['Normal'])
            elementos.append(resumo)
            
            # Rodapé
            elementos.append(Spacer(1, 30))
            rodape = Paragraph(
                "Sistema de Gerenciamento de Extintores - Relatório gerado automaticamente", 
                styles['Normal']
            )
            elementos.append(rodape)
            
            # Gerar PDF
            doc.build(elementos)
            
            self.mostrar_popup('Sucesso', f'Relatório {tipo_relatorio} gerado!\n{filename}')
            
            # VERMELHO: Abrir PDF automaticamente
            try:
                os.startfile(filename)  # Windows
            except:
                pass
                
        except ImportError:
            self.mostrar_popup('Erro', 'Biblioteca reportlab não instalada!\nExecute: pip install reportlab')
        except Exception as e:
            self.mostrar_popup('Erro', f'Erro ao gerar relatório: {str(e)}')
    
    def mostrar_popup(self, titulo, mensagem):
        """Mostra popup com mensagem"""
        content = Label(text=mensagem, color=CORES['texto_azul'])
        popup = Popup(title=titulo, content=content, size_hint=(0.8, 0.4))
        popup.open()

# Atualizar a classe principal para incluir a nova tela
class GerenciadorExtintoresApp(App):
    def build(self):
        # Configurar janela
        Window.clearcolor = CORES['fundo_principal']
        Window.size = (450, 800)  # Tamanho otimizado para celular
        
        # Gerenciador de telas
        sm = ScreenManager()
        
        # Adicionar todas as telas
        sm.add_widget(TelaCadastro())
        sm.add_widget(TelaListagem())
        sm.add_widget(TelaRelatorios())
        
        # Layout principal com navegação
        main_layout = BoxLayout(orientation='vertical')
        
        # Botões de navegação
        nav_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), spacing=dp(2))
        
        btn_cadastro = Button(
            text='CADASTRO',
            background_color=CORES['botao_vermelho'],
            color=CORES['branco'],
            bold=True,
            font_size=sp(12)
        )
        btn_cadastro.bind(on_press=lambda x: setattr(sm, 'current', 'cadastro'))
        
        btn_listagem = Button(
            text='LISTAGEM',
            background_color=CORES['botao_vermelho'],
            color=CORES['branco'],
            bold=True,
            font_size=sp(12)
        )
        btn_listagem.bind(on_press=lambda x: setattr(sm, 'current', 'listagem'))
        
        btn_relatorios = Button(
            text='RELATÓRIOS',
            background_color=CORES['botao_vermelho'],
            color=CORES['branco'],
            bold=True,
            font_size=sp(12)
        )
        btn_relatorios.bind(on_press=lambda x: setattr(sm, 'current', 'relatorios'))
        
        nav_layout.add_widget(btn_cadastro)
        nav_layout.add_widget(btn_listagem)
        nav_layout.add_widget(btn_relatorios)
        
        main_layout.add_widget(nav_layout)
        main_layout.add_widget(sm)
        
        return main_layout
    
    def on_start(self):
        """Executado quando o app inicia"""
        # Verificar e criar diretórios necessários
        docs_path = os.path.join(os.path.expanduser('~'), 'Documents')
        if not os.path.exists(docs_path):
            try:
                os.makedirs(docs_path)
            except:
                pass
        
        # Mostrar informações de inicialização
        print("=== GERENCIADOR DE EXTINTORES INICIADO ===")
        print(f"Banco de dados: {os.path.join(docs_path, 'extintores.db')}")
        print("App rodando em modo de desenvolvimento")

# Função principal
def main():
    """Função principal do aplicativo"""
    try:
        # Verificar se é primeira execução
        if len(sys.argv) > 1 and sys.argv[1] == '--setup':
            setup_projeto()
            return
        
        # Executar aplicativo
        print("Iniciando Gerenciador de Extintores...")
        print("Pressione Ctrl+C para sair")
        
        app = GerenciadorExtintoresApp()
        app.run()
        
    except KeyboardInterrupt:
        print("\nAplicativo encerrado pelo usuário")
    except Exception as e:
        print(f"Erro ao executar aplicativo: {e}")
        input("Pressione Enter para continuar...")

# Executar apenas se for o arquivo principal
if __name__ == '__main__':
    main()

# ===== INSTRUÇÕES DE USO =====
"""
INSTRUÇÕES PARA CONFIGURAR E EXECUTAR:

1. PRIMEIRA CONFIGURAÇÃO:
   Execute: python main.py --setup
   Isso criará todos os arquivos necessários

2. INSTALAR DEPENDÊNCIAS:
   pip install kivy kivymd reportlab

3. EXECUTAR O APLICATIVO:
   python main.py

4. PARA GERAR APK (ANDROID):
   - Instale Android Studio
   - Configure Android SDK
   - Execute: pip install buildozer
   - Execute: buildozer android debug

5. CAMINHOS CONFIGURÁVEIS (VERMELHO):
   - Banco de dados: ~/Documents/extintores.db
   - Relatórios PDF: ~/Desktop/relatorio_*.pdf
   - Android SDK: Configure no buildozer.spec

6. RECURSOS DO SISTEMA:
   ✓ Cadastro completo de extintores
   ✓ Validação de campos e datas
   ✓ Máscaras para entrada de dados
   ✓ Listagem com status colorido
   ✓ Relatórios PDF avançados
   ✓ Estatísticas em tempo real
   ✓ Banco de dados SQLite
   ✓ Interface responsiva para mobile
   ✓ Cores personalizadas (laranja, vermelho, azul)

7. FUNCIONALIDADES:
   - Cadastro: Nome, localização, tipo, datas, etc.
   - Listagem: Visualização com cores por status
   - Relatórios: Completo, vencidos, vencendo, por tipo
   - Alertas: Vencimento em 30 dias e vencidos
   - Exportação: PDF com abertura automática
   - Persistência: Dados salvos automaticamente
"""