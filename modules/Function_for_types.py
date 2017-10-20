import datetime
import random

# Импоритруем константы из настроек
from modules.Settings import *
from User_Settings import *

# Все get_* функции возвращают строку

DATE_MIN_VALUE = int(YEAR_MIN)
DATE_MAX_VALUE = int(YEAR_MAX)

# Подготавливаем данные для значений временой зоны
MIN_TIME_ZONE_VALUES_OBJ = {}

MIN_TIME_ZONE_VALUES_OBJ['SIGN'] = MIN_TIME_ZONE[0]
# Если указана временая зона с секундами
if len(MIN_TIME_ZONE[1:].split(':')) == 3:
    (MIN_TIME_ZONE_VALUES_OBJ['HOUR'],
     MIN_TIME_ZONE_VALUES_OBJ['MINUTE'],
     MIN_TIME_ZONE_VALUES_OBJ['SECOND']) = MIN_TIME_ZONE[1:].split(':')
    MIN_TIME_ZONE_VALUES_OBJ['full_second'] = (int(MIN_TIME_ZONE_VALUES_OBJ['HOUR']) * 3600 +
                                               int(MIN_TIME_ZONE_VALUES_OBJ['MINUTE']) * 60 +
                                               int(MIN_TIME_ZONE_VALUES_OBJ['SECOND']))
else:
    MIN_TIME_ZONE_VALUES_OBJ['HOUR'], MIN_TIME_ZONE_VALUES_OBJ['MINUTE'] = MIN_TIME_ZONE[1:].split(':')
    MIN_TIME_ZONE_VALUES_OBJ['SECOND'] = None
    MIN_TIME_ZONE_VALUES_OBJ['full_second'] = (int(MIN_TIME_ZONE_VALUES_OBJ['HOUR']) * 3600 +
                                               int(MIN_TIME_ZONE_VALUES_OBJ['MINUTE']) * 60)

# Знак
MAX_TIME_ZONE_VALUES_OBJ = {}

MAX_TIME_ZONE_VALUES_OBJ['SIGN'] = MAX_TIME_ZONE[0]
# Если указана временая зона с секундами
if len(MAX_TIME_ZONE[1:].split(':')) == 3:
    (MAX_TIME_ZONE_VALUES_OBJ['HOUR'],
     MAX_TIME_ZONE_VALUES_OBJ['MINUTE'],
     MAX_TIME_ZONE_VALUES_OBJ['SECOND']) = MAX_TIME_ZONE[1:].split(':')
    MAX_TIME_ZONE_VALUES_OBJ['full_second'] = (int(MAX_TIME_ZONE_VALUES_OBJ['HOUR']) * 3600 +
                                               int(MAX_TIME_ZONE_VALUES_OBJ['MINUTE']) * 60 +
                                               int(MAX_TIME_ZONE_VALUES_OBJ['SECOND']))
else:
    MAX_TIME_ZONE_VALUES_OBJ['HOUR'], MAX_TIME_ZONE_VALUES_OBJ['MINUTE'] = MAX_TIME_ZONE[1:].split(':')
    MAX_TIME_ZONE_VALUES_OBJ['SECOND'] = None
    MAX_TIME_ZONE_VALUES_OBJ['full_second'] = (int(MAX_TIME_ZONE_VALUES_OBJ['HOUR']) * 3600 +
                                               int(MAX_TIME_ZONE_VALUES_OBJ['MINUTE']) * 60)


def get_sequence(length=False, precision=False, scale=False, is_null=False):
    # precision - стратовое значение
    # scale - шаг для сиквенса
    if not scale:
        scale = 1
    # print(length, precision, scale, is_null)
    return str(int(precision) + int(scale))


def get_char(length=False, precision=False, scale=False, is_null=False):
    if is_null:
        if random.randint(0, 100) + PERCENT_FOR_NULL_VALUES > 100:
            return VALUE_FOR_NULL

    # Если не было передана длина, берем дефолтную
    if not length:
        rnd_length = random.randint(1, DEFAULT_VALUE_CHAR)
    else:
        rnd_length = random.randint(1, int(length))
    # if rnd_length == 0:
    #     return ''
    return_str = ''
    for i in range(rnd_length):
        symbol = random.choice(ALPHABET)
        return_str += symbol
    if WRAP_STRINGS:
        return WRAP_STRINGS + return_str + WRAP_STRINGS
    else:
        return return_str


