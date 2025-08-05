import requests
import os
import logging

if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class IPMAApi:
    """
    Classe para interagir com a API de dados abertos do IPMA para obter
    previsões meteorológicas diárias e descrições de tipos de tempo.
    """
    def __init__(self):
        self.base_url_daily_forecast = "https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/"
        self.weather_type_classes_url = "https://api.ipma.pt/open-data/weather-type-classe.json"
        self.locations_url = "https://api.ipma.pt/open-data/distrits-islands.json"
        self._weather_descriptions = None
        self._locations_map = None
        
    def get_daily_forecast(self, globalIdLocal):
        """
        Busca a previsão meteorológica diária para um dado ID de localidade.

        Args:
            globalIdLocal (str): O identificador único do local (ex: "1010500" para Lisboa).

        Returns:
            dict or None: Um dicionário contendo os dados da previsão se a chamada for bem-sucedida,
                          ou None em caso de erro.
        """
        if not globalIdLocal:
            logging.error("IPMA API: globalIdLocal não pode ser vazio.")
            return None

        url = f"{self.base_url_daily_forecast}{globalIdLocal}.json"
        
        logging.info(f"IPMA API: A buscar previsão para o ID {globalIdLocal} em {url}")

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            logging.info(f"IPMA API: Pedido bem-sucedido para {globalIdLocal}. Recebido {len(data.get('data', []))} dias de previsão.")
            return data

        except requests.exceptions.RequestException as e:
            logging.error(f"IPMA API Request Error for {globalIdLocal}: {e}")
            return None
        except ValueError as e:
            logging.error(f"IPMA API JSON Decode Error for {globalIdLocal}: {e}")
            return None
        except Exception as e:
            logging.error(f"IPMA API Unexpected error for {globalIdLocal}: {e}")
            return None

    def get_weather_type_descriptions(self):
        """
        Busca e carrega o mapeamento de códigos de tipo de tempo para descrições.
        Utiliza cache para evitar chamadas repetidas à API.
        """
        if self._weather_descriptions is None:
            logging.info("IPMA API: A carregar mapeamento de tipos de tempo...")
            try:
                response = requests.get(self.weather_type_classes_url)
                response.raise_for_status()
                data = response.json()
                self._weather_descriptions = {
                    item['idWeatherType']: item['descWeatherTypePT']
                    for item in data.get('data', [])
                    if 'idWeatherType' in item and 'descWeatherTypePT' in item
                }
                logging.info(f"IPMA API: Carregados {len(self._weather_descriptions)} tipos de tempo.")
            except requests.exceptions.RequestException as e:
                logging.error(f"IPMA API Request Error while fetching weather types: {e}")
                self._weather_descriptions = {}
            except (ValueError, KeyError) as e:
                logging.error(f"IPMA API Error processing weather types JSON. Error: {e}")
                self._weather_descriptions = {}
            except Exception as e:
                logging.error(f"IPMA API Unexpected error while fetching weather types: {e}")
                self._weather_descriptions = {}

        return self._weather_descriptions

    def get_locations_map(self):
        """
        Busca e carrega o mapeamento de globalIdLocal para nomes de locais.
        Utiliza cache para evitar chamadas repetidas à API.
        """
        if self._locations_map is None:
            logging.info("IPMA API: A carregar mapeamento de locais...")
            try:
                response = requests.get(self.locations_url)
                response.raise_for_status()

                data = response.json()
                self._locations_map = {
                    str(item['globalIdLocal']): item['local']
                    for item in data.get('data', [])
                    if 'globalIdLocal' in item and 'local' in item
                }
                logging.info(f"IPMA API: Carregados mapeamentos para {len(self._locations_map)} locais.")
            except requests.exceptions.RequestException as e:
                logging.error(f"IPMA API Request Error while fetching locations: {e}")
                self._locations_map = {}
            except (ValueError, KeyError) as e:
                logging.error(f"IPMA API Error processing locations JSON. Error: {e}")
                self._locations_map = {}
            except Exception as e:
                logging.error(f"IPMA API Unexpected error while fetching locations: {e}")
                self._locations_map = {}

        return self._locations_map

    def get_location_name(self, globalIdLocal):
        """
        Retorna o nome do local para um dado globalIdLocal.
        """
        locations = self.get_locations_map()
        if not locations:
            return f"ID Local: {globalIdLocal}"

        return locations.get(str(globalIdLocal), f"ID Local Desconhecido ({globalIdLocal})")
