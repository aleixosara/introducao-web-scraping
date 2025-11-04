# --- variáveis ---
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

gitIsa:
	git config --global user.name "isa"
	git config --global user.email "isadora.izlou@gmail.com"
	@echo "Git configurado para Isa!"

gitAna:
	git config --global user.name "ana"
	git config --global user.email "ana.luiza.kauffman@gmail.com"
	@echo "Git configurado para Ana!"

gitSara:
	git config --global user.name "sara"
	git config --global user.email "20233005742@estudantes.ifpr.edu.br"
	@echo "Git configurado para Sara!"

# --- instala tudo automaticamente ---
setup:
	@echo "Criando ambiente virtual..."
	python3 -m venv $(VENV)
	@echo "Instalando dependências..."
	$(PIP) install --upgrade pip
	$(PIP) install flask requests beautifulsoup4 lxml
	@echo "Salvando dependências em requirements.txt..."
	$(PIP) freeze > requirements.txt
	@echo "Ambiente pronto! Ative com: source venv/bin/activate"

# --- roda o app Flask ---
run:
	@echo "Iniciando servidor Flask..."
	$(PYTHON) app.py