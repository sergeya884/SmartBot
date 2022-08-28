// Библиотека для работы с Multiservo Shield
// https://github.com/amperka/Multiservo
#include <Multiservo.h>

// Задаём количество сервоприводов
constexpr uint8_t MULTI_SERVO_COUNT = 8;
     
// Создаём массив объектов для работы с сервомоторами
Multiservo multiservo[MULTI_SERVO_COUNT];

// Переменные для чтения порта
String Str;
int s1, s2;

// Функция разбиения строки на числа
void StrSplit(String Str1){
  char buffer[6];
  Str1.toCharArray(buffer,6);
  s1=atoi(strtok(buffer," "));
  s2=atoi(strtok(NULL," "));
}

void setup() {

  //Задаем скорость общения
  Serial.begin(9600);

  // Подключкаем сервоприводы
  for (int count = 0; count < MULTI_SERVO_COUNT; count++) multiservo[count].attach(count);
} 

void loop() {
  if (Serial.available() > 0) {
    
    // Читаем порт
    Str = Serial.readStringUntil('\n');

    // Если пришла команда управления манипуляторам
    if (Str.equals("m")) {
      // Читаем детали
      Str = Serial.readStringUntil('\n');
      // Разбиваем пришедшую команду на номер сервы и угол
      StrSplit(Str);
      // Устанавливаем серво
      multiservo[s1].write(s2);
    }
  }
}
