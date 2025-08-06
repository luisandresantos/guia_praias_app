# 📄 ipma_api.py

## 🔍 O que este ficheiro faz
Este ficheiro implementa a classe `IPMAApi`, que serve como a principal interface para interagir com a API de dados abertos do Instituto Português do Mar e da Atmosfera (IPMA). O seu propósito é abstrair as requisições HTTP, o tratamento de respostas JSON e a gestão de dados em cache para obter informações meteorológicas, como previsões diárias e descrições de tipos de tempo e locais.

## 🧠 Funções principais

- **`__init__(self)`** – Inicializa a classe `IPMAApi`, definindo as URLs base para os diferentes endpoints da API do IPMA e inicializando variáveis internas (`_weather_descriptions`, `_locations_map`) a `None` para implementar o caching de dados.
- **`get_daily_forecast(self, globalIdLocal)`** – Busca a previsão meteorológica diária para um dado `globalIdLocal`. Constrói a URL, faz uma requisição GET à API, verifica o status da resposta, decodifica o JSON e retorna os dados, tratando erros de rede, JSON inválido e outros.
- **`get_weather_type_descriptions(self)`** – Obtém um mapeamento de códigos numéricos de tipos de tempo para as suas descrições textuais em português. Verifica o cache; se os dados não estiverem disponíveis, faz uma requisição à API, processa a resposta num dicionário e armazena-o em cache. Trata erros de requisição e processamento de JSON/KeyError.
- **`get_locations_map(self)`** – Busca um mapeamento de `globalIdLocal` para nomes de locais. Funciona de forma semelhante a `get_weather_type_descriptions`, verificando o cache, fazendo a requisição à API, processando os dados num dicionário (chave: `globalIdLocal` como string, valor: nome do local) e armazenando em cache. Trata também erros comuns.
- **`get_location_name(self, globalIdLocal)`** – Um método de conveniência que utiliza o mapa de locais carregado (via `get_locations_map()`) para retornar o nome de um local dado o seu `globalIdLocal`. Retorna uma mensagem indicativa em caso de falha ou ID desconhecido.

## 🔁 Relações com outros ficheiros

- 📁 **`controllers/main_controller.py`** chama funções de `models/ipma_api.py`:
    - `main_controller.__init__` chama `ipma_api.get_locations_map()` para carregar os dados de locais.
    - `main_controller.fetch_and_display_forecast()` chama `ipma_api.get_daily_forecast()` para buscar previsões.
    - `main_controller.set_location()` usa indiretamente `ipma_api.get_location_name()` através de uma função passada como argumento (`static_data.get_location_name`).
- 📁 **`static_data/weather_glossary.py`** usa dados de `models/ipma_api.py`:
    - Cria uma instância interna de `IPMAApi`.
    - Chama `_ipma_api_instance.get_weather_type_descriptions()` para obter glossários de tempo.
    - Chama `_ipma_api_instance.get_location_name()` para obter nomes de locais.
- 📁 **`tests/test_controller_flow.py`** instancia e usa `models/ipma_api.py`:
    - Cria uma instância de `IPMAApi` para a passar ao `MainController`.

## 📌 O que estudar para entender este ficheiro

- **Manipulação de JSON:** Como analisar e extrair dados de respostas JSON usando `.json()`.
- **Utilização de APIs:** Conceitos de requisições HTTP (GET), endpoints, tratamento de status codes (`raise_for_status()`).
- **Tratamento de Erros:** Uso de blocos `try...except` para lidar com `requests.exceptions.RequestException`, `ValueError`, `KeyError`, e `Exception` genérica.
- **Módulo `logging`:** Como configurar e usar logs para reportar status e erros de forma estruturada.
- **Caching de Dados:** Entender o padrão de usar variáveis de instância (`_weather_descriptions`, `_locations_map`) para armazenar dados e evitar pedidos repetidos à API.
-   **Módulo `requests`:** Especificamente, métodos como `get()`, `raise_for_status()`, `.json()`.
-   **Dicionários em Python:** Uso eficiente de `dict.get()` e compreensão de como criar e aceder a dicionários mapeados.
-   **Convenções de Nomenclatura:** O uso de `_` para atributos "privados" e `snake_case` para nomear funções e variáveis.

## 💡 Sugestões de melhoria

- 📉 **Gestão de Erros Granular:** O tratamento de erros para `get_locations_map` e `get_weather_type_descriptions` retorna dicionários vazios `{}` em caso de falha. Embora funcional para o exemplo, em ambientes mais críticos, poderia ser útil relançar a exceção após o logging para que o chamador saiba que os dados essenciais não foram carregados.
- 🔒 **Configuração de URLs:** As URLs da API estão hardcoded. Para maior flexibilidade, poderiam ser externalizadas para um ficheiro de configuração (ex: `.env` ou `config.yaml`), especialmente se a aplicação precisasse de se conectar a APIs diferentes ou a staging/production environments.
- 🔄 **Retry Logic:** Para requisições HTTP, considerar a implementação de uma política de retries (tentar novamente após um breve período) para lidar com falhas de rede transitórias.
- **Validação de Parâmetros:** O método `get_daily_forecast` verifica se `globalIdLocal` não é vazio, mas não valida o formato esperado de um ID de localidade. Uma validação mais rigorosa poderia ser adicionada.
- 🧪 **Testes Unitários:** Embora exista um teste de fluxo, adicionar testes unitários específicos para `IPMAApi`, que simulem respostas da API (usando, por exemplo, a biblioteca `requests-mock`), garantiria uma cobertura de teste mais completa.