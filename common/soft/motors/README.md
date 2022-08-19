motors.py программа для управления моторами через gpio на python.
Выполняет тестовое перемещение вперед, назад, влево, вправо по 1 секунде.

ride.py программа для управления роботом с клавиатуры

Для установки сделать

pip3 install Jetson.GPIO

sudo groupadd -f -r <gpio_group_name>

sudo usermod -a -G <gpio_group_name> <user_name>
