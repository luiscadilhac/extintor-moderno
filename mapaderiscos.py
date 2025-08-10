# main.py
import kivy
kivy.require('2.3.0') # Verifique a sua versão do Kivy e ajuste aqui se necessário (ex: '2.3.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ObjectProperty, DictProperty, ListProperty
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox
from kivy.metrics import dp # Para garantir tamanhos consistentes em diferentes telas

import random
import sqlite3
import json
import os

# --- Configurações Globais (Cores e Título) ---
APP_TITLE = "Mapa de Riscos Ambientais - MTE - FUNDACENTRO - CIPA - SESMT"
PRIMARY_COLOR_ORANGE = [1.0, 0.65, 0.0, 1.0] # Laranja para o fundo principal
BUTTON_COLOR_LIGHT_YELLOW = [1.0, 1.0, 0.88, 1.0] # Amarelo Claro para os botões
BUTTON_COLOR_SELECTED = [0.8, 0.8, 0.0, 1.0] # Amarelo um pouco mais escuro para seleção
TEXT_COLOR_NAVY_BLUE = [0.0, 0.0, 0.5, 1.0] # Azul Marinho para textos de destaque
TEXT_COLOR_BLACK = [0.0, 0.0, 0.0, 1.0]     # Preto para textos comuns
TEXT_COLOR_WHITE = [1.0, 1.0, 1.0, 1.0]     # Branco para textos em fundos escuros (se aplicável)

# Cores dos Grupos de Risco (para o questionário)
RISK_COLOR_PHYSICAL = [0.0, 0.5, 0.0, 1.0]    # Verde para Riscos Físicos
RISK_COLOR_CHEMICAL = [1.0, 0.0, 0.0, 1.0]   # Vermelho para Riscos Químicos
RISK_COLOR_BIOLOGICAL = [0.65, 0.16, 0.16, 1.0] # Marrom para Riscos Biológicos
RISK_COLOR_ERGONOMIC = [1.0, 1.0, 0.0, 1.0]  # Amarelo para Riscos Ergonômicos
RISK_COLOR_ACCIDENT = [0.0, 0.0, 1.0, 1.0]   # Azul para Riscos de Acidentes

# --- Estrutura do Questionário Padrão ---
# Este dicionário define todas as perguntas e categorias.
# Será salvo no banco de dados para ser acessado pelos funcionários.
QUESTIONNAIRE_DEFAULT_STRUCTURE = {
    "titulo": "Questionário do Mapa de Riscos Ambientais",
    "perguntas": {
        "Riscos Físicos": {
            "cor": RISK_COLOR_PHYSICAL,
            "itens": {
                "ruidos": "Ruídos",
                "temperaturas_extremas": "Temperaturas extremas (calor ou frio)",
                "umidade": "Umidade",
                "calor": "Calor",
                "radiacao_ionizante": "Radiação ionizante",
                "pressao_anormal": "Pressão anormal"
            }
        },
        "Riscos Químicos": {
            "cor": RISK_COLOR_CHEMICAL,
            "itens": {
                "poeiras": "Poeiras",
                "gases": "Gases",
                "vapores": "Vapores",
                "fumos_metalicos": "Fumos Metálicos",
                "nevoas_neblinas": "Névoas/Neblinas"
            }
        },
        "Riscos Biológicos": {
            "cor": RISK_COLOR_BIOLOGICAL,
            "itens": {
                "bacterias_virus_etc": "Bactérias, Vírus, Bacilos, Fungos, Protozoários e Parasitas"
            }
        },
        "Riscos Ergonômicos": { # Ajustado para o nome correto
            "cor": RISK_COLOR_ERGONOMIC,
            "itens": {
                "trabalho_fisico_pesado": "Trabalho físico pesado",
                "posicoes_incorretas": "Posições incorretas e incômodas",
                "ritmos_excessivos": "Ritmos excessivos",
                "monotonia": "Monotonia",
                "trabalhos_em_turnos": "Trabalhos em Turnos (não tem um turno fixo)",
                "jornada_prolongada": "Jornada prolongada (excesso de horas extras)",
                "ambiente_toxico": "Ambiente Tóxico",
                "iluminacao_inadequada": "Iluminação inadequada"
            }
        },
        "Riscos de Acidentes": {
            "cor": RISK_COLOR_ACCIDENT,
            "itens": {
                "arranjo_fisico_inadequado": "Arranjo físico inadequados",
                "maquinas_sem_protecao": "Máquinas e equipamentos sem proteção",
                "ferramentas_inadequadas": "Ferramentas inadequadas ou defeituosas",
                "instalacoes_eletricas_inadequadas": "Instalações elétricas inadequadas",
                "armazenamento_inadequado": "Armazenamento inadequado",
                "animais_peconhentos": "Animais peçonhentos ou venenosos",
                "produtos_sem_rotulagem": "Produtos sem rotulagem ou inadequada",
                "falta_de_epi": "Falta de EPI ou inadequado",
                "transporte_inadequado": "Transporte de equipamentos e materiais de forma inadequada",
                "edificacoes_inadequadas": "Edificações inadequadas ou danificadas"
            }
        }
    }
}


# --- Funções para o Banco de Dados SQLite ---
DB_NAME = 'mapa_riscos.db'

