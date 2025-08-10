import uuid # Para gerar IDs únicos
import random # Para gerar códigos numéricos aleatórios

class SistemaVotacaoCIPA:
    def __init__(self):
        self.candidatos = {} # Ex: {'1': 'Ana', '2': 'Bruno'}
        self.votos = {}      # Ex: {'1': 0, '2': 0}
        self.eleitores_habilitados = {} # {'ID_ELEITOR': 'CODIGO_VALIDACAO_UNICO'}
        self.codigos_ativos = set() # Guarda os códigos que ainda não foram usados

    def adicionar_candidato(self, numero, nome):
        """Adiciona um candidato ao sistema."""
        self.candidatos[str(numero)] = nome
        self.votos[str(numero)] = 0

    def _gerar_codigo_validacao(self):
        """Gera um código de 6 dígitos único."""
        while True:
            codigo = str(random.randint(100000, 999999))
            if codigo not in self.codigos_ativos:
                self.codigos_ativos.add(codigo)
                return codigo

    def habilitar_eleitor(self, id_eleitor_interno):
        """
        Mesário habilita o eleitor e gera um código de validação.
        Retorna o código para o eleitor.
        """
        if id_eleitor_interno in self.eleitores_habilitados:
            return "Eleitor já foi habilitado.", None

        codigo = self._gerar_codigo_validacao()
        self.eleitores_habilitados[id_eleitor_interno] = codigo
        print(f"Mesário: Eleitor '{id_eleitor_interno}' habilitado com código: {codigo}")
        return "Eleitor habilitado com sucesso!", codigo

    def registrar_voto(self, id_eleitor_interno, codigo_informado, numero_candidato):
        """
        Funcionário usa o código para votar.
        O código é invalidado após o uso.
        """
        if id_eleitor_interno not in self.eleitores_habilitados:
            return "Erro: Eleitor não habilitado."

        if self.eleitores_habilitados[id_eleitor_interno] != codigo_informado:
            return "Erro: Código de validação incorreto."

        if codigo_informado not in self.codigos_ativos:
            return "Erro: Este código já foi usado ou é inválido."

        if str(numero_candidato) not in self.candidatos:
            return "Erro: Número de candidato inválido."

        # Registrar o voto e invalidar o código
        self.votos[str(numero_candidato)] += 1
        self.codigos_ativos.remove(codigo_informado) # Remove o código dos ativos
        del self.eleitores_habilitados[id_eleitor_interno] # Remove da lista de habilitados, para não poder votar de novo

        return "Voto registrado com sucesso!"

    def obter_resultados(self):
        """Retorna os resultados da votação."""
        print("\n--- Resultados da Votação ---")
        for numero, total_votos in sorted(self.votos.items(), key=lambda item: item[1], reverse=True):
            print(f"Candidato {numero} - {self.candidatos[numero]}: {total_votos} votos")
        print("-----------------------------")


# --- Testando a Lógica ---
sistema = SistemaVotacaoCIPA()
sistema.adicionar_candidato(1, "Maria Silva")
sistema.adicionar_candidato(2, "João Pereira")
sistema.adicionar_candidato(3, "Ana Costa")

# Cenário 1: Mesário habilita eleitor 1
status, codigo_eleitor1 = sistema.habilitar_eleitor("Func_001")
print(f"Mesário Status: {status}")

# Cenário 2: Eleitor 1 vota
print(f"Eleitor 1 Voto: {sistema.registrar_voto('Func_001', codigo_eleitor1, 1)}")

# Cenário 3: Mesário tenta habilitar eleitor 1 de novo (não deveria ser possível)
status, _ = sistema.habilitar_eleitor("Func_001")
print(f"Mesário Status: {status}")

# Cenário 4: Eleitor 2 é habilitado e vota
status, codigo_eleitor2 = sistema.habilitar_eleitor("Func_002")
print(f"Mesário Status: {status}")
print(f"Eleitor 2 Voto: {sistema.registrar_voto('Func_002', codigo_eleitor2, 2)}")

# Cenário 5: Eleitor 3 é habilitado e tenta votar com código errado
status, codigo_eleitor3 = sistema.habilitar_eleitor("Func_003")
print(f"Mesário Status: {status}")
print(f"Eleitor 3 Voto (código errado): {sistema.registrar_voto('Func_003', '999999', 3)}") # Código errado
print(f"Eleitor 3 Voto (código certo): {sistema.registrar_voto('Func_003', codigo_eleitor3, 3)}") # Código certo

# Cenário 6: Eleitor 4 é habilitado, vota, e tenta votar de novo
status, codigo_eleitor4 = sistema.habilitar_eleitor("Func_004")
print(f"Mesário Status: {status}")
print(f"Eleitor 4 Voto: {sistema.registrar_voto('Func_004', codigo_eleitor4, 1)}")
print(f"Eleitor 4 Tentativa de Voto Duplo: {sistema.registrar_voto('Func_004', codigo_eleitor4, 2)}")

# Ver os resultados
sistema.obter_resultados()