# Scraper
Entrar a la caperta scraper
```
cd scraper
```
Entrar en ambiente virtual que debe tener la version 3.11 de python
- Ya que tiene todas las dependencias para funcionar
En caso de no estar la carpeta crearla con:
```
python -m venv venv
```
``` 
source venv/bin/activate
```
Correr el archivo python dentro de /scraper, notese que al estar en el ambiente virtual aparecerá un *(venv)* antes del bash.
Instalar dependencias:
```
pip install selenium-wire selenium requests
```
```
pip install blinker==1.4
```
Correr el scraper:
```
python wazeScraper.py
```