def init_db(db_path):
    """Inicializa o banco de dados e cria as tabelas se elas não existirem."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empresa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            conteudo_json TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS respostas_funcionario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_empresa TEXT,
            questionario_id INTEGER,
            respostas_json TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def execute_db_operation(func):
    """
    Decorador para gerenciar a conexão e o cursor do banco de dados automaticamente.
    Simplifica as chamadas às funções do DB.
    """
    def wrapper(instance_or_path, *args, **kwargs):
        # Descobre o caminho do banco de dados, seja de uma instância de tela ou diretamente
        db_path = instance_or_path.db_path if hasattr(instance_or_path, 'db_path') else instance_or_path
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            # Chama a função original do banco de dados, passando o cursor
            result = func(cursor, *args, **kwargs)
            conn.commit() # Salva as mudanças
            return result
        except sqlite3.IntegrityError as e:
            conn.rollback() # Desfaz as mudanças em caso de erro de integridade
            raise ValueError(f"Erro de integridade no BD: {e}")
        except Exception as e:
            conn.rollback() # Desfaz as mudanças em caso de qualquer outro erro
            raise Exception(f"Erro no BD: {e}")
        finally:
            conn.close() # Sempre fecha a conexão
    return wrapper

@execute_db_operation
def insert_empresa_codigo(cursor, codigo):
    """Insere ou atualiza o código da empresa no banco de dados."""
    try:
        cursor.execute("INSERT INTO empresa (codigo) VALUES (?)", (codigo,))
        return cursor.lastrowid
    except sqlite3.IntegrityError: # Se o código já existe, ele atualiza
        cursor.execute("UPDATE empresa SET codigo = ? WHERE id = 1", (codigo,))
        return 1

@execute_db_operation
def get_empresa_codigo(cursor):
    """Obtém o código da empresa salvo no banco de dados."""
    cursor.execute("SELECT codigo FROM empresa LIMIT 1")
    result = cursor.fetchone()
    return result[0] if result else None

@execute_db_operation
def insert_questionario(cursor, titulo, conteudo_json):
    """Insere um novo questionário no banco de dados."""
    cursor.execute("INSERT INTO questionarios (titulo, conteudo_json) VALUES (?, ?)", (titulo, conteudo_json))
    return cursor.lastrowid

@execute_db_operation
def get_all_questionarios(cursor):
    """Obtém todos os questionários do banco de dados."""
    cursor.execute("SELECT id, titulo, conteudo_json FROM questionarios")
    results = cursor.fetchall()
    questionarios = []
    for row in results:
        # Carrega o JSON de volta para um dicionário Python
        questionarios.append({'id': row[0], 'titulo': row[1], 'conteudo': json.loads(row[2])})
    return questionarios

@execute_db_operation
def insert_respostas_funcionario(cursor, codigo_empresa, questionario_id, respostas_json):
    """Insere as respostas de um funcionário no banco de dados."""
    cursor.execute(
        "INSERT INTO respostas_funcionario (codigo_empresa, questionario_id, respostas_json) VALUES (?, ?, ?)",
        (codigo_empresa, questionario_id, respostas_json)
    )
    return cursor.lastrowid

@execute_db_operation
def get_respostas_by_codigo_and_questionario(cursor, codigo_empresa, questionario_id=None):
    """Obtém as respostas dos funcionários para um dado código de empresa e opcionalmente um questionário."""
    if questionario_id:
        cursor.execute("SELECT respostas_json FROM respostas_funcionario WHERE codigo_empresa = ? AND questionario_id = ?", (codigo_empresa, questionario_id))
    else:
        cursor.execute("SELECT respostas_json FROM respostas_funcionario WHERE codigo_empresa = ?", (codigo_empresa,))
    results = cursor.fetchall()
    return [json.loads(row[0]) for row in results]


# --- Classes de Telas do Kivy ---

class BaseScreen(Screen):
    """
    Classe base para todas as telas do aplicativo.
    Define o tema de cores e o título padrão.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # O caminho do banco de dados é acessado da instância principal do aplicativo
        self.db_path = App.get_running_app().db_path

        main_layout = BoxLayout(orientation='vertical')
        
        # Rótulo para o Título do Aplicativo no topo de todas as telas
        self.title_label = Label( # Adicionei 'self.' para que possa ser referenciado
            text=APP_TITLE,
            size_hint_y=None,
            height=dp(40), # Altura inicial
            font_size='18sp',
            color=TEXT_COLOR_NAVY_BLUE,
            bold=True,
            halign='center',
            valign='middle'
        )
        # É importante vincular o text_size aqui usando a largura da própria label ou de seu pai
        # para que a altura seja calculada corretamente.
        self.title_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        self.title_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', max(dp(40), value[1])))
        
        main_layout.add_widget(self.title_label)

        # Layout principal de conteúdo da tela, com fundo laranja
        self.content_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))
        self.content_layout.canvas.before.clear()
        with self.content_layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*PRIMARY_COLOR_ORANGE)
            self.rect = Rectangle(size=self.content_layout.size, pos=self.content_layout.pos)
        self.content_layout.bind(size=self._update_rect, pos=self._update_rect)

        main_layout.add_widget(self.content_layout)
        self.add_widget(main_layout)

    def _update_rect(self, instance, value):
        """Atualiza a posição e tamanho do retângulo de fundo."""
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    # Métodos wrapper para o BD, passando 'self' para que o decorador acesse db_path
    def _insert_empresa_codigo(self, codigo): return insert_empresa_codigo(self, codigo)
    def _get_empresa_codigo(self): return get_empresa_codigo(self)
    def _insert_questionario(self, titulo, conteudo_json): return insert_questionario(self, titulo, conteudo_json)
    def _get_all_questionarios(self): return get_all_questionarios(self)
    def _insert_respostas_funcionario(self, cod_empresa, q_id, respostas): return insert_respostas_funcionario(self, cod_empresa, q_id, respostas)
    def _get_respostas_by_codigo_and_questionario(self, cod_empresa, q_id=None): return get_respostas_by_codigo_and_questionario(self, cod_empresa, q_id)


