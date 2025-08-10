import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
import random

kivy.require('2.0.0')

class SistemaVotacaoCIPA:
    def __init__(self):
        self.candidatos = {'1': 'Maria Silva', '2': 'João Pereira', '3': 'Ana Costa'}
        self.eleitores_habilitados = {}
        self.codigos_ativos = set()
        
    def habilitar_eleitor(self, id_eleitor):
        if id_eleitor in self.eleitores_habilitados:
            return False, "Eleitor já habilitado"
        codigo = str(random.randint(100000, 999999))
        self.eleitores_habilitados[id_eleitor] = codigo
        self.codigos_ativos.add(codigo)
        return True, codigo

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=40, spacing=25)
        
        title = Label(text='🗳️ ELEIÇÃO CIPA', font_size='40sp', bold=True, color=[1, 0.8, 0, 1])
        layout.add_widget(title)
        
        mesario_btn = Button(text='👨‍💼 MESÁRIO', font_size='18sp', bold=True,
                            background_color=[0.2, 0.8, 0.2, 1], size_hint_y=None, height=50)
        mesario_btn.bind(on_press=self.go_mesario)
        layout.add_widget(mesario_btn)
        
        self.add_widget(layout)
        
    def go_mesario(self, instance):
        self.manager.current = 'mesario'

class MesarioScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        title = Label(text='👨‍💼 TERMINAL DO MESÁRIO', font_size='28sp', bold=True)
        layout.add_widget(title)

        layout.add_widget(Label(text='🆔 ID do Eleitor:', font_size='20sp'))
        self.id_eleitor_input = TextInput(multiline=False, hint_text='Ex: Func_001')
        layout.add_widget(self.id_eleitor_input)

        habilitar_button = Button(text='✅ HABILITAR E GERAR CÓDIGO', font_size='18sp', bold=True)
        habilitar_button.bind(on_press=self.habilitar)
        layout.add_widget(habilitar_button)

        self.message_label = Label(text='', font_size='18sp', bold=True)
        layout.add_widget(self.message_label)

        self.codigo_display_label = Label(text='', font_size='28sp', bold=True)
        layout.add_widget(self.codigo_display_label)

        back_button = Button(text='🏠 VOLTAR', font_size='16sp', bold=True)
        back_button.bind(on_press=self.go_home)
        layout.add_widget(back_button)
        
        self.add_widget(layout)

    def habilitar(self, instance):
        id_eleitor = self.id_eleitor_input.text.strip()
        self.message_label.text = ""
        self.codigo_display_label.text = ""

        if not id_eleitor:
            self.message_label.text = "Por favor, digite o ID do eleitor."
            return

        app_instance = App.get_running_app()
        sucesso, mensagem_ou_codigo = app_instance.sistema_votacao.habilitar_eleitor(id_eleitor)
        if sucesso:
            self.message_label.text = f"Eleitor '{id_eleitor}' HABILITADO!"
            self.codigo_display_label.text = f"CÓDIGO: {mensagem_ou_codigo}"
        else:
            self.message_label.text = f"Erro: {mensagem_ou_codigo}"
        self.id_eleitor_input.text = ''

    def go_home(self, instance):
        self.manager.current = 'home'

class CIPAApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sistema_votacao = SistemaVotacaoCIPA()

    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(MesarioScreen(name='mesario'))
        return sm

if __name__ == '__main__':
    CIPAApp().run()