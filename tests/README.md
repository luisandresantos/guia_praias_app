# 📄 test_controller_flow.py

## 🔍 O que este ficheiro faz
Este script funciona como uma **demonstração prática** e um **ponto de teste de integração** para o `MainController`. O seu propósito é simular um fluxo de trabalho completo na nossa aplicação de meteorologia:
1.  **Prepara as ferramentas**: Configura a `IPMAApi` (que busca dados da API real), as funções de tradução de termos meteorológicos (`weather_glossary.py`) e o sistema de registo de mensagens (`logging`).
2.  **Monta o `MainController`**: Cria uma instância deste controller, fornecendo-lhe todas as ferramentas necessárias através do padrão de **Injeção de Dependência (DI)**. Isto significa que o `MainController` não se preocupa em *criar* as suas dependências, apenas em *usá-las*, tornando o sistema mais flexível.
3.  **Descobre locais disponíveis**: Apresenta-nos uma lista dos locais que a API do IPMA consegue reconhecer (como "Lisboa", "Braga", etc.), o que é útil para sabermos quais nomes podemos usar nos nossos testes.
4.  **Define um local alvo**: Escolhe um local específico (por exemplo, "Braga") para o qual queremos obter a previsão.
5.  **Executa o fluxo principal**: Pede ao `MainController` para ir buscar a previsão meteorológica para esse local e processar os dados recebidos.
6.  **Mostra os resultados**: Apresenta de forma organizada e fácil de ler a informação meteorológica processada diretamente na consola, incluindo temperaturas, descrições do tempo e detalhes do vento.

Em resumo, este ficheiro é essencial para verificar se todas as partes do sistema (a API, o glossário e o controller) estão a trabalhar em conjunto de forma correta e se a informação final é apresentada como esperado. É um guia passo-a-passo do nosso sistema em funcionamento!

## 🧠 Funções principais

- **`setup_logging()`**
    - **O que faz:** Prepara o sistema de `logging` (registo de mensagens) para que possamos ver informações detalhadas sobre a execução do script no terminal. Isto inclui mensagens informativas (`INFO`) e de erro (`ERROR`).
    - **Como funciona:** Garante que o logging não é configurado múltiplas vezes e define o formato das mensagens, que inclui a data/hora, o tipo de mensagem (INFO, ERROR) e a própria mensagem.

- **`run_test_flow()`**
    - **O que faz:** É a função principal que orquestra toda a sequência de teste.
    - **Como funciona:**
        1.  **Configura o Logging:** Chama `setup_logging()` logo no início.
        2.  **Instancia Dependências:** Cria uma instância da `IPMAApi` (que é a ponte para os dados do IPMA).
        3.  **Cria o `MainController`:** Aqui demonstramos a **Injeção de Dependência**. Passamos a instância da `IPMAApi` e as funções `get_weather_description`, `get_location_name`, `get_wind_speed_description` (do `static_data/weather_glossary.py`) diretamente para o `MainController` ao criá-lo. O controller usa estas funções para *traduzir* os códigos numéricos da API em descrições legíveis.
        4.  **Lista e Mostra Locais Disponíveis:** Pede ao `MainController` (`main_controller.get_available_location_names()`) a lista de todos os locais que ele já carregou (o `MainController` faz isto automaticamente no seu início) e imprime-a, o que nos ajuda a escolher um local de teste válido.
        5.  **Define o Local de Teste:** Escolhe "Braga" como o local alvo (podes alterar para qualquer local da lista que apareceu!).
        6.  **Define a Localização no Controller:** Usa `main_controller.set_location_by_name(target_location_name)` para dizer ao controller qual o local para o qual queremos a previsão.
        7.  **Busca e Processa a Previsão:** Se o local for definido com sucesso, chama `main_controller.fetch_and_display_forecast()` para que o controller obtenha os dados da API e os processe.
        8.  **Apresenta os Resultados:** Recolhe os dados meteorológicos já processados (`main_controller.get_current_weather_data()`) e imprime-os de forma clara no terminal.
        9.  **Trata Erros:** Inclui verificações para mostrar mensagens de erro caso a definição do local ou a obtenção da previsão falhem.

