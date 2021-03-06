import csv
import random
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

FIRST_NAMES = [
    ('Август', 'm'),
    ('Авдей', 'm'),
    ('Аверкий', 'm'),
    ('Аверьян', 'm'),
    ('Авксентий', 'm'),
    ('Автоном', 'm'),
    ('Агап', 'm'),
    ('Агафон', 'm'),
    ('Аггей', 'm'),
    ('Адам', 'm'),
    ('Адриан', 'm'),
    ('Азарий', 'm'),
    ('Аким', 'm'),
    ('Александр', 'm'),
    ('Алексей', 'm'),
    ('Амвросий', 'm'),
    ('Амос', 'm'),
    ('Ананий', 'm'),
    ('Анатолий', 'm'),
    ('Андрей', 'm'),
    ('Андрон', 'm'),
    ('Андроник', 'm'),
    ('Аникей', 'm'),
    ('Аникита', 'm'),
    ('Анисим', 'm'),
    ('Антип', 'm'),
    ('Антонин', 'm'),
    ('Аполлинарий', 'm'),
    ('Аполлон', 'm'),
    ('Арефий', 'm'),
    ('Аристарх', 'm'),
    ('Аркадий', 'm'),
    ('Арсений', 'm'),
    ('Артемий', 'm'),
    ('Артем', 'm'),
    ('Архип', 'm'),
    ('Аскольд', 'm'),
    ('Афанасий', 'm'),
    ('Афиноген', 'm'),
    ('Бажен', 'm'),
    ('Богдан', 'm'),
    ('Болеслав', 'm'),
    ('Борис', 'm'),
    ('Борислав', 'm'),
    ('Боян', 'm'),
    ('Бронислав', 'm'),
    ('Будимир', 'm'),
    ('Вадим', 'm'),
    ('Валентин', 'm'),
    ('Валерий', 'm'),
    ('Валерьян', 'm'),
    ('Варлаам', 'm'),
    ('Варфоломей', 'm'),
    ('Василий', 'm'),
    ('Вацлав', 'm'),
    ('Велимир', 'm'),
    ('Венедикт', 'm'),
    ('Вениамин', 'm'),
    ('Викентий', 'm'),
    ('Виктор', 'm'),
    ('Викторин', 'm'),
    ('Виссарион', 'm'),
    ('Виталий', 'm'),
    ('Владилен', 'm'),
    ('Владлен', 'm'),
    ('Владимир', 'm'),
    ('Владислав', 'm'),
    ('Влас', 'm'),
    ('Всеволод', 'm'),
    ('Всемил', 'm'),
    ('Всеслав', 'm'),
    ('Вышеслав', 'm'),
    ('Вячеслав', 'm'),
    ('Гаврила', 'm'),
    ('Галактион', 'm'),
    ('Гедеон', 'm'),
    ('Геннадий', 'm'),
    ('Георгий', 'm'),
    ('Герасим', 'm'),
    ('Герман', 'm'),
    ('Глеб', 'm'),
    ('Гордей', 'm'),
    ('Гостомысл', 'm'),
    ('Гремислав', 'm'),
    ('Григорий', 'm'),
    ('Гурий', 'm'),
    ('Давыд', 'm'),
    ('Данила', 'm'),
    ('Дементий', 'm'),
    ('Демид', 'm'),
    ('Демьян', 'm'),
    ('Денис', 'm'),
    ('Дмитрий', 'm'),
    ('Добромысл', 'm'),
    ('Доброслав', 'm'),
    ('Дорофей', 'm'),
    ('Евгений', 'm'),
    ('Евграф', 'm'),
    ('Евдоким', 'm'),
    ('Евлампий', 'm'),
    ('Евсей', 'm'),
    ('Евстафий', 'm'),
    ('Евстигней', 'm'),
    ('Егор', 'm'),
    ('Елизар', 'm'),
    ('Елисей', 'm'),
    ('Емельян', 'm'),
    ('Епифан', 'm'),
    ('Еремей', 'm'),
    ('Ермил', 'm'),
    ('Ермолай', 'm'),
    ('Ерофей', 'm'),
    ('Ефим', 'm'),
    ('Ефрем', 'm'),
    ('Захар', 'm'),
    ('Зиновий', 'm'),
    ('Зосима', 'm'),
    ('Иван', 'm'),
    ('Игнатий', 'm'),
    ('Игорь', 'm'),
    ('Измаил', 'm'),
    ('Изот', 'm'),
    ('Изяслав', 'm'),
    ('Иларион', 'm'),
    ('Илья', 'm'),
    ('Иннокентий', 'm'),
    ('Иосиф', 'm'),
    ('Ипат', 'm'),
    ('Ипатий', 'm'),
    ('Ипполит', 'm'),
    ('Ираклий', 'm'),
    ('Исай', 'm'),
    ('Исидор', 'm'),
    ('Казимир', 'm'),
    ('Каллистрат', 'm'),
    ('Капитон', 'm'),
    ('Карл', 'm'),
    ('Карп', 'm'),
    ('Касьян', 'm'),
    ('Ким', 'm'),
    ('Кир', 'm'),
    ('Кирилл', 'm'),
    ('Клавдий', 'm'),
    ('Климент', 'm'),
    ('Кондрат', 'm'),
    ('Кондратий', 'm'),
    ('Конон', 'm'),
    ('Константин', 'm'),
    ('Корнил', 'm'),
    ('Кузьма', 'm'),
    ('Куприян', 'm'),
    ('Лавр', 'm'),
    ('Лаврентий', 'm'),
    ('Ладимир', 'm'),
    ('Ладислав', 'm'),
    ('Лазарь', 'm'),
    ('Лев', 'm'),
    ('Леон', 'm'),
    ('Леонид', 'm'),
    ('Леонтий', 'm'),
    ('Лонгин', 'm'),
    ('Лука', 'm'),
    ('Лукьян', 'm'),
    ('Лучезар', 'm'),
    ('Любим', 'm'),
    ('Любомир', 'm'),
    ('Любосмысл', 'm'),
    ('Макар', 'm'),
    ('Максим', 'm'),
    ('Максимильян', 'm'),
    ('Мариан', 'm'),
    ('Марк', 'm'),
    ('Мартын', 'm'),
    ('Мартьян', 'm'),
    ('Матвей', 'm'),
    ('Мефодий', 'm'),
    ('Мечислав', 'm'),
    ('Милан', 'm'),
    ('Милен', 'm'),
    ('Милий', 'm'),
    ('Милован', 'm'),
    ('Мина', 'm'),
    ('Мир', 'm'),
    ('Мирон', 'm'),
    ('Мирослав', 'm'),
    ('Митофан', 'm'),
    ('Михаил', 'm'),
    ('Михей', 'm'),
    ('Модест', 'm'),
    ('Моисей', 'm'),
    ('Мокей', 'm'),
    ('Мстислав', 'm'),
    ('Назар', 'm'),
    ('Наркис', 'm'),
    ('Натан', 'm'),
    ('Наум', 'm'),
    ('Нестор', 'm'),
    ('Никандр', 'm'),
    ('Никанор', 'm'),
    ('Никита', 'm'),
    ('Никифор', 'm'),
    ('Никодим', 'm'),
    ('Николай', 'm'),
    ('Никон', 'm'),
    ('Нифонт', 'm'),
    ('Олег', 'm'),
    ('Олимпий', 'm'),
    ('Онуфрий', 'm'),
    ('Орест', 'm'),
    ('Осип', 'm'),
    ('Остап', 'm'),
    ('Остромир', 'm'),
    ('Павел', 'm'),
    ('Панкратий', 'm'),
    ('Панкрат', 'm'),
    ('Пантелеймон', 'm'),
    ('Панфил', 'm'),
    ('Парамон', 'm'),
    ('Парфен', 'm'),
    ('Пахом', 'm'),
    ('Петр', 'm'),
    ('Пимен', 'm'),
    ('Платон', 'm'),
    ('Поликарп', 'm'),
    ('Порфирий', 'm'),
    ('Потап', 'm'),
    ('Пров', 'm'),
    ('Прокл', 'm'),
    ('Прокофий', 'm'),
    ('Прохор', 'm'),
    ('Радим', 'm'),
    ('Радислав', 'm'),
    ('Радован', 'm'),
    ('Ратибор', 'm'),
    ('Ратмир', 'm'),
    ('Родион', 'm'),
    ('Роман', 'm'),
    ('Ростислав', 'm'),
    ('Рубен', 'm'),
    ('Руслан', 'm'),
    ('Рюрик', 'm'),
    ('Савва', 'm'),
    ('Савватий', 'm'),
    ('Савелий', 'm'),
    ('Самсон', 'm'),
    ('Самуил', 'm'),
    ('Светозар', 'm'),
    ('Святополк', 'm'),
    ('Святослав', 'm'),
    ('Севастьян', 'm'),
    ('Селиван', 'm'),
    ('Селиверст', 'm'),
    ('Семен', 'm'),
    ('Серафим', 'm'),
    ('Сергей', 'm'),
    ('Сигизмунд', 'm'),
    ('Сидор', 'm'),
    ('Сила', 'm'),
    ('Силантий', 'm'),
    ('Сильвестр', 'm'),
    ('Симон', 'm'),
    ('Сократ', 'm'),
    ('Соломон', 'm'),
    ('Софон', 'm'),
    ('Софрон', 'm'),
    ('Спартак', 'm'),
    ('Спиридон', 'm'),
    ('Станимир', 'm'),
    ('Станислав', 'm'),
    ('Степан', 'm'),
    ('Стоян', 'm'),
    ('Тарас', 'm'),
    ('Твердислав', 'm'),
    ('Творимир', 'm'),
    ('Терентий', 'm'),
    ('Тимофей', 'm'),
    ('Тимур', 'm'),
    ('Тит', 'm'),
    ('Тихон', 'm'),
    ('Трифон', 'm'),
    ('Трофим', 'm'),
    ('Ульян', 'm'),
    ('Устин', 'm'),
    ('Фадей', 'm'),
    ('Федор', 'm'),
    ('Федосий', 'm'),
    ('Федот', 'm'),
    ('Феликс', 'm'),
    ('Феоктист', 'm'),
    ('Феофан', 'm'),
    ('Ферапонт', 'm'),
    ('Филарет', 'm'),
    ('Филимон', 'm'),
    ('Филипп', 'm'),
    ('Фирс', 'm'),
    ('Флорентин', 'm'),
    ('Фока', 'm'),
    ('Фома', 'm'),
    ('Фортунат', 'm'),
    ('Фотий', 'm'),
    ('Фрол', 'm'),
    ('Харитон', 'm'),
    ('Харлампий', 'm'),
    ('Христофор', 'm'),
    ('Чеслав', 'm'),
    ('Эдуард', 'm'),
    ('Эммануил', 'm'),
    ('Эмиль', 'm'),
    ('Эраст', 'm'),
    ('Эрнест', 'm'),
    ('Эрнст', 'm'),
    ('Ювеналий', 'm'),
    ('Юлиан', 'm'),
    ('Юлий', 'm'),
    ('Юрий', 'm'),
    ('Яков', 'm'),
    ('Ян', 'm'),
    ('Якуб', 'm'),
    ('Януарий', 'm'),
    ('Ярополк', 'm'),
    ('Ярослав', 'm'),
    ('Августа', 'w'),
    ('Агата', 'w'),
    ('Агафья', 'w'),
    ('Аглая', 'w'),
    ('Агнесса', 'w'),
    ('Агния', 'w'),
    ('Аграфена', 'w'),
    ('Агриппина', 'w'),
    ('Ада', 'w'),
    ('Аделаида', 'w'),
    ('Аза', 'w'),
    ('Алевтина', 'w'),
    ('Александра', 'w'),
    ('Алина', 'w'),
    ('Алиса', 'w'),
    ('Алла', 'w'),
    ('Альбина', 'w'),
    ('Анастасия', 'w'),
    ('Ангелина', 'w'),
    ('Анисья', 'w'),
    ('Анна', 'w'),
    ('Антонида', 'w'),
    ('Антонина', 'w'),
    ('Анфиса', 'w'),
    ('Аполлинария', 'w'),
    ('Ариадна', 'w'),
    ('Беатриса', 'w'),
    ('Берта', 'w'),
    ('Борислава', 'w'),
    ('Бронислава', 'w'),
    ('Валентина', 'w'),
    ('Валерия', 'w'),
    ('Ванда', 'w'),
    ('Варвара', 'w'),
    ('Василиса', 'w'),
    ('Васса', 'w'),
    ('Вера', 'w'),
    ('Вероника', 'w'),
    ('Викторина', 'w'),
    ('Виктория', 'w'),
    ('Виргиния', 'w'),
    ('Влада', 'w'),
    ('Владилена', 'w'),
    ('Владлена', 'w'),
    ('Владислава', 'w'),
    ('Власта', 'w'),
    ('Всеслава', 'w'),
    ('Галина', 'w'),
    ('Галя', 'w'),
    ('Ганна', 'w'),
    ('Генриетта', 'w'),
    ('Глафира', 'w'),
    ('Горислава', 'w'),
    ('Дарья', 'w'),
    ('Диана', 'w'),
    ('Дина', 'w'),
    ('Доминика', 'w'),
    ('Домна', 'w'),
    ('Ева', 'w'),
    ('Евгеиня', 'w'),
    ('Евдокия', 'w'),
    ('Евлампия', 'w'),
    ('Екатерина', 'w'),
    ('Елена', 'w'),
    ('Елизавета', 'w'),
    ('Ефросинья', 'w'),
    ('Жанна', 'w'),
    ('Зинаида', 'w'),
    ('Злата', 'w'),
    ('Зоя', 'w'),
    ('Изабелла', 'w'),
    ('Изольда', 'w'),
    ('Инга', 'w'),
    ('Инесса', 'w'),
    ('Инна', 'w'),
    ('Ираида', 'w'),
    ('Ирина', 'w'),
    ('Ия', 'w'),
    ('Казимира', 'w'),
    ('Калерия', 'w'),
    ('Капитолина', 'w'),
    ('Каролина', 'w'),
    ('Кира', 'w'),
    ('Клавдия', 'w'),
    ('Клара', 'w'),
    ('Кларисса', 'w'),
    ('Клементина', 'w'),
    ('Клеопатра', 'w'),
    ('Конкордия', 'w'),
    ('Ксения', 'w'),
    ('Лада', 'w'),
    ('Лариса', 'w'),
    ('Леокадия', 'w'),
    ('Лиана', 'w'),
    ('Лидия', 'w'),
    ('Лилиана', 'w'),
    ('Клеопатра', 'w'),
    ('Конкордия', 'w'),
    ('Ксения', 'w'),
    ('Лада', 'w'),
    ('Лариса', 'w'),
    ('Леокадия', 'w'),
    ('Лиана', 'w'),
    ('Лидия', 'w'),
    ('Лилиана', 'w'),
    ('Лилия', 'w'),
    ('Лия', 'w'),
    ('Луиза', 'w'),
    ('Лукерья', 'w'),
    ('Любава', 'w'),
    ('Любовь', 'w'),
    ('Любомила', 'w'),
    ('Любомира', 'w'),
    ('Людмила', 'w'),
    ('Майя', 'w'),
    ('Мальвина', 'w'),
    ('Маргарита', 'w'),
    ('Марианна', 'w'),
    ('Мариетта', 'w'),
    ('Марина', 'w'),
    ('Мария', 'w'),
    ('Марта', 'w'),
    ('Марфа', 'w'),
    ('Меланья', 'w'),
    ('Мелитриса', 'w'),
    ('Милана', 'w'),
    ('Милена', 'w'),
    ('Милица', 'w'),
    ('Мира', 'w'),
    ('Мирослава', 'w'),
    ('Млада', 'w'),
    ('Мстислава', 'w'),
    ('Муза', 'w'),
    ('Надежда', 'w'),
    ('Наталья', 'w'),
    ('Наталия', 'w'),
    ('Неонила', 'w'),
    ('Ника', 'w'),
    ('Нина', 'w'),
    ('Нинель', 'w'),
    ('Нона', 'w'),
    ('Оксана', 'w'),
    ('Октябрина', 'w'),
    ('Олимпиада', 'w'),
    ('Ольга', 'w'),
    ('Пелагея', 'w'),
    ('Поликсена', 'w'),
    ('Полина', 'w'),
    ('Прасковья', 'w'),
    ('Пульхерия', 'w'),
    ('Рада', 'w'),
    ('Раиса', 'w'),
    ('Регина', 'w'),
    ('Рената', 'w'),
    ('Римма', 'w'),
    ('Рогнеда', 'w'),
    ('Роза', 'w'),
    ('Розалия', 'w'),
    ('Розина', 'w'),
    ('Ростислава', 'w'),
    ('Руфина', 'w'),
    ('Светлана', 'w'),
    ('Серафима', 'w'),
    ('Сильва', 'w'),
    ('Сильвия', 'w'),
    ('Саломея', 'w'),
    ('Софья', 'w'),
    ('Станислава', 'w'),
    ('Стела', 'w'),
    ('Степанида', 'w'),
    ('Сусанна', 'w'),
    ('Таисия', 'w'),
    ('Тамара', 'w'),
    ('Татьяна', 'w'),
    ('Ульяна', 'w'),
    ('Фаина', 'w'),
    ('Федосья', 'w'),
    ('Фелицата', 'w'),
    ('Флора', 'w'),
    ('Флорентина', 'w'),
    ('Фатина', 'w'),
    ('Харитина', 'w'),
    ('Христина', 'w'),
    ('Эвелина', 'w'),
    ('Элеонора', 'w'),
    ('Эльвира', 'w'),
    ('Эмилия', 'w'),
    ('Эмма', 'w'),
    ('Юлия', 'w'),
    ('Ядвига', 'w'),
    ('Ярослава', 'w'),
]

