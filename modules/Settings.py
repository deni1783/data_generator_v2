# -*- coding: utf-8 -*-

# В этом файле изменять настройки не нужно!!!
# Для изменения настроек необходимые параметры записываем в файле User_Settings.py
# Все параметры из User_Settings.py временно перезаписывают дефолтные параметры (из Settings.py)


# Внимание !
# COUNT_STRINGS должно делиться на COUNT_SUBPROCESS без остатка !!!
# Иначе будет потеря строк = количеству остатка от деления

# Задаем количество строк (default is 1,000,000)
# Параметр - целочисленное число
COUNT_STRINGS = 1000000

# Количество одновременно запущенных процессов
# (эквивалентно количеству файлов в которые идет одновременная запись)
# Это значение можно изменять, но нужно смотреть на изменение производительности,
# т.к. при 4 одновременно запущенных процессах загрузка центрального процессора доходит до 99%
# все зависит от мощности процессора и количестве ядер

# Параметр - целочисленное число
MAX_COUNT_SUBPROCESS = 4

# Количество результирующих файлов
# Параметр - целочисленное число
COUNT_OUTPUT_FILE = 4


# Нужно ли объеденить все файлы в один
# Параметр - bool  (True/False)
MERGE_ALL_FILE_TO_SINGLE = True

# Удалить промежуточные файлы (True/False)
# Параметр - bool  (True/False)
DEL_ALL_TMP_FILE = True

# Расширение для сгенерированных фалов
# Параметр - строковое значение
OUTPUT_FILE_EXTENSIONS = '.csv'

#  Разделитель колонок
# Параметр - строковое значение
DELIMITER_COLUMN = '|'

#  Разделитель строк
# Параметр - строковое значение
DELIMITER_ROW = '\n'

# Обертки для значений (квотирование значений)
# Например обернуть все строковые типы в двойные кавычки можно установив WRAP_STRINGS = '"'
# Параметр - строковое значение, либо False
WRAP_STRINGS = False
WRAP_DATETIME = False


#  Финальный вид такой:
# WRAP_BINARY_STRINGS + MASC_FOR_BINARY + WRAP_BINARY_VALUE + VALUE + WRAP_BINARY_VALUE + WRAP_BINARY_STRINGS
# Например при WRAP_BINARY_STRINGS = '"' WRAP_BINARY_VALUE = "'" MASC_FOR_BINARY = '0x'
# "0x'value'"
# Параметр - строковое значение, либо False
WRAP_BINARY_STRINGS = False
WRAP_BINARY_VALUE = "'"
MASC_FOR_BINARY = '0x'

# Значение для NULL
# Можно указать пустоту '' или какой либо другой набор символов
# Все спец. символы необходимо экранировать наприпер для \ указываем \\
# Параметр - строковое значение
VALUE_FOR_NULL = 'NULL'

# Процент для NULL значений от 1 до 100
# Параметр - целоцисленное значение
PERCENT_FOR_NULL_VALUES = 10


# Определяет разделитель между double и real
# float(x) = double, при  x > FLOAT_PRECISION
# float(x) = real,   при  FLOAT_PRECISION <= x
# float = real, (без указания длины)
# Параметр - целоцисленное значение
FLOAT_PRECISION = 24



# Значения по умолчанию для количества фракционных секунд
# Параметр - целоцисленное значение

# Для типа timestamp
DEFAULT_VALUE_TIMESTAMP_FRACTIONAL_SECONDS = 6

# Для типа time
DEFAULT_VALUE_TIME_FRACTIONAL_SECONDS = 3



# Максимальная длина для ЛОБов
MAX_LENGTH_CLOB = 100
MAX_LENGTH_BLOB = 100


# Дефолтная длина для строк и бинарных строк
DEFAULT_VALUE_CHAR = 1
DEFAULT_VALUE_BYTE = 1




# Диапазон количества знаков ДО разделителя, для типа DOUBLE
DOUBLE_MIN_PRECISION = 1
DOUBLE_MAX_PRECISION = 20

# Диапазон количества знаков ПОСЛЕ разделителя, для типа DOUBLE
DOUBLE_MIN_SCALE = 1
DOUBLE_MAX_SCALE = 15


