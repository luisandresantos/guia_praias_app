# Modelo de Interação com a API do IPMA (`IPMAApi`)

Este módulo (`models/ipma_api.py`) fornece uma interface programática para interagir com a API de dados abertos do **Instituto Português do Mar e da Atmosfera (IPMA)**. Permite a obtenção de dados meteorológicos essenciais, como previsões diárias e detalhes sobre tipos de tempo, facilitando a sua integração em aplicações.

---

## 📚 Funcionalidades Principais

A classe `IPMAApi` oferece os seguintes métodos para aceder à informação:

*   **`get_daily_forecast(globalIdLocal)`**: Recupera a previsão meteorológica diária detalhada para uma localidade específica.
    *   **Dados Fornecidos:** Inclui previsões para vários dias, temperaturas mínimas/máximas, códigos de tipo de tempo, velocidade e direção do vento, entre outros.
    *   **Identificação de Localidades:** Requer o parâmetro `globalIdLocal`, um identificador único para cada ponto geográfico registado pelo IPMA.

*   **`get_weather_type_descriptions()`**: Obtém um mapeamento entre códigos numéricos (`idWeatherType`) e as suas descrições textuais em Português (`descWeatherTypePT`). Essencial para traduzir os códigos de tempo em informação legível para o utilizador.

*   **`get_locations_map()`**: Busca uma lista completa de todas as localidades registadas pela API do IPMA e retorna um dicionário que mapeia o `globalIdLocal` para o nome do local (`local`). Facilita a descoberta de localizações e as suas correspondentes informações geográficas (latitude/longitude, distrito, etc.).

*   **`get_location_name(globalIdLocal)`**: Um método de conveniência que utiliza o mapa de locais para retornar o nome de uma localidade dado o seu `globalIdLocal`.

---

## ⚙️ Arquitetura e Implementação

### Fluxo de Trabalho Geral

1.  **Inicialização (`__init__`)**:
    *   Define os URLs base para os diferentes endpoints da API do IPMA (`forecast/meteorology/cities/daily/`, `weather-type-classe.json`, `distrits-islands.json`).
    *   Inicializa variáveis para armazenar em cache os dados obtidos da API (`_weather_descriptions`, `_locations_map`), melhorando a performance ao evitar pedidos repetidos para os mesmos dados.

2.  **Pedidos à API:**
    *   Todos os métodos que interagem com a API utilizam a biblioteca `requests` para fazer pedidos HTTP (GET).
    *   Implementam `try...except` blocks para lidar com potenciais erros de rede (`requests.exceptions.RequestException`), erros de decodificação JSON (`ValueError`), e outros erros inesperados (`Exception`), registando as mensagens de erro com o módulo `logging`.
    *   Utilizam `response.raise_for_status()` para verificar se o pedido HTTP foi bem-sucedido (códigos de status 2xx) e lançar uma exceção para códigos de erro (4xx, 5xx).

3.  **Processamento e Caching:**
    *   Ao obter dados que não mudam frequentemente (descrições de tempo, lista de locais), os resultados são armazenados em variáveis de instância (_weather_descriptions, _locations_map). Nas chamadas subsequentes, estes dados são retornados diretamente da cache, sem necessidade de contactar a API novamente.
    *   Os dados JSON recebidos são processados para extrair a informação relevante e formatá-la em estruturas de dados Python (dicionários, listas).

---

## 🛡️ Segurança

### Endpoints Públicos

*   Os endpoints utilizados por esta classe (`api.ipma.pt/open-data/...`) são **públicos e não requerem autenticação ou chaves de API** para acesso.
*   Isto significa que **não é necessário esconder URLs ou credenciais** no código por motivos de segurança para estes endpoints específicos. A informação disponibilizada é de acesso livre.

### Ausência de Dados Sensíveis

*   A classe **não lida com dados sensíveis do utilizador ou credenciais de acesso** (como passwords, tokens de acesso, chaves de API privadas).
*   Se a API do IPMA viesse a exigir autenticação no futuro, seria fundamental implementar mecanismos de segurança para proteger essas credenciais, como o uso de **variáveis de ambiente** e a exclusão de ficheiros de configuração sensíveis (`.env`) do controlo de versão (ex: com `.gitignore`). No entanto, para a configuração atual, essa necessidade não existe.

---

Este módulo é um componente essencial para a recolha de dados meteorológicos, desenhado para ser robusto na comunicação com a API do IPMA e eficiente através do uso de caching.