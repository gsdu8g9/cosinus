import datetime

rasp_t = [
  # 0
  {"start": datetime.time(hour=8,  minute=0 ),
   "end"  : datetime.time(hour=9,  minute=30)},
  # 1
  {"start": datetime.time(hour=9,  minute=50),
   "end"  : datetime.time(hour=11, minute=20)},
  # 2
  {"start": datetime.time(hour=11, minute=40),
   "end"  : datetime.time(hour=13, minute=10)},
  # 3
  {"start": datetime.time(hour=13, minute=45),
   "end"  : datetime.time(hour=15, minute=15)},
  # 4
  {"start": datetime.time(hour=15, minute=35),
   "end"  : datetime.time(hour=17, minute=5 )},
  # 5
  {"start": datetime.time(hour=17, minute=25),
   "end"  : datetime.time(hour=18, minute=55)}
]

rasp_a = {
  "5383": [
    # Понедельник
    { (1,2): {"name": "Построение и анализ алгоритмов (лабы)",
              "class": "3402",
              "teacher": "Фирсов Михаил Александрович"},

      (2,0): {"name": "Объектно-ориентированное программирование (лабы)",
              "class": "3402",
              "teacher": "Жукова Наталья Александровна"},

      (3,0): {"name": "Построение и анализ алгоритмов (лекция)",
              "class": "5230",
              "teacher": "Калишенко Евгений Леонидович"},

      (4,1): {"name": "Построение и анализ алгоритмов (лабы)",
              "class": "3402",
              "teacher": "Фирсов Михаил Александрович"},
      
      (5,1): {"name": "Построение и анализ алгоритмов (практика)",
              "class": "3410",
              "teacher": "Фирсов Михаил Александрович"}},

    # Вторник
    { (2,1): {"name": "Объектно-ориентированное программирование (практика)",
              "class": "3402",
              "teacher": "Жукова Наталья Александровна"},

      (2,2): {"name": "Комплексный анализ (лекция)",
              "class": "3238",
              "teacher": "Коточигов Александр Михайлович"},

      (3,0): {"name": "Комплексный анализ (практика)",
              "class": "2414",
              "teacher": "Колпаков Андрей Сергеевич"},

      (4,0): {"name": "Физкультура",
              "class": "4 корпус",
              "teacher": ""},

      (5,0): {"name": "Организация производства и управление предприятием (лекция)",
              "class": "5423",
              "teacher": "Фомина Ирина Германовна"}},

    # Среда
    { (3,0): {"name": "Теория вероятности и мат. статистика (практика)",
              "class": "3427",
              "teacher": "Лифшиц Борис Анатольевич"},

      (4,0): {"name": "Теория вероятности и мат. статистика (лекция)",
              "class": "3324",
              "teacher": "Лифшиц Борис Анатольевич"},

      (5,0): {"name": "Иностранный язык",
              "class": "Кафедра иностранных языков",
              "teacher": ""}},

    # Четверг
    { (1,0): {"name": "Операционные системы (лекция)",
              "class": "3132",
              "teacher": "Губкин Александр Федорович"},

      (2,0): {"name": "Физкультура",
              "class": "4 корпус",
              "teacher": ""},

      (3,2): {"name": "Организация производства и управление предприятием (практика)",
              "class": "2421",
              "teacher": "Жернаков Антон Борисович"}},

    # Пятница
    { (3,0): {"name": "Объектно-ориентированное програмирование (лекция)",
              "class": "3107",
              "teacher": "Плохой Николай Алексеевич"}},

    # Суббота
    {},

    # Воскресенье
    {}

  ],

  "5371": [
    # Понедельник
    {},

    # Вторник
    { (3,0): {"name": "Экономика организации (практика)",
              "class": "2413",
              "teacher": "Голигузова Галина Васильевна"},

      (4,0): {"name": "Физкультура",
              "class": "4 корпус",
              "teacher": "-"},

      (5,0): {"name": "Алгоритмы и структуры данных (лекция)",
              "class": "1158",
              "teacher": "Ильин Владимир Алексеевич"}},

    # Среда
    { (1,1): {"name": "Специальные разделы математического анализа (практика)",
              "class": "3426",
              "teacher": "Дюмин Виктор Георгиевич"},

      (2,0): {"name": "Алгоритмы и структуры данных (практика)",
              "class": "УИТ 4",
              "teacher": "Кирилл Жеронкин"},

      (3,0): {"name": "Специальные разделы математического анализа (лекция)",
              "class": "5405",
              "teacher": "Дюмин Виктор Георгиевич"}},

    # Четверг
    { (1,0): {"name": "Оптика и атомная физика (лекция)",
              "class": "3107",
              "teacher": "Ходьков Дмитрий Афанасьевич"},

      (2,0): {"name": "Физкультура",
              "class": "4 корпус",
              "teacher": "-"},

      (3,2): {"name": "Оптика и атомная физика (лабы)",
              "class": "кафедра Физики",
              "teacher": "Иманбаева Райхан Талгатовна, Чурганова Серафима Сергеевна"}},

    # Пятница
    { (1,1): {"name": "Теоретические основы электротехники (практика)",
              "class": "2401",
              "teacher": "Соколов Валентин Николаевич"},

      (1,2): {"name": "Теоретические основы электротехники (лабы)",
              "class": "Кафедра ТОЭ",
              "teacher": "Соколов Валентин Николаевич"},

      (2,0): {"name": "Теоретические основы электротехники (лекция)",
              "class": "1158",
              "teacher": "Соколов Валентин Николаевич"},

      (3,0): {"name": "Иностранный язык",
              "class": "кафедра иностранных языков",
              "teacher": "-"},

      (4,0): {"name": "Экономика организации (лекция)",
              "class": "5405",
              "teacher": "Алексеева Ольга Геннадьевна"}},

    # Суббота
    { (1,0): {"name": "Математическая логика и теория алгоритмов (лекция)",
              "class": "3324",
              "teacher": "Поздняков Сергей Николаевич"},

      (2,0): {"name": "Теория вероятности и мат. статистика (лекция)",
              "class": "3324",
              "teacher": "Малов Сергей Васильевич"},

      (3,0): {"name": "Математическая логика и теория алгоритмов (практика)",
              "class": "3308",
              "teacher": "Поздняков Сергей Николаевич"},

      (4,0): {"name": "Теория вероятности и мат. статистика (практика)",
              "class": "3302",
              "teacher": "Костырев Игорь Иванович"}},

    # Воскресенье
    {}

  ]
}
