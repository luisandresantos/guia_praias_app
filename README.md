
# Guia de Praias App

Este projeto tem como objetivo demonstrar a interação entre diferentes módulos Python para obter e apresentar dados meteorológicos em Portugal, utilizando a API aberta do Instituto Português do Mar e da Atmosfera (IPMA). A aplicação simula o fluxo de dados desde a consulta da API até ao processamento e visualização de informações úteis como a previsão do tempo e descrições associadas.

## 1. Descrição Geral do Projeto

### Propósito
O principal propósito desta aplicação é servir como um exemplo prático de desenvolvimento de uma aplicação Python que se conecta a uma API externa (IPMA), processa os dados recebidos e os apresenta de forma estruturada. Visa também demonstrar boas práticas de arquitetura de software, modularização, tratamento de erros e testes.

### Funcionalidades
*   Consulta a API do IPMA para obter previsões meteorológicas diárias para diversas localidades em Portugal.
*   Carrega listas de tipos de tempo e classes de vento para traduzir códigos recebidos da API em descrições textuais legíveis.
*   Permite definir a localização de interesse pelo nome ou pelo ID.
*   Processa os dados brutos da API, extraindo informações relevantes como temperaturas, descrições do tempo e vento.
*   Inclui um script de teste para validar o fluxo completo da aplicação.

### Estrutura Geral
A estrutura do projeto segue um padrão modular, separando as responsabilidades em diferentes ficheiros e pastas:

*   **`/models`**: Contém a lógica de interação com a API externa (`ipma_api.py`).
*   **`/static_data`**: Abriga módulos que fornecem dados estáticos ou funções de tradução/glossário (`weather_glossary.py`).
*   **`/controllers`**: Implementa a lógica de negócio e orquestração dos dados (`main_controller.py`).
*   **`/tests`**: Contém scripts para testar partes ou o fluxo completo da aplicação (`test_controller_flow.py`).

### 2. Componentes Principais

A aplicação está organizada em módulos que trabalham em conjunto:

### 1. `/models/ipma_api.py` - A Interface com o Mundo Exterior

*   **Função:** Esta classe é o ponto de contacto direto com a API pública do IPMA. É responsável por realizar os pedidos HTTP, receber as respostas em formato JSON e armazenar em cache alguns dados (como listas de locais e descrições de tempo) para otimizar o desempenho e evitar múltiplos pedidos para os mesmos dados.

*   **Métodos:**
    *   `get_daily_forecast(globalIdLocal)`: Procura a previsão diária para uma determinada localidade.
    *   `get_weather_type_descriptions()`: Obtém um mapeamento de códigos de tempo para descrições textuais (em português).
    *   `get_locations_map()`: Obtém um mapeamento de IDs de locais para os seus nomes completos.
    *   `get_location_name(globalIdLocal)`: Retorna o nome de um local dado o seu ID.
*   **Relação:** É utilizada principalmente pelo `MainController` para obter dados de previsão brutos (`get_daily_forecast`) e, de forma mais indireta, pelas funções do `weather_glossary` para carregar conjuntos de dados de tradução (mapas de tipos de tempo e locais).

### 2. `/static_data/weather_glossary.py` - Os Tradutores de Dados

*   **Função:** Contém funções que transformam códigos numéricos (obtidos pela API e usados nos dados de previsão) em descrições textuais mais legíveis para o utilizador final. Estas funções acedem a mapeamentos de IDs para texto.

*   **Implementação para Carga de Dados (Detalhe):**
    *   Atualmente, este módulo inicializa internamente uma instância da `IPMAApi` (chamada `_ipma_api_instance`).
    *   Esta instância é utilizada pelas funções `get_weather_description()` e `get_location_name()` para carregar os seus respetivos mapas de tradução (`weather_types_map` e `location_names_map`) a partir dos dados fornecidos pela API.
    *   A função `get_wind_speed_description()` utiliza um dicionário de mapeamento interno, pois os dados de classes de vento são estáticos e não vêm da API do IPMA.
    *   **Nota**: Embora o `MainController` receba estas funções diretamente para injetar dependências, a forma como estas funções obtêm os seus dados de mapeamento (carregando via uma instância `IPMAApi` interna a `weather_glossary.py`) é um aspeto a ser considerado para futuras refatorações em termos de Injeção de Dependências mais profunda para testes unitários isolados destas funções.

*   **Métodos:**
    *   `get_weather_description(weather_id)`: Converte um ID de tempo numérico na sua descrição textual (ex: `1` vira "Céu limpo").
    *   `get_location_name(globalIdLocal)`: Converte um ID de local num nome de local (ex: `1010500` vira "Aveiro").
    *   `get_wind_speed_description(wind_class_id)`: Converte uma classe de vento numérica na sua descrição textual (ex: `1` vira "Vento fraco").

*   **Relação:** As funções deste módulo são passadas como dependências para o `MainController`, que as utiliza para enriquecer (tornar mais legíveis) os dados brutos da previsão recebidos da `IPMAApi` antes de os apresentar.

