# 📄 views/main_window.py e views/minimal_window.py

## 🔍 O que fazem estes ficheiros?:
Estes dois ficheiros definem as interfaces gráficas (Views) da aplicação "Guia de Praias", usando a biblioteca Tkinter do Python.

-   **`main_window.py`**: Implementa a interface gráfica principal e mais completa. Esta janela oferece uma experiência detalhada, incluindo um cabeçalho com logotipo, seleção de localização via `Combobox`, um botão de busca e uma área dedicada para exibir os resultados detalhados da previsão meteorológica (data, temperaturas mínima/máxima, descrição do tempo, direção e velocidade do vento). Ela também suporta o carregamento e redimensionamento de imagens de fundo e logotipo (requer Pillow), e utiliza estilos `ttk` para um visual mais moderno e organizado.
-   **`minimal_window.py`**: Implementa uma interface gráfica mais simples e focada. Possui um cabeçalho básico, um `Combobox` para selecionar a localização, um botão de busca e uma única área de texto para exibir a previsão de forma concisa. Esta versão é otimizada para ocupar menos espaço e apresentar a informação essencial de maneira direta.

Ambas as classes herdam de `ttk.Frame`, sugerindo que podem ser integradas em layouts mais complexos, mas `main_window.py` configura o `master` (a janela root) diretamente, enquanto `minimal_window.py` configura o `master` para que a sua própria frame se encaixe nele.

## 🧠 Funções principais

### `views/main_window.py`
-   `__init__(self, master, controller, project_root_dir, ...)` 🏗️: Construtor da janela principal. Inicializa a janela, configura estilos `ttk`, carrega assets (logo e fundo), cria os widgets da UI e carrega as localizações disponíveis para o `Combobox`.
-   `_configure_styles(self)` 🎨: Define temas e estilos personalizados para os vários widgets `ttk` (frames, labels, botões, combobox), usando cores e fontes pré-definidas para garantir consistência visual.
-   `_load_assets(self)` 🖼️: Tenta carregar imagens de logotipo (`logo_praias.png`) e de fundo (`fundo_praias.png`) a partir do `project_root_dir`. Usa Pillow se disponível. Posiciona o logotipo e prepara o `Canvas` para receber a imagem de fundo.
-   `_resize_background_image(self, event)` 📏: Função vinculada a eventos de redimensionamento. Redimensiona a imagem de fundo para que se ajuste às novas dimensões da janela, mantendo a proporção.
-   `_create_widgets(self)` 🛠️: Monta a estrutura da UI: frame de cabeçalho com título, frame de conteúdo principal para inputs e resultados, o `Combobox` para localização, o botão de busca e a área de exibição dos resultados. Organiza estes elementos usando o sistema de grid.
-   `populate_results_area(self, parent_frame)` 📝: Cria dinamicamente os widgets `Label` que irão exibir os diferentes campos da previsão meteorológica (data, temperatura, etc.). Armazena referências a esses `Label`s em `self.result_labels` para facilitar atualizações futuras.
-   `_load_locations_into_combobox(self)` 🌍: Obtém a lista de nomes de locais do `controller`, ordena-os e preenche o `Combobox` de localização. Lida com erros caso os locais não possam ser carregados.
-   `_on_location_selected(self, event)` 📍: Callback acionado quando o utilizador seleciona um item no `Combobox`. Comunica a seleção ao `controller` e atualiza o feedback visual.
-   `_search_button_command(self)` 🔍: Callback do botão de busca. Verifica se uma localização está selecionada, chama o `controller` para buscar a previsão e, em seguida, atualiza a UI com os dados recebidos ou exibe mensagens de erro.
-   `_update_results_display(self, data)` 🔄: Atualiza os `Label`s na `results_frame` com os dados reais da previsão meteorológica recebidos.
-   `_clear_results_display(self)` 🧹: Limpa os campos de exibição de resultados, retornando-os ao estado padrão.

