
import tkinter as tk
from tkinter import ttk, messagebox, font
import logging

# --- Definições de Cores (simplificadas) ---

PALETTE_PRIMARY = '#4285F4'
PALETTE_ACCENT = '#0F9D58'
PALETTE_TEXT_DARK = '#212121'
PALETTE_BACKGROUND = '#F5F5F5'
PALETTE_SURFACE = '#FFFFFF'
PALETTE_BORDER = '#BDBDBD'

# --- Classe da Janela Minimalista ---
class MinimalWindow(ttk.Frame):
    def __init__(self, master, controller, *args, **kwargs):
        """
        Inicializa a janela GUI minimalista.

        Args:
            master: O widget pai (a janela root do Tkinter).
            controller: A instância do MainController.
        """
        super().__init__(master, *args, **kwargs)
        self.controller = controller
        self.master = master

        self.master.title("Guia de Praias - Previsão (Minimalista)")
        self.master.geometry("340x400") # Tamanho fixo para simplicidade 
        self.master.configure(bg=PALETTE_BACKGROUND)

        # Configurar o grid do master (janela root) para que o frame da janela preencha tudo
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        
        # Este frame (MinimalWindow) auto posiciona-se no grid do master
        self.grid(row=0, column=0, sticky="nsew")

        # --- Configuração de Estilos ttk ---
        self.style = ttk.Style(self.master)
        self._configure_styles()

        # --- Variáveis de Controle ---
        self.selected_location_name = tk.StringVar()
        self.location_names = [] # Para armazenar os nomes dos locais
        self.combo_location = None # Referência ao widget Combobox

        # --- Chamar métodos para construir a UI ---
        self._create_widgets()
        self._load_locations_into_combobox() # Carrega os locais no combobox

    def _configure_styles(self):
        """Configura estilos ttk básicos para este exemplo."""
        self.style.theme_use('clam')

        # Estilo geral para o Frame principal da janela (MinimalWindow)
        self.style.configure('TFrame', background=PALETTE_BACKGROUND)

        # Estilo para o Cabeçalho
        self.style.configure('Header.TLabel',
                             font=font.Font(family='Helvetica', size=16, weight='bold'),
                             background=PALETTE_PRIMARY, foreground=PALETTE_BACKGROUND, padding=10) # Fundo primary, texto claro

        # Estilo para Labels padrão
        self.style.configure('TLabel', background=PALETTE_SURFACE, foreground=PALETTE_TEXT_DARK,
                             font=font.Font(family='Helvetica', size=10))

        # Estilo para Combobox
        self.style.configure('TCombobox',
                             font=font.Font(family='Helvetica', size=10),
                             padding=(5, 5), relief='flat', fieldbackground=PALETTE_SURFACE,
                             borderwidth=1, foreground=PALETTE_TEXT_DARK,
                             bordercolor=PALETTE_BORDER)
        self.style.map('TCombobox',
                       fieldbackground=[('readonly', PALETTE_SURFACE)],
                       bordercolor=[('focus', PALETTE_PRIMARY)])

        # Estilo para Botões
        self.style.configure('TButton',
                             font=font.Font(family='Helvetica', size=10, weight='bold'),
                             padding=8, relief='flat',
                             background=PALETTE_PRIMARY, foreground=PALETTE_BACKGROUND,
                             borderwidth=0)
        self.style.map('TButton',
                       background=[('active', PALETTE_ACCENT)]) # Cor para o botão "Buscar"

        # Estilo para a caixa de resultados
        self.style.configure('Results.TLabel', background=PALETTE_SURFACE, foreground=PALETTE_TEXT_DARK, font=('Helvetica', 10))


    def _create_widgets(self):
        """Cria e posiciona os elementos básicos da UI."""

        # --- Frame do Cabeçalho ---
        # Este cabeçalho ocupa a primeira linha do grid deste frame (MinimalWindow)
        header_frame = ttk.Frame(self, style='TFrame') # Usar o estilo TFrame padrão aqui, sem cor específica
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew") # Ocupa 2 colunas e expande horizontalmente
        # Um Label maior para o título
        ttk.Label(header_frame, text="Guia de Praias", style='Header.TLabel').pack(fill="x", expand=True)

        # --- Frame de Entrada (Seleção de Local) ---
        input_frame = ttk.Frame(self, style='TFrame', padding=10) # Padding interno
        input_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10) # Segunda linha do MinimalWindow
        input_frame.grid_columnconfigure(1, weight=1) # Coluna do combobox expande

        ttk.Label(input_frame, text="Localização:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.combo_location = ttk.Combobox(input_frame, state="readonly", textvariable=self.selected_location_name)
        self.combo_location.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.combo_location.bind("<<ComboboxSelected>>", self._on_location_selected) # Vincula o evento de seleção

        # --- Botão de Busca ---
        search_button = ttk.Button(self, text="Buscar Previsão", command=self._search_button_command)
        search_button.grid(row=2, column=0, columnspan=2, pady=10) # Terceira linha do MinimalWindow

        # --- Área de Resultados (Para o futuro - estática por enquanto) ---
        results_frame = ttk.Frame(self, style='TFrame', padding=10)
        results_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=10)
        results_frame.grid_columnconfigure(0, weight=1) # Faz o Label de resultados expandir
        
        # Um Label simples para mostrar a saída
        self.results_label = ttk.Label(results_frame, text="Selecione um local e clique em 'Buscar Previsão'.", style='Results.TLabel')
        self.results_label.pack(fill="both", expand=True)

        # Configurar as linhas para expandir adequadamente
        self.grid_rowconfigure(3, weight=1) # Faz a área de resultados expandir mais

    def _load_locations_into_combobox(self):
        """Carrega a lista de locais do MainController e popula o Combobox."""
        logging.info("A carregar locais para o Combobox...")
        try:
            # Chama o MainController para obter os nomes dos locais disponíveis
            self.location_names = self.controller.get_available_location_names()
            self.location_names.sort() # Ordena alfabeticamente
            
            if not self.location_names:
                messagebox.showwarning("Erro de Carregamento", "Não foi possível carregar a lista de locais. Verifique sua conexão com a internet ou a API do IPMA.")
                logging.warning("Lista de locais vazia ou não carregada.")
                self.combo_location['values'] = ["Nenhum local disponível"]
                self.combo_location.set("Nenhum local disponível")
                self.combo_location['state'] = 'disabled' # Desativa o combobox
            else:
                self.combo_location['values'] = self.location_names
                self.combo_location.set("Selecione um local...") # Texto inicial
                self.combo_location['state'] = 'readonly' # Permite seleção, não edição
                logging.info(f"Carregados {len(self.location_names)} locais no Combobox.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar locais: {e}")
            logging.error(f"Erro ao carregar locais no combobox: {e}")
            self.combo_location['values'] = ["Erro ao carregar"]
            self.combo_location.set("Erro ao carregar")
            self.combo_location['state'] = 'disabled'

    def _on_location_selected(self, event):
        """Evento acionado quando uma localização é selecionada no Combobox."""
        selected_name = self.selected_location_name.get()
        logging.info(f"Localização selecionada: {selected_name}")
        # Notifica o Controller da mudança de localização
        success = self.controller.set_location_by_name(selected_name)
        if not success:
            messagebox.showwarning("Erro de Seleção", f"Não foi possível definir '{selected_name}' como localização atual.")
            self.results_label.config(text=f"Erro ao selecionar: {selected_name}") # Atualiza o label de resultados
            logging.error(f"Falha ao definir localização por nome: {selected_name}")
        else:
            self.results_label.config(text=f"Local '{selected_name}' selecionado. Clique em 'Buscar Previsão'.") # Feedback visual

    def _search_button_command(self):
        """Comando acionado ao clicar no botão 'Buscar Previsão'."""
        logging.info("Botão 'Buscar Previsão' clicado.")
        if not self.controller.current_location_id:
            messagebox.showwarning("Aviso", "Selecione primeiro uma localização!")
            logging.warning("Tentativa de buscar previsão sem localização selecionada.")
            self.results_label.config(text="Selecione um local primeiro!")
            return

        # Tenta buscar e processar os dados da previsão
        self.results_label.config(text=f"Buscando previsão para {self.controller.current_location_name}...")
        success = self.controller.fetch_and_display_forecast()

        if success:
            forecast_data = self.controller.get_current_weather_data()
            if forecast_data:
                # Exibe os dados processados no Label de resultados
                display_text = (
                    f"Local: {forecast_data.get('location_name', 'N/A')}\n"
                    f"Data: {forecast_data.get('forecast_date', 'N/A')}\n"
                    f"Temp. Mínima: {forecast_data.get('temp_min', 'N/A')}°C\n"
                    f"Temp. Máxima: {forecast_data.get('temp_max', 'N/A')}°C\n"
                    f"Condição: {forecast_data.get('weather_description', 'N/A')}\n"
                    f"Vento: {forecast_data.get('wind_speed_description', 'N/A')} ({forecast_data.get('wind_dir', 'N/A')})"
                )
                self.results_label.config(text=display_text, foreground=PALETTE_TEXT_DARK)
                logging.info("Previsão exibida com sucesso.")
            else:
                self.results_label.config(text="Erro: Dados de previsão não processados corretamente.", foreground=PALETTE_ERROR)
                messagebox.showerror("Erro de Dados", "Dados de previsão não foram processados corretamente.")
                logging.error("Dados de previsão ausentes após fetch_and_display_forecast.")
        else:
            self.results_label.config(text=f"Falha ao obter previsão para {self.controller.current_location_name}.", foreground=PALETTE_ERROR)
            messagebox.showerror("Erro de Previsão", f"Não foi possível obter a previsão para {self.controller.current_location_name}.")
            logging.error(f"Falha ao obter/exibir previsão para {self.controller.current_location_name}.")

# Não precisamos de _update_results_display e _clear_results_display separadamente
# neste exemplo minimalista, pois estamos a atualizar e limpar o mesmo Label.