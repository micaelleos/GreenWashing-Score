# **Análise de Relatórios de ESG e Detecção de Greenwashing**

Este projeto é uma aplicação interativa desenvolvida com **Streamlit**, **LangChain**, e **LangGraph**, projetada para realizar a ingestão e análise de relatórios de Empresas com Compromissos com o Meio Ambiente, Social e Governança (ESG, na sigla em inglês). A ferramenta identifica potenciais indícios de **greenwashing** nos relatórios e atribui uma pontuação com base em critérios específicos. O usuário pode também pesquisar informações no documento por meio de um chat baseado em recuperação de conhecimento (*Retrieval-Augmented Generation* - RAG).

---

## **Funcionalidades**
1. **Upload de Relatórios**:
   - Permite ao usuário fazer o upload de arquivos de relatórios ESG no formato PDF ou texto.
   
2. **Análise Automática**:
   - A ferramenta avalia o relatório com base em critérios predefinidos de risco de **greenwashing**, como:
     - Linguagem vaga ou exagerada.
     - Ausência de métricas claras.
     - Relatos desproporcionais ou inconsistentes com dados financeiros ou de impacto ambiental.

3. **Pontuação de Risco**:
   - Atribui uma pontuação de risco ao relatório, indicando o grau de probabilidade de **greenwashing**.

4. **Chat RAG**:
   - Oferece um sistema de busca interativa, permitindo ao usuário consultar o conteúdo do relatório por meio de perguntas e respostas.

5. **Interface Intuitiva**:
   - Desenvolvido com Streamlit, o app é de fácil navegação e visualização dos resultados.

---

## **Instalação**
Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### **Pré-requisitos**
Certifique-se de que você tem as seguintes ferramentas instaladas:
- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

### **Passo 1: Clone o Repositório**
```bash
git clone https://github.com/seuusuario/nome-do-repositorio.git
cd nome-do-repositorio
```

### **Passo 2: Crie um Ambiente Virtual**
```bash
python -m venv venv
source venv/bin/activate  # No Windows, use: venv\Scripts\activate
```

### **Passo 3: Instale as Dependências**
```bash
pip install -r requirements.txt
```

### **Passo 4: Configure as Variáveis de Ambiente**
Crie um arquivo `.env` na raiz do projeto e configure as seguintes variáveis:
```env
OPENAI_API_KEY=your_openai_api_key
LANGCHAIN_API_KEY=your_langchain_api_key
```

> ⚠️ Substitua `your_openai_api_key` e `your_langchain_api_key` pelas suas chaves de API correspondentes.

### **Passo 5: Execute a Aplicação**
```bash
streamlit run app.py
```

A aplicação estará disponível em [http://localhost:8501](http://localhost:8501).

---

## **Estrutura do Projeto**

```plaintext
GreenWashing Score/
├── app.py                 # Arquivo principal da aplicação Streamlit
├── analysis/
│   ├── risk_scoring.py    # Módulo para cálculo da pontuação de risco
│   ├── criteria.json      # Critérios de análise de greenwashing
├── chat/
│   ├── document_loader.py # Carregamento e processamento de documentos
│   ├── chat_rag.py        # Implementação do Chat RAG com LangChain
├── data/                  # Diretório para armazenar arquivos temporários
├── requirements.txt       # Lista de dependências
├── README.md              # Documentação do projeto
├── .env.example           # Exemplo de configuração de variáveis de ambiente
└── .gitignore             # Arquivos a serem ignorados pelo Git
```

---

## **Licenciamento**
Este software está licenciado sob os seguintes termos:

### **1. Uso Pessoal e Educacional**
Você pode usar, modificar e executar este software **apenas para fins pessoais ou educacionais, sem custo**, desde que o aviso de copyright e os termos de licença sejam incluídos.

### **2. Uso Comercial**
Qualquer uso do software para fins comerciais **requer a compra de uma licença comercial**. Exemplos de uso comercial incluem:
- Integração em produtos ou serviços vendidos ou licenciados.
- Uso em organizações com fins lucrativos.
- Qualquer atividade geradora de receita.

#### Como Adquirir uma Licença Comercial
Entre em contato pelo e-mail [micaelle.osouza@gmail.com] para obter informações sobre planos de licenciamento.

### **3. Proibições**
- Não é permitido sublicenciar, vender ou redistribuir este software sem autorização por escrito.
- Não é permitido remover ou alterar este aviso de licença em qualquer versão do software.

---

## **Contribuindo**
Contribuições são bem-vindas! Siga os passos abaixo para colaborar:

1. Faça um *fork* do projeto.
2. Crie uma nova *branch* para suas alterações:
   ```bash
   git checkout -b minha-feature
   ```
3. Faça *commit* das suas alterações:
   ```bash
   git commit -m "Adiciona nova feature"
   ```
4. Envie para a *branch* principal:
   ```bash
   git push origin minha-feature
   ```
5. Abra um *Pull Request* no GitHub.

---

## **Tecnologias Utilizadas**
- **[Streamlit](https://streamlit.io/):** Para criação da interface interativa.
- **[LangChain](https://www.langchain.com/):** Para implementação de modelos de linguagem e recuperação de dados.
- **[LangGraph](https://github.com/langgraph):** Para orquestração avançada de fluxos de análise.
- **Python:** Linguagem principal do projeto.

---

## **Contato**
Para dúvidas ou suporte, entre em contato:
- **E-mail:** micaelle.osouza@gmail.com
- **GitHub:** [Micaelle Souza](https://github.com/micaelleos)

