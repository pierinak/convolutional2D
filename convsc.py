import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib import pyplot as plt
from PIL import Image, ImageTk

# Função para aplicar um filtro de convolução
def aplicar_filtro(imagem, filtro):
    return cv2.filter2D(imagem, -1, filtro)

# Função para redimensionar a imagem
def redimensionar_imagem(imagem, largura_max, altura_max):
    altura, largura = imagem.shape[:2]
    if largura > largura_max or altura > altura_max:
        proporcao_largura = largura_max / largura
        proporcao_altura = altura_max / altura
        proporcao = min(proporcao_largura, proporcao_altura)
        nova_largura = int(largura * proporcao)
        nova_altura = int(altura * proporcao)
        imagem = cv2.resize(imagem, (nova_largura, nova_altura), interpolation=cv2.INTER_AREA)
    return imagem

# Função para carregar a imagem
def carregar_imagem():
    global imagem, imagem_original
    caminho_imagem = filedialog.askopenfilename()
    if caminho_imagem:
        imagem = cv2.imread(caminho_imagem, cv2.IMREAD_GRAYSCALE)
        if imagem is None:
            messagebox.showerror("Erro", "Erro ao carregar a imagem.")
            return
        imagem_original = imagem.copy()
        imagem = redimensionar_imagem(imagem, largura_max, altura_max)
        exibir_imagem(imagem)

# Função para exibir a imagem na interface
def exibir_imagem(img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)
    painel_imagem.config(image=img_tk)
    painel_imagem.image = img_tk

# Função para aplicar o filtro selecionado
def aplicar_filtro_selecionado():
    global imagem
    if imagem is None:
        messagebox.showwarning("Aviso", "Por favor, carregue uma imagem primeiro.")
        return

    filtro_selecionado = var_filtro.get()
    if filtro_selecionado == "Blur":
        filtro = np.ones((5, 5), np.float32) / 25
    elif filtro_selecionado == "Emboss":
        filtro = np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]])
    elif filtro_selecionado == "Identy":
        filtro = np.array([[0, 0, 0], [0, 1, -0], [0, 0, 0]])
    elif filtro_selecionado == "Bottom sobel":
        filtro = np.array ([[-1, -2, -1],[0, 0, 0],[1 , 2, 1]])
    elif filtro_selecionado == "Left sobel":
        filtro = np.array ([[1, 0 , -1],[2, 0, -2],[1, 0, -1]])
    elif filtro_selecionado == "Right sobel":
        filtro = np.array ([[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]])
    elif filtro_selecionado == "Top sobel":
        filtro = np.array ([[1, 2, 1],[0, 0, 0,],[-1, -2, -1]])
    elif filtro_selecionado == "Outline":
        filtro = np.array ([[-1, -1, -1],[-1, 8, -1],[-1, -1, -1]])
    elif filtro_selecionado == "Shapen":
        filtro = np.array ([[0, -1, 0],[-1, 5, -1],[0, -1, 0]])
    else:
        messagebox.showerror("Erro", "Filtro desconhecido.")
        return

    imagem_filtrada = aplicar_filtro(imagem, filtro)
    exibir_imagem(imagem_filtrada)

# Configuração da interface gráfica
root = tk.Tk()
root.title("Filtro de Imagem")
root.geometry("800x600")

# Definição do tamanho máximo da imagem
largura_max = 600
altura_max = 400

# Variável para armazenar a imagem
imagem = None
imagem_original = None

# Painel para exibir a imagem
painel_imagem = tk.Label(root)
painel_imagem.pack()

# Botão para carregar a imagem
btn_carregar = tk.Button(root, text="Carregar Imagem", command=carregar_imagem)
btn_carregar.pack()

# Opções de filtros
var_filtro = tk.StringVar(value="Blur")
frame_filtros = tk.Frame(root)
frame_filtros.pack()

tk.Radiobutton(frame_filtros, text="Blur", variable=var_filtro, value="Blur").pack(side=tk.LEFT)
tk.Radiobutton(frame_filtros, text="Emboss", variable=var_filtro, value="Emboss").pack(side=tk.LEFT)
tk.Radiobutton(frame_filtros, text="Identy", variable=var_filtro, value="Identy").pack(side=tk.LEFT)
tk.Radiobutton(frame_filtros, text="Bottom sobel", variable=var_filtro, value="Bottom sobel").pack(side=tk.LEFT)
tk.Radiobutton(frame_filtros, text="Right sobel", variable=var_filtro, value="Right sobel").pack(side=tk.LEFT)
tk.Radiobutton(frame_filtros, text="Top sobel", variable=var_filtro, value="Top sobel").pack(side=tk.LEFT)
tk.Radiobutton(frame_filtros, text="Outline", variable=var_filtro, value="Outline").pack(side=tk.LEFT)
tk.Radiobutton(frame_filtros, text="Shapen", variable=var_filtro, value="Shapen").pack(side=tk.LEFT)


# Botão para aplicar o filtro
btn_aplicar = tk.Button(root, text="Aplicar Filtro", command=aplicar_filtro_selecionado)
btn_aplicar.pack()

# Executa a interface
root.mainloop()