- **Bloco `if __name__ == "__main__":`**
    - **O que faz:** É uma convenção em Python que assegura que a função `run_test_flow()` só é executada quando este ficheiro `test_controller_flow.py` é corrido diretamente (e não quando é importado por outro script como um módulo).

## 🔁 Relações com outros ficheiros

- 📁 **`test_controller_flow.py`** é um script de "orquestração" que testa a colaboração entre os seguintes módulos principais:
    - 📁 **`models/ipma_api.py`**: Este script cria e passa uma instância da `IPMAApi` para o `MainController`. `IPMAApi` é responsável por comunicar com a API do IPMA.
    - 📁 **`static_data/weather_glossary.py`**: As funções de tradução (`get_weather_description`, `get_location_name`, `get_wind_speed_description`) deste módulo são passadas para o `MainController`. Elas convertem os códigos da API em descrições legíveis.
    - 📁 **`controllers/main_controller.py`**: É o "cérebro" da aplicação. Este script importa-o e testa as suas funcionalidades, como definir um local e buscar previsões.
    - Módulos padrão do Python (`logging`, `sys`, `os`): São usados para gerir o registo de mensagens e para garantir que os outros módulos do projeto são encontrados corretamente (ajustes ao `sys.path`).

- **Este script é utilizado por:**
    - Ti e outros desenvolvedores, para verificar de forma rápida e prática se o fluxo principal da aplicação está a funcionar como esperado.

## 📌 Tópicos Essenciais para Compreender

-   **Testes de Integração:** Este ficheiro é um excelente exemplo de como testar múltiplos componentes de software (como o `MainController`, `IPMAApi`, `weather_glossary`) em conjunto, simulando um cenário real.
-   **Injeção de Dependência (DI):** Observa como o `MainController` *recebe* as suas dependências (a `IPMAApi`, as funções do glossary) em vez de as *criar internamente*. Isto torna o código mais "desacoplado" (menos dependente de detalhes específicos) e muito mais fácil de testar.
-   **Fluxo de Dados:** Segue a "viagem" dos dados: desde a sua origem bruta na `IPMAApi`, passando pela sua transformação pelas funções de `weather_glossary`, até à sua utilização final no `MainController` e exibição neste script.
-   **Configuração de Logging:** Aprende a usar o módulo `logging` do Python para obter feedback detalhado sobre o que o teu programa está a fazer, essencial para depuração e monitorização.
-   **Organização de Projetos e Imports (`sys.path`):** Entende porque modificamos o `sys.path` para garantir que o Python encontra os ficheiros certos, especialmente quando o código está organizado em pastas diferentes (como `tests/`, `models/`, etc.). (Nota: Este é um tópico que pode ser otimizado futuramente para projetos maiores.)

## 💡 Otimizações e Melhorias Futuras

-   **Testes Unitários com Mocks:**
    -   **O quê:** Para garantir que cada parte do `MainController` funciona perfeitamente, mesmo sem precisar da API real (o que acelera os testes e os torna mais fiáveis). Podemos criar "versões falsas" (mocks) das dependências que devolvem respostas controladas.
    -   **Ação Recomendada:** Pode criar um novo ficheiro de testes (`tests/test_mock_controller.py`) para este propósito, utilizando a biblioteca `unittest.mock`.

-   **Validação Automatizada de Resultados:**
    -   **O quê:** Em vez de apenas imprimir os resultados, o script poderia verificar automaticamente se os dados recebidos (temperaturas, descrições) estão dentro de um formato esperado ou de um intervalo razoável.
    -   **Ação Recomendada:** Incorporar asserções (`assert statements` ou métodos de `unittest.TestCase`) para verificar a corretude dos dados de `output_data`.

-   **Gestão Robusta de Imports:**
    -   **O quê:** A modificação manual do `sys.path` é funcional para este projeto, mas em sistemas maiores, pode ser otimizada.
    -   **Ação Recomendada:** À medida que o projeto cresce, podemos explorar formas mais "padrão" de gerir os imports, como estruturar o projeto como um pacote Python instalável.