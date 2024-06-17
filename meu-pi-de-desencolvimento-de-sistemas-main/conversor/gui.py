from tkinter import Tk, Canvas, Label, Entry, Button, PhotoImage, StringVar, OptionMenu, messagebox
from pathlib import Path
import requests

# Função para obter o caminho relativo aos assets
def relative_to_assets(path: str) -> str:
    # Diretório onde o script está sendo executado
    script_dir = Path(__file__).parent
    
   # Caminho relativo até a pasta assets
    assets_path = script_dir / "assets" / "frame"
    
    # Retorna o caminho absoluto completo até o arquivo desejado
    return str(assets_path / path)

# Definição da lista de moedas
moeda = ['USD', 'BRL', 'EUR', 'CAD', 'AUD', 'CHF', 'JPY', 'RUB', 'INR', 'AOA']

# Função para converter moedas
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

# Configuração da janela principal
window = Tk()
window.geometry("776x654")
window.configure(bg="#FFFFFF")

# Canvas para elementos gráficos
canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=654,
    width=776,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Imagem no canvas
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(388.0, 327.0, image=image_image_1)

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
app_resultado = Label(
    window,
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
entrada_valor = Entry(
    window,
    width=22,
    justify='center',
    font=('Ivy 12 bold'),
    relief='solid',
    bg='#FFFFFF',
    fg='#000000'
)
entrada_valor.place(x=40, y=335, width=310, height=80)

# Dropdown de seleção de moeda "De"
moeda_de = StringVar()
moeda_de.set(moeda[0])

dropdown_de = OptionMenu(
    window,
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
moeda_para = StringVar()
moeda_para.set(moeda[0])  # Define o valor inicial do dropdown

dropdown_para = OptionMenu(
    window,
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
dropdown_para.place(x=578.0, y=233.0, width=180.0, height=32.0)  # Posicionando o dropdown

# Texto informativo no canvas
canvas.create_text(
    429.0,
    237.0,
    anchor="nw",
    text="Esse é o valor em",
    fill="#FFFCFC",
    font=("Inter Medium", 16 * -1)
)

# Retângulo onde o resultado da conversão será exibido (mantido conforme solicitado)
canvas.create_rectangle(
    578.0,
    233.0,
    758.0,
    265.0,
    fill="#000000",
    outline=""
)

# Botão de conversão (imagem)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    window,
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=converter,  # Associando a função de conversão ao botão
    relief="flat"
)
button_1.place(
    x=94.0,
    y=502.0,
    width=216.0,
    height=65.0
)

# Dicionário para mapear símbolos de moedas
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

# Impedir o redimensionamento da janela
window.resizable(False, False)
window.mainloop()
