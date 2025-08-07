import tkinter as tk
from tkinter import ttk, messagebox, font
import logging
import os

# Importar Pillow se disponível, para suportar mais formatos de imagem
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logging.warning("Pillow não está instalado. Imagens PNG/JPG não funcionarão.")

# --- Definições de Cores e Fontes ---
BG_COLOR = '#f0f0f0'
PRIMARY_COLOR = '#3498db'
SECONDARY_COLOR = '#2980b9'
TEXT_COLOR = '#1C1C1C'
HEADER_COLOR = '#2c3e50'
WHITE_COLOR = '#ffffff'
HOVER_BG_COLOR = '#eaf2f8' # Um azul claro para campos em foco

# --- Classe da Janela Principal ---
class MainWindow(ttk.Frame):
    def __init__(self, master, controller, project_root_dir, *args, **kwargs):
        """
        Inicializa a janela principal da aplicação GUI.

        Args:
            master: O widget pai (geralmente a janela root do Tkinter).
            controller: A instância do MainController para interagir com a lógica de backend.
            project_root_dir: Caminho para o diretório raiz do projeto para carregar assets.
        """
        super().__init__(master, *args, **kwargs)
        self.controller = controller
        self.master = master
        self.project_root_dir = project_root_dir # Guardar o caminho raiz

        self.master.title("Guia de Praias - Previsão Meteorológica")
        self.master.minsize(800, 800) # Tamanho mínimo da janela
        self.master.configure(bg=BG_COLOR)

        # --- Configuração de Estilos ttk ---
        self.style = ttk.Style(self.master)
        self._configure_styles()

        # --- Variáveis de Controle ---
        self.selected_location_name = tk.StringVar() # Guarda o nome da localização selecionada
        self.location_names = [] # Lista de nomes de locais a serem exibidos no combobox
        self.combo_location = None # Widget Combobox
        self.result_labels = {} # Dicionário para armazenar os widgets de resultado {key: label_widget}

        # --- Carregar Assets (Logotipo e Fundo) ---
        self.logo_image_tk = None # Referência para a imagem do logo carregada pelo Tkinter
        self.background_image_tk = None # Referência para a imagem de fundo carregada pelo Tkinter
        self._load_assets() # Carrega assets e configura o grid principal

        # --- Criar Widgets da UI ---
        self._create_widgets()

        # --- Carregar localizações iniciais para o Combobox ---
        self._load_locations_into_combobox()

    def _configure_styles(self):
        """Configura os estilos personalizados para widgets ttk."""
        self.style.theme_use('clam')

        # Estilos gerais para frames e botões
        self.style.configure('TFrame', background=BG_COLOR)
        self.style.configure('Header.TFrame', background=HEADER_COLOR)

        # Estilo para o título principal
        self.style.configure('Header.TLabel',
                             font=font.Font(family='Helvetica', size=18, weight='bold'),
                             background=PRIMARY_COLOR, foreground=WHITE_COLOR)

        # Estilo para o frame de conteúdo principal
        self.style.configure('Content.TFrame', background=BG_COLOR, padding=(20, 10))

        # Estilo para Labels de descrição (input labels)
        self.style.configure('TLabel', background=BG_COLOR, foreground=TEXT_COLOR,
                             font=font.Font(family='Helvetica', size=10))
        self.style.configure('LocationLabel.TLabel',
                             font=font.Font(family='Helvetica', size=12, weight='bold'),
                             foreground=PRIMARY_COLOR)

        # Estilo para Entradas (Caixas de texto) e Combobox
        entry_style_options = {
            'font': font.Font(family='Helvetica', size=10),
            'padding': (5, 8), 'relief': 'flat', 'fieldbackground': WHITE_COLOR,
            'borderwidth': 1, 'foreground': TEXT_COLOR
        }
        self.style.configure('TEntry', **entry_style_options)
        self.style.configure('TCombobox', **entry_style_options)

        # Mapeamento de cores para os estados de foco/hover dos widgets
        self.style.map('TEntry',
                       fieldbackground=[('focus', HOVER_BG_COLOR)],
                       foreground=[('focus', TEXT_COLOR)],
                       borderwidth=[('focus', 2)],
                       relief=[('focus', 'solid')])
        self.style.map('TCombobox',
                       fieldbackground=[('readonly', WHITE_COLOR), ('!readonly', WHITE_COLOR)],
                       selectbackground=[('readonly', HOVER_BG_COLOR)],
                       selectforeground=[('readonly', TEXT_COLOR)],
                       background=[('!disabled', WHITE_COLOR)],
                       foreground=[('!disabled', TEXT_COLOR)],
                       bordercolor=[('focus', PRIMARY_COLOR)])

        # Estilo para Botões de Ação
        button_style_options = {
            'font': font.Font(family='Helvetica', size=10, weight='bold'),
            'padding': 10, 'relief': 'flat',
            'background': PRIMARY_COLOR, 'foreground': WHITE_COLOR,
            'borderwidth': 0
        }
        self.style.configure('TButton', **button_style_options)
        self.style.map('TButton',
                       background=[('active', SECONDARY_COLOR)],
                       foreground=[('active', WHITE_COLOR)])

        # Estilo para um botão de "pesquisa" secundário (ex: verde)
        self.style.configure('Search.TButton',
                             font=font.Font(family='Helvetica', size=10, weight='bold'),
                             padding=10, relief='flat',
                             background='#2ecc71', foreground=WHITE_COLOR)
        self.style.map('Search.TButton',
                       background=[('active', '#27ae60')])

        # Estilo para Labels que mostram os resultados da previsão
        self.style.configure('Result.TLabel',
                             font=font.Font(family='Helvetica', size=10),
                             background=BG_COLOR, foreground=TEXT_COLOR,
                             padding=(0, 5))
        self.style.configure('ResultKey.TLabel',
                             font=font.Font(family='Helvetica', size=10, weight='bold'),
                             background=BG_COLOR, foreground=PRIMARY_COLOR,
                             padding=(0, 5))


    def _load_assets(self):
        """Tenta carregar o logotipo e a imagem de fundo, e configura o grid principal."""
        # --- Preparar a grade principal do master para o canvas de fundo ---
        self.master.grid_rowconfigure(0, weight=1) # Linha 0 (canvas/fundo/header) expande verticalmente
        self.master.grid_rowconfigure(1, weight=4) # Linha 1 (conteúdo principal) expande mais
        self.master.grid_columnconfigure(0, weight=1) # Coluna 0 (tudo centralizado) expande horizontalmente

        # --- Carregar Imagem de Fundo ---
        background_filename = "fundo_praias.png"
        background_path = os.path.join(self.project_root_dir, background_filename)

        if PIL_AVAILABLE:
            try:
                img = Image.open(background_path)
                self.background_image_tk = ImageTk.PhotoImage(img)
                logging.info(f"Imagem de fundo carregada de: {background_path}")
            except FileNotFoundError:
                logging.warning(f"Arquivo de fundo não encontrado em: {background_path}. Usando fundo padrão da janela.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar fundo: {e}")
                logging.error(f"Erro ao carregar fundo ({background_path}): {e}")

        # Criar um canvas para o fundo e o logo. Ele ocupa a linha 0, coluna 0.
        self.canvas_background = tk.Canvas(self.master, highlightthickness=0)
        self.canvas_background.grid(row=0, column=0, sticky="nsew")

        if self.background_image_tk:
            self.canvas_background.create_image(0, 0, image=self.background_image_tk, anchor="nw", tags="background_image")
            self.canvas_background.image = self.background_image_tk # Manter referência
            # Vincular evento de redimensionamento para ajustar a imagem de fundo
            self.canvas_background.bind("<Configure>", self._resize_background_image)
        else:
            # Se não houver imagem de fundo, o canvas fica transparente.
            pass

        # --- Carregar Logotipo ---
        logo_filename = "logo_praias.png"
        logo_path = os.path.join(self.project_root_dir, logo_filename)

        if PIL_AVAILABLE:
            try:
                img = Image.open(logo_path)
                # Redimensionar o logo para um tamanho fixo (ex: 150x50 pixels)
                img = img.resize((150, 50), Image.Resampling.LANCZOS)
                self.logo_image_tk = ImageTk.PhotoImage(img)
                logging.info(f"Logotipo carregado de: {logo_path}")
                # Colocar o logo DENTRO do canvas_background usando create_window
                logo_label = ttk.Label(self.master, image=self.logo_image_tk, style="TLabel", background= HOVER_BG_COLOR)
                # Posiciona o logo no canvas (canto superior esquerdo com padding)
                self.canvas_background.create_window(20, 10, window=logo_label, anchor="nw")
            except FileNotFoundError:
                logging.warning(f"Logotipo não encontrado em: {logo_path}. Nenhum logotipo será exibido.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar logotipo: {e}")
                logging.error(f"Erro ao carregar logotipo ({logo_path}): {e}")
        else:
            logging.warning("Pillow não disponível. Não será possível carregar o logotipo.")

    def _resize_background_image(self, event):
        """Redimensiona a imagem de fundo ao redimensionar a janela."""
        # Apenas redimensiona se PIL estiver disponível e o arquivo de fundo existir
        if PIL_AVAILABLE and os.path.exists(os.path.join(self.project_root_dir, "fundo_praias.png")):
            try:
                new_width = event.width
                new_height = event.height
                
                if new_width <= 0 or new_height <= 0: # Evita erros com dimensões zero
                    return

                original_image = Image.open(os.path.join(self.project_root_dir, "fundo_praias.png"))
                resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                self.background_image_tk = ImageTk.PhotoImage(resized_image)

                # Atualizar a imagem no canvas, usando o método de deleção e recreação para garantir
                self.canvas_background.delete("background_image") # Remove a imagem antiga
                self.canvas_background.create_image(0, 0, image=self.background_image_tk, anchor="nw", tags="background_image")
                self.canvas_background.image = self.background_image_tk # Manter a referência atualizada
            except Exception as e:
                logging.error(f"Erro ao redimensionar imagem de fundo: {e}")

    def _create_widgets(self):
        """Cria e posiciona os elementos da UI."""

        # --- Frame para o Cabeçalho ---
        header_frame = ttk.Frame(self.master, style='Header.TFrame')
        header_label = ttk.Label(header_frame, text="Previsão do Tempo - Escolha a localização", style='Header.TLabel')
        header_label.pack(fill='both', expand=True) # O 'label' preenche o 'header_frame'

        # Posicionar o frame do cabeçalho no canvas de fundo (centralizado no topo)
        # Force o cálculo a fazer o update para obter as dimensões corretas antes de posicionar
        self.master.update_idletasks() # Esta linha é CRÍTICA para obter dimensões corretas no início
        self.canvas_background.create_window(self.master.winfo_width() / 2, 30, window=header_frame, anchor="n")

        # --- Frame para o Conteúdo Principal (inputs e resultados) ---
        # Este frame será colocado na segunda "linha" do grid principal do master (linha=1).
        self.content_frame = ttk.Frame(self.master, style='Content.TFrame')
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20) # Corrigido: Fechado o parêntese e adicionado sticky/padx/pady
        
        # Definir que a coluna 1 do content_frame (onde ficam os inputs e valores) se expande
        self.content_frame.grid_columnconfigure(1, weight=1)

        # --- Campos de Localização ---
        ttk.Label(self.content_frame, text="Localização:", style='TLabel').grid(row=0, column=0, sticky="w", padx=(0, 10), pady=10)

        # Combobox para selecionar a localização
        self.combo_location = ttk.Combobox(self.content_frame, state="readonly", textvariable=self.selected_location_name, style='TCombobox')
        self.combo_location.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        self.combo_location.bind("<<ComboboxSelected>>", self._on_location_selected)
        
        # --- Botão de Busca ---
        search_button = ttk.Button(self.content_frame, text="Previsão Completa", command=self._search_button_command, style='Search.TButton')
        search_button.grid(row=1, column=0, columnspan=2, pady=20)

        # --- Área de Exibição de Resultados ---
        # Criar um frame para conter os resultados da previsão
        self.results_frame = ttk.Frame(self.content_frame, style='Content.TFrame')
        self.results_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=15)
        self.results_frame.grid_columnconfigure(1, weight=1) # A coluna de valores se expande

        # Título da seção de resultados (inicialmente vazio ou com placeholder)
        self.current_location_display = ttk.Label(self.results_frame, text="Previsão para: (Selecione um local)", style='LocationLabel.TLabel')
        self.current_location_display.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        # Iniciar o layout para expor os dados dinamicamente.
        # populate_results_area irá criar os Labels que armazenaremos em self.result_labels
        self.populate_results_area(self.results_frame)

    def populate_results_area(self, parent_frame):
        """Cria os rótulos dinamicamente para exibir os dados da previsão."""
        # Definir os campos que queremos mostrar e os seus rótulos (chaves e texto)
        self.fields_to_display_order = [
            ("forecast_date", "Data:"),
            ("temp_min", "Temp. Mínima:"),
            ("temp_max", "Temp. Máxima:"),
            ("weather_description", "Condição do Tempo:"),
            ("wind_dir", "Direção do Vento:"),
            ("wind_speed_description", "Velocidade do Vento:"),
        ]

        row_num = 1 # Começa na linha 1, pois a linha 0 é o título "Previsão para:"
        for key, label_text in self.fields_to_display_order:
            # Rótulo para a chave (ex: "Data:")
            key_label = ttk.Label(parent_frame, text=label_text, style='ResultKey.TLabel')
            key_label.grid(row=row_num, column=0, sticky="w", padx=(0, 10))
            
            # Rótulo para o valor (onde os dados reais serão exibidos)
            value_label = ttk.Label(parent_frame, text="-", style='Result.TLabel') # Texto inicial vazio
            value_label.grid(row=row_num, column=1, sticky="w")
            
            # Armazenar o value_label no dicionário self.result_labels para fácil atualização futura
            self.result_labels[key] = value_label
            row_num += 1

    def _load_locations_into_combobox(self):
        """Carrega a lista de locais da API e popula o Combobox."""
        logging.info("A carregar locais para o Combobox...")
        try:
            # Chama o MainController para obter os nomes dos locais disponíveis
            self.location_names = self.controller.get_available_location_names()
            self.location_names.sort() # Ordena alfabeticamente para melhor usabilidade

            if not self.location_names:
                messagebox.showwarning("Erro de Carregamento", "Não foi possível carregar a lista de locais. Verifique sua conexão com a internet ou a API do IPMA.")
                logging.warning("Lista de locais vazia ou não carregada.")
                self.combo_location['values'] = ["Nenhum local disponível"]
                self.combo_location.set("Nenhum local disponível")
                self.combo_location['state'] = 'disabled' # Desativar o combobox
            else:
                self.combo_location['values'] = self.location_names
                self.combo_location.set("Selecione um local...") # Texto inicial do combobox
                self.combo_location['state'] = 'readonly' # Permitir seleção, mas não edição
                logging.info(f"Carregados {len(self.location_names)} locais no Combobox.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar locais: {e}")
            logging.error(f"Erro ao carregar locais no combobox: {e}")
            self.combo_location['values'] = ["Erro ao carregar"]
            self.combo_location.set("Erro ao carregar")
            self.combo_location['state'] = 'disabled' # Desativar o combobox

    def _on_location_selected(self, event):
        """Evento acionado quando uma localização é selecionada no Combobox."""
        selected_name = self.selected_location_name.get()
        logging.info(f"Localização selecionada: {selected_name}")
        # O controller precisa ser notificado da mudança para definir a localização atual
        success = self.controller.set_location_by_name(selected_name)
        if not success:
            messagebox.showwarning("Erro de Seleção", f"Não foi possível definir '{selected_name}' como localização atual.")
            logging.error(f"Falha ao definir localização por nome: {selected_name}")

    def _search_button_command(self):
        """Comando acionado ao clicar no botão 'Buscar Previsão'."""
        logging.info("Botão 'Buscar Previsão' clicado.")
        if not self.controller.current_location_id:
            messagebox.showwarning("Aviso", "Selecione primeiro uma localização!")
            logging.warning("Tentativa de buscar previsão sem localização selecionada.")
            return

        # Busca e processa os dados da previsão
        success = self.controller.fetch_and_display_forecast()

        if success:
            forecast_data = self.controller.get_current_weather_data()
            if forecast_data:
                # Atualiza o título da seção de previsão
                self.current_location_display.config(text=f"Previsão para: {forecast_data.get('location_name', 'N/A')}")
                # Atualiza os Labels com os dados da previsão
                self._update_results_display(forecast_data)
                logging.info("Previsão exibida com sucesso.")
            else:
                messagebox.showerror("Erro de Dados", "Dados de previsão não foram processados corretamente.")
                logging.error("Dados de previsão ausentes após fetch_and_display_forecast.")
                self._clear_results_display() # Limpa os resultados em caso de erro
        else:
            messagebox.showerror("Erro de Previsão", f"Não foi possível obter a previsão para {self.controller.current_location_name}.")
            logging.error(f"Falha ao obter/exibir previsão para {self.controller.current_location_name}.")
            self._clear_results_display() # Limpa os resultados em caso de erro

    def _update_results_display(self, data):
        """Atualiza os rótulos da seção de resultados com os novos dados."""
        for key, _ in self.fields_to_display_order:
            if key in self.result_labels:
                value = data.get(key, 'N/A')
                # Adiciona unidades apropriadas para temperaturas
                if key in ["temp_min", "temp_max"] and value != 'N/A':
                    value = f"{value}°C"
                self.result_labels[key].config(text=value)

    def _clear_results_display(self):
        """Limpa o display de resultados."""
        self.current_location_display.config(text="Previsão para: (Selecione um local)")
        for key in self.result_labels:
            self.result_labels[key].config(text="-")

