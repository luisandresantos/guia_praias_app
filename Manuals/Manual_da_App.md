# 🏖️ Guia de Praias - Manual de Utilização

## 📅 Data da Última Atualização: 2025-08-08 

Este manual explica como obter a previsão meteorológica das praias portuguesas usando a aplicação "Guia de Praias", desenvolvida em Python com a API do IPMA.

---

## 1. Sobre a Aplicação

O "Guia de Praias" é uma aplicação desktop desenvolvida em Python que consome dados da API aberta do IPMA. Permite consultar a previsão meteorológica para diversas localizações em Portugal através de interfaces gráficas intuitivas (`tkinter`).

## 2. Requisitos do Sistema

Para executar a aplicação, necessitará de ter instalado:

*   **Sistema Operativo:** Qualquer sistema que suporte Python (Windows, macOS, Linux).
*   **Python:** Versão 3.x (recomendado 3.7 ou superior).
*   **Dependências:** Listadas em `requirements.txt`.

## 3. Instalação


1.  **Clone o repositório**:
    ```bash
    git clone https://github.com/luisandresantos/guia_praias_app.git
    cd guia_praias_app
    ```
2.  **Crie um ambiente virtual** (recomendado):
    ```bash
    python -m venv venv
    ```
3.  **Ative o ambiente virtual:**
    *   Windows: `.\venv\Scripts\activate`
    *   macOS/Linux: `source venv/bin/activate`
4.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

---

## 4. Executando a Aplicação

A aplicação pode ser iniciada a partir do terminal na pasta raiz do projeto.

*   **Para iniciar a interface completa (`MainWindow`):**
    ```bash
    python main.py
    ```

*   **Para iniciar a interface minimalista (`MinimalWindow`):**
    ```bash
    python main.py --view minimal
    ```
    

---

## 5. Como Usar a Aplicação

Após iniciar a aplicação, verá uma janela. Siga estes passos:

### 5.1 Selecionando um Local

*   Utilize o menu dropdown (Combobox) para escolher uma cidade ou região de Portugal.

### 5.2 Obtendo a Previsão

*   Clique no botão "Buscar Previsão" (ou similar).
*   A aplicação comunicará com a API do IPMA.

### 5.3 Visualizando os Resultados

*   Os detalhes da previsão (temperatura, descrição do tempo, vento, etc.) serão exibidos na área de resultados.
*   Os dados são apresentados em português, graças a um glossário interno.

---

## 6. Conhecendo os Componentes (Visão Rápida)

Para entender como a aplicação funciona por baixo do capô:

*   **`main.py`:** O ponto de partida que inicia tudo.
*   **`models/ipma_api.py`:** Busca os dados "crus" da API do IPMA.
*   **`static_data/weather_glossary.py`:** Traduz códigos (ex: tempo, vento) em texto legível.
*   **`controllers/main_controller.py`:** Orquestra a lógica, coordena Model, Glossary e View.
*   **`views/*.py`:** São as interfaces (`MainWindow`, `MinimalWindow`) que mostram a informação.

---

## 7. Vantagens da Arquitetura

A estrutura do projeto (MVC-like, Injeção de Dependência) garante:

*   **Modularidade:** Fácil de adicionar ou modificar partes.
*   **Testabilidade:** Código mais simples de testar e verificar.
*   **Organização:** Clara separação de responsabilidades.

---

## 8. Resolução de Problemas Comuns

*   **Erro de Dependências:** Certifique-se de ativar o ambiente virtual (`venv`) e instalar com `pip install -r requirements.txt`.
*   **Carregamento Lento:** Pode ser a API do IPMA; o *caching* no `ipma_api.py` ajuda em chamadas repetidas.
*   **Dados Incorretos/Ausentes:** Verifique a localização selecionada e a disponibilidade de dados para ela na API do IPMA.

---

## 9. Ideias Futuras

*   Mais dados da API do IPMA (marés, ondas).
*   Integração com bases de dados locais (SQLite) para histórico.
*   Gráficos de previsão (com `matplotlib`).

---

## 10. Dúvidas?

Se tiver alguma questão sobre o uso da aplicação, não hesite em perguntar!