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

- 📉 **Definição de `WIND_SPEED_CLASSES`:** A lista `WIND_SPEED_CLASSES` parece ser uma estimativa. Se houver uma fonte oficial ou um endpoint na API do IPMA que forneça estas descrições, seria ideal integrá-lo para maior precisão. Caso contrário, documentar a origem destas estimativas é uma boa prática.
- 🧩 **Separação de Dados Estáticos:** Para uma melhor organização, as `WIND_SPEED_CLASSES` poderiam estar num ficheiro de configuração separado (ex: `config/wind_classes.py` ou `data/wind_classes.json`), especialmente se fossem mais extensas ou viessem de fontes externas.
- 🧪 **Testes Unitários:** Seria excelente adicionar testes unitários para as funções `get_weather_description` e `get_wind_speed_description`, cobrindo casos com IDs válidos, inválidos, `None`, e IDs que não existem nos dicionários.