LAST_NAMES = [
    'Смирнов',
    'Иванов',
    'Кузнецов',
    'Соколов',
    'Попов',
    'Лебедев',
    'Козлов',
    'Новиков',
    'Морозов',
    'Петров',
    'Волков',
    'Соловьёв',
    'Васильев',
    'Зайцев',
    'Павлов',
    'Семёнов',
    'Голубев',
    'Виноградов',
    'Богданов',
    'Воробьёв',
    'Фёдоров',
    'Михайлов',
    'Беляев',
    'Тарасов',
    'Белов',
    'Комаров',
    'Орлов',
    'Киселёв',
    'Макаров',
    'Андреев',
    'Ковалёв',
    'Ильин',
    'Гусев',
    'Титов',
    'Кузьмин',
    'Кудрявцев',
    'Баранов',
    'Куликов',
    'Алексеев',
    'Степанов',
    'Яковлев',
    'Сорокин',
    'Сергеев',
    'Романов',
    'Захаров',
    'Борисов',
    'Королёв',
    'Герасимов',
    'Пономарёв',
    'Григорьев',
    'Лазарев',
    'Медведев',
    'Ершов',
    'Никитин',
    'Соболев',
    'Рябов',
    'Поляков',
    'Цветков',
    'Данилов',
    'Жуков',
    'Фролов',
    'Журавлёв',
    'Николаев',
    'Крылов',
    'Максимов',
    'Сидоров',
    'Осипов',
    'Белоусов',
    'Федотов',
    'Дорофеев',
    'Егоров',
    'Матвеев',
    'Бобров',
    'Дмитриев',
    'Калинин',
    'Анисимов',
    'Петухов',
    'Антонов',
    'Тимофеев',
    'Никифоров',
    'Веселов',
    'Филиппов',
    'Марков',
    'Большаков',
    'Суханов',
    'Миронов',
    'Ширяев',
    'Александров',
    'Коновалов',
    'Шестаков',
    'Казаков',
    'Ефимов',
    'Денисов',
    'Громов',
    'Фомин',
    'Давыдов',
    'Мельников',
    'Щербаков',
    'Блинов',
    'Колесников',
    'Карпов',
    'Афанасьев',
    'Власов',
    'Маслов',
    'Исаков',
    'Тихонов',
    'Аксёнов',
    'Гаврилов',
    'Родионов',
    'Котов',
    'Горбунов',
    'Кудряшов',
    'Быков',
    'Зуев',
    'Третьяков',
    'Савельев',
    'Панов',
    'Рыбаков',
    'Суворов',
    'Абрамов',
    'Воронов',
    'Мухин',
    'Архипов',
    'Трофимов',
    'Мартынов',
    'Емельянов',
    'Горшков',
    'Чернов',
    'Овчинников',
    'Селезнёв',
    'Панфилов',
    'Копылов',
    'Михеев',
    'Галкин',
    'Назаров',
    'Лобанов',
    'Лукин',
    'Беляков',
    'Потапов',
    'Некрасов',
    'Хохлов',
    'Жданов',
    'Наумов',
    'Шилов',
    'Воронцов',
    'Ермаков',
    'Дроздов',
    'Игнатьев',
    'Савин',
    'Логинов',
    'Сафонов',
    'Капустин',
    'Кириллов',
    'Моисеев',
    'Елисеев',
    'Кошелев',
    'Костин',
    'Горбачёв',
    'Орехов',
    'Ефремов',
    'Исаев',
    'Евдокимов',
    'Калашников',
    'Кабанов',
    'Носков',
    'Юдин',
    'Кулагин',
    'Лапин',
    'Прохоров',
    'Нестеров',
    'Харитонов',
    'Агафонов',
    'Муравьёв',
    'Ларионов',
    'Федосеев',
    'Зимин',
    'Пахомов',
    'Шубин',
    'Игнатов',
    'Филатов',
    'Крюков',
    'Рогов',
    'Кулаков',
    'Терентьев',
    'Молчанов',
    'Владимиров',
    'Артемьев',
    'Гурьев',
    'Зиновьев',
    'Гришин',
    'Кононов',
    'Дементьев',
    'Ситников',
    'Симонов',
    'Мишин',
    'Фадеев',
    'Комиссаров',
    'Мамонтов',
    'Носов',
    'Гуляев',
    'Шаров',
    'Устинов',
    'Вишняков',
    'Евсеев',
    'Лаврентьев',
    'Брагин',
    'Константинов',
    'Корнилов',
    'Авдеев',
    'Зыков',
    'Бирюков',
    'Шарапов',
    'Никонов',
    'Щукин',
    'Дьячков',
    'Одинцов',
    'Сазонов',
    'Якушев',
    'Красильников',
    'Гордеев',
    'Самойлов',
    'Князев',
    'Беспалов',
    'Уваров',
    'Шашков',
    'Бобылёв',
    'Доронин',
    'Белозёров',
    'Рожков',
    'Самсонов',
    'Мясников',
    'Лихачёв',
    'Буров',
    'Сысоев',
    'Фомичёв',
    'Русаков',
    'Стрелков',
    'Гущин',
    'Тетерин',
    'Колобов',
    'Субботин',
    'Фокин',
    'Блохин',
    'Селиверстов',
    'Пестов',
    'Кондратьев',
    'Силин',
    'Меркушев',
    'Лыткин',
    'Туров',
]


