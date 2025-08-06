"""
Contém funções para aceder a dados estáticos de referência, como glossários
de tipos de tempo e nomes de locais, carregados dinamicamente da API do IPMA.
"""

# Importa as classes e funções necessárias
from models.ipma_api import IPMAApi
import logging

# Cria uma instância da API para usar nos métodos de glossary.
# Em aplicações maiores, esta instância pode ser passada de fora (injected).
_ipma_api_instance = IPMAApi()

# --- Glossário de Tipos de Tempo ---
def get_weather_description(weather_id):
    """
    Retorna a descrição textual do tipo de tempo para um dado ID numérico,

    obtendo os dados da API do IPMA de forma robusta.

    Esta função traduz um código numérico de estado do tempo (ex: 2)
    para uma descrição legível (ex: "Poucas nuvens").

    Args:
        weather_id: O ID numérico ou o seu equivalente em string do estado do tempo.
                    Pode ser None ou um valor que precise de conversão para inteiro.

    Returns:
        str: A descrição textual do estado do tempo, uma mensagem de erro se o ID for inválido,
             ou uma mensagem indicando que os dados não puderam ser obtidos.
    """
    # 1. Obter o dicionário de descrições de tempo:
    #    Esta linha chama o método get_weather_type_descriptions da instância IPMAApi (_ipma_api_instance).
    #    Este método busca os dados na API do IPMA (ou retorna da cache se já os tiver buscado).
    #    O resultado esperado é um dicionário onde as chaves são os IDs dos tipos de tempo (como inteiros)
    #    e os valores são as descrições em texto (como strings).
    #    Exemplo de retorno: {2: "Poucas nuvens", 10: "Chuva fraca", ...}
    weather_descriptions = _ipma_api_instance.get_weather_type_descriptions()

    try:
        # 2. Verificar se o weather_id recebido é nulo:
        #    Se o identificador do tempo não foi fornecido (é None), não podemos fazer a busca.
        #    Retorna uma mensagem indicando que não há dados disponíveis.
        if weather_id is None:
            return "Dados de tempo não disponíveis"
        
        # 3. Preparar o weather_id para a pesquisa no dicionário:
        #    A API do IPMA pode retornar IDs como inteiros ou strings.
        #    Para garantir que a pesquisa no dicionário funciona corretamente (assumindo que as chaves são inteiros),
        #    tentamos converter `weather_id` para um número inteiro.
        weather_id_int = int(weather_id)

        # 4. Procurar a descrição no dicionário e retornar:
        #    Utilizamos o método .get() do dicionário 'weather_descriptions'.
        #    Este método é crucial por duas razões:
        #    a) Se weather_id_int EXISTIR como chave no dicionário, '.get()' retorna o valor associado (a descrição).
        #       Ex: Se weather_id_int for 2, e weather_descriptions[2] for "Poucas nuvens", retorna "Poucas nuvens".
        #    b) Se weather_id_int NÃO EXISTIR como chave no dicionário (o que pode acontecer se a API adicionar novos códigos
        #       ou se houver uma inconsistência), '.get()' não causa um erro (KeyError), mas retorna o SEGUNDO argumento fornecido,
        #       que é o nosso valor de 'fallback' ou padrão.
        #    O valor de fallback é uma mensagem informativa: f"Código de Tempo Desconhecido ({weather_id_int})".
        return weather_descriptions.get(weather_id_int, f"Código de Tempo Desconhecido ({weather_id_int})")

    # 5. Capturar erros de conversão de tipo:
    #    Se o `weather_id` recebido não puder ser convertido para um inteiro (por exemplo, se for uma string como "chuva"
    #    em vez de um número), ocorrerá um erro `ValueError` ou `TypeError` durante o int(weather_id).
    #    Este bloco 'except' captura esses erros.
    #    Quando um erro de conversão é apanhado, retornamos uma mensagem indicando que o ID fornecido é inválido.
    except (ValueError, TypeError):
        return f"ID de Tempo Inválido ({weather_id})"

# --- Mapeamento de Locais ---
def get_location_name(globalIdLocal):
    """
    Retorna o nome do local associado a um dado globalIdLocal, usando a API do IPMA.
    """
    return _ipma_api_instance.get_location_name(globalIdLocal)

# --- Glossário de Classes de Vento ---
# A lista de classes de vento é tipicamente estática se não houver um endpoint API para ela.
# Se a documentação do IPMA não fornecer os valores exatos das classes de vento,
# teremos de fazer uma suposição ou deixar como placeholder.
# Vamos assumir que vamos adicioná-la aqui como estatística por agora.

WIND_SPEED_CLASSES = {
    0: "Calmo",
    1: "Vento fraco",
    2: "Vento moderado",
    3: "Vento forte",
    4: "Vento muito forte",
    # Estimar as classes com base em fontes comuns, pois o IPMA não forneceu um endpoint.
    # Se tiveres a lista completa, atualiza aqui.
}

def get_wind_speed_description(wind_class_id):
    """
    Retorna a descrição textual para uma dada classe de velocidade do vento.
    """
    try:
        if wind_class_id is None:
            return "Informação de vento indisponível"
        
        wind_class_int = int(wind_class_id)
        return WIND_SPEED_CLASSES.get(wind_class_int, f"Classe de Vento Desconhecida ({wind_class_int})")
    except (ValueError, TypeError):
        return f"ID de Classe de Vento Inválido ({wind_class_id})"