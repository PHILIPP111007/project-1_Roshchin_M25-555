/*
Вариант 4

Рощин Филипп Андреевич

Описание предметной области
Описание хранящихся на складе товаров. Включает в себя: описание помещений, описание стеллажей,
описание клиентов, описание товаров, хранящихся на стеллажах. Описание помещения состоит из: названия,
полезного объёма, температурных и влажностных условий. Описание стеллажа состоит из: номера, указания
помещения, в котором стеллаж находится, количества мест для хранения в стеллаже, высоты, ширины и длины одного места,
максимальной суммарной нагрузки. Описание клиента состоит из: названия юридического лица и банковских реквизитов в виде большого текста.
Описание товара, хранящегося на стеллажах, состоит из: высоты, ширины, длины, веса, даты поступления, номера договора,
указания, от какого клиента поступил, даты окончания договора, температурных и влажностных условий хранения, указания стеллажа,
и позиции размещения на нём, представляемой в виде целого номера.

На одном стеллаже могут храниться товары разных клиентов.
*/

-- Таблица клиентов
CREATE TABLE clients (
    id INTEGER PRIMARY KEY,
    name_of_a_legal_entity TEXT NOT NULL,
    bank_details TEXT NOT NULL
);

-- Таблица помещений
CREATE TABLE rooms (
    id INTEGER PRIMARY KEY,
    room_name TEXT NOT NULL,
    useful_volume REAL NOT NULL,
    min_temperature REAL,
    max_temperature REAL,
    min_humidity REAL,
    max_humidity REAL
);

-- Таблица стеллажей
CREATE TABLE racks (-- Таблица клиентов
CREATE TABLE clients (
    id INTEGER PRIMARY KEY,
    name_of_a_legal_entity TEXT NOT NULL,
    bank_details TEXT NOT NULL
);

-- Таблица помещений
CREATE TABLE rooms (
    id INTEGER PRIMARY KEY,
    room_name TEXT NOT NULL,
    useful_volume REAL NOT NULL,
    min_temperature REAL,
    max_temperature REAL,
    min_humidity REAL,
    max_humidity REAL
);

-- Таблица стеллажей
CREATE TABLE racks (
    id INTEGER PRIMARY KEY,
    room_id INTEGER NOT NULL,
    rack_number TEXT NOT NULL,
    storage_spaces_count INTEGER NOT NULL,
    space_height REAL NOT NULL,
    space_width REAL NOT NULL,
    space_length REAL NOT NULL,
    max_total_load REAL NOT NULL,
    FOREIGN KEY (room_id) REFERENCES rooms(id),
    UNIQUE (rack_number, room_id)
);

-- Таблица товаров
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    height REAL NOT NULL,
    width REAL NOT NULL,
    length REAL NOT NULL,
    weight REAL NOT NULL,
    admission_date TEXT NOT NULL,
    contract_number TEXT NOT NULL,
    client_id INTEGER NOT NULL,
    contract_expiration_date TEXT NOT NULL,
    min_temperature REAL,
    max_temperature REAL,
    min_humidity REAL,
    max_humidity REAL,
    rack_id INTEGER NOT NULL,
    position_number INTEGER NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (rack_id) REFERENCES racks(id),
    UNIQUE (rack_id, position_number)
);

    id INTEGER PRIMARY KEY,
    room_id INTEGER NOT NULL,
    rack_number TEXT NOT NULL,
    storage_spaces_count INTEGER NOT NULL,
    space_height REAL NOT NULL,
    space_width REAL NOT NULL,
    space_length REAL NOT NULL,
    max_total_load REAL NOT NULL,
    FOREIGN KEY (room_id) REFERENCES rooms(id),
    UNIQUE (rack_number, room_id)
);

-- Таблица товаров
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    height REAL NOT NULL,
    width REAL NOT NULL,
    length REAL NOT NULL,
    weight REAL NOT NULL,
    admission_date TEXT NOT NULL,
    contract_number TEXT NOT NULL,
    client_id INTEGER NOT NULL,
    contract_expiration_date TEXT NOT NULL,
    min_temperature REAL,
    max_temperature REAL,
    min_humidity REAL,
    max_humidity REAL,
    rack_id INTEGER NOT NULL,
    position_number INTEGER NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (rack_id) REFERENCES racks(id),
    UNIQUE (rack_id, position_number)
);