@dataclass
class Customer:
    id: int
    first_name: str
    last_name: Optional[str]
    birthdate: Optional[date]
    email: Optional[str]
    phone_number: str
    registered_at: datetime


@dataclass
class Employee:
    id: int
    first_name: str
    last_name: str
    employed_since: date
    birthdate: date
    rating: float
    salary: float
    email: str
    phone_number: str


CUSTOMERS: list[Customer] = []
EMPLOYEES: list[Employee] = []


def load_customers() -> None:
    global CUSTOMERS
    with open('../data/customers_old.csv', newline='') as f:
        reader = csv.reader(f, delimiter=',')
        CUSTOMERS = [
            Customer(
                id=int(row[0]),
                first_name=row[1],
                last_name=row[2] if row[2] else None,
                birthdate=datetime.strptime(row[3], "%Y-%m-%d") if row[3] else None,
                email=row[4] if row[4] else None,
                phone_number=row[5],
                registered_at=datetime.strptime(row[6], "%Y-%m-%d %H:%M:%S"),
            ) for row in reader]


def load_employees() -> None:
    global EMPLOYEES
    with open('../data/employees_old.csv', newline='') as f:
        reader = csv.reader(f, delimiter=',')
        EMPLOYEES = [
            Employee(
                id=int(row[0]),
                first_name=row[1],
                last_name=row[2],
                employed_since=datetime.strptime(row[3], "%Y-%m-%d"),
                birthdate=datetime.strptime(row[4], "%Y-%m-%d"),
                rating=float(row[5]),
                salary=float(row[6]),
                email=row[7],
                phone_number=row[8],
            ) for row in reader]


def go():
    with open('../data/customers.csv', 'w') as f:
        for c in CUSTOMERS:
            name, sex = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES) + ('а' if sex == 'w' else '')
            birthdate = str(c.birthdate).split()[0] if c.birthdate is not None else ''
            email = c.email if c.email is not None else ''
            f.write(f'{c.id},{name},{last_name},{birthdate},{email},{c.phone_number},{c.registered_at}\n')

    with open('../data/employees.csv', 'w') as f:
        for e in EMPLOYEES:
            name, sex = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES) + ('а' if sex == 'w' else '')
            f.write(
                f'{e.id},{name},{last_name},{str(e.employed_since).split()[0]},{str(e.birthdate).split()[0]},{e.rating},{e.salary},{e.email},{e.phone_number}\n')


if __name__ == '__main__':
    load_customers()
    load_employees()
    go()