def get_binary(length=False, precision=False, scale=False, is_null=False):
    if is_null:
        if random.randint(0, 100) + PERCENT_FOR_NULL_VALUES > 100:
            return VALUE_FOR_NULL
    if not length:
        rnd_length = random.randint(1, DEFAULT_VALUE_CHAR)
    else:
        rnd_length = random.randint(1, int(length))
    return_str = ''
    for i in range(rnd_length):
        symbol = str(random.choice(ALPHABET_HEX))
        return_str += symbol

    # Добавляем обертку для значения
    if WRAP_BINARY_VALUE:
        with_wrap_value = WRAP_BINARY_VALUE + return_str + WRAP_BINARY_VALUE
    else:
        with_wrap_value = return_str

    # Добавляем маску для значения
    if MASC_FOR_BINARY:
        with_mask = MASC_FOR_BINARY + with_wrap_value
    else:
        with_mask = with_wrap_value

    # Добавляе обертку для всей строки
    if WRAP_BINARY_STRINGS:
        result_str = WRAP_BINARY_STRINGS + with_mask + WRAP_BINARY_STRINGS
    else:
        result_str = with_mask

    return result_str


# Decimal data type
###################################
def get_decimal(length=False, precision=False, scale=False, is_null=False):
    if is_null:
        if random.randint(0, 100) + PERCENT_FOR_NULL_VALUES > 100:
            return VALUE_FOR_NULL

    min_val = 0

    # Если scale нулевой то возвращаем только precision
    if not scale or int(scale) == 0:
        return str(random.randint(min_val, int('9' * int(precision))))
    elif (int(precision) == int(scale)):
        scale_max = int('9' * int(scale))
        rnd_scale = random.randint(min_val, scale_max)
        return '0.' + str(rnd_scale)
    else:
        prec_max = int('9' * (int(precision) - int(scale)))
        scale_max = int('9' * int(scale))

        rnd_prec = random.randint(min_val, prec_max)
        rnd_scale = random.randint(min_val, scale_max)
        return str(rnd_prec) + '.' + str(rnd_scale)


# Float data types
def get_double(length=False, precision=False, scale=False, is_null=False):
    dbl_max_prec = random.randint(DOUBLE_MIN_PRECISION, DOUBLE_MAX_PRECISION)
    dbl_max_scale = random.randint(DOUBLE_MIN_SCALE, DOUBLE_MAX_SCALE)
    return get_decimal(precision=dbl_max_prec + dbl_max_scale, scale=dbl_max_scale)


def get_real(length=False, precision=False, scale=False, is_null=False):
    dbl_max_prec = random.randint(FLOAT_MIN_PRECISION, FLOAT_MAX_PRECISION)
    dbl_max_scale = random.randint(FLOAT_MIN_SCALE, FLOAT_MAX_SCALE)
    return get_decimal(precision=dbl_max_prec + dbl_max_scale, scale=dbl_max_scale)


###################################


# Integer data types
###################################
def get_tinyint(length=False, precision=False, scale=False, is_null=False):
    if is_null:
        if random.randint(0, 100) + PERCENT_FOR_NULL_VALUES > 100:
            return VALUE_FOR_NULL
    return str(random.randint(TINYINT_MIN, TINYINT_MAX))


def get_smallint(length=False, precision=False, scale=False, is_null=False):
    if is_null:
        if random.randint(0, 100) + PERCENT_FOR_NULL_VALUES > 100:
            return VALUE_FOR_NULL
    return str(random.randint(SMALLINT_MIN, SMALLINT_MAX))


def get_mediumint(length=False, precision=False, scale=False, is_null=False):
    if is_null:
        if random.randint(0, 100) + PERCENT_FOR_NULL_VALUES > 100:
            return VALUE_FOR_NULL
    return str(random.randint(MEDIUMINT_MIN, MEDIUMINT_MAX))


