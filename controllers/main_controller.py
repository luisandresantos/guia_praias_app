import logging

# Importa as classes/funções necessárias dos outros módulos 
from models.ipma_api import IPMAApi
from static_data.weather_glossary import get_weather_description, get_location_name, get_wind_speed_description
# from views.main_window import MainWindow # A ser importado mais tarde

class MainController:
    def __init__(self, ipma_api: IPMAApi, weather_desc_func, location_name_func, wind_desc_func):
        """
        Inicializa o MainController com suas dependências.
        """
        self.ipma_api = ipma_api
        self.get_weather_desc = weather_desc_func
        self.get_location_name = location_name_func
        self.get_wind_desc = wind_desc_func
        self.current_location_id = None
        self.current_location_name = "N/A" # Para guardar o nome do local
        self.current_weather_data = None

        # Carrega o mapa de locais (id -> nome) imediatamente ao inicializar
        self.locations_map_id_to_name = self.ipma_api.get_locations_map()
        
        # Cria o mapa inverso (nome -> id) com base no mapa carregado
        # Garante que este mapa é criado APÓS o mapa id->nome ser carregado
        self.locations_map_name_to_id = {v: k for k, v in self.locations_map_id_to_name.items()}

        if not self.locations_map_id_to_name:
            logging.warning("Não foi possível carregar o mapa de locais. A pesquisa por nome pode falhar.")
        else:
            logging.info(f"MainController inicializado com {len(self.locations_map_id_to_name)} locais carregados.")

    # Método para definir a localização através do NOME
    def set_location_by_name(self, location_name):
        """
        Define a localização atual usando o nome do local e encontra o ID correspondente.
        """
        if not location_name:
            logging.warning("Nome de localização inválido fornecido.")
            return False

        location_name_cleaned = location_name.strip() # Limpa espaços em branco

        # Procura o ID no mapa inverso (agora já inicializado corretamente)
        location_id = self.locations_map_name_to_id.get(location_name_cleaned)

        if location_id:
            # Se encontrou o ID, usa o set_location normal para definir o ID e o nome
            self.set_location(location_id) # Este método atualiza o ID e busca o nome usando o ID
            logging.info(f"Local '{location_name_cleaned}' encontrado com ID: {location_id}.")
            return True
        else:
            logging.warning(f"Localização com nome '{location_name_cleaned}' não encontrada. Verifique o nome ou a lista de locais disponíveis.")
            self.current_location_id = None # Reseta se não encontrar
            self.current_location_name = "N/A"
            return False

    # Método para definir a localização através do ID (para garantir que funciona corretamente)
    def set_location(self, location_id):
        """
        Define a localização atual apenas pelo ID.
        """
        # Tenta obter o ID como string para consistência nos mapas
        location_id_str = str(location_id)
        
        # Usa a função do glossário para obter o nome (que por sua vez usa a API)
        location_name = self.get_location_name(location_id_str)

        if location_name.startswith("ID Local Desconhecido"):
            logging.warning(f"Tentativa de definir localização com ID desconhecido: {location_id_str}")
            self.current_location_id = None
            self.current_location_name = "N/A"
            return False
        else:
            self.current_location_id = location_id_str
            self.current_location_name = location_name
            logging.info(f"Localização definida para: {self.current_location_name} (ID: {self.current_location_id})")
            return True

    def fetch_and_display_forecast(self):
        """
        Busca, processa e prepara os dados da previsão para exibição na UI.
        """
        if not self.current_location_id:
            logging.warning("Não há localização definida para mostrar a previsão.")
            return False

        logging.info(f"A procurar a previsão para: {self.current_location_name} (ID: {self.current_location_id})")
        
        # 1. Encontrar a previsão diária
        forecast_data = self.ipma_api.get_daily_forecast(self.current_location_id)
        
        if forecast_data is None:
            logging.error(f"Falha ao obter dados de previsão para {self.current_location_name}.")
            # Limpa os dados antigos, se houver
            self.current_weather_data = None
            return False

        # 2. Processar os dados brutos
        processed_data = self._process_forecast_data(forecast_data)
        
        if processed_data is None:
            logging.error("Faltam dados essenciais na resposta da API ou ocorreram erros no processamento para {self.current_location_name}.")
            self.current_weather_data = None
            return False
            
        self.current_weather_data = processed_data
        logging.info(f"Previsão processada para {self.current_location_name} pronta para exibição.")
        
        # 3. Transmitir os dados processados para a UI
        # Numa UI real: self.ui.display_weather_data(self.current_weather_data) = UI PARA DESENVOLVER 
        return True

    def _process_forecast_data(self, raw_forecast_data):
        """
        Processa os dados brutos da API para extracção e formatação.
        """
        if not raw_forecast_data or not raw_forecast_data.get('data'):
            logging.warning("Dados brutos de previsão vazios ou mal formatados.")
            return None

        daily_forecasts = raw_forecast_data['data']
        if not daily_forecasts:
            logging.warning("Nenhum dia de previsão encontrado nos dados brutos.")
            return None

        # Assume-se que a primeira entrada na lista 'data' é a previsão mais relevante.
        # Numa aplicação mais complexa, poderiam existir mecanismos para selecionar um dia específico. 
        #   ======================  "IMPORTANTE" ================ ESCALABILIDADE E FUNCIONALIDADE ======
        first_day_data = daily_forecasts[0]
        
        try:
            processed_info = {
                "location_name": self.current_location_name, # O nome já está definido no controller
                "location_id": raw_forecast_data.get("globalIdLocal", self.current_location_id),
                "forecast_date": first_day_data.get("forecastDate", "N/A"),
                "temp_min": first_day_data.get("tMin", "N/A"),
                "temp_max": first_day_data.get("tMax", "N/A"),
                "weather_id": first_day_data.get("idWeatherType"),
                "wind_speed_class": first_day_data.get("classWindSpeed", "N/A"),
                "wind_dir": first_day_data.get("predWindDir", "N/A"),
            }
            
            # Traduz os IDs usando as funções do glossário
            processed_info["weather_description"] = self.get_weather_desc(processed_info["weather_id"])
            processed_info["wind_speed_description"] = self.get_wind_desc(processed_info["wind_speed_class"])
            
            logging.info(f"Dados de previsão processados para {self.current_location_name}.")
            return processed_info
            
        except Exception as e:
            logging.error(f"Erro ao processar dados de previsão para {self.current_location_name}: {e}")
            return None

    # Método para obter os dados processados para a UI
    def get_current_weather_data(self):
        """Retorna os dados de previsão processados para a localização atual."""
        return self.current_weather_data

    # Métodos relacionados com a lista completa de locais (se necessário no futuro)
    def get_available_location_names(self):
        """Retorna uma lista de nomes de todas as localizações disponíveis."""
        # Usa o mapa que já foi carregado para obter apenas os nomes
        return list(self.locations_map_id_to_name.values())