class MainScreen(BaseScreen):
    """Tela inicial do aplicativo com as opções 'Empresa' e 'Funcionário'."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'main_screen'
        self.content_layout.clear_widgets() # Limpa o conteúdo padrão da BaseScreen

        # Botão para o Modo Empresa
        btn_empresa = Button(
            text="Modo Empresa",
            size_hint=(None, None), # Tamanho fixo
            size=(dp(250), dp(70)),
            pos_hint={'center_x': 0.5}, # Centraliza horizontalmente
            background_color=BUTTON_COLOR_LIGHT_YELLOW,
            color=TEXT_COLOR_NAVY_BLUE,
            font_size='22sp'
        )
        btn_empresa.bind(on_release=self.go_to_empresa_screen)

        # Botão para o Modo Funcionário
        btn_funcionario = Button(
            text="Modo Funcionário",
            size_hint=(None, None),
            size=(dp(250), dp(70)),
            pos_hint={'center_x': 0.5},
            background_color=BUTTON_COLOR_LIGHT_YELLOW,
            color=TEXT_COLOR_NAVY_BLUE,
            font_size='22sp'
        )
        btn_funcionario.bind(on_release=self.go_to_funcionario_access_screen)

        # Layout para os botões principais, centralizado
        button_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(30),
            size_hint=(None, None),
            size=(dp(300), dp(200)), # Define um tamanho para o layout que contém os botões
            pos_hint={'center_x': 0.5, 'center_y': 0.5} # Centraliza o layout dos botões na tela
        )
        button_layout.add_widget(btn_empresa)
        button_layout.add_widget(btn_funcionario)

        self.content_layout.add_widget(button_layout)

    def go_to_empresa_screen(self, instance):
        """Muda para a tela do Modo Empresa."""
        self.manager.current = 'empresa_screen'

    def go_to_funcionario_access_screen(self, instance):
        """Muda para a tela de acesso do Modo Funcionário (onde digita o código)."""
        self.manager.current = 'funcionario_screen_access'


class EmpresaScreen(BaseScreen):
    """Tela do Modo Empresa: gerencia código e visualiza respostas."""
    codigo_gerado = StringProperty('') # Propriedade para exibir o código da empresa

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'empresa_screen'
        self.content_layout.clear_widgets()
        self.build_ui()
        self.load_initial_data() # Carrega o código e as respostas ao entrar na tela

    def build_ui(self):
        """Constrói a interface de usuário da tela da empresa."""
        btn_back = Button(
            text="Voltar",
            size_hint=(None, None),
            size=(dp(100), dp(40)),
            background_color=BUTTON_COLOR_LIGHT_YELLOW,
            color=TEXT_COLOR_NAVY_BLUE
        )
        btn_back.bind(on_release=self.go_back_to_main)
        self.content_layout.add_widget(btn_back)

        self.content_layout.add_widget(Label(text="Painel da Empresa", font_size='24sp', color=TEXT_COLOR_NAVY_BLUE))
        self.codigo_label = Label(text=self.codigo_gerado, font_size='18sp', color=TEXT_COLOR_NAVY_BLUE)
        self.content_layout.add_widget(self.codigo_label)

        btn_gerar_codigo = Button(
            text="Gerar Novo Código",
            size_hint=(None, None),
            size=(dp(250), dp(50)),
            pos_hint={'center_x': 0.5},
            background_color=BUTTON_COLOR_LIGHT_YELLOW,
            color=TEXT_COLOR_NAVY_BLUE
        )
        btn_gerar_codigo.bind(on_release=self.gerar_e_salvar_codigo)
        self.content_layout.add_widget(btn_gerar_codigo)

        self.content_layout.add_widget(Label(text="--- Gerenciar Questionários ---", font_size='20sp', color=TEXT_COLOR_NAVY_BLUE))
        
        # LABEL: Questionário padrão info
        label_q_info = Label(text="O questionário padrão será carregado automaticamente no primeiro acesso. Você pode forçar o recarregamento.", 
                             color=TEXT_COLOR_BLACK, 
                             halign='center',
                             size_hint_y=None)
        label_q_info.bind(width=lambda instance, value: setattr(instance, 'text_size', (value - dp(40), None))) # Ajuste do text_size
        label_q_info.bind(texture_size=lambda instance, value: setattr(instance, 'height', max(dp(30), value[1]))) # Ajuste de altura
        self.content_layout.add_widget(label_q_info)

        btn_load_default_q = Button(
            text="Forçar Recarregamento Questionário Padrão",
            size_hint=(None, None),
            size=(dp(280), dp(40)),
            pos_hint={'center_x': 0.5},
            background_color=BUTTON_COLOR_LIGHT_YELLOW,
            color=TEXT_COLOR_NAVY_BLUE
        )
        btn_load_default_q.bind(on_release=self.ensure_default_questionnaire)
        self.content_layout.add_widget(btn_load_default_q)


        self.respostas_label = Label(text="Respostas dos Funcionários:", font_size='18sp', color=TEXT_COLOR_NAVY_BLUE)
        self.content_layout.add_widget(self.respostas_label)

        # ScrollView para exibir as respostas, permitindo rolagem
        self.respostas_scroll_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.respostas_scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.respostas_scroll.add_widget(self.respostas_scroll_layout)
        # Importante: A altura do layout interno é ajustada ao seu conteúdo
        self.respostas_scroll_layout.bind(minimum_height=self.respostas_scroll_layout.setter('height'))
        
        # Label para exibir as respostas formatadas
        self.respostas_display = Label(
            text="", 
            size_hint_y=None, # Não fixa a altura, ela será ajustada pelo bind
            halign='left', valign='top',
            color=TEXT_COLOR_BLACK,
            padding=[dp(10), dp(10)] # Espaçamento interno para o texto
        )
        # Bind para ajustar o text_size à largura disponível e a altura à textura
        self.respostas_display.bind(width=lambda instance, value: setattr(instance, 'text_size', (value - dp(20), None))) # dp(20) de padding horizontal
        self.respostas_display.bind(texture_size=lambda instance, value: setattr(instance, 'height', max(dp(50), value[1] + dp(20)))) # +dp(20) padding vertical
        self.respostas_display.height = dp(50) # Altura mínima inicial para evitar visualização vazia
        
        self.respostas_scroll_layout.add_widget(self.respostas_display)
        self.content_layout.add_widget(self.respostas_scroll)

        btn_carregar_respostas = Button(
            text="Recarregar Respostas",
            size_hint=(None, None),
            size=(dp(180), dp(40)),
            pos_hint={'center_x': 0.5},
            background_color=BUTTON_COLOR_LIGHT_YELLOW,
            color=TEXT_COLOR_NAVY_BLUE
        )
        btn_carregar_respostas.bind(on_release=self.carregar_respostas)
        self.content_layout.add_widget(btn_carregar_respostas)

    def go_back_to_main(self, instance):
        """Muda para a tela principal."""
        self.manager.current = 'main_screen'

    def load_initial_data(self):
        """Carrega o código da empresa e as respostas salvas ao iniciar a tela."""
        codigo_salvo = self._get_empresa_codigo()
        if codigo_salvo:
            self.codigo_gerado = f"Código Atual: {codigo_salvo}"
        else:
            self.codigo_gerado = "Nenhum código gerado."
        self.codigo_label.text = self.codigo_gerado
        self.carregar_respostas()
        self.ensure_default_questionnaire() # Garante que o questionário padrão esteja no DB

    def gerar_e_salvar_codigo(self, instance):
        """Gera um novo código de 4 dígitos e o salva no banco de dados."""
        codigo = str(random.randint(1000, 9999))
        try:
            self._insert_empresa_codigo(codigo)
            self.codigo_gerado = f"Novo Código: {codigo}"
            self.codigo_label.text = self.codigo_gerado
            App.get_running_app().show_toast(f"Código gerado e salvo: {codigo}")
        except Exception as e:
            App.get_running_app().show_toast(f"Erro ao gerar código: {e}")

    def ensure_default_questionnaire(self, instance=None):
        """Verifica se o questionário padrão já existe no DB e o insere se não existir."""
        questionarios_no_db = self._get_all_questionarios()
        default_q_exists = False
        for q in questionarios_no_db:
            if q['titulo'] == QUESTIONNAIRE_DEFAULT_STRUCTURE['titulo']:
                default_q_exists = True
                break

        if not default_q_exists:
            try:
                self._insert_questionario(
                    QUESTIONNAIRE_DEFAULT_STRUCTURE['titulo'],
                    json.dumps(QUESTIONNAIRE_DEFAULT_STRUCTURE['perguntas'])
                )
                App.get_running_app().show_toast("Questionário padrão inserido no banco de dados.")
            except Exception as e:
                App.get_running_app().show_toast(f"Erro ao inserir questionário padrão: {e}")
        else:
            App.get_running_app().show_toast("Questionário padrão já existe no banco de dados.")

    def carregar_respostas(self, instance=None):
        """Carrega e exibe as respostas dos funcionários do banco de dados."""
        codigo_empresa = self._get_empresa_codigo()
        if not codigo_empresa:
            self.respostas_display.text = "Nenhum código de empresa definido para carregar respostas."
            # A altura já será definida pelo bind de texture_size, mas garantir o mínimo aqui não faz mal
            self.respostas_display.height = dp(50) 
            return

        respostas = self._get_respostas_by_codigo_and_questionario(codigo_empresa)
        if respostas:
            display_text = "Respostas Recebidas:\n"
            for idx, resp in enumerate(respostas):
                display_text += f"--- Resposta {idx+1} ---\n"
                for group_name, risk_data in resp.items():
                    display_text += f"  {group_name}:\n"
                    for risk_name, status in risk_data.items():
                        # Verifica se o risco foi realmente selecionado
                        if status.get('selecionado', False):
                            # Exibe o risco e seu tamanho, se houver
                            display_text += f"    - {risk_name}: {status.get('tamanho', 'Não especificado')}\n"
                display_text += "\n" # Adiciona uma linha em branco entre respostas para melhor leitura
            self.respostas_display.text = display_text
        else:
            self.respostas_display.text = "Nenhuma resposta recebida ainda."
            self.respostas_display.height = dp(50) # Garante altura mínima


class FuncionarioAccessScreen(BaseScreen):
    """Tela para o funcionário digitar o código da empresa."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'funcionario_screen_access'
        self.content_layout.clear_widgets()
        self.build_ui()

    def build_ui(self):
        """Constrói a interface de usuário da tela de acesso do funcionário."""
        btn_back = Button(
            text="Voltar",
            size_hint=(None, None),
            size=(dp(100), dp(40)),
            background_color=BUTTON_COLOR_LIGHT_YELLOW,
            color=TEXT_COLOR_NAVY_BLUE
        )
        btn_back.bind(on_release=self.go_back_to_main)
        self.content_layout.add_widget(btn_back)

        self.content_layout.add_widget(Label(text="Modo Funcionário - Acesso", font_size='24sp', color=TEXT_COLOR_NAVY_BLUE))

        self.ti_codigo = TextInput(
            hint_text="Digite o Código da Empresa (4 dígitos)",
            size_hint_y=None, height=dp(40), multiline=False,
            input_type='number', # Sugestão de teclado numérico para Android
            background_color=TEXT_COLOR_WHITE, foreground_color=TEXT_COLOR_BLACK
        )
        self.content_layout.add_widget(self.ti_codigo)

        btn_acessar = Button(
            text="Acessar Orientação do Questionário",
            size_hint=(None, None),
            size=(dp(280), dp(50)),
            pos_hint={'center_x': 0.5},
            background_color=BUTTON_COLOR_LIGHT_YELLOW,
            color=TEXT_COLOR_NAVY_BLUE
        )
        btn_acessar.bind(on_release=self.acessar_orientacao_questionario)
        self.content_layout.add_widget(btn_acessar)

    def go_back_to_main(self, instance):
        """Muda para a tela principal."""
        self.manager.current = 'main_screen'

    def acessar_orientacao_questionario(self, instance):
        """Valida o código da empresa e direciona para a tela de orientação."""
        codigo_digitado = self.ti_codigo.text
        # Verifica se o código tem 4 dígitos e é composto apenas por números
        if not codigo_digitado or len(codigo_digitado) != 4 or not codigo_digitado.isdigit():
            App.get_running_app().show_toast("Por favor, digite um código de 4 dígitos válido.")
            return

        codigo_empresa_salvo = self._get_empresa_codigo()

        if codigo_digitado == codigo_empresa_salvo:
            App.get_running_app().show_toast("Código correto! Direcionando para a orientação.")
            self.manager.current = 'questionnaire_orientation_screen'
        else:
            App.get_running_app().show_toast("Código incorreto. Tente novamente.")


