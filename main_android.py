from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.clock import Clock
from datetime import datetime
import json
import os

class GlowButton(Button):
    def __init__(self, bg_color=(0.2, 0.6, 1, 0.8), **kwargs):
        super().__init__(**kwargs)
        self.background_color = bg_color
        self.font_size = '16sp'
        self.bold = True

class ModernCard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 10
        with self.canvas.before:
            Color(1, 1, 1, 0.9)
            self.bg = RoundedRectangle(size=self.size, pos=self.pos, radius=[10])
        self.bind(size=self._update_bg, pos=self._update_bg)
    
    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos

class DataManager:
    def __init__(self):
        self.filename = 'extintores_data.json'
        self.extintores = self.load_data()
    
    def load_data(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def save_data(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.extintores, f, ensure_ascii=False, indent=2)
        except:
            pass

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        with self.canvas.before:
            Color(0.1, 0.1, 0.2, 1)
            self.bg = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)
        
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        title = Label(text='🔥 EXTINTOR MANAGER', font_size='36sp', bold=True,
                     color=[1, 0.8, 0.2, 1], size_hint_y=None, height=100)
        main_layout.add_widget(title)
        
        cards_layout = GridLayout(cols=2, spacing=20, size_hint_y=None, height=400)
        
        # Card Cadastro
        cadastro_card = ModernCard()
        cadastro_btn = GlowButton(text='📝 CADASTRO', bg_color=(0.2, 0.8, 0.2, 0.8))
        cadastro_btn.bind(on_press=self.go_cadastro)
        cadastro_card.add_widget(cadastro_btn)
        
        # Card Consulta
        consulta_card = ModernCard()
        consulta_btn = GlowButton(text='🔍 CONSULTA', bg_color=(0.8, 0.4, 1, 0.8))
        consulta_btn.bind(on_press=self.go_consulta)
        consulta_card.add_widget(consulta_btn)
        
        # Card Dashboard
        dashboard_card = ModernCard()
        dashboard_btn = GlowButton(text='📊 DASHBOARD', bg_color=(1, 0.6, 0.2, 0.8))
        dashboard_btn.bind(on_press=self.go_dashboard)
        dashboard_card.add_widget(dashboard_btn)
        
        # Card Sair
        sair_card = ModernCard()
        sair_btn = GlowButton(text='❌ SAIR', bg_color=(0.8, 0.2, 0.2, 0.8))
        sair_btn.bind(on_press=self.sair_app)
        sair_card.add_widget(sair_btn)
        
        cards_layout.add_widget(cadastro_card)
        cards_layout.add_widget(consulta_card)
        cards_layout.add_widget(dashboard_card)
        cards_layout.add_widget(sair_card)
        
        main_layout.add_widget(cards_layout)
        self.add_widget(main_layout)
    
    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos
    
    def go_cadastro(self, instance):
        self.manager.transition = SlideTransition(direction='up')
        self.manager.current = 'cadastro'
    
    def go_consulta(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'consulta'
    
    def go_dashboard(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'dashboard'
    
    def sair_app(self, instance):
        App.get_running_app().stop()

class CadastroScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_index = -1
        
        with self.canvas.before:
            Color(0.95, 0.95, 0.85, 1)
            self.bg = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)
        
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=80)
        back_btn = GlowButton(text='VOLTAR', size_hint_x=None, width=120, bg_color=(0.4, 0.8, 0.67, 1))
        back_btn.bind(on_press=self.go_back)
        
        title = Label(text='📝 CADASTRO DE EXTINTORES', font_size='28sp', bold=True,
                     color=[1, 0.8, 0.2, 1])
        
        header.add_widget(back_btn)
        header.add_widget(title)
        main_layout.add_widget(header)
        
        # Form
        form_card = ModernCard()
        form_layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        form_layout.bind(minimum_height=form_layout.setter('height'))
        
        self.inputs = {}
        fields = [
            ('numero', 'Número:', TextInput()),
            ('tipo', 'Tipo:', Spinner(values=['Pó Químico ABC', 'CO2', 'Água'], text='Selecione')),
            ('capacidade', 'Capacidade:', TextInput()),
            ('fabricante', 'Fabricante:', TextInput()),
            ('localizacao', 'Localização:', TextInput()),
            ('data_fabricacao', 'Data Fabricação:', TextInput()),
            ('data_vencimento', 'Data Vencimento:', TextInput()),
            ('ultima_recarga', 'Última Recarga:', TextInput()),
            ('proxima_recarga', 'Próxima Recarga:', TextInput()),
            ('observacoes', 'Observações:', TextInput())
        ]
        
        for field_name, label_text, widget in fields:
            form_layout.add_widget(Label(text=label_text, size_hint_y=None, height=40))
            form_layout.add_widget(widget)
            self.inputs[field_name] = widget
        
        scroll = ScrollView()
        scroll.add_widget(form_layout)
        form_card.add_widget(scroll)
        
        # Buttons
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=60)
        
        salvar_btn = GlowButton(text='💾 SALVAR', bg_color=(0.2, 0.8, 0.2, 0.8))
        salvar_btn.bind(on_press=self.salvar_extintor)
        
        limpar_btn = GlowButton(text='🗑️ LIMPAR', bg_color=(0.8, 0.6, 0.2, 0.8))
        limpar_btn.bind(on_press=self.limpar_campos)
        
        btn_layout.add_widget(salvar_btn)
        btn_layout.add_widget(limpar_btn)
        
        main_layout.add_widget(form_card)
        main_layout.add_widget(btn_layout)
        self.add_widget(main_layout)
    
    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos
    
    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='down')
        self.manager.current = 'home'
    
    def salvar_extintor(self, instance):
        app = App.get_running_app()
        extintor = {}
        
        for field, widget in self.inputs.items():
            if hasattr(widget, 'text'):
                extintor[field] = widget.text
            else:
                extintor[field] = widget.text if widget.text != 'Selecione' else ''
        
        extintor['status'] = 'Ativo'
        extintor['data_cadastro'] = datetime.now().strftime('%d/%m/%Y %H:%M')
        
        app.data.extintores.append(extintor)
        app.data.save_data()
        
        self.show_popup('Sucesso', 'Extintor cadastrado com sucesso!')
        self.limpar_campos(None)
    
    def limpar_campos(self, instance):
        for widget in self.inputs.values():
            if hasattr(widget, 'text'):
                widget.text = ''
            else:
                widget.text = 'Selecione'
    
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
        
        title = Label(text='🔍 CONSULTA DE EXTINTORES', font_size='28sp', bold=True,
                     color=[1, 0.8, 0.2, 1])
        
        header.add_widget(back_btn)
        header.add_widget(title)
        main_layout.add_widget(header)
        
        # Lista de resultados
        results_card = ModernCard()
        self.results_layout = BoxLayout(orientation='vertical', spacing=10)
        
        scroll = ScrollView()
        scroll.add_widget(self.results_layout)
        results_card.add_widget(scroll)
        
        main_layout.add_widget(results_card)
        self.add_widget(main_layout)
        
        Clock.schedule_once(self.load_data, 0.1)
    
    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos
    
    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'home'
    
    def load_data(self, dt):
        app = App.get_running_app()
        self.display_extintores(app.data.extintores)
    
    def display_extintores(self, extintores):
        self.results_layout.clear_widgets()
        
        if not extintores:
            self.results_layout.add_widget(Label(text='Nenhum extintor cadastrado', font_size='18sp'))
            return
        
        for extintor in extintores:
            item_card = ModernCard(size_hint_y=None, height=120)
            item_layout = BoxLayout(orientation='vertical')
            
            numero_label = Label(text=f"Nº: {extintor.get('numero', 'N/A')}", 
                               font_size='18sp', bold=True, color=[1, 0.8, 0.2, 1])
            tipo_label = Label(text=f"Tipo: {extintor.get('tipo', 'N/A')}", font_size='14sp')
            local_label = Label(text=f"Local: {extintor.get('localizacao', 'N/A')}", font_size='14sp')
            
            item_layout.add_widget(numero_label)
            item_layout.add_widget(tipo_label)
            item_layout.add_widget(local_label)
            
            item_card.add_widget(item_layout)
            self.results_layout.add_widget(item_card)

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        with self.canvas.before:
            Color(0.85, 0.95, 1, 1)
            self.bg = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)
        
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=80)
        back_btn = GlowButton(text='VOLTAR', size_hint_x=None, width=120, bg_color=(0.4, 0.8, 0.67, 1))
        back_btn.bind(on_press=self.go_back)
        
        title = Label(text='📊 DASHBOARD', font_size='32sp', bold=True,
                     color=[1, 0.8, 0.2, 1])
        
        header.add_widget(back_btn)
        header.add_widget(title)
        main_layout.add_widget(header)
        
        # Stats
        stats_card = ModernCard()
        self.stats_layout = BoxLayout(orientation='vertical', spacing=10)
        stats_card.add_widget(self.stats_layout)
        
        main_layout.add_widget(stats_card)
        self.add_widget(main_layout)
        
        Clock.schedule_once(self.load_stats, 0.1)
    
    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos
    
    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'home'
    
    def load_stats(self, dt):
        app = App.get_running_app()
        extintores = app.data.extintores
        
        total = len(extintores)
        tipos = {}
        
        for extintor in extintores:
            tipo = extintor.get('tipo', 'Não informado')
            tipos[tipo] = tipos.get(tipo, 0) + 1
        
        self.stats_layout.add_widget(Label(text=f'Total de Extintores: {total}', font_size='20sp', bold=True))
        
        for tipo, count in tipos.items():
            self.stats_layout.add_widget(Label(text=f'{tipo}: {count}', font_size='16sp'))

class ExtintorManagerApp(App):
    def build(self):
        self.data = DataManager()
        
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(CadastroScreen(name='cadastro'))
        sm.add_widget(ConsultaScreen(name='consulta'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        
        return sm

if __name__ == '__main__':
    ExtintorManagerApp().run()