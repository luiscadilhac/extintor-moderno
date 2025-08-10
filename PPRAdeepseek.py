import tkinter as tk
from tkinter import ttk, font as tkfont, messagebox, simpledialog

class SistemaControleRiscos:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Controle de Riscos Ocupacionais")
        self.root.geometry("1300x800")
        self.root.configure(bg='#ffd700')  # Cor do entorno da tela
        
        # Dados de exemplo com estrutura hierárquica correta
        self.dados = {
            "Empresas": {
                "Empresa A": {
                    "Setores": {
                        "Produção": {
                            "Cargos": {
                                "Operador de Máquina": {
                                    "Atividades": "Operação de equipamentos",
                                    "Ambiente": "Área industrial",
                                    "Riscos": [
                                        ["Ruído", "85 dB", "8h/dia", "Alto risco", "EPI - Protetor auricular", "Manutenção preventiva"]
                                    ]
                                },
                                "Supervisor": {
                                    "Atividades": "Supervisão de equipe",
                                    "Ambiente": "Escritório/Área industrial",
                                    "Riscos": []
                                }
                            }
                        },
                        "Administrativo": {
                            "Cargos": {
                                "Assistente": {
                                    "Atividades": "Tarefas administrativas",
                                    "Ambiente": "Escritório",
                                    "Riscos": []
                                }
                            }
                        }
                    }
                },
                "Empresa B": {
                    "Setores": {
                        "TI": {
                            "Cargos": {
                                "Desenvolvedor": {
                                    "Atividades": "Programação",
                                    "Ambiente": "Escritório",
                                    "Riscos": []
                                }
                            }
                        }
                    }
                }
            }
        }
        
        # Variáveis de controle
        self.empresa_selecionada = tk.StringVar()
        self.setor_selecionado = tk.StringVar()
        self.cargo_selecionado = tk.StringVar()
        self.atividade_var = tk.StringVar()
        self.ambiente_var = tk.StringVar()
        
        # Configuração de fontes
        self.fonte_normal = tkfont.Font(family="Arial", size=11)
        self.fonte_cabecalho = tkfont.Font(family="Arial", size=12, weight="bold")
        self.fonte_titulo = tkfont.Font(family="Arial", size=14, weight="bold")
        
        # Cores
        self.cor_fundo = '#ffffe0'  # Cor do interior da tela
        self.cor_titulo = '#1e90ff'  # Cor dos títulos
        self.cor_borda = '#ffd700'  # Cor do entorno
        
        # Frame principal
        self.main_frame = tk.Frame(root, bg=self.cor_fundo, bd=5, relief=tk.GROOVE)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Variável para armazenar o frame dos dados da tabela de riscos
        self.scrollable_frame = None
        self.linhas_riscos = []
        
        # Criação da interface
        self.criar_interface()
        
        # Carrega dados iniciais
        self.carregar_empresas()

    def criar_interface(self):
        # Título principal
        tk.Label(
            self.main_frame,
            text="CONTROLE DE RISCOS OCUPACIONAIS",
            font=self.fonte_titulo,
            bg=self.cor_fundo,
            fg=self.cor_titulo,
            pady=10
        ).pack(fill=tk.X)
        
        # Frame da hierarquia
        frame_hierarquia = tk.Frame(self.main_frame, bg=self.cor_fundo, padx=15, pady=15)
        frame_hierarquia.pack(fill=tk.X, pady=(0, 20))
        
        # Título da hierarquia
        tk.Label(
            frame_hierarquia,
            text="HIERARQUIA DE CADASTRO",
            font=self.fonte_cabecalho,
            bg=self.cor_fundo,
            fg=self.cor_titulo
        ).grid(row=0, column=0, columnspan=6, sticky="w", pady=(0, 10))
        
        # Configuração do grid
        for i in range(6):
            frame_hierarquia.grid_columnconfigure(i, weight=1)
        
        # EMPRESA
        tk.Label(
            frame_hierarquia,
            text="EMPRESA:",
            font=self.fonte_cabecalho,
            bg=self.cor_fundo
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        
        self.cb_empresa = ttk.Combobox(
            frame_hierarquia,
            textvariable=self.empresa_selecionada,
            font=self.fonte_normal,
            state="readonly"
        )
        self.cb_empresa.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.cb_empresa.bind("<<ComboboxSelected>>", self.atualizar_setores)
        
        # Botões de navegação e edição para EMPRESA
        tk.Button(
            frame_hierarquia,
            text="◄",
            font=self.fonte_normal,
            bg='#e0e0e0',
            command=self.empresa_anterior
        ).grid(row=1, column=2, padx=2, sticky="e")
        
        tk.Button(
            frame_hierarquia,
            text="►",
            font=self.fonte_normal,
            bg='#e0e0e0',
            command=self.empresa_proxima
        ).grid(row=1, column=3, padx=2, sticky="w")
        
        tk.Button(
            frame_hierarquia,
            text="+",
            font=self.fonte_normal,
            bg='#7fffd4',
            command=self.adicionar_empresa
        ).grid(row=1, column=4, padx=2, sticky="w")
        
        tk.Button(
            frame_hierarquia,
            text="-",
            font=self.fonte_normal,
            bg='#ff9999',
            command=self.remover_empresa
        ).grid(row=1, column=5, padx=2, sticky="w")
        
        # SETOR (vinculado à empresa)
        tk.Label(
            frame_hierarquia,
            text="SETOR:",
            font=self.fonte_cabecalho,
            bg=self.cor_fundo
        ).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        
        self.cb_setor = ttk.Combobox(
            frame_hierarquia,
            textvariable=self.setor_selecionado,
            font=self.fonte_normal,
            state="readonly"
        )
        self.cb_setor.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.cb_setor.bind("<<ComboboxSelected>>", self.atualizar_cargos)
        
        # Botões de navegação e edição para SETOR
        tk.Button(
            frame_hierarquia,
            text="◄",
            font=self.fonte_normal,
            bg='#e0e0e0',
            command=self.setor_anterior
        ).grid(row=2, column=2, padx=2, sticky="e")
        
        tk.Button(
            frame_hierarquia,
            text="►",
            font=self.fonte_normal,
            bg='#e0e0e0',
            command=self.setor_proximo
        ).grid(row=2, column=3, padx=2, sticky="w")
        
        tk.Button(
            frame_hierarquia,
            text="+",
            font=self.fonte_normal,
            bg='#7fffd4',
            command=self.adicionar_setor
        ).grid(row=2, column=4, padx=2, sticky="w")
        
        tk.Button(
            frame_hierarquia,
            text="-",
            font=self.fonte_normal,
            bg='#ff9999',
            command=self.remover_setor
        ).grid(row=2, column=5, padx=2, sticky="w")
        
        # CARGO (vinculado ao setor)
        tk.Label(
            frame_hierarquia,
            text="CARGO:",
            font=self.fonte_cabecalho,
            bg=self.cor_fundo
        ).grid(row=3, column=0, padx=5, pady=5, sticky="e")
        
        self.cb_cargo = ttk.Combobox(
            frame_hierarquia,
            textvariable=self.cargo_selecionado,
            font=self.fonte_normal,
            state="readonly"
        )
        self.cb_cargo.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.cb_cargo.bind("<<ComboboxSelected>>", self.atualizar_detalhes_cargo)
        
        # Botões de navegação e edição para CARGO
        tk.Button(
            frame_hierarquia,
            text="◄",
            font=self.fonte_normal,
            bg='#e0e0e0',
            command=self.cargo_anterior
        ).grid(row=3, column=2, padx=2, sticky="e")
        
        tk.Button(
            frame_hierarquia,
            text="►",
            font=self.fonte_normal,
            bg='#e0e0e0',
            command=self.cargo_proximo
        ).grid(row=3, column=3, padx=2, sticky="w")
        
        tk.Button(
            frame_hierarquia,
            text="+",
            font=self.fonte_normal,
            bg='#7fffd4',
            command=self.adicionar_cargo
        ).grid(row=3, column=4, padx=2, sticky="w")
        
        tk.Button(
            frame_hierarquia,
            text="-",
            font=self.fonte_normal,
            bg='#ff9999',
            command=self.remover_cargo
        ).grid(row=3, column=5, padx=2, sticky="w")
        
        # ATIVIDADE (vinculada ao cargo)
        tk.Label(
            frame_hierarquia,
            text="ATIVIDADE:",
            font=self.fonte_cabecalho,
            bg=self.cor_fundo
        ).grid(row=4, column=0, padx=5, pady=5, sticky="e")
        
        tk.Entry(
            frame_hierarquia,
            textvariable=self.atividade_var,
            font=self.fonte_normal,
            state='readonly',
            bg='white'
        ).grid(row=4, column=1, padx=5, pady=5, sticky="ew", columnspan=5)
        
        # AMBIENTE LABORATIVO (vinculado ao cargo)
        tk.Label(
            frame_hierarquia,
            text="AMBIENTE LABORATIVO:",
            font=self.fonte_cabecalho,
            bg=self.cor_fundo
        ).grid(row=5, column=0, padx=5, pady=5, sticky="e")
        
        tk.Entry(
            frame_hierarquia,
            textvariable=self.ambiente_var,
            font=self.fonte_normal,
            state='readonly',
            bg='white'
        ).grid(row=5, column=1, padx=5, pady=5, sticky="ew", columnspan=5)
        
        # Frame da tabela de riscos
        frame_tabela = tk.Frame(self.main_frame, bg='white', padx=10, pady=10)
        frame_tabela.pack(fill=tk.BOTH, expand=True)
        
        # Título da tabela
        tk.Label(
            frame_tabela,
            text="TABELA DE RISCOS OCUPACIONAIS",
            font=self.fonte_cabecalho,
            bg='white',
            fg=self.cor_titulo
        ).pack(fill=tk.X, pady=(0, 10))
        
        # Criação da tabela de riscos
        self.criar_tabela_riscos(frame_tabela)
        
        # Botões de ação
        self.criar_botoes_acao()

    def criar_tabela_riscos(self, parent):
        # Cabeçalhos
        cabecalhos = ["Agente", "Concentração", "Exposição", "Análise", "Medidas Existentes", "Medidas Necessárias"]
        
        # Frame para os cabeçalhos
        frame_cabecalhos = tk.Frame(parent, bg=self.cor_titulo)
        frame_cabecalhos.pack(fill=tk.X)
        
        for col, cabecalho in enumerate(cabecalhos):
            tk.Label(
                frame_cabecalhos,
                text=cabecalho,
                font=self.fonte_cabecalho,
                bg=self.cor_titulo,
                fg='white',
                padx=10,
                pady=5
            ).grid(row=0, column=col, sticky="nsew")
            frame_cabecalhos.grid_columnconfigure(col, weight=1)
        
        # Frame para os dados (com scrollbar)
        frame_dados = tk.Frame(parent, bg='white')
        frame_dados.pack(fill=tk.BOTH, expand=True)
        
        # Canvas e scrollbar
        canvas = tk.Canvas(frame_dados, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_dados, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='white')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Inicializa a lista de linhas de riscos
        self.linhas_riscos = []

    def criar_botoes_acao(self):
        frame_botoes = tk.Frame(self.main_frame, bg=self.cor_fundo)
        frame_botoes.pack(pady=10)
        
        tk.Button(
            frame_botoes,
            text="ADICIONAR RISCO",
            font=self.fonte_normal,
            bg='#4CAF50',
            fg='white',
            command=self.adicionar_risco
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            frame_botoes,
            text="REMOVER RISCO",
            font=self.fonte_normal,
            bg='#F44336',
            fg='white',
            command=self.remover_risco
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            frame_botoes,
            text="SALVAR ALTERAÇÕES",
            font=self.fonte_normal,
            bg='#2196F3',
            fg='white',
            command=self.salvar_dados
        ).pack(side=tk.LEFT, padx=5)

    # Métodos de navegação corrigidos
    def empresa_anterior(self):
        current = self.cb_empresa.current()
        if current > 0:
            self.cb_empresa.current(current - 1)
            self.empresa_selecionada.set(self.cb_empresa.get())
            self.atualizar_setores()

    def empresa_proxima(self):
        current = self.cb_empresa.current()
        if current < len(self.cb_empresa['values']) - 1:
            self.cb_empresa.current(current + 1)
            self.empresa_selecionada.set(self.cb_empresa.get())
            self.atualizar_setores()

    def setor_anterior(self):
        current = self.cb_setor.current()
        if current > 0:
            self.cb_setor.current(current - 1)
            self.setor_selecionado.set(self.cb_setor.get())
            self.atualizar_cargos()

    def setor_proximo(self):
        current = self.cb_setor.current()
        if current < len(self.cb_setor['values']) - 1:
            self.cb_setor.current(current + 1)
            self.setor_selecionado.set(self.cb_setor.get())
            self.atualizar_cargos()

    def cargo_anterior(self):
        current = self.cb_cargo.current()
        if current > 0:
            self.cb_cargo.current(current - 1)
            self.cargo_selecionado.set(self.cb_cargo.get())
            self.atualizar_detalhes_cargo()

    def cargo_proximo(self):
        current = self.cb_cargo.current()
        if current < len(self.cb_cargo['values']) - 1:
            self.cb_cargo.current(current + 1)
            self.cargo_selecionado.set(self.cb_cargo.get())
            self.atualizar_detalhes_cargo()

    # Métodos de atualização
    def carregar_empresas(self):
        empresas = list(self.dados["Empresas"].keys())
        self.cb_empresa['values'] = empresas
        if empresas:
            self.cb_empresa.current(0)
            self.empresa_selecionada.set(empresas[0])
            self.atualizar_setores()

    def atualizar_setores(self, event=None):
        empresa = self.empresa_selecionada.get()
        if empresa in self.dados["Empresas"]:
            setores = list(self.dados["Empresas"][empresa]["Setores"].keys())
            self.cb_setor['values'] = setores
            if setores:
                self.cb_setor.current(0)
                self.setor_selecionado.set(setores[0])
                self.atualizar_cargos()
            else:
                self.cb_setor.set('')
                self.limpar_campos_setor()

    def atualizar_cargos(self, event=None):
        empresa = self.empresa_selecionada.get()
        setor = self.setor_selecionado.get()
        if (empresa in self.dados["Empresas"] and 
            setor in self.dados["Empresas"][empresa]["Setores"]):
            
            cargos = list(self.dados["Empresas"][empresa]["Setores"][setor]["Cargos"].keys())
            self.cb_cargo['values'] = cargos
            if cargos:
                self.cb_cargo.current(0)
                self.cargo_selecionado.set(cargos[0])
                self.atualizar_detalhes_cargo()
            else:
                self.cb_cargo.set('')
                self.limpar_campos_cargo()

    def atualizar_detalhes_cargo(self, event=None):
        empresa = self.empresa_selecionada.get()
        setor = self.setor_selecionado.get()
        cargo = self.cargo_selecionado.get()
        
        if (empresa in self.dados["Empresas"] and 
            setor in self.dados["Empresas"][empresa]["Setores"] and 
            cargo in self.dados["Empresas"][empresa]["Setores"][setor]["Cargos"]):
            
            cargo_data = self.dados["Empresas"][empresa]["Setores"][setor]["Cargos"][cargo]
            self.atividade_var.set(cargo_data.get("Atividades", ""))
            self.ambiente_var.set(cargo_data.get("Ambiente", ""))
            
            # Carrega os riscos do cargo
            self.carregar_riscos_cargo(empresa, setor, cargo)
        else:
            self.limpar_campos_cargo()

    def limpar_campos_setor(self):
        self.cb_cargo.set('')
        self.cargo_selecionado.set('')
        self.cb_cargo['values'] = []
        self.limpar_campos_cargo()

    def limpar_campos_cargo(self):
        self.atividade_var.set('')
        self.ambiente_var.set('')
        self.limpar_tabela_riscos()

    def limpar_tabela_riscos(self):
        # Remove todas as linhas existentes
        for linha in self.linhas_riscos:
            for widget in linha:
                widget.destroy()
        self.linhas_riscos = []

    def carregar_riscos_cargo(self, empresa, setor, cargo):
        # Limpa a tabela atual
        self.limpar_tabela_riscos()
        
        # Obtém os riscos do cargo
        riscos = self.dados["Empresas"][empresa]["Setores"][setor]["Cargos"][cargo].get("Riscos", [])
        
        # Adiciona os riscos à tabela
        for risco in riscos:
            self.adicionar_linha_risco(risco)
        
        # Se não houver riscos, adiciona uma linha vazia
        if not riscos:
            self.adicionar_linha_risco()

    # Métodos de edição
    def adicionar_empresa(self):
        nova_empresa = simpledialog.askstring("Nova Empresa", "Nome da nova empresa:")
        if nova_empresa and nova_empresa not in self.dados["Empresas"]:
            self.dados["Empresas"][nova_empresa] = {"Setores": {}}
            self.carregar_empresas()
            self.cb_empresa.set(nova_empresa)
            self.empresa_selecionada.set(nova_empresa)

    def remover_empresa(self):
        empresa = self.empresa_selecionada.get()
        if empresa and messagebox.askyesno("Confirmar", f"Remover a empresa {empresa} e todos seus dados?"):
            self.dados["Empresas"].pop(empresa, None)
            self.carregar_empresas()

    def adicionar_setor(self):
        empresa = self.empresa_selecionada.get()
        if empresa:
            novo_setor = simpledialog.askstring("Novo Setor", "Nome do novo setor:")
            if novo_setor and novo_setor not in self.dados["Empresas"][empresa]["Setores"]:
                self.dados["Empresas"][empresa]["Setores"][novo_setor] = {"Cargos": {}}
                self.atualizar_setores()
                self.cb_setor.set(novo_setor)
                self.setor_selecionado.set(novo_setor)

    def remover_setor(self):
        empresa = self.empresa_selecionada.get()
        setor = self.setor_selecionado.get()
        if empresa and setor and messagebox.askyesno("Confirmar", f"Remover o setor {setor} e todos seus cargos?"):
            self.dados["Empresas"][empresa]["Setores"].pop(setor, None)
            self.atualizar_setores()

    def adicionar_cargo(self):
        empresa = self.empresa_selecionada.get()
        setor = self.setor_selecionado.get()
        if empresa and setor:
            novo_cargo = simpledialog.askstring("Novo Cargo", "Nome do novo cargo:")
            if novo_cargo and novo_cargo not in self.dados["Empresas"][empresa]["Setores"][setor]["Cargos"]:
                atividades = simpledialog.askstring("Atividades", "Descreva as atividades:")
                ambiente = simpledialog.askstring("Ambiente", "Descreva o ambiente laborativo:")
                
                if atividades and ambiente:
                    self.dados["Empresas"][empresa]["Setores"][setor]["Cargos"][novo_cargo] = {
                        "Atividades": atividades,
                        "Ambiente": ambiente,
                        "Riscos": []
                    }
                    self.atualizar_cargos()
                    self.cb_cargo.set(novo_cargo)
                    self.cargo_selecionado.set(novo_cargo)

    def remover_cargo(self):
        empresa = self.empresa_selecionada.get()
        setor = self.setor_selecionado.get()
        cargo = self.cargo_selecionado.get()
        if empresa and setor and cargo and messagebox.askyesno("Confirmar", f"Remover o cargo {cargo}?"):
            self.dados["Empresas"][empresa]["Setores"][setor]["Cargos"].pop(cargo, None)
            self.atualizar_cargos()

    # Métodos para gerenciar riscos
    def adicionar_risco(self):
        # Adiciona uma linha vazia na tabela
        self.adicionar_linha_risco()

    def adicionar_linha_risco(self, dados=None):
        if not self.scrollable_frame:
            return
            
        linha_num = len(self.linhas_riscos)
        campos = []
        
        for col in range(6):
            valor = dados[col] if dados and col < len(dados) else ""
            entry = tk.Entry(self.scrollable_frame, font=self.fonte_normal)
            entry.insert(0, valor)
            entry.grid(row=linha_num, column=col, sticky="nsew", padx=1, pady=1)
            campos.append(entry)
        
        self.linhas_riscos.append(campos)

    def remover_risco(self):
        if self.linhas_riscos:
            linha = self.linhas_riscos.pop()
            for widget in linha:
                widget.destroy()

    def salvar_dados(self):
        empresa = self.empresa_selecionada.get()
        setor = self.setor_selecionado.get()
        cargo = self.cargo_selecionado.get()
        
        if not (empresa and setor and cargo):
            messagebox.showwarning("Aviso", "Selecione um cargo antes de salvar")
            return
        
        # Coleta os dados da tabela
        riscos = []
        for linha in self.linhas_riscos:
            risco = []
            for campo in linha:
                risco.append(campo.get())
            if any(risco):  # Só adiciona se houver algum dado
                riscos.append(risco)
        
        # Atualiza os riscos no cargo selecionado
        if "Riscos" not in self.dados["Empresas"][empresa]["Setores"][setor]["Cargos"][cargo]:
            self.dados["Empresas"][empresa]["Setores"][setor]["Cargos"][cargo]["Riscos"] = []
        
        self.dados["Empresas"][empresa]["Setores"][setor]["Cargos"][cargo]["Riscos"] = riscos
        
        messagebox.showinfo("Sucesso", "Riscos salvos com sucesso para o cargo selecionado")

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaControleRiscos(root)
    root.mainloop()