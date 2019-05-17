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
  6. doxygen (min. 1.8.15; ścieżka do doxygen **MUSI** być ustawiona jako zmienna środowiskowa, aby skrypt **generate_doc.bat** mógł się wykonać)
  7. virtualenv, Flask, flask-socketio, eventlet, pyd, pytest (do zainstalowania poprzez skrypt -> **scripts/Windows/prequisities.bat**)
- **Linux (Ubuntu 16.04 Xenial)**
  1. g++
  2. doxygen
  3. Python 3.5m, libboost-all-dev (boost), scons, python3-pip, virtualenv, Flask, flask-socketio, eventlet, pytest (do zainstalowania poprzez skrypt -> **scripts/Linux/prequisities.sh**)

### Kompilacja
Należy wejść do katalogu scripts, wybrać katalog Linux/Windows, a następnie uruchomić skrpyt:
**build.sh / build.bat**

### Czyszczenie plików utworzonych przy budowaniu projektu
Należy wejść do katalogu scripts, wybrać katalog Linux/Windows, a następnie uruchomić skrpyt:
**clean.sh / clean.bat**

### Uruchamianie serwera (wraz z automatycznymi testami)
Należy wejść do katalogu scripts, wybrać katalog Linux/Windows, a następnie uruchomić skrpyt: 
**runServer.sh / runServer.bat**

### Generacja dokumentacji
Należy wejść do katalogu scripts, wybrać katalog Linux/Windows, a następnie uruchomić skrpyt: 
**generate_doc.sh / generate_doc.bat**

## Uwagi
Aby usunąć wirtualne środowisko tworzone przy wykonywaniu się skryptu prequisities należy wejść do katalogu scripts, wybrać katalog Linux/Windows, a następnie uruchomić skrpyt:
 **remove_venv.sh / remove_venv.bat**.

## Autorzy
- **Bochenek Mateusz** - [mbochene](https://github.com/mbochene)
- **Adrian Nadratowski** - [nadadrian](https://github.com/nadadrian)