# Диапазон количества знаков ДО разделителя, для типа REAL
FLOAT_MIN_PRECISION = 1
FLOAT_MAX_PRECISION = 10

# Диапазон количества знаков ПОСЛЕ разделителя, для типа REAL
FLOAT_MIN_SCALE = 1
FLOAT_MAX_SCALE = 6





# Integer data types
TINYINT_MIN = -128
TINYINT_MAX = 127

SMALLINT_MIN = -32768
SMALLINT_MAX = 32767

MEDIUMINT_MIN = -8388608
MEDIUMINT_MAX = 8388607

INTEGER_MIN = -2147483648
INTEGER_MAX = 2147483647

BIGINT_MIN = -9223372036854775808
BIGINT_MAX = 9223372036854775807



UN_TINYINT_MIN = 0
UN_TINYINT_MAX = 255

UN_SMALLINT_MIN = 0
UN_SMALLINT_MAX = 65535

UN_MEDIUMINT_MIN = 0
UN_MEDIUMINT_MAX = 16777215

UN_INTEGER_MIN = 0
UN_INTEGER_MAX = 4294967295

UN_BIGINT_MIN = 0
UN_BIGINT_MAX = 18446744073709551615


# DateTime data types


# Минимальное и максимальное значение для типов date и timestamp
# Параметр - строковое значение

# MIN = '0001'
# МАX = '9999'

YEAR_MIN = '1600'
YEAR_MAX = '9999'


# Минимальное и максимальное значение для TIME ZONE
# Ограничений нет.
# Так же можно задавать вместе с секундами. Например MIN_TIME_ZONE = '-12:00:00'
# Параметр - строковое значение
MIN_TIME_ZONE = '-12:00'
MAX_TIME_ZONE = '+12:00'

# Набор символов для строковых типов
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z', ' ']


# Набор хексовых значений (получен из ALPHABET)
ALPHABET_HEX = ['41', '42', '43', '44', '45', '46', '47', '48', '49', '4a', '4b', '4c', '4d', '4e', '4f', '50', '51',
                '52', '53', '54', '55', '56', '57', '58', '59', '5a', '61', '62', '63', '64', '65', '66', '67', '68',
                '69', '6a', '6b', '6c', '6d', '6e', '6f', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79',
                '7a', '20']

# Для генерации хекс значений из ALPHABET
# ALPHABET_HEX = []
# for i in ALPHABET:
#     ALPHABET_HEX.append(hex(ord(i))[2:])


# Синонимы для типов
# Поддерживаемые базовые типы:
#   char,
#   binary
#   date, time, timestamp,
#   decimal, double, real,
#   tinyint, smallint, integer, bigint
#   un_tinyint, un_smallint, un_integer, un_bigint
SYNONYMS_DICT = {
    'int(1)': 'tinyint',
    'int(2)': 'smallint',
    'int(4)': 'integer',
    'int(8)': 'bigint',

    'int': 'integer',

    'unsigned tinyint': 'un_tinyint',
    'unsigned smallint': 'un_smallint',
    'unsigned integer': 'un_integer',
    'unsigned bigint': 'un_bigint',

    'unsigned int': 'un_integer',

    'varchar': 'char',
    'character': 'char',
    'character varying': 'char',

    'numeric': 'decimal',
    'number': 'decimal',

    'text': 'char({})'.format(MAX_LENGTH_CLOB),
    'clob': 'char({})'.format(MAX_LENGTH_CLOB),

    'datetime2': 'timestamp(7)',
    'datetime': 'timestamp(3)',
    'smalldatetime': 'timestamp(0)',

    'timestamp with time zone': 'timestamp_tz',
    'timestamp without time zone': 'timestamp',
    'time without time zone': 'time',
    'time with time zone': 'time_tz',

    'bigtime': 'time(6)',

    'varbinary': 'binary',
    'byte': 'binary',
    'varbyte': 'binary',
    'bytea': 'binary',

    'blob': 'binary({})'.format(MAX_LENGTH_BLOB),

    'double precision': 'double',
    'un_int': 'un_integer',

    'bit': 'boolean',
    'bool': 'boolean',
    'uniqueidentifier': 'binary(16)',
    'float': 'real'
}
