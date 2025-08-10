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

class SistemaVotacao:
    def __init__(self):
        self.candidatos = {'1': 'Maria', '2': 'João', '3': 'Ana'}
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
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        layout.add_widget(Label(text='ELEIÇÃO CIPA', font_size='30sp'))
        
        btn_mesario = Button(text='MESÁRIO', size_hint_y=None, height=60)
        btn_mesario.bind(on_press=self.go_mesario)
        layout.add_widget(btn_mesario)
        
        self.add_widget(layout)
        
    def go_mesario(self, instance):
        self.manager.current = 'mesario'

class MesarioScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        layout.add_widget(Label(text='TERMINAL MESÁRIO', font_size='24sp'))
        
        self.id_input = TextInput(hint_text='ID do Eleitor', multiline=False)
        layout.add_widget(self.id_input)
        
        btn_habilitar = Button(text='HABILITAR', size_hint_y=None, height=50)
        btn_habilitar.bind(on_press=self.habilitar)
        layout.add_widget(btn_habilitar)
        
        self.message_label = Label(text='')
        layout.add_widget(self.message_label)
        
        btn_voltar = Button(text='VOLTAR', size_hint_y=None, height=50)
        btn_voltar.bind(on_press=self.voltar)
        layout.add_widget(btn_voltar)
        
        self.add_widget(layout)
        
    def habilitar(self, instance):
        id_eleitor = self.id_input.text.strip()
        if not id_eleitor:
            self.message_label.text = "Digite um ID"
            return
            
        app = App.get_running_app()
        sucesso, codigo = app.sistema.habilitar_eleitor(id_eleitor)
        
        if sucesso:
            self.message_label.text = f"Código: {codigo}"
        else:
            self.message_label.text = codigo
            
        self.id_input.text = ''
        
    def voltar(self, instance):
        self.manager.current = 'home'

class TestApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sistema = SistemaVotacao()
        
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(MesarioScreen(name='mesario'))
        return sm

if __name__ == '__main__':
    TestApp().run()