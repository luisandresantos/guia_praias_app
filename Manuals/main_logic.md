# 📄 main.py - no diretório principal

## 🔍 O que faz este ficheiro?:
Este ficheiro atua como o ponto de entrada principal (`entry point`) da aplicação "Guia de Praias - Previsão Meteorológica". Ele é responsável por inicializar todo o ambiente necessário para o funcionamento da GUI, incluindo a configuração de logging, a parsing de argumentos de linha de comando para seleção da interface (view), a inicialização do backend (controlador) e o lançamento do loop principal do Tkinter.

## 🧠 Funções principais
- `setup_application_logging()` – Configura o sistema de logging da aplicação. Garante que os logs sejam formatados e exibidos de forma consistente, sendo crucial para depuração e monitorização do fluxo da aplicação.
- `run_application()` 🚀 – Orquestra o início da aplicação. Realiza as seguintes etapas:
    - Chama `setup_application_logging()`.
    - Configura `argparse` para permitir a escolha entre a `MainWindow` (completa) e a `MinimalWindow` (simplificada) através do argumento `--view`.
    - Instancia o `IPMAApi` para comunicação com a API do IPMA.
    - Cria uma instância de `MainController`, passando as dependências do `IPMAApi` e as funções auxiliares para descrição de dados meteorológicos.
    - Inicializa a janela `tk.Tk()` (o `root` da aplicação Tkinter).
    - Com base no argumento `--view` (ou o padrão 'main'), decide qual classe de janela (view) instanciar (`MainWindow` ou `MinimalWindow`).
    - Configura a janela selecionada para expandir e preencher o `root` (usando `grid` e `grid_rowconfigure`/`grid_columnconfigure`).
    - Inicia o `root.mainloop()`, que é o loop de eventos principal do Tkinter, mantendo a aplicação GUI em execução e responsiva.

## 🔁 Relações com outros ficheiros
- 📁 `models/ipma_api.py` 🔗: Este ficheiro importa e instancia a classe `IPMAApi` para interagir com os dados meteorológicos.
- 📁 `static_data/weather_glossary.py` 🔗: Importa funções auxiliares (`get_weather_description`, `get_location_name`, `get_wind_speed_description`) que são passadas para o `MainController`, usadas para traduzir códigos da API em descrições legíveis.
- 📁 `controllers/main_controller.py` 🤝: Importa e instancia o `MainController`, que age como o intermediário entre as views e os modelos, orquestrando a lógica de negócios e a obtenção de dados. O `main.py` passa o `IPMAApi` e as funções de glossário para ele.
- 📁 `views/main_window.py` 🖼️: Importa e, dependendo do argumento `--view`, instancia a `MainWindow`, que é a interface gráfica mais completa da aplicação.
- 📁 `views/minimal_window.py` 🌟: Importa e, se o argumento `--view` for 'minimal', instancia a `MinimalWindow`, uma versão mais simples da interface gráfica.

## 📌 O que estudar para entender este ficheiro
- 🐍 **Programação Orientada a Objetos (POO) em Python**: Entender como classes são instanciadas e como objetos interagem entre si (especialmente no contexto do padrão MVC/MVVM).
- 🖼️ **Tkinter (Módulo GUI do Python)**: Conceitos de `Tk()` (root window), `mainloop()`, `grid()` para layout, e como as widgets são organizadas.
- ⚙️ **`argparse` Module**: Compreender como parser argumentos de linha de comando para tornar a aplicação configurável e flexível.
- 🪵 **`logging` Module**: Saber como configurar e usar o sistema de logging para depuração e monitorização da aplicação.
- 📂 **Estrutura de Projetos Python**: A importância de organizar o código em módulos (`models`, `views`, `controllers`, `static_data`) e como `sys.path` é usado para importar esses módulos.

## 💡 Sugestões de melhoria
- 📏 **Configuração via Ficheiro**: Em vez de apenas argumentos de linha de comando, permitir carregar configurações (como a view padrão ou outras configurações futuras) de um ficheiro (e.g., `.ini`, YAML, JSON) para maior flexibilidade.
- 🧪 **Testes Unitários/Integração**: Embora `main.py` seja um orquestrador, partes da sua lógica de inicialização (como a parsing de argumentos ou a criação condicional da view) poderiam ser testadas para garantir que o setup inicial funciona como esperado.
- 🤝 **Dependency Injection Container**: Para aplicações maiores, um container de injeção de dependências pode simplificar a gestão e passagem de instâncias como `IPMAApi` e `MainController` para as várias partes da aplicação, tornando o código mais testável e modular.
- 🌍 **Internacionalização**: Se houver planos de dar suporte a múltiplos idiomas, o título da janela (`root.title`) e as descrições do `argparse` poderiam ser externalizados.