import cv2
import numpy as np
try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False
import os
import json
from datetime import datetime
import hashlib
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

class GerenciadorFotos:
    def __init__(self):
        self.pasta_fotos = 'fotos_candidatos'
        if not os.path.exists(self.pasta_fotos):
            os.makedirs(self.pasta_fotos)
    
    def capturar_foto(self, nome_candidato):
        """Captura foto usando a webcam"""
        try:
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                return None, "Câmera não encontrada"
            
            print("Pressione ESPAÇO para capturar a foto ou ESC para cancelar")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Espelhar a imagem
                frame = cv2.flip(frame, 1)
                
                # Mostrar preview
                cv2.imshow('Captura de Foto - Pressione ESPAÇO', frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord(' '):  # Espaço para capturar
                    # Salvar foto
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    nome_arquivo = f"{self.pasta_fotos}/{nome_candidato}_{timestamp}.jpg"
                    cv2.imwrite(nome_arquivo, frame)
                    
                    cap.release()
                    cv2.destroyAllWindows()
                    return nome_arquivo, "Foto capturada com sucesso"
                
                elif key == 27:  # ESC para cancelar
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            return None, "Captura cancelada"
            
        except Exception as e:
            return None, f"Erro ao capturar foto: {str(e)}"
    
    def verificar_face(self, foto_path, fotos_cadastradas):
        """Verifica se a face já está cadastrada"""
        if not FACE_RECOGNITION_AVAILABLE:
            return False, "Reconhecimento facial não disponível (face_recognition não instalado)"
        
        try:
            # Carregar a foto atual
            imagem_atual = face_recognition.load_image_file(foto_path)
            encodings_atual = face_recognition.face_encodings(imagem_atual)
            
            if not encodings_atual:
                return False, "Nenhuma face detectada na foto"
            
            encoding_atual = encodings_atual[0]
            
            # Comparar com fotos cadastradas
            for foto_cadastrada in fotos_cadastradas:
                if os.path.exists(foto_cadastrada):
                    imagem_cadastrada = face_recognition.load_image_file(foto_cadastrada)
                    encodings_cadastrada = face_recognition.face_encodings(imagem_cadastrada)
                    
                    if encodings_cadastrada:
                        resultado = face_recognition.compare_faces([encodings_cadastrada[0]], encoding_atual)
                        if resultado[0]:
                            return True, "Face já cadastrada no sistema"
            
            return False, "Face não encontrada no sistema"
            
        except Exception as e:
            return False, f"Erro na verificação: {str(e)}"

class GeradorRelatorios:
    def __init__(self):
        self.pasta_relatorios = 'relatorios'
        if not os.path.exists(self.pasta_relatorios):
            os.makedirs(self.pasta_relatorios)
    
    def gerar_comprovante_inscricao(self, dados_candidato):
        """Gera comprovante de inscrição em PDF"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.pasta_relatorios}/comprovante_inscricao_{dados_candidato['nome'].replace(' ', '_')}_{timestamp}.pdf"
        
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Título
        titulo = Paragraph("COMPROVANTE DE INSCRIÇÃO", styles['Title'])
        story.append(titulo)
        story.append(Spacer(1, 20))
        
        # Subtítulo
        subtitulo = Paragraph("ELEIÇÃO CIPA 2024", styles['Heading2'])
        story.append(subtitulo)
        story.append(Spacer(1, 30))
        
        # Dados do candidato
        dados = [
            ['Nome:', dados_candidato['nome']],
            ['CPF:', dados_candidato['cpf']],
            ['Cargo/Função:', dados_candidato['cargo']],
            ['Empresa:', dados_candidato['empresa']],
            ['Número do Candidato:', f"{dados_candidato['numero']:02d}"],
            ['Data de Inscrição:', datetime.fromisoformat(dados_candidato['data_inscricao']).strftime('%d/%m/%Y %H:%M:%S')]
        ]
        
        tabela = Table(dados, colWidths=[2*inch, 4*inch])
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(tabela)
        story.append(Spacer(1, 40))
        
        # Assinatura
        assinatura = Paragraph("_" * 50, styles['Normal'])
        story.append(assinatura)
        assinatura_texto = Paragraph("Assinatura do Candidato", styles['Normal'])
        story.append(assinatura_texto)
        
        story.append(Spacer(1, 20))
        
        # Data e hora de emissão
        emissao = Paragraph(f"Documento emitido em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}", 
                           styles['Normal'])
        story.append(emissao)
        
        doc.build(story)
        return filename
    
    def gerar_comprovante_votacao(self, eleitor_id, empresa, timestamp):
        """Gera comprovante de votação"""
        filename = f"{self.pasta_relatorios}/comprovante_votacao_{eleitor_id}.pdf"
        
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Título
        titulo = Paragraph("COMPROVANTE DE VOTAÇÃO", styles['Title'])
        story.append(titulo)
        story.append(Spacer(1, 20))
        
        # Subtítulo
        subtitulo = Paragraph("ELEIÇÃO CIPA 2024", styles['Heading2'])
        story.append(subtitulo)
        story.append(Spacer(1, 30))
        
        # Dados da votação
        dados = [
            ['Código do Eleitor:', eleitor_id],
            ['Empresa:', empresa],
            ['Data/Hora da Votação:', datetime.fromisoformat(timestamp).strftime('%d/%m/%Y %H:%M:%S')],
            ['Status:', 'VOTO REGISTRADO COM SUCESSO']
        ]
        
        tabela = Table(dados, colWidths=[2*inch, 4*inch])
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.lightgreen),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(tabela)
        story.append(Spacer(1, 40))
        
        # Observações
        obs = Paragraph("OBSERVAÇÕES:", styles['Heading3'])
        story.append(obs)
        
        obs_texto = Paragraph(
            "• Este comprovante confirma que seu voto foi registrado no sistema.<br/>"
            "• O sigilo do voto é garantido conforme legislação vigente.<br/>"
            "• Guarde este comprovante como prova de participação na eleição.",
            styles['Normal']
        )
        story.append(obs_texto)
        
        story.append(Spacer(1, 30))
        
        # Data de emissão
        emissao = Paragraph(f"Documento emitido em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}", 
                           styles['Normal'])
        story.append(emissao)
        
        doc.build(story)
        return filename
    
    def gerar_relatorio_final(self, dados_eleicao):
        """Gera relatório final da eleição"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.pasta_relatorios}/relatorio_final_eleicao_{timestamp}.pdf"
        
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Título
        titulo = Paragraph("RELATÓRIO FINAL DA ELEIÇÃO CIPA", styles['Title'])
        story.append(titulo)
        story.append(Spacer(1, 30))
        
        # Informações gerais
        config = dados_eleicao['configuracoes']
        info_geral = [
            ['Data de Início:', datetime.fromisoformat(config['data_inicio']).strftime('%d/%m/%Y %H:%M:%S') if config.get('data_inicio') else 'N/A'],
            ['Data de Fim:', datetime.fromisoformat(config['data_fim']).strftime('%d/%m/%Y %H:%M:%S') if config.get('data_fim') else 'N/A'],
            ['Total de Empresas:', str(len(dados_eleicao['empresas']))],
            ['Total de Candidatos:', str(len(dados_eleicao['candidatos']))],
            ['Total de Eleitores:', str(len(dados_eleicao['eleitores']))]
        ]
        
        tabela_info = Table(info_geral, colWidths=[2*inch, 4*inch])
        tabela_info.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(tabela_info)
        story.append(Spacer(1, 30))
        
        # Resultados por empresa
        for empresa, votos in dados_eleicao['votos'].items():
            empresa_titulo = Paragraph(f"RESULTADOS - EMPRESA: {empresa}", styles['Heading2'])
            story.append(empresa_titulo)
            story.append(Spacer(1, 15))
            
            # Dados dos resultados
            dados_resultados = [['Número', 'Nome do Candidato', 'Votos', 'Percentual']]
            
            total_votos = sum(votos.values())
            votos_ordenados = sorted(votos.items(), key=lambda x: x[1], reverse=True)
            
            for numero, qtd_votos in votos_ordenados:
                # Buscar nome do candidato
                nome_candidato = "Candidato não encontrado"
                for cand_id, dados_cand in dados_eleicao['candidatos'].items():
                    if dados_cand['numero'] == int(numero):
                        nome_candidato = dados_cand['nome']
                        break
                
                percentual = (qtd_votos / total_votos * 100) if total_votos > 0 else 0
                dados_resultados.append([
                    f"{numero:02d}",
                    nome_candidato,
                    str(qtd_votos),
                    f"{percentual:.1f}%"
                ])
            
            # Adicionar total
            dados_resultados.append(['', 'TOTAL', str(total_votos), '100.0%'])
            
            tabela_resultados = Table(dados_resultados, colWidths=[0.8*inch, 3*inch, 1*inch, 1.2*inch])
            tabela_resultados.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(tabela_resultados)
            story.append(Spacer(1, 30))
        
        # Rodapé
        rodape = Paragraph(f"Relatório gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}", 
                          styles['Normal'])
        story.append(rodape)
        
        doc.build(story)
        return filename

class GerenciadorSons:
    def __init__(self):
        self.pasta_sons = 'sons'
        if not os.path.exists(self.pasta_sons):
            os.makedirs(self.pasta_sons)
        
        # Criar sons simulados se não existirem
        self.criar_sons_simulados()
    
    def criar_sons_simulados(self):
        """Cria arquivos de som simulados (placeholder)"""
        sons = ['tecla.wav', 'confirma.wav', 'corrige.wav']
        
        for som in sons:
            caminho = os.path.join(self.pasta_sons, som)
            if not os.path.exists(caminho):
                # Criar arquivo vazio como placeholder
                with open(caminho, 'w') as f:
                    f.write('')

class ValidadorDados:
    @staticmethod
    def validar_cpf(cpf):
        """Valida CPF"""
        cpf = ''.join(filter(str.isdigit, cpf))
        
        if len(cpf) != 11:
            return False
        
        if cpf == cpf[0] * 11:
            return False
        
        # Validar primeiro dígito
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digito1 = (soma * 10) % 11
        if digito1 == 10:
            digito1 = 0
        
        if int(cpf[9]) != digito1:
            return False
        
        # Validar segundo dígito
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digito2 = (soma * 10) % 11
        if digito2 == 10:
            digito2 = 0
        
        return int(cpf[10]) == digito2
    
    @staticmethod
    def validar_cnpj(cnpj):
        """Valida CNPJ"""
        cnpj = ''.join(filter(str.isdigit, cnpj))
        
        if len(cnpj) != 14:
            return False
        
        if cnpj == cnpj[0] * 14:
            return False
        
        # Validar primeiro dígito
        pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
        digito1 = soma % 11
        digito1 = 0 if digito1 < 2 else 11 - digito1
        
        if int(cnpj[12]) != digito1:
            return False
        
        # Validar segundo dígito
        pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
        digito2 = soma % 11
        digito2 = 0 if digito2 < 2 else 11 - digito2
        
        return int(cnpj[13]) == digito2

class BackupManager:
    def __init__(self):
        self.pasta_backup = 'backups'
        if not os.path.exists(self.pasta_backup):
            os.makedirs(self.pasta_backup)
    
    def criar_backup(self, dados):
        """Cria backup dos dados"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.pasta_backup}/backup_urna_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        
        return filename
    
    def restaurar_backup(self, filename):
        """Restaura dados do backup"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            return None, str(e)
    
    def listar_backups(self):
        """Lista todos os backups disponíveis"""
        backups = []
        for arquivo in os.listdir(self.pasta_backup):
            if arquivo.endswith('.json') and arquivo.startswith('backup_urna_'):
                caminho = os.path.join(self.pasta_backup, arquivo)
                timestamp = os.path.getctime(caminho)
                backups.append({
                    'arquivo': arquivo,
                    'caminho': caminho,
                    'data': datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y %H:%M:%S')
                })
        
        return sorted(backups, key=lambda x: x['data'], reverse=True)