### `views/minimal_window.py`
-   `__init__(self, master, controller, ...)` 🏗️: Construtor da janela minimalista. Define o título, tamanho inicial, configura estilos `ttk` básicos, cria os widgets essenciais (cabeçalho, combobox, botão, label de resultado) e carrega os locais disponíveis.
-   `_configure_styles(self)` 🎨: Define um conjunto de estilos `ttk` mais simples, focados em cores primárias, secundárias e de fundo básicas.
-   `_create_widgets(self)` 🛠️: Monta a estrutura da UI minimalista: um cabeçalho, um frame de entrada com `Label` e `Combobox`, um botão "Buscar Previsão" e um único `Label` para exibir todos os resultados consolidados. Usa `grid` para organizar estes elementos.
-   `_load_locations_into_combobox(self)` 🌍: Similar à versão `main_window`, carrega os nomes de locais do `controller` e os insere no `Combobox`.
-   `_on_location_selected(self, event)` 📍: Callback para a seleção no `Combobox`. Notifica o `controller` e fornece feedback ao utilizador através do `results_label`.
-   `_search_button_command(self)` 🔍: Callback do botão "Buscar Previsão". Verifica a seleção de localização, chama o `controller` para obter a previsão e apresenta os dados consolidados no `results_label`.

## 🔁 Relações com outros ficheiros
-   Ambos os ficheiros (`main_window.py` e `minimal_window.py`) importam e dependem do `controllers.main_controller.MainController` para obter dados e executar a lógica de negócios.
-   Ambos utilizam `tkinter` e `tkinter.ttk` para construir a interface gráfica.
-   Ambos importam `logging` para registo de eventos e `messagebox` para exibir alertas e erros.
-   `main_window.py` também importa `os` para manipulação de caminhos de ficheiros e tenta importar `PIL` (Pillow) para suporte a imagens, usando `ImageTk` e `Image`.
-   Estes ficheiros são, por sua vez, importados e utilizados pelo `main.py`, que decide qual delas instanciar com base nos argumentos de linha de comando.

## 📌 O que estudar para entender estes ficheiros
-   **Tkinter e ttk**: Como criar janelas, frames, labels, comboboxes, botões e usar layouts (especialmente `grid`).
-   **Estilização com `ttk.Style`**: Entender como criar temas e mapear estados para widgets `ttk`.
-   **Callbacks e Event Binding**: Como vincular eventos de widgets (ex: `<<ComboboxSelected>>`) a funções Python.
-   **Variáveis de Controle (`tk.StringVar`)**: Como usá-las para ligar dados a widgets e receber atualizações.
-   **Manipulação de Imagens (com Pillow)**: Se estiver a trabalhar com `main_window.py`, entender `PIL.Image`, `ImageTk.PhotoImage`, `resize()`, e como referenciar imagens para evitar que sejam garbage collected.
-   **Padrão de Design MVC/MVVM (Contexto)**: Compreender o papel destas classes como "Views" num padrão de arquitetura de aplicação.

## 💡 Sugestões de melhoria
-   **`main_window.py`**:
    -   📉 **Gestão de Assets**: Tornar o carregamento de assets mais robusto, talvez com um fallback para cores sólidas se as imagens falharem, e gerir melhor as referências de imagem para evitar vazamentos de memória (embora `self.image = ...` ajude).
    -   ✨ **Elementos Visuais Adicionais**: Adicionar ícones para as traduções das condições meteorológicas, talvez um `Progressbar` durante a busca, ou tooltips informativos.
    -   🚀 **Layout Responsivo** (Avançado): Embora o `STICKY` ajude, um layout verdadeiramente responsivo em Tkinter pode ser complexo, especialmente com imagens de fundo.
-   **`minimal_window.py`**:
    -   📦 **Mais Informação no Resultado**: O `results_label` está a exibir tudo numa única string. Poderia ser melhor formatado com mais `Label`s, mesmo num layout simples, para clareza.
    -   🎨 **Paleta de Cores**: Explorar outras paletas de cores que possam ser mais apelativas ou consistentes com a identidade visual, se houver.
    -   🔄 **Feedback de Carregamento**: Adicionar um indicador visual (como um texto "A carregar...") enquanto a previsão está a ser obtida.
-   **Para Ambos**:
    -   ❌ **Tratamento de Erros do Controller**: As mensagens de aviso/erro que vêm do controller poderiam ser melhor integradas na UI (ex: através de um status bar ou banners).
    -   ✅ **Validação de Input**: Para além de selecionar, garantir que a localização selecionada é válida antes de prosseguir. (Embora o `controller` já faça parte disto).