### 3. `/controllers/main_controller.py` - O Maestro da Aplicação

*   **Função:** Atua como o orquestrador central da aplicação. Ele recebe as dependências necessárias (a instância da `IPMAApi` e as funções de tradução), gerencia o estado da aplicação (como a localização atual e os últimos dados de previsão), e coordena as chamadas entre os diferentes módulos para construir um fluxo de dados coerente.
*   **Métodos:**
    *   `__init__`: O construtor, que inicializa o controller, carrega um mapa interno de locais (para permitir a pesquisa por nome) e recebe as funções de tradução através de Injeção de Dependência.
    *   `set_location_by_name(location_name)`: Permite ao utilizador definir a localização de interesse através do seu nome (ex: "Lisboa"). O controller usa o seu mapa interno para encontrar o ID correspondente.
    *   `set_location(location_id)`: Define a localização de interesse diretamente pelo seu ID. Internamente, usa a função `static_data.get_location_name` para obter o nome legível associado ao ID.
    *   `fetch_and_display_forecast()`: Coordena o processo de procura e processamento de dados. Chama a `IPMAApi` para obter a previsão e depois o seu método interno de processamento dos dados.
    *   `_process_forecast_data(raw_forecast_data)`: Lida com os dados brutos recebidos da `IPMAApi`, extrai a informação relevante (temperatura, IDs de tempo/vento) e utiliza as funções de tradução que foram injetadas (`self.get_weather_desc`, `self.get_wind_desc`) para os converter em descrições legíveis.
    *   `get_available_location_names()`: Fornece uma lista de todos os nomes de locais que a aplicação conhece, o que é útil para interfaces de utilizador ou testes.
    *   `get_current_weather_data()`: Retorna os dados meteorológicos mais recentes processados pelo controller, prontos para serem apresentados.
*   **Relação:** É o componente central que integra tudo: usa a `IPMAApi` para procurarr dados, utiliza as funções do `static_data/weather_glossary.py` para traduzir/enriquecer esses dados, e gere o fluxo geral da aplicação do ponto de vista da lógica de negócio.

### 4. `/tests/test_controller_flow.py` - O Verificador Integrado

*   **Função:** Este é um script de teste de integração crucial que valida se todos os componentes principais da aplicação (`IPMAApi`, `weather_glossary`, `MainController`) funcionam bem em conjunto. Ele simula um ciclo completo de uso da aplicação, desde a sua inicialização até à obtenção e exibição da previsão.
*   **Métodos:**
    *   `setup_logging()`: Prepara o sistema de logs para que todas as etapas do teste sejam detalhadamente registadas.
    *   `run_test_flow()`: É a sequência de teste principal:
        1.  Instancia a `IPMAApi`.
        2.  Instancia o `MainController`, injetando a `IPMAApi` e as funções de tradução do `weather_glossary`.
        3.  Pede ao `MainController` a lista de locais disponíveis e a exibe.
        4.  Define uma localização específica (ex: "Braga") para o teste.
        5.  Chama `main_controller.set_location_by_name()` para configurar o local.
        6.  Se a definição do local for bem-sucedida, chama `main_controller.fetch_and_display_forecast()` para procurarr e processar a previsão.
        7.  Obtém os dados processados via `main_controller.get_current_weather_data()` e os imprime na consola.
        8.  Inclui lógica para reportar falhas durante o fluxo.
*   **Relação:** Serve como o ponto de partida para demonstrar como os módulos devem ser usados em conjunto e verifica se o fluxo de dados e a lógica estão corretos. É a "prova de vida" do sistema.

## 3. Fluxo da Aplicação (Exemplo: Obter Previsão para "Aveiro")

1.  **Início em `test_controller_flow.py`:**
    *   O script de teste é executado (`if __name__ == "__main__":`).
    *   `run_test_flow()` é chamado.
    *   Uma instância de `IPMAApi` é criada (`ipma_api_instance`). Ao ser criada, a `IPMAApi` prepara-se para carregar os mapas de locais e tipos de tempo.
    *   Uma instância de `MainController` é criada, recebendo `ipma_api_instance` e os ponteiros para as funções do `weather_glossary`.
    *   O `MainController`, no seu `__init__`, chama **`ipma_api_instance.get_locations_map()`** para carregar todos os locais e a partir daí constrói o seu mapa interno nome->ID.

2.  **Definição da Localização:**
    *   O script de teste define `target_location_name = "Aveiro"`.
    *   Chama `main_controller.set_location_by_name("Aveiro")`.
    *   O `MainController` procura "Aveiro" no seu mapa `locations_map_name_to_id`.
    *   Se encontrado, obtém o ID correspondente (ex: "1010500").
    *   Chama `main_controller.set_location("1010500")`.
    *   `main_controller.set_location()` chama **`static_data.get_location_name("1010500")`**.
    *   `static_data.get_location_name` chama **`ipma_api_instance.get_location_name("1010500")`**, que retorna "Aveiro" (usando os dados carregados).
    *   O `MainController` guarda `self.current_location_id = "1010500"` e `self.current_location_name = "Aveiro"`.

