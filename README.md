# ZPR - Ultimate tic tac toe
Tematem projektu jest zaimplementowanie gry przeglądarkowej „ultimate tic tac toe” w oparciu o architekturę klient-serwer.

## Technologie
Technologie wykorzystywane w projekcie:
- Python -> Flask, Flask-SocketIO, eventlet, PyTest
- C++ -> boost_unit_test_framework, Boost.Python
- JavaScript

## Budowanie i uruchamianie aplikacji

### Wymagania wstępne
- **Windows**
  1. msvc (min. 14.0)
  2. Python 3.7 (zlokalizowany w C:\Python37 , jeśli scons ma zadziałać bez modyfikacji)
  3. boost 1_70_0 (biblioteki linkowane dynamicznie; zlokalizowany w C:\boost_1_70_0 , jeśli scons ma zadziałać bez modyfikacji)
  4. pip3 (powinien być domyślnie zainstalowany wraz z Pythonem)
  5. scons (powinien być domyślnie zainstalowany wraz z Pythonem)
  6. Flask, flask-socketio, eventlet, pyd, pytest (do zainstalowania poprzez skrypt -> **scripts/Windows/prequisities.bat**)
- **Linux (Ubuntu 16.04 Xenial)**
  1. g++
  2. pyenv (do zainstalowania poprzez skrypt --> **scripts/Linux/install_pyenv.sh**)
  3. Python 2.7.16, libboost-all-dev (boost), scons, python3-pip, Flask, flask-socketio, eventlet, pytest (do zainstalowania poprzez skrypt -> **scripts/Linux/prequisities.sh**)

### Kompilacja
Należy wywołać z poziomu głównego katalogu projektu:
**sconst**

### Czyszczenie plików utworzonych przez SConst
Należy wywołać z poziomu głównego katalogu projektu:
**sconst --clean**

### Uruchamianie serwera (wraz z automatycznymi testami)
Należy wejść do katalogu scripts, wybrać katalog Linux/Windows, a następnie uruchomić skrpyt: 
**runServer**

## Uwagi
Skrypt prequisities.sh pobiera Python 2.7.16 i ustawia tę wersję jako domyślną. Aby przywrócić ustawienia sprzed wywołania skryptu należy wywołać skrypt **scripts/Linux/restore_python_version.sh**.

## Autorzy
- **Bochenek Mateusz** - [mbochene](https://github.com/mbochene)
- **Adrian Nadratowski** - [nadadrian](https://github.com/nadadrian)

