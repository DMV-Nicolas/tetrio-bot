# TETRIO BOT

Bot para jugar al tetrio.\
Este documento explica cómo instalarlo y usarlo en Linux.

# Grupo Avocado - Introducción a los sistemas inteligentes
- Gabriel Andres Anzola Tachak (1000150107)<br>
- Nicolas David Moreno Villanueva (1024480471)

------------------------------------------------------------------------

## 📦 Instalación (Linux)

### 1. Clonar el repositorio

``` bash
git clone git@github.com:DMV-Nicolas/tetrio-bot.git
```

### 2. Instalar dependencias

Asegúrate de tener **Python** y **pip** instalados.

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## ▶️ Uso (Linux)

### 1. Importar la configuración en TETRIO

Dentro de **TETRIO**, importa el archivo:

    tetrio_config.ttc

### 2. Generar dimensiones del juego

Ejecuta el script para establecer correctamente el área del juego:

``` bash
python generate_dimensions.py
```

### 3. Ejecutar el bot

Inicia el bot con:

``` bash
python main.py
```

------------------------------------------------------------------------

## 📝 Notas


-   Si cambias la resolución o el tamaño de la ventana del juego, vuelve
    a ejecutar:

``` bash
python generate_dimensions.py
```