class QuestionnaireOrientationScreen(BaseScreen):
    """Tela de orientação para o funcionário antes de iniciar o questionário."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'questionnaire_orientation_screen'
        self.content_layout.clear_widgets()
        self.build_ui()

    def build_ui(self):
        """Constrói a interface de usuário da tela de orientação."""
        # Texto completo da orientação
        orientation_text = """
        Questionário do Mapa de Riscos Ambientais - MTE - FUNDACENTRO - NR-5 CIPA.

        Este questionário servirá como base para a confecção do Mapa de riscos do seu setor. Você estará auxiliando nos trabalhos da CIPA e do SESMT.
        É importante que você entenda que o questionário representa a sua visão de riscos do seu ambiente de trabalho, independente de laudos técnicos, opiniões de outros funcionários e de qual o nível de sua formação.
        As opiniões diferentes entre funcionários do mesmo setor, não invalidam as respostas e sim agregam. Um exemplo muito comum, são homens e mulheres terem sensibilidades diferentes entre o frio e o calor em uma sala de atividades administrativa climatizada.

        Forma de responder o questionário.

        Os riscos serão listados por grupos. Você vai **clicar no risco** que entende que esteja presente em seu ambiente de trabalho (marcando a caixa de seleção ao lado do risco). APÓS CLICAR NO RISCO, clique no **tamanho do risco** (Pequeno, Médio, Grande), considerando os menos graves, menores e os mais graves, maiores. Terá as opções **Pequeno**, **Médio** e **Grande**.
        """

        # ScrollView para o texto de orientação, garantindo que todo o conteúdo seja visível
        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        orientation_label = Label(
            text=orientation_text,
            size_hint_y=None, # A altura será ajustada automaticamente
            halign='left', # Alinhamento do texto à esquerda
            valign='top', # Alinhamento vertical do texto ao topo
            color=TEXT_COLOR_BLACK, # Mantém preto para o texto de orientação
            markup=True, # Habilita o uso de negrito no texto de orientação
            padding=(dp(10), dp(10)) # Espaçamento interno
        )
        # Binds para garantir que text_size e height são ajustados dinamicamente e corretamente
        # Primeiro, vincular text_size à largura da label
        orientation_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value - dp(20), None))) # subtrai padding
        # Depois, vincular a altura ao texture_size (que será atualizado pelo text_size)
        orientation_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', max(dp(50), value[1] + dp(20))))
        
        scroll_view.add_widget(orientation_label)
        self.content_layout.add_widget(scroll_view)

        # Botão para Prosseguir para o Questionário
        btn_prosseguir = Button(
            text="Prosseguir para o Questionário",
            size_hint=(None, None),
            size=(dp(280), dp(50)),
            pos_hint={'center_x': 0.5},
            background_color=BUTTON_COLOR_LIGHT_YELLOW,
            color=TEXT_COLOR_NAVY_BLUE
        )
        btn_prosseguir.bind(on_release=self.go_to_questionnaire)
        self.content_layout.add_widget(btn_prosseguir)

    def go_to_questionnaire(self, instance):
        """Muda para a tela do questionário."""
        self.manager.current = 'funcionario_questionnaire_screen'


class FuncionarioQuestionnaireScreen(BaseScreen):
    """Tela principal onde o funcionário responde ao questionário."""
    current_questionario_data = ObjectProperty(None)
    responses_collector = DictProperty({})
    
    # Adicionando um DictProperty para armazenar referências aos botões de risco e tamanho
    # Isso permitirá que possamos mudar a cor do botão quando o checkbox associado é ativado/desativado.
    risk_button_references = DictProperty({}) # {risk_full_key: Button_instance}
    size_button_references = DictProperty({}) # {risk_full_key: {size_option: Button_instance}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'funcionario_questionnaire_screen'
        self.content_layout.clear_widgets()
        self.build_ui()

    def build_ui(self):
        """Constrói a interface de usuário da tela do questionário."""
        btn_back = Button(
            text="Voltar à Orientação",
            size_hint=(None, None),
            size=(dp(150), dp(40)),
            background_color=BUTTON_COLOR_LIGHT_YELLOW,
            color=TEXT_COLOR_NAVY_BLUE
        )
        btn_back.bind(on_release=self.go_back_to_orientation)
        self.content_layout.add_widget(btn_back)

        self.questionario_title_label = Label(text="Carregando Questionário...", font_size='24sp', color=TEXT_COLOR_NAVY_BLUE)
        self.content_layout.add_widget(self.questionario_title_label)

        # ScrollView para o conteúdo do questionário, permitindo rolagem
        self.questionario_scroll_layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, padding=dp(5))
        self.questionario_scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.questionario_scroll.add_widget(self.questionario_scroll_layout)
        self.questionario_scroll_layout.bind(minimum_height=self.questionario_scroll_layout.setter('height'))
        self.content_layout.add_widget(self.questionario_scroll)

        # Botão para enviar as respostas
        btn_enviar_respostas = Button(
            text="Enviar Respostas",
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            pos_hint={'center_x': 0.5},
            background_color=BUTTON_COLOR_LIGHT_YELLOW,
            color=TEXT_COLOR_NAVY_BLUE
        )
        btn_enviar_respostas.bind(on_release=self.enviar_respostas)
        self.content_layout.add_widget(btn_enviar_respostas)

    def on_enter(self, *args):
        """Chamado toda vez que a tela do questionário é exibida."""
        self.load_questionnaire_data()

    def go_back_to_orientation(self, instance):
        """Muda de volta para a tela de orientação."""
        self.manager.current = 'questionnaire_orientation_screen'

    def load_questionnaire_data(self):
        """Carrega o questionário do banco de dados e o renderiza na tela."""
        questionarios_disponiveis = self._get_all_questionarios()
        if questionarios_disponiveis:
            self.current_questionario_data = questionarios_disponiveis[0]
            self.render_questionnaire()
        else:
            App.get_running_app().show_toast("Nenhum questionário encontrado para preencher.")
            self.questionario_title_label.text = "Nenhum questionário disponível."
            self.clear_questionnaire_ui()

    def render_questionnaire(self):
        """Renderiza dinamicamente as perguntas do questionário na tela."""
        self.questionario_scroll_layout.clear_widgets()
        self.responses_collector = {} 
        self.risk_button_references = {} # Resetar referências dos botões de risco
        self.size_button_references = {} # Resetar referências dos botões de tamanho

        if not self.current_questionario_data:
            return

        self.questionario_title_label.text = self.current_questionario_data['titulo']

        for group_name, group_data in self.current_questionario_data['conteudo'].items():
            group_label = Label(
                text=f"[color={self.get_hex_color(group_data['cor'])}]{group_name}[/color]",
                font_size='18sp',
                size_hint_y=None,
                halign='left',
                markup=True,
                bold=True
            )
            group_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value - dp(20), None)))
            group_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', max(dp(30), value[1])))
            
            self.questionario_scroll_layout.add_widget(group_label)

            for risk_key, risk_text in group_data['itens'].items():
                risk_full_key = f"{group_name}_{risk_key}"
                self.responses_collector[risk_full_key] = {'selecionado': False, 'tamanho': ''}

                risk_item_layout = BoxLayout(orientation='vertical', size_hint_y=None, padding=(0,0,0,dp(5)))
                
                # Layout para o checkbox de "risco presente" e o BOTÃO de descrição
                present_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40)) # Definir altura para consistência
                
                # Checkbox principal
                present_checkbox = CheckBox(size_hint_x=None, width=dp(40))
                present_checkbox.risk_key = risk_full_key 
                present_checkbox.bind(active=self.on_risk_checkbox_active) # Novo handler para o checkbox
                
                # BOTÃO para o texto do risco - este será o "campo clicável" principal
                risk_text_button = Button(
                    text=risk_text,
                    size_hint_x=1,
                    background_color=BUTTON_COLOR_LIGHT_YELLOW, # Cor inicial
                    color=TEXT_COLOR_NAVY_BLUE,
                    halign='left', valign='middle',
                    text_size=(self.width - dp(80), None), # Ajusta para largura disponível do botão
                    padding=(dp(10), 0) # Padding interno para o texto do botão
                )
                risk_text_button.bind(on_release=lambda btn, rk=risk_full_key, cb=present_checkbox: self.toggle_risk_selection_from_button(rk, cb))
                self.risk_button_references[risk_full_key] = risk_text_button # Armazenar referência do botão

                present_layout.add_widget(present_checkbox)
                present_layout.add_widget(risk_text_button)
                risk_item_layout.add_widget(present_layout)

                # Layout para as opções de tamanho (Pequeno, Médio, Grande)
                size_options_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(30), padding=(dp(40), 0, 0, 0), spacing=dp(5)) 
                radio_group_name = f"group_{risk_full_key}" 
                
                self.size_button_references[risk_full_key] = {} # Dicionário para botões de tamanho

                for size_option in ["Pequeno", "Médio", "Grande"]:
                    size_checkbox = CheckBox(group=radio_group_name, size_hint_x=None, width=dp(40), opacity=0) # Checkbox invisível
                    size_checkbox.disabled = True # Desabilita o clique direto no checkbox para forçar uso do botão
                    #size_checkbox.active = False # Garante que começam desmarcados (já é o padrão)

                    # BOTÃO para o texto do tamanho
                    size_option_button = Button(
                        text=size_option,
                        size_hint_x=None, width=dp(80),
                        background_color=BUTTON_COLOR_LIGHT_YELLOW, # Cor inicial
                        color=TEXT_COLOR_NAVY_BLUE,
                        font_size='14sp'
                    )
                    # O clique no botão de tamanho ativa o checkbox de tamanho correspondente
                    size_option_button.bind(on_release=lambda btn, cb=size_checkbox: setattr(cb, 'active', True))
                    # Vincula o evento 'active' do checkbox para atualizar a cor do botão
                    size_checkbox.bind(active=lambda cb, value, btn=size_option_button, rk=risk_full_key, so=size_option: self.on_risk_size_checkbox_active(cb, value, btn, rk, so))
                    
                    self.size_button_references[risk_full_key][size_option] = size_option_button # Armazenar referência

                    size_options_layout.add_widget(size_checkbox) # Adiciona o checkbox invisível
                    size_options_layout.add_widget(size_option_button)
                
                risk_item_layout.add_widget(size_options_layout)
                risk_item_layout.bind(minimum_height=risk_item_layout.setter('height'))

                self.questionario_scroll_layout.add_widget(risk_item_layout)

        # Atualiza o estado visual inicial de todos os botões com base em responses_collector
        self.update_buttons_visual_state()

    def toggle_risk_selection_from_button(self, risk_full_key, checkbox_instance):
        """
        Chamado quando o botão de texto do risco é clicado.
        Alterna o estado do checkbox associado.
        """
        checkbox_instance.active = not checkbox_instance.active

    def on_risk_checkbox_active(self, checkbox_instance, is_selected):
        """
        Chamado quando o checkbox principal de um risco é marcado/desmarcado (via checkbox ou botão).
        Atualiza o coletor de respostas e gerencia os botões de tamanho.
        """
        risk_key = checkbox_instance.risk_key
        self.responses_collector[risk_key]['selecionado'] = is_selected

        # Atualiza a cor do botão de risco
        if risk_key in self.risk_button_references:
            btn = self.risk_button_references[risk_key]
            btn.background_color = BUTTON_COLOR_SELECTED if is_selected else BUTTON_COLOR_LIGHT_YELLOW

        if not is_selected:
            # Se o risco foi desmarcado, resetar o tamanho selecionado e desmarcar todos os checkboxes de tamanho
            self.responses_collector[risk_key]['tamanho'] = ''
            if risk_key in self.size_button_references:
                for size_option, size_btn in self.size_button_references[risk_key].items():
                    # Para garantir que o checkbox interno também seja desmarcado e o evento dispare
                    # Precisamos acessar o checkbox associado ao botão, não apenas o botão.
                    # Isso é um pouco mais complexo se o checkbox está "escondido" e o botão o controla.
                    # Uma forma é, no 'render_questionnaire', passar também o checkbox para o size_button_references.
                    # Por enquanto, vamos apenas resetar a cor dos botões de tamanho.
                    size_btn.background_color = BUTTON_COLOR_LIGHT_YELLOW
        elif not self.responses_collector[risk_key]['tamanho']:
            App.get_running_app().show_toast("Por favor, selecione o tamanho do risco (Pequeno, Médio, Grande).")
        
        # O estado visual dos botões de tamanho é tratado em on_risk_size_checkbox_active
        # Mas para garantir que todos fiquem desmarcados quando o risco principal é desmarcado:
        if not is_selected and risk_key in self.size_button_references:
             for size_option, btn in self.size_button_references[risk_key].items():
                 btn.background_color = BUTTON_COLOR_LIGHT_YELLOW


    def on_risk_size_checkbox_active(self, checkbox_instance, is_active, button_instance, risk_key, size_option):
        """
        Chamado quando um checkbox de tamanho (Pequeno, Médio, Grande) é marcado/desmarcado.
        Atualiza o coletor de respostas e a cor do botão de tamanho.
        """
        if is_active:
            # Verifica se o risco principal está marcado. Se não estiver, desmarca o tamanho.
            if not self.responses_collector[risk_key]['selecionado']:
                App.get_running_app().show_toast("Primeiro marque o risco como presente antes de definir o tamanho.")
                checkbox_instance.active = False # Desativa o checkbox que foi ativado indevidamente
                button_instance.background_color = BUTTON_COLOR_LIGHT_YELLOW # Volta a cor original
                return

            self.responses_collector[risk_key]['tamanho'] = size_option
            # Muda a cor do botão selecionado
            button_instance.background_color = BUTTON_COLOR_SELECTED
            
            # Desativa e reseta a cor dos outros botões de tamanho do mesmo grupo (simula radio button visualmente)
            if risk_key in self.size_button_references:
                for other_size_option, other_btn in self.size_button_references[risk_key].items():
                    if other_size_option != size_option:
                        other_btn.background_color = BUTTON_COLOR_LIGHT_YELLOW
        else:
            # Se o checkbox de tamanho foi desativado (geralmente por outro ser selecionado no mesmo grupo)
            # e se a opção desativada era a atualmente salva, limpa a seleção.
            if self.responses_collector[risk_key]['tamanho'] == size_option:
                self.responses_collector[risk_key]['tamanho'] = ''
            button_instance.background_color = BUTTON_COLOR_LIGHT_YELLOW # Volta a cor original

    def update_buttons_visual_state(self):
        """
        Atualiza o estado visual de todos os botões de risco e tamanho
        com base nos dados em `responses_collector`. Chamado ao carregar o questionário.
        """
        for risk_full_key, data in self.responses_collector.items():
            is_selected = data['selecionado']
            selected_size = data['tamanho']

            # Atualiza o botão do risco
            if risk_full_key in self.risk_button_references:
                btn = self.risk_button_references[risk_full_key]
                btn.background_color = BUTTON_COLOR_SELECTED if is_selected else BUTTON_COLOR_LIGHT_YELLOW
            
            # Atualiza os botões de tamanho
            if risk_full_key in self.size_button_references:
                for size_option, btn in self.size_button_references[risk_full_key].items():
                    if is_selected and size_option == selected_size:
                        btn.background_color = BUTTON_COLOR_SELECTED
                    else:
                        btn.background_color = BUTTON_COLOR_LIGHT_YELLOW


    def get_hex_color(self, rgba_color):
        """Converte uma cor RGBA (lista) para o formato hexadecimal (string) para uso com markup."""
        return '#%02x%02x%02x' % (int(rgba_color[0]*255), int(rgba_color[1]*255), int(rgba_color[2]*255))

    def enviar_respostas(self, instance):
        """Coleta as respostas e as envia para o banco de dados (para o modo Empresa)."""
        codigo_empresa = App.get_running_app().root.get_screen('funcionario_screen_access').ti_codigo.text
        if not codigo_empresa:
            App.get_running_app().show_toast("Erro: Código da empresa não encontrado. Por favor, volte e digite-o novamente.")
            return

        if not self.current_questionario_data:
            App.get_running_app().show_toast("Nenhum questionário carregado para enviar.")
            return

        questionario_id = self.current_questionario_data['id']
        final_responses = {} 

        for group_name, group_data in self.current_questionario_data['conteudo'].items():
            final_responses[group_name] = {}
            for risk_key, risk_text in group_data['itens'].items():
                full_risk_key = f"{group_name}_{risk_key}"
                response_status = self.responses_collector.get(full_risk_key, {'selecionado': False, 'tamanho': ''})
                
                final_responses[group_name][risk_text] = {
                    'selecionado': response_status['selecionado'],
                    'tamanho': response_status['tamanho']
                }

        try:
            self._insert_respostas_funcionario(codigo_empresa, questionario_id, json.dumps(final_responses))
            App.get_running_app().show_toast("Respostas enviadas com sucesso!")
            self.clear_questionnaire_ui() 
            self.manager.current = 'funcionario_screen_access' 
        except Exception as e:
            App.get_running_app().show_toast(f"Erro ao enviar respostas: {e}")

    def clear_questionnaire_ui(self):
        """Limpa todos os widgets do questionário e reseta o coletor de respostas."""
        self.questionario_scroll_layout.clear_widgets()
        self.responses_collector = {}
        self.risk_button_references = {}
        self.size_button_references = {}
        self.questionario_title_label.text = "Questionário Limpo"


# --- Aplicativo Principal Kivy ---

class MapaRiscosApp(App):
    """Classe principal do aplicativo Kivy."""
    def build(self):
        self.db_path = os.path.join(self.user_data_dir, DB_NAME)
        init_db(self.db_path) 

        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(MainScreen())
        self.screen_manager.add_widget(EmpresaScreen())
        self.screen_manager.add_widget(FuncionarioAccessScreen()) 
        self.screen_manager.add_widget(QuestionnaireOrientationScreen()) 
        self.screen_manager.add_widget(FuncionarioQuestionnaireScreen()) 

        Window.clearcolor = PRIMARY_COLOR_ORANGE
        return self.screen_manager

    def show_toast(self, message):
        """Exibe uma mensagem de 'toast' (pop-up temporário) na tela."""
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
        content.add_widget(Label(text=message, color=TEXT_COLOR_BLACK, halign='center', valign='middle',
                                 text_size=(Window.width * 0.7, None))) 
        popup = Popup(title='Aviso', content=content, size_hint=(0.8, None), height=dp(120), auto_dismiss=True)
        popup.open()
        from kivy.clock import Clock
        Clock.schedule_once(popup.dismiss, 2)


if __name__ == '__main__':
    MapaRiscosApp().run()