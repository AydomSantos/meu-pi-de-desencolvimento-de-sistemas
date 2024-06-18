
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Label, Toplevel,messagebox,StringVar,OptionMenu
import re
from tkinter import *
import requests

# Define o caminho de saída
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/img_sistema")


def relative_to_assets_converso(path: str) -> str:
    # Diretório onde o script está sendo executado
    script_dir = Path(__file__).parent
    
   # Caminho relativo até a pasta assets
    assets_path = script_dir / "assets" / "img_converso"
    
    # Retorna o caminho absoluto completo até o arquivo desejado
    return str(assets_path / path)

# Define o caminho de saída relativo
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Função para validar o email
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Função para validar o número de telefone
def is_valid_phone(phone):
    return re.match(r"^\d{10,15}$", phone)

# Função para verificar se a senha e a confirmação da senha correspondem
def passwords_match(password, confirm_password):
    return password == confirm_password

# Função para validar todos os campos de entrada
def validate_inputs(name, email, phone, password, confirm_password):
    error_message = ""

    if not name:
        error_message += "Nome não pode estar vazio.\n"
    if not email or not is_valid_email(email):
        error_message += "Email inválido.\n"
    if not phone or not is_valid_phone(phone):
        error_message += "Telefone inválido. Deve conter apenas números e ter entre 10 e 15 dígitos.\n"
    if not password:
        error_message += "Senha não pode estar vazia.\n"
    if not confirm_password:
        error_message += "Confirme a Senha não pode estar vazio.\n"
    if password and confirm_password and not passwords_match(password, confirm_password):
        error_message += "As senhas não correspondem.\n"

    return error_message

# Função para validar o login

def validate_login():
    email = entry_1.get()
    password = entry_2.get()
    error_message = ""

    if not email or not is_valid_email(email):
        error_message += "Email inválido.\n"
    if not password:
        error_message += "Senha não pode estar vazia.\n"

    if error_message:
        error_label.config(text=error_message, fg="red")
    else:
        error_label.config(text="Login realizado com sucesso!", fg="green")
        print("Login realizado")
        open_conversor_window()
        # Aqui
# função que ira construir a tela de register

