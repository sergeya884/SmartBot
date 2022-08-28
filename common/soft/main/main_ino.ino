// Библиотека для работы с Multiservo Shield
// https://github.com/amperka/Multiservo
#include <Multiservo.h>

// Motor shield использует четыре контакта 4, 5, 6, 7 для управления моторами 
// 4 и 7 — для направления, 5 и 6 — для скорости
#define SPEED_1      5 
#define DIR_1        4
#define SPEED_2      6
#define DIR_2        7

// Пины управления L293d
#define TOWER_L      9
#define TOWER_R      10

// Пин управления реле пушки
#define FIRE         11 

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

// Функция движения. Route направление: 1-вперед(в сторону манипулятора), 
// 2 - назад, 3 - влево, 4 - вправо. Speed скорость от 0 до 255.
void go(int Route, int Speed){
  // Если движемся вперед или вправо, то левые моторы крутится вперед
  if (Route == 1 or Route == 4) digitalWrite(DIR_1, HIGH);
  // Если назад или влево, то левые крутится назад 
  else digitalWrite(DIR_1, LOW);
  
  // Аналогично с правыми моторами
  if (Route == 2 or Route == 4) digitalWrite(DIR_2, HIGH);
  else digitalWrite(DIR_2, LOW);
  
  // Включаем моторы с заданной скоростью
  analogWrite(SPEED_1, Speed);
  analogWrite(SPEED_2, Speed);
}

// Функция остановки, выключаем шасси и башню
void Stop(){
  analogWrite(SPEED_1, 0);
  analogWrite(SPEED_2, 0);
  analogWrite(TOWER_L, 0);
  analogWrite(TOWER_R, 0);
}

// Функция "огонь"
void fire(){
  // Включить и выключить реле на пушке
  analogWrite(FIRE, 255);
  delay(500);
  digitalWrite(FIRE, LOW);
  delay(50);
  multiservo[7].write(180);
  delay(400);
  multiservo[7].write(0);
  delay(400);
}

// Функция поворота башни. Route направление: 1 - влево, 2 - вправо. Speed скорость от 0 до 255.
void tower(int Route, int Speed){
  if (Route == 1) {
    analogWrite(TOWER_R, 0);
    analogWrite(TOWER_L, Speed);
  }
  else {
    analogWrite(TOWER_L, 0);
    analogWrite(TOWER_R, Speed);
  }
}

void setup() {
   // настраиваем выводы платы 4, 5, 6, 7 на вывод сигналов 
  for (int i = 4; i < 8; i++) pinMode(i, OUTPUT);
  Serial.begin(9600);

  // Подключкаем сервоприводы
  for (int count = 0; count < MULTI_SERVO_COUNT; count++) {
    multiservo[count].attach(count);
  }
  multiservo[0].write(90);
  multiservo[1].write(10);
  multiservo[2].write(70);
  multiservo[3].write(90);
  multiservo[4].write(0);
  multiservo[5].write(90);
  multiservo[6].write(90);
  multiservo[7].write(0);

} 

void loop() {
  if (Serial.available() > 0) {
    
    // Читаем порт
    Str = Serial.readStringUntil('\n');

    // Если пришла команда "огонь"
    if (Str.equals("f")) fire();

    // Если пришла команда "поехать"
    if (Str.equals("g")) {
      // Читаем детали
      Str = Serial.readStringUntil('\n');
      // Разбиваем пришедшую команду на направление и скорость
      StrSplit(Str);
      // Поехали
      go(s1, s2);
    }

    // Если пришла команда "стоп"
    if (Str.equals("s")) Stop();

    // Если пришла команда управления манипуляторам
    if (Str.equals("m")) {
      // Читаем детали
      Str = Serial.readStringUntil('\n');
      // Разбиваем пришедшую команду на номер сервы и угол
      StrSplit(Str);
      // Устанавливаем серво
      multiservo[s1].write(s2);
    }
    
    // Если пришла команда поворота башни
    if (Str.equals("t")) {
      // Читаем детали
      Str = Serial.readStringUntil('\n');
      // Разбиваем пришедшую команду на направление и скорость
      StrSplit(Str);
      // Поворачиваем башню
      tower(s1, s2);
    }
  }
  //go(5,0);
}
