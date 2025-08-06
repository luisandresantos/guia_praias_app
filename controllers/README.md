# 📄 main_controller.py

## 🔍 O que este ficheiro faz
Este ficheiro implementa a classe `MainController`, que atua como o "maestro" da aplicação. É responsável por organizar a lógica de negócio, gerir o estado da aplicação (como a localização atual e os dados de previsão) e coordenar a interação entre os diferentes módulos (API, glossário, e eventualmente a UI). O `MainController` é o cérebro que decide quando procurar dados, como processá-los e como prepará-los para serem apresentados.

## 🧠 Funções principais

- **`__init__(self, ipma_api: IPMAApi, ...)`** – Inicializa o controller, recebendo como dependências a instância da `IPMAApi` e as funções de tradução do `weather_glossary`. Começa por carregar mapas de locais (ID->Nome e Nome->ID) usando a `IPMAApi` para permitir a pesquisa de locais por nome. O uso do código comentado `# from views.main_window import MainWindow` indica que a integração com a UI ainda não está implementada, mas está planeada.
- **`set_location_by_name(self, location_name)`** – Permite definir a localização de interesse pelo nome. Usa o mapa `nome->id` previamente carregado para encontrar o ID correspondente e depois chama `set_location()` com esse ID. Inclui validação básica do nome fornecido e limpeza de espaços em branco.
- **`set_location(self, location_id)`** – Define o `current_location_id` e `current_location_name` na instância do controller. Utiliza a função `get_location_name` (fornecida como dependência, que por sua vez usa `IPMAApi`) para obter o nome correto a partir do ID fornecido, garantindo a consistência dos dados. O método retorna um booleano indicando o sucesso da operação.
- **`fetch_and_display_forecast(self)`** – Orquestra o ciclo de obter e processar a previsão do tempo. Verifica se uma localização está definida, chama `ipma_api.get_daily_forecast()` para obter os dados brutos, e depois chama `_process_forecast_data()` para formatar esses dados. O resultado é armazenado em `self.current_weather_data`. Um comentário indica onde a integração com a UI seria feita (`self.ui.display_weather_data`). Retorna um booleano indicando o sucesso.
- **`_process_forecast_data(self, raw_forecast_data)`** – Método privado que extrai e formata dados específicos da previsão (temperaturas, IDs de tempo/vento, data). Usa as funções de tradução (`self.get_weather_desc`, `self.get_wind_desc`) para converter os IDs numéricos em descrições textuais legíveis. Um comentário nota que a seleção da previsão assume que a primeira entrada na lista de dados é a mais relevante, e que uma lógica mais complexa poderia ser necessária no futuro. Retorna um dicionário com os dados processados ou `None` em caso de falha.
- **`get_current_weather_data(self)`** – Um getter simples que retorna os dados de previsão processados (`self.current_weather_data`), prontos para serem exibidos pela UI.
- **`get_available_location_names(self)`** – Fornece uma lista com os nomes de todos os locais disponíveis, extraindo-os do mapa `locations_map_id_to_name` carregado na inicialização. Útil para preencher dropdowns ou listas na UI.

## 🔁 Relações com outros ficheiros

- 📁 **`controllers/main_controller.py`** é o orquestrador central.
    - **Depende de:**
        - 📁 `models/ipma_api.py`: Usa uma instância da classe `IPMAApi` para buscar dados crus da API.
        - 📁 `static_data/weather_glossary.py`: Recebe as funções `get_weather_description`, `get_location_name`, `get_wind_speed_description` como dependências para traduzir dados.
    - **É usado por:**
        - 📁 `tests/test_controller_flow.py`: Este script instancia o `MainController`, passa-lhe as dependências (`IPMAApi` e funções do glossary) e chama os seus métodos públicos para simular o fluxo da aplicação e verificar a sua integridade.
    - **Futura dependência:**
        - 📁 `views/main_window.py` (comentado): Indica que o controller irá interagir com uma futura UI para exibir os dados processados.

## 📌 O que estudar para entender este ficheiro

- **Programação Orientada a Objetos (POO):** Conceitos como classes, objetos, atributos de instância, métodos e encapsulamento.
- **Injeção de Dependências:** Entender o padrão de passar objetos e funções como argumentos no `__init__` em vez de criá-los dentro da classe. Isto aumenta a flexibilidade e a testabilidade.
-   **Gestão de Estado:** Como um objeto (o controller) mantém informações ao longo do tempo (`self.current_location_id`, `self.current_weather_data`).
-   **Estrutura de Módulos e Importações:** Como organizar código em diferentes ficheiros e importá-los corretamente (`import`, `from...import`).
-   **Desenvolvimento Guiado por Testes (TDD) - Conceitos:** A forma como as dependências são passadas facilita escrever testes de integração (como em `test_controller_flow.py`). A separação de responsabilidades é chave.
-   **Parsing de JSON (Implícito):** O `_process_forecast_data` depende da estrutura de dados retornada por `ipma_api.py`, que por sua vez depende de um bom parsing de JSON.
-   **Tratamento de Resultados de Funções:** Como verificar valores de retorno booleanos ou `None` para continuar o fluxo da aplicação (ex: `if not self.current_location_id:`, `if forecast_data is None:`).

## 💡 Sugestões de melhoria

- 📉 **Tratamento de Erros Específico:** No método `_process_forecast_data`, o `except Exception as e:` é um pouco genérico. Poderia ser mais específico, capturando `KeyError` (se um campo chave como `tMin` estiver em falta) ou `TypeError` (se um valor não for do tipo esperado), permitindo uma gestão de erros mais granular.
- 🎯 **Seleção de Data da Previsão:** Atualmente, a `_process_forecast_data` utiliza sempre o primeiro dia de previsão (`daily_forecasts[0]`). Se a API retornar dados para múltiplos dias, seria uma melhoria permitir ao utilizador escolher qual o dia de previsão a visualizar, ou implementar uma lógica para selecionar o dia mais relevante.
- 🧩 **Separação de Responsabilidades (UI):** O comentário `# from views.main_window import MainWindow` e a linha comentada `self.ui.display_weather_data(...)` indicam que a interação com a UI ainda não está implementada. Quando for, é crucial que o `MainController` apenas passe os dados processados para uma camada de UI (ex: uma classe `MainWindow`), sem que o controller execute diretamente operações de UI (como `print` ou manipulação de widgets).
- 🔗 **Gestão de Cache em `dependencies`:** O `MainController` carrega a cache de locais na inicialização. Se a API mudar ou se for necessário atualizar os locais, seria preciso um mecanismo para invalidar ou recarregar este cache. Atualmente, o cache é carregado apenas uma vez.
- 🧪 **Testes Unitários para `_process_forecast_data`:** Seria vantajoso criar testes unitários específicos para esta função, passando diferentes exemplos de `raw_forecast_data` (incluindo dados em falta ou mal formatados) para garantir que a extração e tradução funcionam como esperado em todos os cenários.