def get_integer(length=False, precision=False, scale=False, is_null=False):
    if is_null:
        if random.randint(0, 100) + PERCENT_FOR_NULL_VALUES > 100:
            return VALUE_FOR_NULL
    return str(random.randint(INTEGER_MIN, INTEGER_MAX))


def get_bigint(length=False, precision=False, scale=False, is_null=False):
    if is_null:
        if random.randint(0, 100) + PERCENT_FOR_NULL_VALUES > 100:
            return VALUE_FOR_NULL
    return str(random.randint(BIGINT_MIN, BIGINT_MAX))


#  Unsigned integer data types
def get_un_tinyint(length=False, precision=False, scale=False, is_null=False):
    if is_null:
        if random.randint(0, 100) + PERCENT_FOR_NULL_VALUES > 100:
            return VALUE_FOR_NULL
    return str(random.randint(UN_TINYINT_MIN, UN_TINYINT_MAX))


def get_un_smallint(length=False, precision=False, scale=False, is_null=False):
    if is_null:
        if random.randint(0, 100) + PERCENT_FOR_NULL_VALUES > 100:
            return VALUE_FOR_NULL
    return str(random.randint(UN_SMALLINT_MIN, UN_SMALLINT_MAX))


def get_un_mediumint(length=False, precision=False, scale=False, is_null=False):
    if is_null:
        if random.randint(0, 100) + PERCENT_FOR_NULL_VALUES > 100:
            return VALUE_FOR_NULL
    return str(random.randint(UN_MEDIUMINT_MIN, UN_MEDIUMINT_MAX))


def get_un_integer(length=False, precision=False, scale=False, is_null=False):
    if is_null:
        if random.randint(0, 100) + PERCENT_FOR_NULL_VALUES > 100:
            return VALUE_FOR_NULL
    return str(random.randint(UN_INTEGER_MIN, UN_INTEGER_MAX))


def get_un_bigint(length=False, precision=False, scale=False, is_null=False):
    if is_null:
        if random.randint(0, 100) + PERCENT_FOR_NULL_VALUES > 100:
            return VALUE_FOR_NULL
    return str(random.randint(UN_BIGINT_MIN, UN_BIGINT_MAX))


###################################


# DateTime data types
###################################

# Создает объект типа datetime, вида YYYY-MM-DD HH:MI:SS (формат '%Y-%m-%d %H:%M:%S')
def make_timestamp():
    min_value = 0
    max_value = 31535999  # Количество секунд в одном году
    rnd_value = random.randint(min_value, max_value)
    random_date = str(random.randint(DATE_MIN_VALUE, DATE_MAX_VALUE)).zfill(4)
    random_timestamp = random_date + datetime.datetime.utcfromtimestamp(rnd_value).strftime("-%m-%d %H:%M:%S")
    return datetime.datetime.strptime(random_timestamp, '%Y-%m-%d %H:%M:%S')


# Создает строку с фракционными секундами вида ".999999" (с лидирующими нулями)
def make_fractional_seconds(cnt_seconds):
    if cnt_seconds and int(cnt_seconds) != 0:
        cnt_seconds = int(cnt_seconds)
        f = int('9' * cnt_seconds)
        return '.' + str(random.randint(0, f)).zfill(cnt_seconds)
    else:
        return ''


# Создает строку временной зоны вида ' +00:00:00'
def make_time_zone():
    # obj['SIGN'] знак
    # obj['HOUR']
    # obj['MINUTE']
    # obj['SECOND']
    # obj['full_second'] количество секунд в промежутке

    random_tz = random.choice([0, 1])
    # 0 - MIN, 1 - MAX
    if random_tz == 0:
        obj = MIN_TIME_ZONE_VALUES_OBJ
    else:
        obj = MAX_TIME_ZONE_VALUES_OBJ
    rnd_seconds = random.randint(0, obj['full_second'])
    if obj['SECOND']:
        time_zone = datetime.datetime.utcfromtimestamp(rnd_seconds).time()

    # Если указано без секунд возвращаем только часы и минуты
    else:
        time_zone = (str(datetime.datetime.utcfromtimestamp(rnd_seconds).hour).zfill(2) +
                     ':' +
                     str(datetime.datetime.utcfromtimestamp(rnd_seconds).minute).zfill(2))
    return ' ' + obj['SIGN'] + str(time_zone)


