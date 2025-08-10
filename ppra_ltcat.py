import tkinter as tk
from tkinter import ttk, messagebox, font

class PPRA_LTCAT:
    def __init__(self, root):
        self.root = root
        self.root.title("Programa Preventivo de Riscos Ambientais e LTCAT")
        self.root.geometry("950x700")
        
        # Configurar fonte padrão para tamanho 14 sem negrito
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(size=14, weight="normal")
        self.root.option_add("*Font", self.default_font)
        
        # Configurar fundo azul claro
        self.root.configure(bg='#E6F3FF')
        
        # Dados simulados com 10 registros cada
        self.empresas = [
            {"nome": "Empresa Alpha Ltda"},
            {"nome": "Empresa Beta S/A"},
            {"nome": "Empresa Gamma Indústria"},
            {"nome": "Empresa Delta Comércio"},
            {"nome": "Empresa Epsilon Serviços"},
            {"nome": "Empresa Zeta Tecnologia"},
            {"nome": "Empresa Eta Construção"},
            {"nome": "Empresa Theta Logística"},
            {"nome": "Empresa Iota Alimentos"},
            {"nome": "Empresa Kappa Saúde"}
        ]
        
        self.setores = [
            {"nome": "Administração", "empresa": "Empresa Alpha Ltda"},
            {"nome": "Produção", "empresa": "Empresa Alpha Ltda"},
            {"nome": "TI", "empresa": "Empresa Beta S/A"},
            {"nome": "RH", "empresa": "Empresa Beta S/A"},
            {"nome": "Contabilidade", "empresa": "Empresa Gamma Indústria"},
            {"nome": "Manutenção", "empresa": "Empresa Gamma Indústria"},
            {"nome": "Vendas", "empresa": "Empresa Delta Comércio"},
            {"nome": "Estoque", "empresa": "Empresa Delta Comércio"},
            {"nome": "Atendimento", "empresa": "Empresa Epsilon Serviços"},
            {"nome": "Qualidade", "empresa": "Empresa Epsilon Serviços"}
        ]
        
        self.cargos = [
            {"nome": "Gerente Administrativo", "setor": "Administração"},
            {"nome": "Assistente Administrativo", "setor": "Administração"},
            {"nome": "Operador de Máquina", "setor": "Produção"},
            {"nome": "Supervisor de Produção", "setor": "Produção"},
            {"nome": "Desenvolvedor Senior", "setor": "TI"},
            {"nome": "Analista de Sistemas", "setor": "TI"},
            {"nome": "Coordenador de RH", "setor": "RH"},
            {"nome": "Recrutador", "setor": "RH"},
            {"nome": "Contador", "setor": "Contabilidade"},
            {"nome": "Auxiliar de Contabilidade", "setor": "Contabilidade"}
        ]
        
        self.atividades = [
            {"descricao": "Gestão de equipe", "cargo": "Gerente Administrativo"},
            {"descricao": "Relatórios administrativos", "cargo": "Assistente Administrativo"},
            {"descricao": "Operação de máquinas industriais", "cargo": "Operador de Máquina"},
            {"descricao": "Supervisão de linha de produção", "cargo": "Supervisor de Produção"},
            {"descricao": "Desenvolvimento de software", "cargo": "Desenvolvedor Senior"},
            {"descricao": "Análise de requisitos", "cargo": "Analista de Sistemas"},
            {"descricao": "Gestão de pessoas", "cargo": "Coordenador de RH"},
            {"descricao": "Processos seletivos", "cargo": "Recrutador"},
            {"descricao": "Conciliação contábil", "cargo": "Contador"},
            {"descricao": "Lançamentos fiscais", "cargo": "Auxiliar de Contabilidade"}
        ]
        
        self.ambientes = [
            {"descricao": "Sala de reuniões", "atividade": "Gestão de equipe"},
            {"descricao": "Escritório administrativo", "atividade": "Relatórios administrativos"},
            {"descricao": "Linha de produção", "atividade": "Operação de máquinas industriais"},
            {"descricao": "Área de supervisão", "atividade": "Supervisão de linha de produção"},
            {"descricao": "Estação de desenvolvimento", "atividade": "Desenvolvimento de software"},
            {"descricao": "Sala de reuniões técnicas", "atividade": "Análise de requisitos"},
            {"descricao": "Departamento de RH", "atividade": "Gestão de pessoas"},
            {"descricao": "Sala de entrevista", "atividade": "Processos seletivos"},
            {"descricao": "Setor contábil", "atividade": "Conciliação contábil"},
            {"descricao": "Departamento fiscal", "atividade": "Lançamentos fiscais"}
        ]
        
        # Índices atuais
        self.empresa_idx = 0
        self.setor_idx = 0
        self.cargo_idx = 0
        self.atividade_idx = 0
        self.ambiente_idx = 0
        
        # Referências para os botões de navegação
        self.nav_empresa_primeiro_btn = None
        self.nav_empresa_anterior_btn = None
        self.nav_empresa_proximo_btn = None
        self.nav_empresa_ultimo_btn = None
        self.empresa_novo_btn = None
        self.empresa_salvar_btn = None
        self.empresa_editar_btn = None
        self.empresa_excluir_btn = None
        
        self.nav_setor_primeiro_btn = None
        self.nav_setor_anterior_btn = None
        self.nav_setor_proximo_btn = None
        self.nav_setor_ultimo_btn = None
        self.setor_novo_btn = None
        self.setor_salvar_btn = None
        self.setor_editar_btn = None
        self.setor_excluir_btn = None
        
        self.nav_cargo_primeiro_btn = None
        self.nav_cargo_anterior_btn = None
        self.nav_cargo_proximo_btn = None
        self.nav_cargo_ultimo_btn = None
        self.cargo_novo_btn = None
        self.cargo_salvar_btn = None
        self.cargo_editar_btn = None
        self.cargo_excluir_btn = None
        
        self.atividade_novo_btn = None
        self.atividade_salvar_btn = None
        self.atividade_editar_btn = None
        self.atividade_excluir_btn = None
        
        self.ambiente_novo_btn = None
        self.ambiente_salvar_btn = None
        self.ambiente_editar_btn = None
        self.ambiente_excluir_btn = None
        
        self.create_widgets()
        self.mostrar_empresa()
        
    def create_widgets(self):
        # Frame principal com fundo azul claro
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.configure(style='Blue.TFrame')
        
        # Configurar estilo para frames com fundo azul claro
        style = ttk.Style()
        style.configure('Blue.TFrame', background='#E6F3FF')
        style.configure('Blue.TLabelframe', background='#E6F3FF')
        style.configure('Blue.TLabelframe.Label', background='#E6F3FF', font=('TkDefaultFont', 15, 'bold'), foreground='#FFA500')
        style.configure('Blue.TLabel', background='#E6F3FF', font=('TkDefaultFont', 14, 'normal'))
        style.configure('Blue.TButton', font=('TkDefaultFont', 12, 'normal'))
        
        # Frame Empresa
        empresa_frame = ttk.LabelFrame(main_frame, text="Empresa", padding="10", style='Blue.TLabelframe')
        empresa_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(empresa_frame, text="Nome:", style='Blue.TLabel').grid(row=0, column=0, sticky=tk.W)
        self.empresa_entry = ttk.Entry(empresa_frame, width=50, font=('TkDefaultFont', 14, 'normal'))
        self.empresa_entry.grid(row=0, column=1, padx=5)
        
        # Navegação Empresa
        nav_empresa_frame = ttk.Frame(empresa_frame, style='Blue.TFrame')
        nav_empresa_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        self.nav_empresa_primeiro_btn = ttk.Button(nav_empresa_frame, text="⏮️", command=self.nav_empresa_primeiro, width=3, style='Blue.TButton')
        self.nav_empresa_primeiro_btn.pack(side=tk.LEFT, padx=2)
        
        self.nav_empresa_anterior_btn = ttk.Button(nav_empresa_frame, text="◀️", command=self.nav_empresa_anterior, width=3, style='Blue.TButton')
        self.nav_empresa_anterior_btn.pack(side=tk.LEFT, padx=2)
        
        self.nav_empresa_proximo_btn = ttk.Button(nav_empresa_frame, text="▶️", command=self.nav_empresa_proximo, width=3, style='Blue.TButton')
        self.nav_empresa_proximo_btn.pack(side=tk.LEFT, padx=2)
        
        self.nav_empresa_ultimo_btn = ttk.Button(nav_empresa_frame, text="⏭️", command=self.nav_empresa_ultimo, width=3, style='Blue.TButton')
        self.nav_empresa_ultimo_btn.pack(side=tk.LEFT, padx=2)
        
        # Separador entre navegação e ações
        ttk.Separator(nav_empresa_frame, orient='vertical').pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        self.empresa_novo_btn = ttk.Button(nav_empresa_frame, text="✨", command=self.nova_empresa, width=3, style='Blue.TButton')
        self.empresa_novo_btn.pack(side=tk.LEFT, padx=2)
        
        self.empresa_salvar_btn = ttk.Button(nav_empresa_frame, text="💾", command=self.salvar_empresa, width=3, style='Blue.TButton')
        self.empresa_salvar_btn.pack(side=tk.LEFT, padx=2)
        
        self.empresa_editar_btn = ttk.Button(nav_empresa_frame, text="✏️", command=self.editar_empresa, width=3, style='Blue.TButton')
        self.empresa_editar_btn.pack(side=tk.LEFT, padx=2)
        
        self.empresa_excluir_btn = ttk.Button(nav_empresa_frame, text="🗑️", command=self.excluir_empresa, width=3, style='Blue.TButton')
        self.empresa_excluir_btn.pack(side=tk.LEFT, padx=2)
        
        # Frame Setor
        setor_frame = ttk.LabelFrame(main_frame, text="Setor", padding="10", style='Blue.TLabelframe')
        setor_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(setor_frame, text="Nome:", style='Blue.TLabel').grid(row=0, column=0, sticky=tk.W)
        self.setor_entry = ttk.Entry(setor_frame, width=50, font=('TkDefaultFont', 14, 'normal'))
        self.setor_entry.grid(row=0, column=1, padx=5)
        
        # Navegação Setor
        nav_setor_frame = ttk.Frame(setor_frame, style='Blue.TFrame')
        nav_setor_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        self.nav_setor_primeiro_btn = ttk.Button(nav_setor_frame, text="⏮️", command=self.nav_setor_primeiro, width=3, style='Blue.TButton')
        self.nav_setor_primeiro_btn.pack(side=tk.LEFT, padx=2)
        
        self.nav_setor_anterior_btn = ttk.Button(nav_setor_frame, text="◀️", command=self.nav_setor_anterior, width=3, style='Blue.TButton')
        self.nav_setor_anterior_btn.pack(side=tk.LEFT, padx=2)
        
        self.nav_setor_proximo_btn = ttk.Button(nav_setor_frame, text="▶️", command=self.nav_setor_proximo, width=3, style='Blue.TButton')
        self.nav_setor_proximo_btn.pack(side=tk.LEFT, padx=2)
        
        self.nav_setor_ultimo_btn = ttk.Button(nav_setor_frame, text="⏭️", command=self.nav_setor_ultimo, width=3, style='Blue.TButton')
        self.nav_setor_ultimo_btn.pack(side=tk.LEFT, padx=2)
        
        # Separador entre navegação e ações
        ttk.Separator(nav_setor_frame, orient='vertical').pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        self.setor_novo_btn = ttk.Button(nav_setor_frame, text="✨", command=self.novo_setor, width=3, style='Blue.TButton')
        self.setor_novo_btn.pack(side=tk.LEFT, padx=2)
        
        self.setor_salvar_btn = ttk.Button(nav_setor_frame, text="💾", command=self.salvar_setor, width=3, style='Blue.TButton')
        self.setor_salvar_btn.pack(side=tk.LEFT, padx=2)
        
        self.setor_editar_btn = ttk.Button(nav_setor_frame, text="✏️", command=self.editar_setor, width=3, style='Blue.TButton')
        self.setor_editar_btn.pack(side=tk.LEFT, padx=2)
        
        self.setor_excluir_btn = ttk.Button(nav_setor_frame, text="🗑️", command=self.excluir_setor, width=3, style='Blue.TButton')
        self.setor_excluir_btn.pack(side=tk.LEFT, padx=2)
        
        # Frame Cargo
        cargo_frame = ttk.LabelFrame(main_frame, text="Cargo", padding="10", style='Blue.TLabelframe')
        cargo_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(cargo_frame, text="Nome:", style='Blue.TLabel').grid(row=0, column=0, sticky=tk.W)
        self.cargo_entry = ttk.Entry(cargo_frame, width=50, font=('TkDefaultFont', 14, 'normal'))
        self.cargo_entry.grid(row=0, column=1, padx=5)
        
        # Navegação Cargo
        nav_cargo_frame = ttk.Frame(cargo_frame, style='Blue.TFrame')
        nav_cargo_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        self.nav_cargo_primeiro_btn = ttk.Button(nav_cargo_frame, text="⏮️", command=self.nav_cargo_primeiro, width=3, style='Blue.TButton')
        self.nav_cargo_primeiro_btn.pack(side=tk.LEFT, padx=2)
        
        self.nav_cargo_anterior_btn = ttk.Button(nav_cargo_frame, text="◀️", command=self.nav_cargo_anterior, width=3, style='Blue.TButton')
        self.nav_cargo_anterior_btn.pack(side=tk.LEFT, padx=2)
        
        self.nav_cargo_proximo_btn = ttk.Button(nav_cargo_frame, text="▶️", command=self.nav_cargo_proximo, width=3, style='Blue.TButton')
        self.nav_cargo_proximo_btn.pack(side=tk.LEFT, padx=2)
        
        self.nav_cargo_ultimo_btn = ttk.Button(nav_cargo_frame, text="⏭️", command=self.nav_cargo_ultimo, width=3, style='Blue.TButton')
        self.nav_cargo_ultimo_btn.pack(side=tk.LEFT, padx=2)
        
        # Separador entre navegação e ações
        ttk.Separator(nav_cargo_frame, orient='vertical').pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        self.cargo_novo_btn = ttk.Button(nav_cargo_frame, text="✨", command=self.novo_cargo, width=3, style='Blue.TButton')
        self.cargo_novo_btn.pack(side=tk.LEFT, padx=2)
        
        self.cargo_salvar_btn = ttk.Button(nav_cargo_frame, text="💾", command=self.salvar_cargo, width=3, style='Blue.TButton')
        self.cargo_salvar_btn.pack(side=tk.LEFT, padx=2)
        
        self.cargo_editar_btn = ttk.Button(nav_cargo_frame, text="✏️", command=self.editar_cargo, width=3, style='Blue.TButton')
        self.cargo_editar_btn.pack(side=tk.LEFT, padx=2)
        
        self.cargo_excluir_btn = ttk.Button(nav_cargo_frame, text="🗑️", command=self.excluir_cargo, width=3, style='Blue.TButton')
        self.cargo_excluir_btn.pack(side=tk.LEFT, padx=2)
        
        # Frame Atividade
        atividade_frame = ttk.LabelFrame(main_frame, text="Atividade", padding="10", style='Blue.TLabelframe')
        atividade_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(atividade_frame, text="Descrição:", style='Blue.TLabel').grid(row=0, column=0, sticky=tk.W)
        self.atividade_entry = ttk.Entry(atividade_frame, width=50, font=('TkDefaultFont', 14, 'normal'))
        self.atividade_entry.grid(row=0, column=1, padx=5)
        
        # Botões Atividade
        nav_atividade_frame = ttk.Frame(atividade_frame, style='Blue.TFrame')
        nav_atividade_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        self.atividade_novo_btn = ttk.Button(nav_atividade_frame, text="✨", command=self.nova_atividade, width=3, style='Blue.TButton')
        self.atividade_novo_btn.pack(side=tk.LEFT, padx=2)
        
        self.atividade_salvar_btn = ttk.Button(nav_atividade_frame, text="💾", command=self.salvar_atividade, width=3, style='Blue.TButton')
        self.atividade_salvar_btn.pack(side=tk.LEFT, padx=2)
        
        self.atividade_editar_btn = ttk.Button(nav_atividade_frame, text="✏️", command=self.editar_atividade, width=3, style='Blue.TButton')
        self.atividade_editar_btn.pack(side=tk.LEFT, padx=2)
        
        self.atividade_excluir_btn = ttk.Button(nav_atividade_frame, text="🗑️", command=self.excluir_atividade, width=3, style='Blue.TButton')
        self.atividade_excluir_btn.pack(side=tk.LEFT, padx=2)
        
        # Frame Ambiente
        ambiente_frame = ttk.LabelFrame(main_frame, text="Ambiente Laborativo", padding="10", style='Blue.TLabelframe')
        ambiente_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(ambiente_frame, text="Descrição:", style='Blue.TLabel').grid(row=0, column=0, sticky=tk.W)
        self.ambiente_entry = ttk.Entry(ambiente_frame, width=50, font=('TkDefaultFont', 14, 'normal'))
        self.ambiente_entry.grid(row=0, column=1, padx=5)
        
        # Botões Ambiente
        nav_ambiente_frame = ttk.Frame(ambiente_frame, style='Blue.TFrame')
        nav_ambiente_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        self.ambiente_novo_btn = ttk.Button(nav_ambiente_frame, text="✨", command=self.novo_ambiente, width=3, style='Blue.TButton')
        self.ambiente_novo_btn.pack(side=tk.LEFT, padx=2)
        
        self.ambiente_salvar_btn = ttk.Button(nav_ambiente_frame, text="💾", command=self.salvar_ambiente, width=3, style='Blue.TButton')
        self.ambiente_salvar_btn.pack(side=tk.LEFT, padx=2)
        
        self.ambiente_editar_btn = ttk.Button(nav_ambiente_frame, text="✏️", command=self.editar_ambiente, width=3, style='Blue.TButton')
        self.ambiente_editar_btn.pack(side=tk.LEFT, padx=2)
        
        self.ambiente_excluir_btn = ttk.Button(nav_ambiente_frame, text="🗑️", command=self.excluir_ambiente, width=3, style='Blue.TButton')
        self.ambiente_excluir_btn.pack(side=tk.LEFT, padx=2)
        
        # Status Bar com fundo azul claro
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, style='Blue.TLabel')
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    # Métodos de navegação - Empresa
    def nav_empresa_primeiro(self):
        if self.empresas:
            self.empresa_idx = 0
            self.mostrar_empresa()
    
    def nav_empresa_anterior(self):
        if self.empresa_idx > 0:
            self.empresa_idx -= 1
            self.mostrar_empresa()
    
    def nav_empresa_proximo(self):
        if self.empresa_idx < len(self.empresas) - 1:
            self.empresa_idx += 1
            self.mostrar_empresa()
    
    def nav_empresa_ultimo(self):
        if self.empresas:
            self.empresa_idx = len(self.empresas) - 1
            self.mostrar_empresa()
    
    # Métodos de navegação - Setor
    def nav_setor_primeiro(self):
        setores_empresa = self.get_setores_empresa()
        if setores_empresa:
            self.setor_idx = 0
            self.mostrar_setor()
    
    def nav_setor_anterior(self):
        setores_empresa = self.get_setores_empresa()
        if self.setor_idx > 0 and setores_empresa:
            self.setor_idx -= 1
            self.mostrar_setor()
    
    def nav_setor_proximo(self):
        setores_empresa = self.get_setores_empresa()
        if setores_empresa and self.setor_idx < len(setores_empresa) - 1:
            self.setor_idx += 1
            self.mostrar_setor()
    
    def nav_setor_ultimo(self):
        setores_empresa = self.get_setores_empresa()
        if setores_empresa:
            self.setor_idx = len(setores_empresa) - 1
            self.mostrar_setor()
    
    # Métodos de navegação - Cargo
    def nav_cargo_primeiro(self):
        cargos_setor = self.get_cargos_setor()
        if cargos_setor:
            self.cargo_idx = 0
            self.mostrar_cargo()
    
    def nav_cargo_anterior(self):
        cargos_setor = self.get_cargos_setor()
        if self.cargo_idx > 0 and cargos_setor:
            self.cargo_idx -= 1
            self.mostrar_cargo()
    
    def nav_cargo_proximo(self):
        cargos_setor = self.get_cargos_setor()
        if cargos_setor and self.cargo_idx < len(cargos_setor) - 1:
            self.cargo_idx += 1
            self.mostrar_cargo()
    
    def nav_cargo_ultimo(self):
        cargos_setor = self.get_cargos_setor()
        if cargos_setor:
            self.cargo_idx = len(cargos_setor) - 1
            self.mostrar_cargo()
    
    # Métodos auxiliares para obter registros filtrados
    def get_setores_empresa(self):
        if self.empresa_idx >= 0:
            empresa_atual = self.empresas[self.empresa_idx]["nome"]
            return [s for s in self.setores if s["empresa"] == empresa_atual]
        return []
    
    def get_cargos_setor(self):
        setores_empresa = self.get_setores_empresa()
        if setores_empresa and self.setor_idx >= 0 and self.setor_idx < len(setores_empresa):
            setor_atual = setores_empresa[self.setor_idx]["nome"]
            return [c for c in self.cargos if c["setor"] == setor_atual]
        return []
    
    def get_atividades_cargo(self):
        cargos_setor = self.get_cargos_setor()
        if cargos_setor and self.cargo_idx >= 0 and self.cargo_idx < len(cargos_setor):
            cargo_atual = cargos_setor[self.cargo_idx]["nome"]
            return [a for a in self.atividades if a["cargo"] == cargo_atual]
        return []
    
    def get_ambientes_atividade(self):
        atividades_cargo = self.get_atividades_cargo()
        if atividades_cargo and self.atividade_idx >= 0 and self.atividade_idx < len(atividades_cargo):
            atividade_atual = atividades_cargo[self.atividade_idx]["descricao"]
            return [a for a in self.ambientes if a["atividade"] == atividade_atual]
        return []
    
    # Métodos de cadastro
    def nova_empresa(self):
        self.empresa_entry.delete(0, tk.END)
        self.empresa_idx = -1
        self.update_navigation_buttons()
        self.status_var.set("Nova empresa - Preencha os dados")
    
    def salvar_empresa(self):
        nome = self.empresa_entry.get().strip()
        if not nome:
            messagebox.showerror("Erro", "Nome da empresa é obrigatório")
            return
            
        if self.empresa_idx == -1:
            self.empresas.append({"nome": nome})
            self.empresa_idx = len(self.empresas) - 1
            self.status_var.set(f"Empresa '{nome}' cadastrada com sucesso")
        else:
            self.empresas[self.empresa_idx]["nome"] = nome
            self.status_var.set(f"Empresa '{nome}' atualizada com sucesso")
        
        self.mostrar_empresa()
    
    def novo_setor(self):
        if self.empresa_idx == -1:
            messagebox.showerror("Erro", "Selecione uma empresa primeiro")
            return
            
        self.setor_entry.delete(0, tk.END)
        self.setor_idx = -1
        self.update_navigation_buttons()
        self.status_var.set("Novo setor - Preencha os dados")
    
    def salvar_setor(self):
        if self.empresa_idx == -1:
            messagebox.showerror("Erro", "Selecione uma empresa primeiro")
            return
            
        nome = self.setor_entry.get().strip()
        if not nome:
            messagebox.showerror("Erro", "Nome do setor é obrigatório")
            return
            
        empresa = self.empresas[self.empresa_idx]["nome"]
        
        if self.setor_idx == -1:
            self.setores.append({
                "nome": nome,
                "empresa": empresa
            })
            self.setor_idx = len(self.get_setores_empresa()) - 1
            self.status_var.set(f"Setor '{nome}' cadastrado com sucesso")
        else:
            setores_empresa = self.get_setores_empresa()
            if self.setor_idx < len(setores_empresa):
                # Encontrar o índice original do setor
                setor_nome = setores_empresa[self.setor_idx]["nome"]
                for i, s in enumerate(self.setores):
                    if s["nome"] == setor_nome and s["empresa"] == empresa:
                        self.setores[i]["nome"] = nome
                        break
                self.status_var.set(f"Setor '{nome}' atualizado com sucesso")
        
        self.mostrar_setor()
    
    def novo_cargo(self):
        if self.empresa_idx == -1 or self.setor_idx == -1:
            messagebox.showerror("Erro", "Selecione uma empresa e um setor primeiro")
            return
            
        self.cargo_entry.delete(0, tk.END)
        self.cargo_idx = -1
        self.update_navigation_buttons()
        self.status_var.set("Novo cargo - Preencha os dados")
    
    def salvar_cargo(self):
        if self.empresa_idx == -1 or self.setor_idx == -1:
            messagebox.showerror("Erro", "Selecione uma empresa e um setor primeiro")
            return
            
        nome = self.cargo_entry.get().strip()
        if not nome:
            messagebox.showerror("Erro", "Nome do cargo é obrigatório")
            return
            
        setores_empresa = self.get_setores_empresa()
        if self.setor_idx < 0 or self.setor_idx >= len(setores_empresa):
            messagebox.showerror("Erro", "Setor inválido")
            return
            
        setor = setores_empresa[self.setor_idx]["nome"]
        
        if self.cargo_idx == -1:
            self.cargos.append({
                "nome": nome,
                "setor": setor
            })
            self.cargo_idx = len(self.get_cargos_setor()) - 1
            self.status_var.set(f"Cargo '{nome}' cadastrado com sucesso")
        else:
            cargos_setor = self.get_cargos_setor()
            if self.cargo_idx < len(cargos_setor):
                # Encontrar o índice original do cargo
                cargo_nome = cargos_setor[self.cargo_idx]["nome"]
                for i, c in enumerate(self.cargos):
                    if c["nome"] == cargo_nome and c["setor"] == setor:
                        self.cargos[i]["nome"] = nome
                        break
                self.status_var.set(f"Cargo '{nome}' atualizado com sucesso")
        
        self.mostrar_cargo()
    
    def nova_atividade(self):
        if self.empresa_idx == -1 or self.setor_idx == -1 or self.cargo_idx == -1:
            messagebox.showerror("Erro", "Selecione uma empresa, setor e cargo primeiro")
            return
            
        self.atividade_entry.delete(0, tk.END)
        self.atividade_idx = -1
        self.status_var.set("Nova atividade - Preencha os dados")
    
    def salvar_atividade(self):
        if self.empresa_idx == -1 or self.setor_idx == -1 or self.cargo_idx == -1:
            messagebox.showerror("Erro", "Selecione uma empresa, setor e cargo primeiro")
            return
            
        descricao = self.atividade_entry.get().strip()
        if not descricao:
            messagebox.showerror("Erro", "Descrição da atividade é obrigatória")
            return
            
        cargos_setor = self.get_cargos_setor()
        if self.cargo_idx < 0 or self.cargo_idx >= len(cargos_setor):
            messagebox.showerror("Erro", "Cargo inválido")
            return
            
        cargo = cargos_setor[self.cargo_idx]["nome"]
        
        if self.atividade_idx == -1:
            self.atividades.append({
                "descricao": descricao,
                "cargo": cargo
            })
            self.atividade_idx = len(self.get_atividades_cargo()) - 1
            self.status_var.set(f"Atividade '{descricao}' cadastrada com sucesso")
        else:
            atividades_cargo = self.get_atividades_cargo()
            if self.atividade_idx < len(atividades_cargo):
                # Encontrar o índice original da atividade
                atividade_desc = atividades_cargo[self.atividade_idx]["descricao"]
                for i, a in enumerate(self.atividades):
                    if a["descricao"] == atividade_desc and a["cargo"] == cargo:
                        self.atividades[i]["descricao"] = descricao
                        break
                self.status_var.set(f"Atividade '{descricao}' atualizada com sucesso")
        
        self.mostrar_atividade()
    
    def novo_ambiente(self):
        if self.empresa_idx == -1 or self.setor_idx == -1 or self.cargo_idx == -1 or self.atividade_idx == -1:
            messagebox.showerror("Erro", "Selecione uma empresa, setor, cargo e atividade primeiro")
            return
            
        self.ambiente_entry.delete(0, tk.END)
        self.ambiente_idx = -1
        self.status_var.set("Novo ambiente - Preencha os dados")
    
    def salvar_ambiente(self):
        if self.empresa_idx == -1 or self.setor_idx == -1 or self.cargo_idx == -1 or self.atividade_idx == -1:
            messagebox.showerror("Erro", "Selecione uma empresa, setor, cargo e atividade primeiro")
            return
            
        descricao = self.ambiente_entry.get().strip()
        if not descricao:
            messagebox.showerror("Erro", "Descrição do ambiente é obrigatória")
            return
            
        atividades_cargo = self.get_atividades_cargo()
        if self.atividade_idx < 0 or self.atividade_idx >= len(atividades_cargo):
            messagebox.showerror("Erro", "Atividade inválida")
            return
            
        atividade = atividades_cargo[self.atividade_idx]["descricao"]
        
        if self.ambiente_idx == -1:
            self.ambientes.append({
                "descricao": descricao,
                "atividade": atividade
            })
            self.ambiente_idx = len(self.get_ambientes_atividade()) - 1
            self.status_var.set(f"Ambiente '{descricao}' cadastrado com sucesso")
        else:
            ambientes_atividade = self.get_ambientes_atividade()
            if self.ambiente_idx < len(ambientes_atividade):
                # Encontrar o índice original do ambiente
                ambiente_desc = ambientes_atividade[self.ambiente_idx]["descricao"]
                for i, a in enumerate(self.ambientes):
                    if a["descricao"] == ambiente_desc and a["atividade"] == atividade:
                        self.ambientes[i]["descricao"] = descricao
                        break
                self.status_var.set(f"Ambiente '{descricao}' atualizado com sucesso")
        
        self.mostrar_ambiente()
    
    # Métodos de edição
    def editar_empresa(self):
        if self.empresa_idx >= 0:
            self.empresa_entry.config(state='normal')
            self.status_var.set(f"Editando empresa: {self.empresas[self.empresa_idx]['nome']}")
    
    def editar_setor(self):
        if self.setor_idx >= 0:
            setores_empresa = self.get_setores_empresa()
            if self.setor_idx < len(setores_empresa):
                self.setor_entry.config(state='normal')
                self.status_var.set(f"Editando setor: {setores_empresa[self.setor_idx]['nome']}")
    
    def editar_cargo(self):
        if self.cargo_idx >= 0:
            cargos_setor = self.get_cargos_setor()
            if self.cargo_idx < len(cargos_setor):
                self.cargo_entry.config(state='normal')
                self.status_var.set(f"Editando cargo: {cargos_setor[self.cargo_idx]['nome']}")
    
    def editar_atividade(self):
        if self.atividade_idx >= 0:
            atividades_cargo = self.get_atividades_cargo()
            if self.atividade_idx < len(atividades_cargo):
                self.atividade_entry.config(state='normal')
                self.status_var.set(f"Editando atividade: {atividades_cargo[self.atividade_idx]['descricao']}")
    
    def editar_ambiente(self):
        if self.ambiente_idx >= 0:
            ambientes_atividade = self.get_ambientes_atividade()
            if self.ambiente_idx < len(ambientes_atividade):
                self.ambiente_entry.config(state='normal')
                self.status_var.set(f"Editando ambiente: {ambientes_atividade[self.ambiente_idx]['descricao']}")
    
    # Métodos de exclusão
    def excluir_empresa(self):
        if self.empresa_idx >= 0:
            empresa = self.empresas[self.empresa_idx]["nome"]
            if messagebox.askyesno("Confirmar Exclusão", f"Deseja excluir a empresa '{empresa}' e todos os dados relacionados?"):
                del self.empresas[self.empresa_idx]
                
                # Excluir setores, cargos, atividades e ambientes relacionados
                self.setores = [s for s in self.setores if s["empresa"] != empresa]
                
                if self.empresas:
                    self.empresa_idx = min(self.empresa_idx, len(self.empresas) - 1)
                    self.mostrar_empresa()
                else:
                    self.empresa_idx = -1
                    self.empresa_entry.delete(0, tk.END)
                    self.setor_idx = -1
                    self.setor_entry.delete(0, tk.END)
                    self.cargo_idx = -1
                    self.cargo_entry.delete(0, tk.END)
                    self.atividade_idx = -1
                    self.atividade_entry.delete(0, tk.END)
                    self.ambiente_idx = -1
                    self.ambiente_entry.delete(0, tk.END)
                    self.update_navigation_buttons()
                
                self.status_var.set(f"Empresa '{empresa}' excluída com sucesso")
    
    def excluir_setor(self):
        if self.setor_idx >= 0:
            setores_empresa = self.get_setores_empresa()
            if self.setor_idx < len(setores_empresa):
                setor = setores_empresa[self.setor_idx]["nome"]
                if messagebox.askyesno("Confirmar Exclusão", f"Deseja excluir o setor '{setor}' e todos os dados relacionados?"):
                    # Encontrar e excluir o setor na lista original
                    empresa = self.empresas[self.empresa_idx]["nome"]
                    self.setores = [s for s in self.setores if not (s["nome"] == setor and s["empresa"] == empresa)]
                    
                    # Excluir cargos, atividades e ambientes relacionados
                    self.cargos = [c for c in self.cargos if c["setor"] != setor]
                    
                    if self.get_setores_empresa():
                        self.setor_idx = min(self.setor_idx, len(self.get_setores_empresa()) - 1)
                        self.mostrar_setor()
                    else:
                        self.setor_idx = -1
                        self.setor_entry.delete(0, tk.END)
                        self.cargo_idx = -1
                        self.cargo_entry.delete(0, tk.END)
                        self.atividade_idx = -1
                        self.atividade_entry.delete(0, tk.END)
                        self.ambiente_idx = -1
                        self.ambiente_entry.delete(0, tk.END)
                        self.update_navigation_buttons()
                    
                    self.status_var.set(f"Setor '{setor}' excluído com sucesso")
    
    def excluir_cargo(self):
        if self.cargo_idx >= 0:
            cargos_setor = self.get_cargos_setor()
            if self.cargo_idx < len(cargos_setor):
                cargo = cargos_setor[self.cargo_idx]["nome"]
                if messagebox.askyesno("Confirmar Exclusão", f"Deseja excluir o cargo '{cargo}' e todos os dados relacionados?"):
                    # Encontrar e excluir o cargo na lista original
                    setores_empresa = self.get_setores_empresa()
                    setor = setores_empresa[self.setor_idx]["nome"]
                    self.cargos = [c for c in self.cargos if not (c["nome"] == cargo and c["setor"] == setor)]
                    
                    # Excluir atividades e ambientes relacionados
                    self.atividades = [a for a in self.atividades if a["cargo"] != cargo]
                    
                    if self.get_cargos_setor():
                        self.cargo_idx = min(self.cargo_idx, len(self.get_cargos_setor()) - 1)
                        self.mostrar_cargo()
                    else:
                        self.cargo_idx = -1
                        self.cargo_entry.delete(0, tk.END)
                        self.atividade_idx = -1
                        self.atividade_entry.delete(0, tk.END)
                        self.ambiente_idx = -1
                        self.ambiente_entry.delete(0, tk.END)
                        self.update_navigation_buttons()
                    
                    self.status_var.set(f"Cargo '{cargo}' excluído com sucesso")
    
    def excluir_atividade(self):
        if self.atividade_idx >= 0:
            atividades_cargo = self.get_atividades_cargo()
            if self.atividade_idx < len(atividades_cargo):
                atividade = atividades_cargo[self.atividade_idx]["descricao"]
                if messagebox.askyesno("Confirmar Exclusão", f"Deseja excluir a atividade '{atividade}' e todos os dados relacionados?"):
                    # Encontrar e excluir a atividade na lista original
                    cargos_setor = self.get_cargos_setor()
                    cargo = cargos_setor[self.cargo_idx]["nome"]
                    self.atividades = [a for a in self.atividades if not (a["descricao"] == atividade and a["cargo"] == cargo)]
                    
                    # Excluir ambientes relacionados
                    self.ambientes = [a for a in self.ambientes if a["atividade"] != atividade]
                    
                    if self.get_atividades_cargo():
                        self.atividade_idx = min(self.atividade_idx, len(self.get_atividades_cargo()) - 1)
                        self.mostrar_atividade()
                    else:
                        self.atividade_idx = -1
                        self.atividade_entry.delete(0, tk.END)
                        self.ambiente_idx = -1
                        self.ambiente_entry.delete(0, tk.END)
                        self.update_navigation_buttons()
                    
                    self.status_var.set(f"Atividade '{atividade}' excluída com sucesso")
    
    def excluir_ambiente(self):
        if self.ambiente_idx >= 0:
            ambientes_atividade = self.get_ambientes_atividade()
            if self.ambiente_idx < len(ambientes_atividade):
                ambiente = ambientes_atividade[self.ambiente_idx]["descricao"]
                if messagebox.askyesno("Confirmar Exclusão", f"Deseja excluir o ambiente '{ambiente}'?"):
                    # Encontrar e excluir o ambiente na lista original
                    atividades_cargo = self.get_atividades_cargo()
                    atividade = atividades_cargo[self.atividade_idx]["descricao"]
                    self.ambientes = [a for a in self.ambientes if not (a["descricao"] == ambiente and a["atividade"] == atividade)]
                    
                    if self.get_ambientes_atividade():
                        self.ambiente_idx = min(self.ambiente_idx, len(self.get_ambientes_atividade()) - 1)
                        self.mostrar_ambiente()
                    else:
                        self.ambiente_idx = -1
                        self.ambiente_entry.delete(0, tk.END)
                        self.update_navigation_buttons()
                    
                    self.status_var.set(f"Ambiente '{ambiente}' excluído com sucesso")
    
    # Métodos de exibição
    def mostrar_empresa(self):
        if self.empresa_idx >= 0 and self.empresa_idx < len(self.empresas):
            self.empresa_entry.delete(0, tk.END)
            self.empresa_entry.insert(0, self.empresas[self.empresa_idx]["nome"])
            self.mostrar_setor()
            self.update_navigation_buttons()
    
    def mostrar_setor(self):
        setores_empresa = self.get_setores_empresa()
        if setores_empresa and self.setor_idx >= 0 and self.setor_idx < len(setores_empresa):
            self.setor_entry.delete(0, tk.END)
            self.setor_entry.insert(0, setores_empresa[self.setor_idx]["nome"])
            self.mostrar_cargo()
        else:
            self.setor_entry.delete(0, tk.END)
            self.cargo_entry.delete(0, tk.END)
            self.atividade_entry.delete(0, tk.END)
            self.ambiente_entry.delete(0, tk.END)
            self.cargo_idx = -1
            self.atividade_idx = -1
            self.ambiente_idx = -1
        self.update_navigation_buttons()
    
    def mostrar_cargo(self):
        cargos_setor = self.get_cargos_setor()
        if cargos_setor and self.cargo_idx >= 0 and self.cargo_idx < len(cargos_setor):
            self.cargo_entry.delete(0, tk.END)
            self.cargo_entry.insert(0, cargos_setor[self.cargo_idx]["nome"])
            self.mostrar_atividade()
        else:
            self.cargo_entry.delete(0, tk.END)
            self.atividade_entry.delete(0, tk.END)
            self.ambiente_entry.delete(0, tk.END)
            self.atividade_idx = -1
            self.ambiente_idx = -1
        self.update_navigation_buttons()
    
    def mostrar_atividade(self):
        atividades_cargo = self.get_atividades_cargo()
        if atividades_cargo and self.atividade_idx >= 0 and self.atividade_idx < len(atividades_cargo):
            self.atividade_entry.delete(0, tk.END)
            self.atividade_entry.insert(0, atividades_cargo[self.atividade_idx]["descricao"])
            self.mostrar_ambiente()
        else:
            self.atividade_entry.delete(0, tk.END)
            self.ambiente_entry.delete(0, tk.END)
            self.ambiente_idx = -1
        self.update_navigation_buttons()
    
    def mostrar_ambiente(self):
        ambientes_atividade = self.get_ambientes_atividade()
        if ambientes_atividade and self.ambiente_idx >= 0 and self.ambiente_idx < len(ambientes_atividade):
            self.ambiente_entry.delete(0, tk.END)
            self.ambiente_entry.insert(0, ambientes_atividade[self.ambiente_idx]["descricao"])
        else:
            self.ambiente_entry.delete(0, tk.END)
        self.update_navigation_buttons()
    
    def update_navigation_buttons(self):
        # Atualizar botões de navegação da empresa
        self.nav_empresa_primeiro_btn['state'] = tk.NORMAL if self.empresa_idx > 0 else tk.DISABLED
        self.nav_empresa_anterior_btn['state'] = tk.NORMAL if self.empresa_idx > 0 else tk.DISABLED
        self.nav_empresa_proximo_btn['state'] = tk.NORMAL if self.empresa_idx < len(self.empresas) - 1 else tk.DISABLED
        self.nav_empresa_ultimo_btn['state'] = tk.NORMAL if self.empresa_idx < len(self.empresas) - 1 else tk.DISABLED
        
        # Atualizar botões de edição e exclusão da empresa
        self.empresa_editar_btn['state'] = tk.NORMAL if self.empresa_idx >= 0 else tk.DISABLED
        self.empresa_excluir_btn['state'] = tk.NORMAL if self.empresa_idx >= 0 else tk.DISABLED
        
        # Atualizar botões de navegação do setor
        setores_empresa = self.get_setores_empresa()
        self.nav_setor_primeiro_btn['state'] = tk.NORMAL if self.setor_idx > 0 and setores_empresa else tk.DISABLED
        self.nav_setor_anterior_btn['state'] = tk.NORMAL if self.setor_idx > 0 and setores_empresa else tk.DISABLED
        self.nav_setor_proximo_btn['state'] = tk.NORMAL if setores_empresa and self.setor_idx < len(setores_empresa) - 1 else tk.DISABLED
        self.nav_setor_ultimo_btn['state'] = tk.NORMAL if setores_empresa and self.setor_idx < len(setores_empresa) - 1 else tk.DISABLED
        
        # Atualizar botões de edição e exclusão do setor
        self.setor_editar_btn['state'] = tk.NORMAL if self.setor_idx >= 0 and setores_empresa else tk.DISABLED
        self.setor_excluir_btn['state'] = tk.NORMAL if self.setor_idx >= 0 and setores_empresa else tk.DISABLED
        
        # Atualizar botões de navegação do cargo
        cargos_setor = self.get_cargos_setor()
        self.nav_cargo_primeiro_btn['state'] = tk.NORMAL if self.cargo_idx > 0 and cargos_setor else tk.DISABLED
        self.nav_cargo_anterior_btn['state'] = tk.NORMAL if self.cargo_idx > 0 and cargos_setor else tk.DISABLED
        self.nav_cargo_proximo_btn['state'] = tk.NORMAL if cargos_setor and self.cargo_idx < len(cargos_setor) - 1 else tk.DISABLED
        self.nav_cargo_ultimo_btn['state'] = tk.NORMAL if cargos_setor and self.cargo_idx < len(cargos_setor) - 1 else tk.DISABLED
        
        # Atualizar botões de edição e exclusão do cargo
        self.cargo_editar_btn['state'] = tk.NORMAL if self.cargo_idx >= 0 and cargos_setor else tk.DISABLED
        self.cargo_excluir_btn['state'] = tk.NORMAL if self.cargo_idx >= 0 and cargos_setor else tk.DISABLED
        
        # Atualizar botões de edição e exclusão da atividade
        atividades_cargo = self.get_atividades_cargo()
        self.atividade_editar_btn['state'] = tk.NORMAL if self.atividade_idx >= 0 and atividades_cargo else tk.DISABLED
        self.atividade_excluir_btn['state'] = tk.NORMAL if self.atividade_idx >= 0 and atividades_cargo else tk.DISABLED
        
        # Atualizar botões de edição e exclusão do ambiente
        ambientes_atividade = self.get_ambientes_atividade()
        self.ambiente_editar_btn['state'] = tk.NORMAL if self.ambiente_idx >= 0 and ambientes_atividade else tk.DISABLED
        self.ambiente_excluir_btn['state'] = tk.NORMAL if self.ambiente_idx >= 0 and ambientes_atividade else tk.DISABLED

if __name__ == "__main__":
    root = tk.Tk()
    app = PPRA_LTCAT(root)
    root.mainloop()