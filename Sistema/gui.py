from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Label, Toplevel
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
    #command=validate_login,  # Você precisa definir essa função
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
