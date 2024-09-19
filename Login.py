import sys
import os
import sqlite3
from PySide6.QtCore import QFile, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QMessageBox, QPushButton, QLineEdit, QLabel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap, QIcon  # Adicione QIcon

# Definindo a configuração antes de criar qualquer objeto Qt
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

class LoginDialog(QDialog):
    def __init__(self):
        super(LoginDialog, self).__init__()
        
        # muda o icone da janela
        self.setWindowIcon(QIcon('resources/pngegg.ico'))
        
        loader = QUiLoader()
        file = QFile("loginbanco.ui")
        if not file.exists():
            print(f"Arquivo .ui não encontrado: {file.fileName()}")
            sys.exit(-1)
        file.open(QFile.ReadOnly)
        self.window = loader.load(file, self)
        file.close()

        # mantem o tamanho da janela de login
        self.setFixedSize(self.window.size())

        # qlabel do background da tela de login
        self.backgroundLabel = self.window.findChild(QLabel, "backgroundLabel")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "resources", "icon.png")

        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.backgroundLabel.setPixmap(pixmap)
            self.backgroundLabel.setScaledContents(True)
        else:
            print("Erro ao carregar a imagem de fundo. Verifique o caminho.")

        self.loginButton = self.window.findChild(QPushButton, "loginButton")
        self.loginLineEdit = self.window.findChild(QLineEdit, "loginLineEdit")
        self.senhaLineEdit = self.window.findChild(QLineEdit, "senhaLineEdit")
        self.hostLineEdit = self.window.findChild(QLineEdit, "hostLineEdit")
        self.bancoLineEdit = self.window.findChild(QLineEdit, "bancoLineEdit")
        self.portaLineEdit = self.window.findChild(QLineEdit, "portaLineEdit")

        if not self.loginButton or not self.loginLineEdit or not self.senhaLineEdit or not self.hostLineEdit or not self.bancoLineEdit or not self.portaLineEdit:
            print("Erro ao carregar widgets. Verifique se os IDs dos widgets no arquivo .ui correspondem aos usados no código.")
            sys.exit(-1)

        self.loginButton.clicked.connect(self.check_login)

    def check_login(self):
        login = self.loginLineEdit.text()
        senha = self.senhaLineEdit.text()
        host = self.hostLineEdit.text()
        banco = self.bancoLineEdit.text()
        porta = self.portaLineEdit.text()

        if self.validate_credentials(login, senha, host, banco, porta):
            self.accept()
        else:
            QMessageBox.warning(self, "Erro de Login", "Credenciais inválidas ou usuário não é administrador.")

    def validate_credentials(self, login, senha, host, banco, porta):
        try:
            # entrar no banco de dados (SQLite p ficar simples, arrume se precisar)
            conn = sqlite3.connect(f'{banco}.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT is_admin FROM usuarios WHERE login=? AND senha=?", (login, senha))
            result = cursor.fetchone()
            conn.close()

            if result and result[0] == 1:
                return True
            else:
                return False

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível conectar ao banco de dados: {e}")
            return False

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        # muda o icone da janela
        self.setWindowIcon(QIcon('resources/seu_icone.ico'))

        loader = QUiLoader()
        file = QFile("interfaceparagerararquivos.ui")
        if not file.exists():
            print(f"Arquivo .ui não encontrado: {file.fileName()}")
            sys.exit(-1)
        file.open(QFile.ReadOnly)
        self.window = loader.load(file, self)
        file.close()

        # mantem o tamanho da janela
        self.setFixedSize(self.window.size())

        # qlabel do background
        self.backgroundLabel = self.window.findChild(QLabel, "backgroundLabel")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "resources", "icon.png")

        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.backgroundLabel.setPixmap(pixmap)
            self.backgroundLabel.setScaledContents(True)
        else:
            print("Erro ao carregar a imagem de fundo. Verifique o caminho.")

        self.setCentralWidget(self.window)

        self.gerarArquivosButton = self.window.findChild(QPushButton, "gerarArquivosButton")

        if not self.gerarArquivosButton:
            print("Erro ao carregar widget. Verifique se o ID do widget no arquivo .ui corresponde ao usado no código.")
            sys.exit(-1)

        self.gerarArquivosButton.clicked.connect(self.gerar_arquivos)

    def gerar_arquivos(self):
        create_tables_text = "Texto relacionado a Create Tables"
        possiveis_juncoes_text = "Texto relacionado a Possíveis Junções"
        tabelas_removidas_text = "Texto relacionado a Tabelas Removidas ou Aglutinadas"
        ordenamento_etl_text = "Texto relacionado ao Ordenamento ETL"
        
        file_dialog = QFileDialog(self)
        save_dir = file_dialog.getExistingDirectory(self, "Escolha o diretório para salvar os arquivos")
        
        if save_dir:
            try:
                self.salvar_arquivo(save_dir, "Create_Tables.txt", create_tables_text)
                self.salvar_arquivo(save_dir, "Possiveis_Juncoes.txt", possiveis_juncoes_text)
                self.salvar_arquivo(save_dir, "Tabelas_Removidas.txt", tabelas_removidas_text)
                self.salvar_arquivo(save_dir, "Ordenamento_ETL.txt", ordenamento_etl_text)
                
                QMessageBox.information(self, "Sucesso", "Arquivos gerados com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao gerar os arquivos: {e}")
    
    def salvar_arquivo(self, diretorio, nome_arquivo, conteudo):
        caminho_arquivo = f"{diretorio}/{nome_arquivo}"
        with open(caminho_arquivo, 'w') as arquivo:
            arquivo.write(conteudo)
        print(f"Arquivo salvo em: {caminho_arquivo}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    loginDialog = LoginDialog()
    if loginDialog.exec() == QDialog.Accepted:
        mainWin = MainWindow()
        mainWin.show()
        sys.exit(app.exec())

        # oi fofoca nois deixa pra quem nao faz as notas 
