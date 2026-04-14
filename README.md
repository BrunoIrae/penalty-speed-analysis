# ⚽ Penalty Speed Analysis (Visão Computacional)

## 🎓 Tema do Projeto
**Tema 4 - Análise de esportes**

---

## 👥 Integrantes do Grupo
- **Bruno Iraê dos Reis**
- **Leonardo Henrique Caturyty da Silva Cavalcante**

---
## 📌 Descrição

Este projeto utiliza técnicas de visão computacional para analisar um vídeo de pênalti e calcular a velocidade da bola.

O sistema realiza:
- 🎯 Rastreamento da bola
- 🚀 Detecção do momento do chute
- ⚽ Detecção automática do gol
- 📊 Cálculo de velocidade máxima e média

---

## 🧠 Tecnologias Utilizadas

- Python
- OpenCV
- YOLO (Ultralytics)
- NumPy

---

## ⚙️ Como o Algoritmo Funciona

1. O usuário seleciona a bola manualmente no primeiro frame
2. O sistema utiliza YOLO para detectar a bola nos frames seguintes
3. Aplica suavização para evitar ruídos no tracking
4. Caso a bola seja ocultada (ex: goleiro), o sistema prevê sua posição (oclusão)
5. Calcula a velocidade com base no deslocamento entre frames
6. Detecta o gol quando a **frente da bola cruza a linha da trave**

---

## 🚀 Como Executar o Projeto

### 📦 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/penalty-speed-analysis.git
cd penalty-speed-analysis
```

### 🐍 2. Criar ambiente virtual
```bash
python -m venv .venv
```
### Ativar (Windows):
```bash
.venv\Scripts\activate
```
### 📥 3. Instalar dependências
```bash
pip install -r requirements.txt
```
### 🤖 4. YOLO (Importante)
```bash
model = YOLO("yolov8s.pt")
```
### 🎥 5. Adicionar o vídeo
```bash
penalti.mp4
```
### ▶️ 6. Executar
```bash
python main.py
```
