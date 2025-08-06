# 📄 weather_glossary.py

## 🔍 O que este ficheiro faz
Este ficheiro implementa um módulo (`static_data/weather_glossary.py`) que serve como uma camada de "tradução" e acesso a dados de referência, principalmente para o que é considerado "estático" ou de lookup. Ele pega em códigos numéricos (como IDs de estado do tempo ou classes de vento) e nos IDs de locais, e usa uma instância da `IPMAApi` (ou dados estáticos definidos localmente) para os converter em descrições textuais legíveis pelo ser humano. É, essencialmente, um glossário que enriquece os dados brutos.

## 🧠 Funções principais

- **`get_weather_description(weather_id)`** – Traduz um ID numérico de estado do tempo para uma descrição textual.
    - Utiliza `_ipma_api_instance.get_weather_type_descriptions()` para obter um dicionário de todos os tipos de tempo (ID -> Descrição).
    - Tenta converter o `weather_id` de entrada para um inteiro.
    - Usa `.get()` no dicionário para retornar a descrição, ou uma mensagem de erro se o ID for `None`, inválido para conversão para inteiro, ou um código desconhecido.
- **`get_location_name(globalIdLocal)`** – Obtém o nome legível de um local a partir do seu `globalIdLocal`.
    - Delega diretamente para o método `_ipma_api_instance.get_location_name()`, aproveitando o cache e tratamento de erros já implementados na `IPMAApi`.
- **`get_wind_speed_description(wind_class_id)`** – Traduz um ID de classe de velocidade do vento para uma descrição textual.
    - Utiliza um dicionário estático local `WIND_SPEED_CLASSES` (assumindo que estes valores são fixos ou foram obtidos de outra fonte, pois não parecem vir diretamente da API do IPMA através de um endpoint específico na classe `IPMAApi` atual).
    - Tenta converter o `wind_class_id` de entrada para um inteiro.
    - Usa `.get()` no dicionário estático para retornar a descrição, ou uma mensagem de erro se o ID for `None`, inválido para conversão, ou um código desconhecido.

## 🔁 Relações com outros ficheiros

- 📁 **`static_data/weather_glossary.py`** é um módulo de utilidades de dados.
    - **Depende de:**
        - 📁 `models/ipma_api.py`: Importa a classe `IPMAApi` e cria uma instância (`_ipma_api_instance`) para aceder aos dados dinâmicos da API (tipos de tempo e nomes de locais).
        - `logging`: Para registar mensagens informativas e de erro.
    - **É usado por:**
        - 📁 `controllers/main_controller.py`: As três funções principais deste módulo (`get_weather_description`, `get_location_name`, `get_wind_speed_description`) são passadas como dependências para o `MainController`, que as utiliza para traduzir os dados brutos de previsão.

## 📌 O que estudar para entender este ficheiro

- **Tratamento de Dados "Estáticos":** Como gerir dados de referência que não são buscados a cada interação, mas sim carregados uma vez e reutilizados (e.g., dicionários estáticos).
-   **Mapeamentos e Dicionários:** Uso avançado de dicionários em Python, incluindo criação, acesso com `.get()` e compilação de dicionários (`{k: v for ...}`).
-   **Conversão de Tipos de Dados:** A importância de garantir que os dados de entrada estão no formato correto (neste caso, convertendo para `int`) antes de os usar como chaves em dicionários ou em operações.
-   **Tratamento de Erros Específicos:** Capturar `ValueError` e `TypeError` para lidar com entradas inválidas durante a conversão de tipos.
-   **Uso de Instâncias de Classe:** Compreender como uma instância de outra classe (`IPMAApi`) é criada e utilizada dentro de um módulo para aceder aos seus métodos. A nota sobre "injecting" a instância no `__init__` é uma boa prática a considerar para modularidade.
-   **Fontes de Dados para Referência:** Como definir e gerir dados (como as classes de vento) quando não há um endpoint API direto, possivelmente recorrendo a documentação ou fontes externas.

## 💡 Sugestões de melhoria

## 💡 Otimizações e Melhorias Futuras

-   **Validação/Integração das Classes de Vento:** A coleção `WIND_SPEED_CLASSES` foi estabelecida com base em estimativas. Para garantir a máxima precisão e conformidade, recomenda-se:
    *   Validar estes valores com a documentação oficial do IPMA.
    *   Integrar um endpoint da API, caso venha a existir, que forneça estas descrições diretamente.
    -   **Ação Recomendada:** Atualizar `WIND_SPEED_CLASSES` com dados validados ou provenientes de um endpoint API.

-   **Modularização de Dados Estáticos:** Dada a natureza destes dados de referência, sugere-se a sua centralização numa estrutura mais organizada:
    -   Considerar a criação de ficheiros de configuração dedicados (ex: `config/wind_classes.py` ou `data/wind_classes.json`) para dados como `WIND_SPEED_CLASSES`.
    -   **Ação Recomendada:** Migrar `WIND_SPEED_CLASSES` para um ficheiro de configuração separado para melhor gerir e escalei os dados de referência.

-   **Cobertura de Testes Unitários:** Para assegurar a robustez e corretude das funções de tradução, é essencial implementar testes unitários.
    -   Testar as funções com IDs válidos, `None`, IDs inválidos para conversão, e IDs que não existem nos dicionários de referência. (Unitest ou Pytest)
    -   **Ação Recomendada:** Desenvolver testes unitários para `get_weather_description` e `get_wind_speed_description` para cobrir todos os cenários de input e output.

-   **Injeção de Dependência para `IPMAApi`:** Embora a criação da instância `_ipma_api_instance` dentro do módulo seja funcional, a injeção de dependência (passar a instância de `IPMAApi` via argumento no `__init__` ou em outra função de setup) oferece maior flexibilidade e facilita a escrita de testes.
    -   **Ação Recomendada:** Refatorar para receber a instância de `IPMAApi` como parâmetro em vez de criá-la internamente, seguindo o padrão aplicado no `MainController`. (FEITO)