def open_registration_window():
    """
    Cria e exibe uma tela de registro com campos de entrada de usuário e um botão de registro.

    - Usa Tkinter para elementos da GUI.
    - Fornece feedback visual por meio de mudanças de cor para o campo de número de telefone e mensagens de erro.
    - Inclui marcadores de posição para validação (`validar_entradas`) e lógica de registro (`registrar`).
    """

    registration_window = Toplevel(window)
    registration_window.geometry("800x800")
    registration_window.configure(bg="#F39421")
    registration_window.title("Cadastro")

    # Cria um canvas para a janela de registro

    registration_canvas = Canvas(
        registration_window,
        bg="#F39421",
        height=800,
        width=800,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    registration_canvas.place(x=0, y=0)

    # =============================================

    # Texto do título

    registration_canvas.create_text(
        50.0,
        20.0,
        anchor="nw",
        text="Cadastro",
        fill="#FFFDFD",
        font=("MontserratItalic Medium", 48 * -1)
    )

    # ============================================

    

    # Lista de campos do formulário

    fields = ["Nome", "Email", "Telefone", "Senha", "Confirme a Senha"]
    entry_fields = []
    for i, field in enumerate(fields):
        entry = Entry(
            registration_window,
            bd=0,
            bg="#FFFDFD" if i != 2 else "#FFFFFF",  
            fg="#000716",
            highlightthickness=0,
            font=("Helvetica", 16),
            show="*" if "Senha" in field else ""
        )
        entry.place(
            x=35.0,
            y=140.0 + i * 100,
            width=730.0,
            height=50.0
        )
        entry_fields.append(entry)

        registration_canvas.create_text(
            45.0,
            110.0 + i * 100,
            anchor="nw",
            text=field,
            fill="#FFFFFF",
            font=("Lato Medium", 18 * -1)
        )

        # ==================================================
   
    def register():
        values = [entry.get() for entry in entry_fields]
        error_message = validate_inputs(*values)

        if error_message:
            registration_error_label.config(text=error_message, fg="red")
        else:
            registration_error_label.config(text="Cadastro realizado com sucesso!", fg="green")
            print("Cadastro realizado")
            

    # Adicione um botão para o registro
            
    registration_button = Button(
        registration_window,
        text="Register",
        font=("Helvetica", 16),
        bg="#4CAF50",
        fg="white",
        borderwidth=0,
        highlightthickness=0,
        command=register,
        relief="flat"
    )
    registration_button.place(
        x=250.0,
        y=620.0,
        width=278.0,
        height=78.0
    )

    # ========================================================

    # Adicione um rótulo para exibir mensagens de erro, se houver
    registration_error_label = Label(
        registration_window,
        text="",
        bg="#F39421",
        font=("Helvetica", 14)
    )
    registration_error_label.place(
        x=35.0,
        y=710.0,
        width=730.0,
        height=50.0
    )

    # =====================================================

 

# Função para realizar a conversão
def converter():
    try:
        moeda_de_valor = moeda_de.get()
        moeda_para_valor = moeda_para.get()
        valor_entrada = float(entrada_valor.get().replace(',', '.'))  # Tratamento para aceitar vírgula como separador decimal

        # Chamada à API para obter as taxas de câmbio
        url = f'https://api.exchangerate-api.com/v4/latest/{moeda_de_valor}'
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            taxa_cambio = data['rates'][moeda_para_valor]
            valor_convertido = valor_entrada * taxa_cambio
            
            # Formatação do valor convertido para exibição
            simbolo_moeda = dict_moedas.get(moeda_para_valor, moeda_para_valor)
            valor_formatado = f"{simbolo_moeda} {valor_convertido:.2f}"
            
            # Atualiza o label com o resultado da conversão
            app_resultado.config(text=valor_formatado)
        else:
            messagebox.showerror('Erro!', 'Falha ao obter as taxas de câmbio. Tente novamente mais tarde.')

    except Exception as e:
        messagebox.showerror('Erro!', f'Ocorreu um erro na conversão: {str(e)}')

def open_conversor_window():
    conversor_window = Toplevel(window)
    conversor_window.geometry("776x654")
    conversor_window.configure(bg="#FFFFFF")
    conversor_window.title("Conversor")

    moeda = ['USD', 'BRL', 'EUR', 'CAD', 'AUD', 'CHF', 'JPY', 'RUB', 'INR', 'AOA']
    global dict_moedas
    dict_moedas = {
        'USD': '$',
        'BRL': 'R$',
        'EUR': '€',
        'CAD': 'C$',
        'AUD': 'A$',
        'CHF': 'Fr',
        'JPY': '¥',
        'RUB': 'RUB',
        'INR': '₹',
        'AOA': 'Kz'
    }

    # Canvas para elementos gráficos
    canvas = Canvas(
        conversor_window,
        bg="#FFFFFF",
        height=654,
        width=776,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Imagem de fundo no canvas
    image_image_1 = PhotoImage(file=relative_to_assets_converso("tela.png"))
    canvas.create_image(388.0, 327.0, image=image_image_1)

    # Texto informativo no canvas
    canvas.create_text(
        33.0,
        241.0,
        anchor="nw",
        text="Digite o valor em",
        fill="#000000",
        font=("Inter Medium", 16 * -1)
    )

    # Label de resultado da conversão
    global app_resultado
    app_resultado = Label(
        conversor_window,
        text='',
        width=16,
        height=2,
        anchor='center',
        font=('Ivy 15 bold'),
        bg='#FFFFFF',
        fg='#333333'
    )
    app_resultado.place(x=430, y=335, width=315, height=80)

    # Entrada para o valor a ser convertido
    global entrada_valor
    entrada_valor = Entry(
        conversor_window,
        width=22,
        justify='center',
        font=('Ivy 12 bold'),
        relief='solid',
        bg='#FFFFFF',
        fg='#000000'
    )
    entrada_valor.place(x=40, y=335, width=310, height=80)

    # Dropdown de seleção de moeda "De"
    global moeda_de
    moeda_de = StringVar()
    moeda_de.set(moeda[0])

    dropdown_de = OptionMenu(
        conversor_window,
        moeda_de,
        *moeda
    )
    dropdown_de.config(
        width=8,
        font=('Ivy 12 bold'),
        bg='#FFFFFF',
        fg='#333333',
        relief='solid'
    )
    dropdown_de.place(x=200, y=235)

    # Dropdown de seleção de moeda "Para"
    global moeda_para
    moeda_para = StringVar()
    moeda_para.set(moeda[1])  # Define o valor inicial do dropdown

    dropdown_para = OptionMenu(
        conversor_window,
        moeda_para,
        *moeda
    )
    dropdown_para.config(
        width=8,
        font=('Ivy 12 bold'),
        bg='#FFFFFF',
        fg='#333333',
        relief='solid'
    )
    dropdown_para.place(x=578, y=233, width=180, height=32)

    # Texto informativo no canvas
    canvas.create_text(
        429.0,
        237.0,
        anchor="nw",
        text="Esse é o valor em",
        fill="#000000",
        font=("Inter Medium", 16 * -1)
    )

 # Botão de conversão (imagem)
    button_image_1 = PhotoImage(file=relative_to_assets_converso("conversor_button.png"))
    button_1 = Button(
    conversor_window,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=converter,
        relief="flat"
    )

    # Adicione o botão ao canvas na posição específica desejada
    canvas.create_window(200, 565, window=button_1)  # Ajuste as coordenadas conforme necessário

    # Executar o loop principal
    conversor_window.mainloop()

    

# construção da tela de login 
    
window = Tk()
window.geometry("800x800")
window.configure(bg="#F39421")

# Create a canvas
canvas = Canvas(
    window,
    bg="#F39421",
    height=800,
    width=800,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Add title text
canvas.create_text(
    50.0,
    20.0,
    anchor="nw",
    text="Convertion Cash",
    fill="#FFFDFD",
    font=("MontserratItalic Medium", 48 * -1)
)

# Create entry fields
entry_1 = Entry(
    bd=0,
    bg="#FFFDFD",
    fg="#000716",
    highlightthickness=0,
    font=("Helvetica", 16)
)
entry_1.place(
    x=35.0,
    y=280.0,
    width=730.0,
    height=50.0
)

entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
    font=("Helvetica", 16),
    show="*"
)
entry_2.place(
    x=35.0,
    y=380.0,
    width=730.0,
    height=50.0
)

# Add labels
canvas.create_text(
    45.0,
    250.0,
    anchor="nw",
    text="Digite o seu email",
    fill="#FFFDFD",
    font=("Lato Medium", 24 * -1)
)

canvas.create_text(
    45.0,
    350.0,
    anchor="nw",
    text="Digite a sua senha",
    fill="#FFFDFD",
    font=("Lato Medium", 24 * -1)
)

canvas.create_text(
    45.0,
    290.0,
    anchor="nw",
    text="Email",
    fill="#FFFFFF",
    font=("Lato Medium", 18 * -1)
)

canvas.create_text(
    45.0,
    390.0,
    anchor="nw",
    text="Senha",
    fill="#FFFFFF",
    font=("Lato Medium",
18 * -1)
)

# Add buttons
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=validate_login, 
    relief="flat"
)
button_1.place(
    x=250.0,
    y=480.0,
    width=278.0,
    height=78.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=open_registration_window,
    relief="flat"
)
button_2.place(
    x=250.0,
    y=600.0,
    width=278.0,
    height=78.0
)

# Add error label
error_label = Label(
    window,
    text="",
    bg="#F39421",
    font=("Helvetica", 14)
)
error_label.place(
    x=35.0,
    y=700.0,
    width=730.0,
    height=50.0
)

# Run the main loop
window.resizable(False, False)
window.mainloop()








'''
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, Label, Toplevel
import re

# Define o caminho de saída
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Função para validar o email
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Função para validar o número de telefone
def is_valid_phone(phone):
    return re.match(r"^\d{10,15}$", phone)

# Função para verificar se a senha e a confirmação da senha correspondem
def passwords_match(password, confirm_password):
    return password == confirm_password

# Função para validar todos os campos de entrada
def validate_inputs(name, email, phone, password, confirm_password):
    error_message = ""

    if not name:
        error_message += "Nome não pode estar vazio.\n"
    if not email or not is_valid_email(email):
        error_message += "Email inválido.\n"
    if not phone or not is_valid_phone(phone):
        error_message += "Telefone inválido. Deve conter apenas números e ter entre 10 e 15 dígitos.\n"
    if not password:
        error_message += "Senha não pode estar vazia.\n"
    if not confirm_password:
        error_message += "Confirme a Senha não pode estar vazio.\n"
    if password and confirm_password and not passwords_match(password, confirm_password):
        error_message += "As senhas não correspondem.\n"

    return error_message

# Função para validar a entrada no campo de telefone
def validate_phone_entry(char):
    return char.isdigit() or char == ""

# Função para validar a entrada no campo de nome
def validate_name_entry(char):
    return char.isalpha() or char == ""

def open_registration_window():
    registration_window = Toplevel(window)
    registration_window.geometry("800x800")
    registration_window.configure(bg="#F39421")
    registration_window.title("Cadastro")

    registration_canvas = Canvas(
        registration_window,
        bg="#F39421",
        height=800,
        width=800,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    registration_canvas.place(x=0, y=0)

    registration_canvas.create_text(
        50.0,
        20.0,
        anchor="nw",
        text="Cadastro",
        fill="#FFFDFD",
        font=("MontserratItalic Medium", 48 * -1)
    )

    fields = ["Nome", "Email", "Telefone", "Senha", "Confirme a Senha"]
    entry_fields = []
    for i, field in enumerate(fields):
        entry = Entry(
            registration_window,
            bd=0,
            bg="#FFFDFD" if i != 2 else "#FFFFFF",  # Cor diferente para o campo de telefone
            fg="#000716",
            highlightthickness=0,
            font=("Helvetica", 16),
            show="*" if "Senha" in field else ""
        )
        entry.place(
            x=35.0,
            y=140.0 + i * 100,
            width=730.0,
            height=50.0
        )
        
        if field == "Telefone":
            validate_cmd = (registration_window.register(validate_phone_entry), "%S")
            entry.config(validate="key", validatecommand=validate_cmd)
        elif field == "Nome":
            validate_cmd = (registration_window.register(validate_name_entry), "%S")
            entry.config(validate="key", validatecommand=validate_cmd)

        entry_fields.append(entry)

        registration_canvas.create_text(
            45.0,
            110.0 + i * 100,
            anchor="nw",
            text=field,
            fill="#FFFFFF",
            font=("Lato Medium", 18 * -1)
        )

    # Função para lidar com o evento de registro
    def register():
        values = [entry.get() for entry in entry_fields]
        error_message = validate_inputs(*values)

        if error_message:
            registration_error_label.config(text=error_message, fg="red")
        else:
            registration_error_label.config(text="Cadastro realizado com sucesso!", fg="green")
            print("Cadastro realizado")
            # Aqui você pode adicionar o código para realmente realizar o cadastro

    # Adicione um botão para o registro
    registration_button = Button(
        registration_window,
        text="Registrar",
        font=("Helvetica", 16),
        bg="#4CAF50",
        fg="white",
        borderwidth=0,
        highlightthickness=0,
        command=register,
        relief="flat"
    )
    registration_button.place(
        x=250.0,
        y=620.0,
        width=278.0,
        height=78.0
    )

    # Adicione um rótulo para exibir mensagens de erro, se houver
    registration_error_label = Label(
        registration_window,
        text="",
        bg="#F39421",
        font=("Helvetica", 14)
    )
    registration_error_label.place(
        x=35.0,
        y=710.0,
        width=730.0,
        height=50.0
    )

# Função para validar o login


# Create the main window
window = Tk()
window.geometry("800x800")
window.configure(bg="#F39421")

# Create a canvas
canvas = Canvas(
    window,
    bg="#F39421",
    height=800,
    width=800,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Add title text
canvas.create_text(
    50.0,
    20.0,
    anchor="nw",
    text="Convertion Cash",
    fill="#FFFDFD",
    font=("MontserratItalic Medium", 48 * -1)
)

# Create entry fields
entry_1 = Entry(
    bd=0,
    bg="#FFFDFD",
    fg="#000716",
    highlightthickness=0,
    font=("Helvetica", 16)
)
entry_1.place(
    x=35.0,
    y=280.0,
    width=730.0,
    height=50.0
)

entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
    font=("Helvetica", 16),
    show="*"
)
entry_2.place(
    x=35.0,
    y=380.0,
    width=730.0,
    height=50.0
)

# Add labels
canvas.create_text(
    45.0,
    250.0,
    anchor="nw",
    text="Digite o seu email",
    fill="#FFFDFD",
    font=("Lato Medium", 24 * -1)
)

canvas.create_text(
    45.0,
    350.0,
    anchor="nw",
    text="Digite a sua senha",
    fill="#FFFDFD",
    font=("Lato Medium", 24 * -1)
)

canvas.create_text(
    45.0,
    290.0,
    anchor="nw",
    text="Email",
    fill="#FFFFFF",
    font=("Lato Medium", 18 * -1)
)

canvas.create_text(
    45.0,
    390.0,
    anchor="nw",
    text="Senha",
    fill="#FFFFFF",
    font=("Lato Medium", 18 * -1)
)

# Add buttons

button_1 = Button(
    text="Login",
    borderwidth=0,
    highlightthickness=0,
    command=validate_login,
    relief="flat"
)
button_1.place(
    x=250.0,
    y=480.0,
    width=278.0,
    height=78.0
)


button_2 = Button(
    text="Registrar",
    borderwidth=0,
    highlightthickness=0,
    command=open_registration_window,
    relief="flat"
)
button_2.place(
    x=250.0,
    y=600.0,
    width=278.0,
    height=78.0
)

# Add error label
error_label = Label(
    window,
    text="",
    bg="#F39421",
    font=("Helvetica", 14)
)
error_label.place(
    x=35.0,
    y=700.0,
    width=730.0,
    height=50.0
)

# Run the main loop
window.resizable(False, False)
window.mainloop()

'''
