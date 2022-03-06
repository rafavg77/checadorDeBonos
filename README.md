# checadorDeBonos
Telegram bot para revisar el saldo de los bonos

## Instalación
```bash
$ git clone git@github.com:rafavg77/checadorDeBonos.git
$ #Instalar chromiun
$ sudo apt-get install chromium-chromedriver
$ #acceder a carpeta de proyecto
$ cd checadorDeBonos
$ #Crear ambiente virtual
$ virtualevn venv
$ #Ejecutar ambiente virtual
$ source venv/bin/active
$ #Instalar Depedencias
$ pip3 install -r requeriments.txt
$ cd .. 
$ cd systemd
$ # Crear servicios systemd
$ sudo cp bot-checadorBonos-telegram.service /etc/systemd/system/bot-checadorBonos-telegram.service
$ sudo systemctl enable bot-checadorBonos-telegram.service
$ # Ejecutar bot
$ sudo service bot-checadorBonos-telegram start
$ sudo service bot-checadorBonos-telegram status
```
