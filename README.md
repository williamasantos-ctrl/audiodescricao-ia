\# 🎙️ Audiodescrição IA



Sistema de audiodescrição automática em tempo real usando \*\*Gemini AI + OpenCV + Edge TTS + Python\*\*.



O projeto analisa frames de vídeos locais, YouTube ou TikTok e gera descrições narradas por voz automaticamente.



\---



\## ✨ Funcionalidades



\* 🎥 Leitura de vídeos locais (`.mp4`)

\* 🌐 Suporte a links do YouTube e TikTok

\* 🤖 Análise visual com Google Gemini

\* 🔊 Conversão texto → voz com Edge TTS

\* 🖼️ Captura automática de frames

\* ⚡ Processamento em tempo real



\---



\## 📦 Tecnologias usadas



\* Python 3.12+

\* Google Gemini API

\* OpenCV

\* Edge-TTS

\* Pygame

\* Pillow

\* Whisper (opcional)



\---



\## 🚀 Instalação



Clone o repositório:



```bash

git clone https://github.com/williamasantos-ctrl/audiodescricao-ia.git

```



Entre na pasta:



```bash

cd audiodescricao-ia

```



Crie ambiente virtual:



\### Windows



```bash

python -m venv venv

venv\\Scripts\\activate

```



\### Linux / Mac



```bash

python3 -m venv venv

source venv/bin/activate

```



Instale as dependências:



```bash

pip install -r requirements.txt

```



\---



\## 🔑 Configuração da API Gemini



Crie um arquivo chamado `.env` na raiz do projeto.



Exemplo:



```env

GEMINI\_API\_KEY=sua\_api\_key\_aqui

```



Para gerar sua chave:



1\. Acesse Google AI Studio

2\. Crie uma API Key

3\. Copie a chave para o arquivo `.env`



\---



\## ▶️ Como executar



Execute:



```bash

python main.py

```



O programa pedirá um vídeo.



Você pode fornecer:



\### Arquivo local



```txt

C:\\videos\\meuvideo.mp4

```



\### Link YouTube



```txt

https://youtube.com/...

```



\### Link TikTok



```txt

https://tiktok.com/...

```



\---



\## 📁 Estrutura do projeto



```txt

audiodescricao\_ai/

│

├── main.py

├── config.py

├── prompts.py

├── test\_flash.py

├── .env

├── requirements.txt

│

├── audio/

│   └── temp/

│

└── frames/

```



\---



\## ⚠️ Observações



O arquivo `.env` \*\*não deve ser enviado ao GitHub\*\*.



A chave da API deve permanecer privada.





