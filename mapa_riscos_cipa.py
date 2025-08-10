import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from PIL import Image, ImageTk, ImageDraw
import json
import os
from datetime import datetime

class MapaRiscosCIPA:
    def __init__(self, root):
        self.root = root
        self.root.title("Mapa de Riscos Ambientais - CIPA")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Dados do aplicativo
        self.layout_image = None
        self.layout_photo = None
        self.riscos = []
        self.mode = 'view'  # 'view', 'add'
        self.canvas_width = 800
        self.canvas_height = 600
        
        # Configurações dos tipos de risco
        self.tipos_risco = {
            'fisico': {'cor': '#28a745', 'label': 'Físico', 'icon': '⚡'},
            'quimico': {'cor': '#dc3545', 'label': 'Químico', 'icon': '🧪'},
            'biologico': {'cor': '#6f42c1', 'label': 'Biológico', 'icon': '🦠'},
            'ergonomico': {'cor': '#fd7e14', 'label': 'Ergonômico', 'icon': '👤'},
            'acidente': {'cor': '#007bff', 'label': 'Acidente', 'icon': '⚠️'}
        }
        
        self.intensidades = {
            'baixa': {'tamanho': 20, 'label': 'Baixa'},
            'media': {'tamanho': 30, 'label': 'Média'},
            'alta': {'tamanho': 40, 'label': 'Alta'}
        }
        
        self.criar_interface()
        
    def criar_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(main_frame, text="Mapa de Riscos Ambientais - CIPA", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Barra de ferramentas
        toolbar_frame = ttk.Frame(main_frame)
        toolbar_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(toolbar_frame, text="Carregar Layout", 
                  command=self.carregar_layout).grid(row=0, column=0, padx=(0, 5))
        
        self.btn_add = ttk.Button(toolbar_frame, text="Adicionar Risco", 
                                 command=self.toggle_add_mode)
        self.btn_add.grid(row=0, column=1, padx=5)
        
        ttk.Button(toolbar_frame, text="Salvar Projeto", 
                  command=self.salvar_projeto).grid(row=0, column=2, padx=5)
        
        ttk.Button(toolbar_frame, text="Carregar Projeto", 
                  command=self.carregar_projeto).grid(row=0, column=3, padx=5)
        
        ttk.Button(toolbar_frame, text="Exportar Mapa", 
                  command=self.exportar_mapa).grid(row=0, column=4, padx=5)
        
        ttk.Button(toolbar_frame, text="Gerar Relatório", 
                  command=self.gerar_relatorio).grid(row=0, column=5, padx=5)
        
        # Frame do conteúdo
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Canvas do mapa
        self.canvas_frame = ttk.LabelFrame(content_frame, text="Mapa de Riscos", padding="10")
        self.canvas_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.canvas = tk.Canvas(self.canvas_frame, width=self.canvas_width, 
                               height=self.canvas_height, bg='white', relief='sunken', bd=2)
        self.canvas.grid(row=0, column=0)
        self.canvas.bind("<Button-1>", self.canvas_click)
        
        # Painel lateral
        sidebar_frame = ttk.Frame(content_frame)
        sidebar_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E))
        
        # Legenda
        legenda_frame = ttk.LabelFrame(sidebar_frame, text="Legenda", padding="10")
        legenda_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        for i, (key, tipo) in enumerate(self.tipos_risco.items()):
            ttk.Label(legenda_frame, text=f"{tipo['icon']} {tipo['label']}", 
                     font=('Arial', 10)).grid(row=i, column=0, sticky=tk.W, pady=2)
        
        # Intensidades
        ttk.Label(legenda_frame, text="Intensidade:", font=('Arial', 10, 'bold')).grid(
            row=len(self.tipos_risco), column=0, sticky=tk.W, pady=(10, 5))
        
        for i, (key, int_info) in enumerate(self.intensidades.items()):
            ttk.Label(legenda_frame, text=f"● {int_info['label']}", 
                     font=('Arial', 9)).grid(row=len(self.tipos_risco) + 1 + i, 
                                           column=0, sticky=tk.W, pady=1)
        
        # Lista de riscos
        self.riscos_frame = ttk.LabelFrame(sidebar_frame, text="Riscos Identificados", padding="10")
        self.riscos_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Treeview para lista de riscos
        self.tree = ttk.Treeview(self.riscos_frame, columns=('Tipo', 'Descrição', 'Intensidade'), 
                                show='tree headings', height=15)
        self.tree.heading('#0', text='#')
        self.tree.heading('Tipo', text='Tipo')
        self.tree.heading('Descrição', text='Descrição')
        self.tree.heading('Intensidade', text='Intensidade')
        
        self.tree.column('#0', width=30)
        self.tree.column('Tipo', width=80)
        self.tree.column('Descrição', width=150)
        self.tree.column('Intensidade', width=70)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar para a lista
        scrollbar = ttk.Scrollbar(self.riscos_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Botões para editar/excluir riscos
        btn_frame = ttk.Frame(self.riscos_frame)
        btn_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(btn_frame, text="Editar", command=self.editar_risco).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(btn_frame, text="Excluir", command=self.excluir_risco).grid(row=0, column=1)
        
        # Configurar redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Status inicial
        self.atualizar_status()
        
    def carregar_layout(self):
        file_path = filedialog.askopenfilename(
            title="Selecionar Layout",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp"), ("Todos", "*.*")]
        )
        
        if file_path:
            try:
                self.layout_image = Image.open(file_path)
                self.layout_image = self.layout_image.resize((self.canvas_width, self.canvas_height), 
                                                           Image.Resampling.LANCZOS)
                self.layout_photo = ImageTk.PhotoImage(self.layout_image)
                self.desenhar_mapa()
                messagebox.showinfo("Sucesso", "Layout carregado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar layout: {str(e)}")
    
    def toggle_add_mode(self):
        if self.mode == 'view':
            self.mode = 'add'
            self.btn_add.config(text="Cancelar Adição")
            self.canvas.config(cursor="cross")
            messagebox.showinfo("Modo Adição", "Clique no mapa para adicionar um risco")
        else:
            self.mode = 'view'
            self.btn_add.config(text="Adicionar Risco")
            self.canvas.config(cursor="")
    
    def canvas_click(self, event):
        if self.mode == 'add':
            x, y = event.x, event.y
            self.abrir_form_risco(x, y)
    
    def abrir_form_risco(self, x=0, y=0, risco_index=None):
        # Criar janela do formulário
        form_window = tk.Toplevel(self.root)
        form_window.title("Adicionar Risco" if risco_index is None else "Editar Risco")
        form_window.geometry("400x500")
        form_window.resizable(False, False)
        
        # Variáveis do formulário
        tipo_var = tk.StringVar()
        descricao_var = tk.StringVar()
        intensidade_var = tk.StringVar(value='baixa')
        medidas_var = tk.StringVar()
        
        # Se for edição, preencher com dados existentes
        if risco_index is not None:
            risco = self.riscos[risco_index]
            tipo_var.set(risco['tipo'])
            descricao_var.set(risco['descricao'])
            intensidade_var.set(risco['intensidade'])
            medidas_var.set(risco['medidas'])
            x, y = risco['x'], risco['y']
        
        # Campos do formulário
        ttk.Label(form_window, text="Tipo de Risco *", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, padx=10, pady=(10, 5))
        
        tipo_combo = ttk.Combobox(form_window, textvariable=tipo_var, width=30)
        tipo_combo['values'] = [self.tipos_risco[k]['label'] for k in self.tipos_risco.keys()]
        tipo_combo.grid(row=1, column=0, padx=10, pady=(0, 10), sticky=(tk.W, tk.E))
        
        ttk.Label(form_window, text="Descrição *", font=('Arial', 10, 'bold')).grid(
            row=2, column=0, sticky=tk.W, padx=10, pady=(0, 5))
        
        descricao_text = tk.Text(form_window, height=4, width=40)
        descricao_text.grid(row=3, column=0, padx=10, pady=(0, 10), sticky=(tk.W, tk.E))
        descricao_text.insert('1.0', descricao_var.get())
        
        ttk.Label(form_window, text="Intensidade", font=('Arial', 10, 'bold')).grid(
            row=4, column=0, sticky=tk.W, padx=10, pady=(0, 5))
        
        intensidade_combo = ttk.Combobox(form_window, textvariable=intensidade_var, width=30)
        intensidade_combo['values'] = [self.intensidades[k]['label'] for k in self.intensidades.keys()]
        intensidade_combo.grid(row=5, column=0, padx=10, pady=(0, 10), sticky=(tk.W, tk.E))
        
        ttk.Label(form_window, text="Medidas Preventivas", font=('Arial', 10, 'bold')).grid(
            row=6, column=0, sticky=tk.W, padx=10, pady=(0, 5))
        
        medidas_text = tk.Text(form_window, height=4, width=40)
        medidas_text.grid(row=7, column=0, padx=10, pady=(0, 10), sticky=(tk.W, tk.E))
        medidas_text.insert('1.0', medidas_var.get())
        
        # Botões
        btn_frame = ttk.Frame(form_window)
        btn_frame.grid(row=8, column=0, pady=20)
        
        def salvar():
            # Validação
            tipo_selecionado = tipo_var.get()
            descricao = descricao_text.get('1.0', tk.END).strip()
            
            if not tipo_selecionado or not descricao:
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
                return
            
            # Encontrar chave do tipo
            tipo_key = None
            for key, info in self.tipos_risco.items():
                if info['label'] == tipo_selecionado:
                    tipo_key = key
                    break
            
            # Encontrar chave da intensidade
            intensidade_key = None
            for key, info in self.intensidades.items():
                if info['label'] == intensidade_var.get():
                    intensidade_key = key
                    break
            
            # Criar dados do risco
            risco_data = {
                'tipo': tipo_key,
                'descricao': descricao,
                'intensidade': intensidade_key,
                'medidas': medidas_text.get('1.0', tk.END).strip(),
                'x': x,
                'y': y
            }
            
            # Salvar ou editar
            if risco_index is not None:
                self.riscos[risco_index] = risco_data
            else:
                self.riscos.append(risco_data)
            
            # Atualizar interface
            self.desenhar_mapa()
            self.atualizar_lista_riscos()
            self.toggle_add_mode()  # Voltar ao modo view
            form_window.destroy()
            
            messagebox.showinfo("Sucesso", "Risco salvo com sucesso!")
        
        ttk.Button(btn_frame, text="Salvar", command=salvar).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(btn_frame, text="Cancelar", command=form_window.destroy).grid(row=0, column=1)
        
        # Configurar redimensionamento
        form_window.columnconfigure(0, weight=1)
    
    def desenhar_mapa(self):
        self.canvas.delete("all")
        
        # Desenhar layout de fundo se existir
        if self.layout_photo:
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.layout_photo)
        
        # Desenhar riscos
        for i, risco in enumerate(self.riscos):
            tipo_info = self.tipos_risco[risco['tipo']]
            intensidade_info = self.intensidades[risco['intensidade']]
            
            # Desenhar círculo do risco
            x1 = risco['x'] - intensidade_info['tamanho']
            y1 = risco['y'] - intensidade_info['tamanho']
            x2 = risco['x'] + intensidade_info['tamanho']
            y2 = risco['y'] + intensidade_info['tamanho']
            
            self.canvas.create_oval(x1, y1, x2, y2, 
                                  fill=tipo_info['cor'], 
                                  outline=tipo_info['cor'], 
                                  width=2,
                                  stipple='gray50')
            
            # Desenhar número do risco
            self.canvas.create_text(risco['x'], risco['y'], 
                                  text=str(i + 1), 
                                  fill='white', 
                                  font=('Arial', 12, 'bold'))
    
    def atualizar_lista_riscos(self):
        # Limpar lista
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Adicionar riscos
        for i, risco in enumerate(self.riscos):
            tipo_label = self.tipos_risco[risco['tipo']]['label']
            intensidade_label = self.intensidades[risco['intensidade']]['label']
            
            self.tree.insert('', 'end', text=str(i + 1),
                           values=(tipo_label, risco['descricao'][:30] + '...' if len(risco['descricao']) > 30 else risco['descricao'], intensidade_label))
    
    def editar_risco(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um risco para editar")
            return
        
        item = self.tree.item(selected[0])
        risco_index = int(item['text']) - 1
        self.abrir_form_risco(risco_index=risco_index)
    
    def excluir_risco(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um risco para excluir")
            return
        
        if messagebox.askyesno("Confirmação", "Deseja excluir este risco?"):
            item = self.tree.item(selected[0])
            risco_index = int(item['text']) - 1
            del self.riscos[risco_index]
            self.desenhar_mapa()
            self.atualizar_lista_riscos()
            messagebox.showinfo("Sucesso", "Risco excluído com sucesso!")
    
    def salvar_projeto(self):
        file_path = filedialog.asksaveasfilename(
            title="Salvar Projeto",
            defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos", "*.*")]
        )
        
        if file_path:
            try:
                projeto = {
                    'riscos': self.riscos,
                    'data_criacao': datetime.now().isoformat(),
                    'versao': '1.0'
                }
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(projeto, f, ensure_ascii=False, indent=2)
                
                messagebox.showinfo("Sucesso", "Projeto salvo com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar projeto: {str(e)}")
    
    def carregar_projeto(self):
        file_path = filedialog.askopenfilename(
            title="Carregar Projeto",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    projeto = json.load(f)
                
                self.riscos = projeto.get('riscos', [])
                self.desenhar_mapa()
                self.atualizar_lista_riscos()
                
                messagebox.showinfo("Sucesso", "Projeto carregado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar projeto: {str(e)}")
    
    def exportar_mapa(self):
        if not self.layout_image:
            messagebox.showwarning("Aviso", "Carregue um layout primeiro")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Exportar Mapa",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("Todos", "*.*")]
        )
        
        if file_path:
            try:
                # Criar imagem com os riscos
                img = self.layout_image.copy()
                draw = ImageDraw.Draw(img)
                
                for i, risco in enumerate(self.riscos):
                    tipo_info = self.tipos_risco[risco['tipo']]
                    intensidade_info = self.intensidades[risco['intensidade']]
                    
                    # Desenhar círculo
                    x1 = risco['x'] - intensidade_info['tamanho']
                    y1 = risco['y'] - intensidade_info['tamanho']
                    x2 = risco['x'] + intensidade_info['tamanho']
                    y2 = risco['y'] + intensidade_info['tamanho']
                    
                    draw.ellipse([x1, y1, x2, y2], fill=tipo_info['cor'], outline=tipo_info['cor'], width=2)
                    
                    # Desenhar número
                    draw.text((risco['x'], risco['y']), str(i + 1), fill='white', anchor='mm')
                
                img.save(file_path)
                messagebox.showinfo("Sucesso", "Mapa exportado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar mapa: {str(e)}")
    
    def gerar_relatorio(self):
        if not self.riscos:
            messagebox.showwarning("Aviso", "Nenhum risco identificado")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Gerar Relatório",
            defaultextension=".txt",
            filetypes=[("Arquivo de Texto", "*.txt"), ("Todos", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("RELATÓRIO DO MAPA DE RISCOS AMBIENTAIS\n")
                    f.write("="*50 + "\n\n")
                    f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                    f.write(f"Total de Riscos Identificados: {len(self.riscos)}\n\n")
                    
                    for i, risco in enumerate(self.riscos):
                        tipo_label = self.tipos_risco[risco['tipo']]['label']
                        intensidade_label = self.intensidades[risco['intensidade']]['label']
                        
                        f.write(f"{i + 1}. {tipo_label.upper()}\n")
                        f.write(f"   Descrição: {risco['descricao']}\n")
                        f.write(f"   Intensidade: {intensidade_label}\n")
                        f.write(f"   Medidas Preventivas: {risco['medidas']}\n")
                        f.write(f"   Posição: X={risco['x']}, Y={risco['y']}\n\n")
                
                messagebox.showinfo("Sucesso", "Relatório gerado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")
    
    def atualizar_status(self):
        self.atualizar_lista_riscos()

def main():
    root = tk.Tk()
    app = MapaRiscosCIPA(root)
    root.mainloop()

if __name__ == "__main__":
    main()