def get_date(length=False, precision=False, scale=False, is_null=False):
    if is_null:
        if random.randint(0, 100) + PERCENT_FOR_NULL_VALUES > 100:
            return VALUE_FOR_NULL
    # Если установлена обертка, то возвращаем строку в обертке, иначе без нее
    if WRAP_DATETIME:
        return WRAP_DATETIME + str(make_timestamp().date()) + WRAP_DATETIME
    else:
        return str(make_timestamp().date())


def get_time(length=False, precision=False, scale=False, is_null=False):
    if is_null:
        if random.randint(0, 100) + PERCENT_FOR_NULL_VALUES > 100:
            return VALUE_FOR_NULL

    # Именно если параметр не передан, а не передан 0
    if str(length) == 'False':
        length = DEFAULT_VALUE_TIME_FRACTIONAL_SECONDS

    # Если 0 то без фракционных секунд
    if not length:
        result = str(make_timestamp().time())
    else:
        result = str(make_timestamp().time()) + make_fractional_seconds(length)

    # Если установлена обертка, то возвращаем строку в обертке, иначе без нее
    if WRAP_DATETIME:
        return WRAP_DATETIME + result + WRAP_DATETIME
    else:
        return result


def get_time_tz(length=False, precision=False, scale=False, is_null=False):
    if is_null:
        if random.randint(0, 100) + PERCENT_FOR_NULL_VALUES > 100:
            return VALUE_FOR_NULL

    # Именно если параметр не передан, а не передан 0
    if str(length) == 'False':
        length = DEFAULT_VALUE_TIME_FRACTIONAL_SECONDS

    # Если 0 то без фракционных секунд
    if not length:
        result = str(make_timestamp().time()) + make_time_zone()
    else:
        result = str(make_timestamp().time()) + make_fractional_seconds(length) + make_time_zone()

    # Если установлена обертка, то возвращаем строку в обертке, иначе без нее
    if WRAP_DATETIME:
        return WRAP_DATETIME + result + WRAP_DATETIME
    else:
        return result


def get_timestamp(length=False, precision=False, scale=False, is_null=False):
    if is_null:
        if random.randint(0, 100) + PERCENT_FOR_NULL_VALUES > 100:
            return VALUE_FOR_NULL

    if str(length) == 'False':
        length = DEFAULT_VALUE_TIMESTAMP_FRACTIONAL_SECONDS

    # Если 0 то без фракционных секунд
    if not length:
        result = str(make_timestamp())
    else:
        result = str(make_timestamp()) + make_fractional_seconds(length)

    # Если установлена обертка, то возвращаем строку в обертке, иначе без нее
    if WRAP_DATETIME:
        return WRAP_DATETIME + result + WRAP_DATETIME
    else:
        return result


def get_timestamp_tz(length=False, precision=False, scale=False, is_null=False):
    if is_null:
        if random.randint(0, 100) + PERCENT_FOR_NULL_VALUES > 100:
            return VALUE_FOR_NULL

    if str(length) == 'False':
        length = DEFAULT_VALUE_TIMESTAMP_FRACTIONAL_SECONDS

    if not length:
        result = str(make_timestamp()) + make_time_zone()
    else:
        result = str(make_timestamp()) + make_fractional_seconds(length) + make_time_zone()

    # Если установлена обертка, то возвращаем строку в обертке, иначе без нее
    if WRAP_DATETIME:
        return WRAP_DATETIME + result + WRAP_DATETIME
    else:
        return result


def get_boolean(length=False, precision=False, scale=False, is_null=False):
    if is_null:
        if random.randint(0, 100) + PERCENT_FOR_NULL_VALUES > 100:
            return VALUE_FOR_NULL
    return str(random.randint(0, 1))


def get_interval(length=False, precision=False, scale=False, is_null=False):
    if is_null:
        if random.randint(0, 100) + PERCENT_FOR_NULL_VALUES > 100:
            return VALUE_FOR_NULL
    years = random.randint(1, 9999) + ' years'
    months = random.randint(1, 11) + ' months'
    days = random.randint(1, 28) + ' days'
    hours = random.randint(1, 23) + ' hours'
    seconds = random.randint(1, 59) + ' seconds'
###################################
