from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.lang import Builder
import os
from functools import partial
from kivy.uix.modalview import ModalView
import pyrebase

firebaseConfig = {
                'apiKey': "AIzaSyBAHXIqw3gh_LVQ7j2yDN6jOiq73wLMNcU",
                'authDomain': "login-9f193.firebaseapp.com",
                'databaseURL': "https://trialauth-7eea1.firebaseio.com",
                'projectId': "login-9f193",
                'storageBucket': "login-9f193.appspot.com",
                'messagingSenderId': "454847795375",
                'appId': "1:454847795375:web:e7a3700a116fb26906c45a",
                'measurementId': "G-3G2D78LNF0"
}

firebase=pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth=firebase.auth()


Window.size = (300,600)

# Obter o caminho absoluto do diretório onde o script está localizado
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construir o caminho absoluto para o arquivo KV
kv_file = os.path.join(current_dir, 'login.kv')

# Verificar se o arquivo KV existe
if not os.path.exists(kv_file):
    print(f"Arquivo KV não encontrado: {kv_file}")
    raise FileNotFoundError(f"Arquivo KV não encontrado: {kv_file}")

# Carregar o arquivo KV
Builder.load_file(kv_file)

class TelaLogin(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = (1, 1, 1, 1)
        self.arg1 = None  # Inicializando arg1 como None
        self.arg2 = None  # Inicializando arg2 como None

    def on_kv_post(self, base_widget):
        # Widgets são acessíveis após o arquivo KV ser carregado
        self.texto_senha = self.ids.texto_senha
        self.texto_email = self.ids.texto_email
        self.login = self.ids.login
        self.login.bind(on_release=lambda instance: self.login_user(self.texto_email.text, self.texto_senha.text))
        self.cadastro = self.ids.cadastro
        self.cadastro.bind(on_release=partial(self.entrar_cadastro))

    def entrar_cadastro(self, instance):
        cadastro = Cadastro()
        cadastro.open()

    def login_user(self, email, password):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            print("Logged in successfully!")
            # You can now access the user's data in the Realtime Database
            user_data = db.child("users").child(user.uid).get()
            user_ref = db.child("users").push(user_data)
            print(user_data.val())
        except Exception as e:
            print("Error logging in:", e)

    def on_cadastro_button_press(self):
        email = self.texto_email.text
        password = self.texto_senha.text
        self.login_user(email, password)

    def open(self):
        self._window = ModalView(size_hint=(1, 1))
        self._window.add_widget(self)
        self._window.background_color = (1, 1, 1, 1)  # Definir o fundo do ModalView como preto
        self._window.open()

class Cadastro(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = (1, 1, 1, 1)
        self.arg1 = None  # Inicializando arg1 como None
        self.arg2 = None  # Inicializando arg2 como None

    def on_kv_post(self, base_widget):
        # Widgets são acessíveis após o arquivo KV ser carregado
        self.voltar = self.ids.voltar
        self.voltar.bind(on_release=partial(self.voltar_login))
        self.texto_senhac = self.ids.texto_senhac
        self.texto_emailc = self.ids.texto_emailc
        self.cadastroc = self.ids.cadastroc
        self.cadastroc.bind(on_release=lambda instance: self.create_user(self.texto_emailc.text, self.texto_senhac.text))

    def voltar_login(self, instance):
        voltar = TelaLogin()
        voltar.open()

    def create_user(self, email, password):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            print("User created successfully!")
            # Crie um dicionário com os dados do usuário
            user_data = {"email": email, "password": password}
            # Salve os dados do usuário no banco de dados usando a chave gerada pelo Firebase
            user_ref = db.child("users").push(user_data)
            print("User data saved successfully!")
        except Exception as e:
            print("Error creating user:", e)


    def on_cadastro_button_press(self):
        email = self.texto_emailc.text
        password = self.texto_senhac.text
        self.create_user(email, password)


    def open(self):
        self._window = ModalView(size_hint=(1, 1))
        self._window.add_widget(self)
        self._window.background_color = (1, 1, 1, 1)  # Definir o fundo do ModalView como preto
        self._window.open()

class MyApp(App):
    def build(self):
        return TelaLogin()
        
if __name__ == '__main__':
    MyApp().run()