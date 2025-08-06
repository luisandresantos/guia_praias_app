# test_controller_flow.py
"""
Script dedicado para testar o fluxo completo do MainController,
simulando a sua inicialização e a chamada para obter e processar dados
meteorológicos de uma localização específica, usando o nome do local.

"""

import logging
import sys
import os

# Adicionar o diretório pai ao path para garantir que os imports funcionam
# Se o script estiver na raiz do projeto:
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
# Se estiver a mover este script para uma pasta 'tests/', o caminho será:
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Importa as classes e funções necessárias
from models.ipma_api import IPMAApi
from static_data.weather_glossary import get_weather_description, get_location_name, get_wind_speed_description
from controllers.main_controller import MainController


def setup_logging():
    """Configura o logging básico para o script de teste."""
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
        )
    logging.info("Logging configurado.")

def run_test_flow():
    """Executa o fluxo de teste do MainController usando o nome do local."""
    setup_logging()
    logging.info("--- Iniciando Teste de Fluxo do MainController ---")

    # 1. Instanciar as dependências que o Controller precisa
    ipma_api_instance = IPMAApi()

    # 2. Instanciar o Controller, passando todas as dependências necessárias
    main_controller = MainController(
        ipma_api=ipma_api_instance,
        weather_desc_func=get_weather_description,
        location_name_func=get_location_name, # Passa a função para obter nome pelo ID # 
                                              # Conversão static_data/weather_glossary.py (dados enriquecidos)
        wind_desc_func=get_wind_speed_description # Passa a função para descrever o vento - tb manipulado por static_data*
    )

    # --- INÍCIO DA ADIÇÃO TEMPORÁRIA ---
    print("\n--- Lista de Nomes de Locais Disponíveis na API ---")

    # Obtém a lista de nomes a partir do controller
    available_locations = main_controller.get_available_location_names()

    if available_locations:
        # Ordena a lista alfabeticamente para facilitar a leitura
        available_locations.sort()
        # Junta os nomes numa única string para imprimir
        print(", ".join(available_locations))
        print(f"\nTotal de locais disponíveis: {len(available_locations)}")
    else:
        print("Não foi possível obter a lista de locais disponíveis.")
    print("--------------------------------------------------\n")
    # --- FIM DA ADIÇÃO TEMPORÁRIA ---

    # 3. Definir uma localização para o teste PELO NOME
    # Exemplo: "Lisboa". Para testar um nome que não existe, usa um incorreto como "Lisboa City".
    # target_location_name = "Esposende"
    # target_location_name = "Invalid Location Name" # Para testar um erro

    # Se quiser testar um nome que sabes que existe na API, usa um da LISTAGEM ACIMA!
    
    target_location_name = "Braga" # Usa um nome da lista que aparecerá no output ** AQUI - EXPRIMENTAR (= **

    logging.info(f"A tentar definir a localização pelo nome: '{target_location_name}'")

    # Usa o novo método, anteriormente testado com IDs' mas é de extrema importancia definir a localização a partir do nome
    set_success = main_controller.set_location_by_name(target_location_name)

    if not set_success:
        logging.error(f"Falha ao definir a localização pelo nome: '{target_location_name}'. A testar sem uma localização válida.")
        # Se falhar ao definir, o fetch_and_display_forecast também falhará, o que é bom para testar o fluxo de erro.
    else:
        # 4. Se a localização foi definida com sucesso, procura e processa a previsão
        logging.info(f"Localização definida com sucesso. A solicitar a previsão.")
        success = main_controller.fetch_and_display_forecast()

        # 5. Analisar o resultado e apresentar na consola
        if success:
            logging.info("Fluxo do Controller executado com sucesso.")
            print("\n--- Resultado do Teste do Controller:")

            output_data = main_controller.get_current_weather_data() # Obtem os dados processados
            if output_data:
                print(f"Localização: {output_data.get('location_name')}") # NOME
                print(f"Data da Previsão: {output_data.get('forecast_date')}")
                print(f"Temperatura Mínima: {output_data.get('temp_min')}°C")
                print(f"Temperatura Máxima: {output_data.get('temp_max')}°C")
                print(f"Descrição do Tempo: {output_data.get('weather_description')}")
                print(f"Direção do Vento: {output_data.get('wind_dir')}")
                print(f"Descrição da Classe de Vento: {output_data.get('wind_speed_description')}")
            else:
                print("  Nenhum dado de previsão processado foi retornado.")
                
        else:
            logging.error(f"O fluxo do Controller falhou ao procurar/processar a previsão para '{main_controller.current_location_name}'.")
            print(f"\nFalha ao procurar ou processar a previsão para '{main_controller.current_location_name}'.")
            print("Verifique os logs para mais detalhes sobre o erro.")

    logging.info("--- Teste de Fluxo do MainController Concluído ---")

if __name__ == "__main__":
    # Garantir que o diretório do projeto está no PYTHONPATH
    # Isto é importante se estivermos a executar este script de um local diferente
    
    run_test_flow()

