
import tkinter as tk
import logging
import sys
import os
import argparse # Importa o módulo argparse para a utilização de duas views

# --- Configuração do Path e Imports ---
project_root_dir = os.path.abspath(os.path.dirname(__file__))
if project_root_dir not in sys.path:
    sys.path.insert(0, project_root_dir)

# Importa as dependências do backend
from models.ipma_api import IPMAApi
from static_data.weather_glossary import get_weather_description, get_location_name, get_wind_speed_description
from controllers.main_controller import MainController

# Importa as classes de janela (ambas)
from views.main_window import MainWindow # A view mais "completa" (demais para o caso útil)
from views.minimal_window import MinimalWindow # A view mais "simples"


def setup_application_logging():
    """Configura o logging global para a aplicação."""
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        )
    logging.info("Logging configurado para a aplicação.")

def run_application():
    """Inicia a aplicação GUI."""
    setup_application_logging()
    logging.info("Iniciando a aplicação GUI...")

    # --- Configuração do argparse para escolher a view ---
    parser = argparse.ArgumentParser(description="Guia de Praias - Aplicação de Previsão Meteorológica.")
    parser.add_argument('--view', type=str, default='main',
                        choices=['main', 'minimal'],
                        help="Escolha a view a ser utilizada: 'main' (padrão) ou 'minimal'.")
    args = parser.parse_args()

    # --- Inicialização do Backend (Controller) ---
    ipma_api_instance = IPMAApi()
    main_controller = MainController(
        ipma_api=ipma_api_instance,
        weather_desc_func=get_weather_description,
        location_name_func=get_location_name,
        wind_desc_func=get_wind_speed_description
    )

    # --- Criação da Janela Principal (View Selecionada) ---
    root = tk.Tk()
    root.title("Guia de Praias - Previsão Meteorológica") # Define o título da aplicação
    root.geometry("800x600") # Define um tamanho inicial para a janela

    if args.view == 'minimal':
        logging.info("Utilizando a view: MinimalWindow")
        app_window = MinimalWindow(root, main_controller)
    else: # args.view == 'main' ou default
        logging.info("Utilizando a view: MainWindow")
        # PASSA project_root_dir AQUI:
        app_window = MainWindow(root, main_controller, project_root_dir)

    # Configuração para ambas as janelas para preencher o root
    app_window.grid(row=0, column=0, sticky="nsew")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # --- Loop Principal Tkinter ---
    root.mainloop()

if __name__ == "__main__":
    run_application()

