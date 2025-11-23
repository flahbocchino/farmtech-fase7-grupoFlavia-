# 🌾 FarmTech – Fase 7: A Consolidação de um Sistema  
**FIAP – Inteligência Artificial | Global Solution 2025**  
**Autora:** Flávia Bocchino (RM564213)

---

## 🎯 Descrição do Projeto

O **FarmTech** é um sistema integrado de **gestão inteligente para o agronegócio**, que consolida todas as fases anteriores (1 a 6) em uma única plataforma interativa, desenvolvida em **Python com Streamlit**.  
O projeto simula uma fazenda digital com sensores IoT, visão computacional e alertas automáticos, oferecendo uma visão completa da operação agrícola.

---

## 🧩 Fases Integradas no Sistema

### 🌱 **Fase 1 – Base de Dados Inicial**
- Cálculo de áreas de plantio e manejo de insumos.
- Integração com uma **API meteorológica pública**.
- Criação de base de dados inicial para alimentar o sistema.

### 🧮 **Fase 2 – Banco de Dados Relacional**
- Estruturação de um banco **SQLite** relacional.  
- Integração de dados agrícolas de forma organizada e escalável.

### 🌦️ **Fase 3 – IoT e Automação Inteligente**
- Simulação de sensores (umidade, pH, nutrientes) via **ESP32**.  
- CRUD completo com integração ao banco de dados.  
- Lógica de irrigação automática e alerta em tempo real.

### 📊 **Fase 4 – Dashboard Interativo e Machine Learning**
- Desenvolvimento de **dashboard Streamlit** com visualização de dados em tempo real.  
- Aplicação de modelos preditivos com **Scikit-Learn**.  
- Exibição de recomendações automatizadas de manejo.

### ☁️ **Fase 5 – Cloud Computing & Segurança (AWS)**
- Integração com serviços em nuvem para envio de alertas.  
- Boas práticas de segurança da informação inspiradas em **ISO 27001 e 27002**.

### 👁️ **Fase 6 – Visão Computacional (YOLO)**
- Detecção de **doenças e pragas em folhas** a partir de imagens.  
- Rede neural YOLO para classificação de imagens agrícolas.  
- Resultados exibidos diretamente no dashboard.

### 🔗 **Fase 7 – Consolidação Final**
- Integração de todas as fases anteriores em uma única interface.  
- Sistema centralizado que exibe dados meteorológicos, sensores IoT, visão computacional e produtividade.  
- Geração de alertas inteligentes e visão unificada da fazenda.

---

## 📁 Estrutura do Projeto

```bash
farmtech-fase7-grupoFlavia/
│
├── fase1_base_dados/
├── fase2_banco_relacional/
├── fase3_iot_esp32/
├── fase4_dashboard/
├── fase5_aws/
├── fase6_visao_computacional/
├── fase7_notebook/
├── imagens/               ← prints da dashboard e execução
└── README.md
⚙️ Como Executar o Sistema

Baixar o projeto pelo GitHub:

Acesse o repositório no GitHub.

Clique no botão verde “Code”.

Selecione “Download ZIP”.

Extrair o arquivo ZIP:

Extraia o conteúdo do .zip em uma pasta no seu computador.

Abrir a pasta do projeto:

Abra a pasta extraída no VS Code ou use o Prompt de Comando / PowerShell dentro dessa pasta.

Instalar as dependências (em um terminal dentro da pasta do projeto):
Instalar as dependências (em um terminal dentro da pasta do projeto):

pip install -r requirements.txt


Executar o dashboard (no mesmo terminal):

streamlit run app.py


Abrir no navegador:
👉 Acesse http://localhost:8501

📸 Imagens da Dashboard

As capturas de tela da aplicação em execução estão disponíveis na pasta /imagens

🎥 Vídeo Demonstrativo

📺 Vídeo da apresentação da Fase 7 no YouTube (não listado):
https://www.youtube.com/watch?v=kRjINO9BKbM

Demonstração completa das Fases 1 a 7, com explicação das integrações, execução do dashboard e funcionamento geral do sistema.

🧠 Tecnologias Utilizadas
Categoria	Tecnologias
Linguagem	Python 3.11
Framework	Streamlit
Banco de Dados	SQLite
Bibliotecas	Pandas, NumPy, Matplotlib, Seaborn
Machine Learning	Scikit-Learn
IoT	ESP32 (simulado)
Visão Computacional	YOLO, OpenCV
Cloud	AWS (alertas e integração básica)
💡 Possíveis Expansões Futuras

Implantação real do ESP32-CAM para captura em tempo real.

Integração com AWS Rekognition para análises visuais avançadas.

Previsão de produtividade usando redes neurais profundas.

Aplicativo mobile para controle remoto da fazenda.

🧾 Autoria

Projeto desenvolvido por:
👩‍💻 Flávia Bocchino (RM564213)
📍 São Paulo – FIAP – Inteligência Artificial 2025