3.  **procura e Processamento da Previsão:**
    *   O script de teste chama `main_controller.fetch_and_display_forecast()`.
    *   O `MainController` verifica que tem uma localização definida.
    *   Chama **`ipma_api_instance.get_daily_forecast("1010500")`** para procurarr os dados brutos da previsão.
    *   Se for bem-sucedido, chama `main_controller._process_forecast_data(dados_brutos_da_API)`.
    *   `_process_forecast_data` extrai os IDs de tempo e vento como `weather_id` e `wind_speed_class`.
    *   Para traduzir `weather_id`, chama **`self.get_weather_desc(weather_id)`**, que por sua vez executa a função `static_data.get_weather_description(weather_id)`.
    *   Esta função chama **`_ipma_api_instance.get_weather_type_descriptions()`** (que carrega os dados de tempo se ainda não o fez) e usa o resultado para retornar a descrição textual.
    *   Similarmente, para traduzir `wind_speed_class`, chama **`self.get_wind_desc(wind_speed_class)`**, que executa `static_data.get_wind_speed_description(wind_speed_class)`, usando um dicionário interno para a descrição.
    *   O resultado é um dicionário com dados formatados e descrições traduzidas.

4.  **Exibição dos Resultados:**
    *   O `MainController` armazena os dados processados.
    *   O script de teste chama `main_controller.get_current_weather_data()` para obter os dados.
    *   Os dados são impressos na consola em formato legível.

## 4. Exemplo de Execução

**Comando:**
Executar o script de teste:
```bash
python tests/test_controller_flow.py
```

**Output Esperado (exemplo para Aveiro):**

*(O output conterá logs detalhados e, no final, a informação processada)*
--- Lista de Nomes de Locais Disponíveis na API --- Angra do Heroísmo, Aveiro, Beja, Braga, Bragança, Castelo Branco, Coimbra, Faro, Funchal, Guarda, Guimarães, Horta, Leiria, Lisboa, Loulé, Madalena, Penhas Douradas, Ponta Delgada, Portalegre, Portimão, Porto, Porto Santo, Sagres, Santa Cruz da Graciosa, Santa Cruz das Flores, Santarém, Setúbal, Sines, Velas, Viana do Castelo, Vila Real, Vila do Corvo, Vila do Porto, Viseu, Évora 

Total de locais disponíveis: 35

--- Resultado do Teste do Controller: Localização: Aveiro Data da Previsão: 2025-08-05 Temperatura Mínima: 16.4°C Temperatura Máxima: 27.2°C Descrição do Tempo: Céu parcialmente nublado Direção do Vento: NW Descrição da Classe de Vento: Vento fraco


**Explicação:**
O script de teste encontrou "Aveiro" na lista de locais disponíveis, obteve o seu ID, encontrou a previsão do tempo para esse ID na API do IPMA, traduziu os códigos de tempo e vento para descrições legíveis com a ajuda das funções do `weather_glossary`, e apresentou os dados consolidados no terminal. (dados enriquecidos por static_data TRATAMENTO DADOS)

## 5. Sugestões de Estudo

Para quem quiser aprofundar a compreensão deste projeto e do desenvolvimento de aplicações em Python, recomenda-se estudar os seguintes tópicos:

*   **Requisições HTTP com `requests`:** Compreender como fazer pedidos a APIs externas é fundamental (conceitos como GET, POST, headers, JSON).
*   **Processamento de JSON:** Saber como analisar e extrair dados de respostas JSON é essencial para interagir com APIs web.
*   **Tratamento de Erros (`try...except`):** Fundamental para construir aplicações robustas que lidam com falhas (ex: rede, dados inválidos).
*   **Modularização e Importações em Python:** Entender como organizar o código em vários ficheiros e como os importar corretamente (`import`, `from ... import`).
*   **Dicionários em Python:** Uso eficiente de dicionários para mapeamento de dados e procura rápida.
*   **Funções e Closures:** Compreender como passar funções como argumentos (usado no padrão de injeção de dependência no `MainController`). CHAVE PRINCIPAL DE ESTUDO.
*   **Testes Unitários e de Integração:** Saber como escrever testes (como `test_controller_flow.py`) para verificar o comportamento do código e garantir a sua correção ao longo do tempo.
*   **APIs Abertas e Web Scraping (conceito):** Entender como encontrar e consumir dados disponíveis publicamente na internet.
*   **Arquitetura MVC (Model-View-Controller) ou Padrões Similares:** Embora este projeto não seja estritamente MVC, os conceitos de separação de responsabilidades (API->Model, Lógica->Controller, Dados Estáticos->Glossary) são importantes.
*   **Logging:** Configurar e utilizar o módulo `logging` para fornecer feedback estruturado sobre a execução da aplicação.
