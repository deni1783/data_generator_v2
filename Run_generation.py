# -*- coding: utf-8 -*-
import os
import sys
import time
from multiprocessing import Process
from subprocess import Popen, PIPE

# Импорт функций для каждого базового типа
from modules.Function_for_types import *

# Список базовых типов
# Ключ значение между типом и функцией его обработки
BASE_DATA_TYPES = {
    'char': get_char,
    'binary': get_binary,

    'date': get_date,
    'time': get_time,
    'timestamp': get_timestamp,

    'time_tz': get_time_tz,
    'timestamp_tz': get_timestamp_tz,

    'decimal': get_decimal,

    'double': get_double,
    'real': get_real,

    'tinyint': get_tinyint,
    'smallint': get_smallint,
    'integer': get_integer,
    'bigint': get_bigint,

    'un_tinyint': get_un_tinyint,
    'un_smallint': get_un_smallint,
    'un_integer': get_un_integer,
    'un_bigint': get_un_bigint,
}


# Посчитать кольчество строк в файле
def count_rows(file):
    cnt = 0
    for _ in open(file, 'r'):
        cnt += 1
    return cnt


def run_process(cnt, file, table_object):
    f = open(file, 'w')

    for i in range(cnt):
        arr = get_full_row_from_obj(table_object)
        st = ''
        for j in arr:
            st += j + DELIMITER_COLUMN
        # Убираем лишний последний разделитель между колонками
        result_string = st[: st.find(DELIMITER_COLUMN, -1)]
        f.write(result_string + DELIMITER_ROW)

    f.close()


def make_multiprocess(out_data_file, start_file_name, count_multiprocess, count_for_process, table_object):
    # Проверка параметров
    # out_data_file без расширения файла
    main_obj = {}
    start_file = start_file_name

    # Заполняем объект main_obj
    for k in range(count_multiprocess):
        str_k = str(k)
        proc_id = 'process_' + str_k
        main_obj[proc_id] = {}
        main_obj[proc_id]['file_name'] = out_data_file + '_part_' + str(start_file) + OUTPUT_FILE_EXTENSIONS
        main_obj[proc_id]['process_obj'] = Process(target=run_process,
                                                   args=(
                                                       count_for_process, main_obj[proc_id]['file_name'], table_object))
        start_file += 1
    return main_obj


# Делит строку из файла на части (column_name, data_type, is_nullable)
def pars_string_from_ddl(main_string: str):
    """
    Функция обрабатывает голую строку из файла и возвращает нормализированные объекты
    :param main_string: строка из файла
    :return: column_name: str (имя колонки),
             data_type:str (имя типа, без проверок),
             is_nullable:bool (True если null, False если not null)
    """
    # Пример
    # timestamptype timestamp(6) without time zone,

    # Преобразуем строку в нижний регистр и убираем лишние переводы строк и прочие символы
    normalize_string = main_string.lower().strip()

    # Убираем запятую
    if normalize_string[-1] == ',':
        normalize_string = normalize_string[:-1]

    column_name = normalize_string.split()[0]

    if 'not null' in normalize_string:
        data_type = normalize_string[len(column_name): normalize_string.index('not null')].strip()
        is_nullable = False

    elif 'null' in normalize_string:
        data_type = normalize_string[len(column_name): normalize_string.index('null')].strip()
        is_nullable = True

    else:
        data_type = normalize_string[len(column_name):]
        is_nullable = True

    # Убираем из типа 'default' и все что после него, если он есть
    if 'default' in data_type:
        data_type = data_type[:data_type.index('default')].strip()

    return column_name, data_type, is_nullable


# Разделяет тип и параметры на отдельные части (data_type, params)
def split_type_and_params(dt_name: str):
    """
    Разделить тип и параметры на отдельные объекты
    :param dt_name:
    :return: (data_type_name: str, parameters)

    parameters = value | False
    """

    # Убираем пробельные символы
    dt_name = dt_name.strip()
    if '(' in dt_name:
        indx_open = dt_name.index('(')
        indx_close = dt_name.index(')')
        new_data_type = (dt_name[:indx_open] + dt_name[indx_close + 1:])
        params = dt_name[indx_open + 1:indx_close]
    else:
        new_data_type = dt_name
        params = False
    return new_data_type, params


# Разделяет параметры на составные части (dt_length, prec, scale)
def split_parameters(params, is_decimal=False):
    """
    Разделяет параметры на отдельные части, с учетом обработки decimal
    :param params:
    :param is_decimal: default False, если True то обрабатывает как целочисленные
    :return: (dt_length, prec, scale)   Либо значения, либо False
    """
    if params:
        if ',' in params:
            prec, scale = params.split(',')
            dt_length = False
        else:
            if is_decimal:
                prec = params
                dt_length, scale = False, False
            else:
                dt_length = params
                prec, scale = False, False
        return dt_length, prec, scale
    else:
        return False, False, False


# Если для типа есть синоним то возвращает его иначе первоначальный тип
def check_synonym(dt_name: str, synonym_obj):
    dt_name = dt_name.strip()
    if dt_name in synonym_obj:
        return synonym_obj[dt_name]
    else:
        return dt_name


# Если тип отсутствует в фабрике, возвращает False, иначе True
def is_type_correct(dt_name: str):
    if not dt_name.strip() in BASE_DATA_TYPES:
        return False
    else:
        return True


def get_correctly_float(params):
    if int(params) > FLOAT_PRECISION:
        return 'double'
    else:
        return 'real'


# формирование объекта данных и тового количеста строк (columns:dict, new_count_strings)
def get_object_from_ddl_file(ddl_file):
    """
    Формирует объект типа dict с типами данных,
    а так же если в файле был явно изменен параметр COUNT_STRINGS обрабатывает его.

    :param ddl_file:
    :return: columns: dict, new_count_strings, error_obj: list

    new_count_strings value или False
    error_obj если были ошибки то список ошибок, иначе пустой массив
    """
    """
    Пример объекта с типами данных
    columns = {
        column_name: {
            data_type:   'data type name',
            dt_length:   value | False,
            precision:   value | False,
            scale:       value | False,
            is_nullable: True  | False  (if null then True, if not null then False)
        },
        ...
    }
    """

    columns = {}
    line_number = 1

    error_obj = []
    new_count_strings = False

    for line in open(ddl_file, 'r'):
        # Если строка пустая пропускаем ее
        if not line.strip():
            line_number += 1
            continue

        # Если для файла явно указано количество строк, берем его
        if line.strip().split()[0] == 'COUNT_STRINGS':
            new_count_strings = line.strip().split('=')[1].strip()
            line_number += 1
            continue

        if (line.strip() == '('
            or line.strip() == ')'
            or 'create table' in line.strip().lower()):
            line_number += 1
            continue

        # data_type - промежуточная (не обработанная)
        column_name, tmp_data_type, is_nullable = pars_string_from_ddl(line)

        # Проверка на наличие синонимов именно если тип с парапетрами
        # Например 'int(8)': 'bigint'
        without_synonym_type = check_synonym(tmp_data_type, SYNONYMS_DICT)

        # Разделяем тип и параметры
        dt_type, params = split_type_and_params(without_synonym_type)

        # В зависимости от значения params и FLOAT_PRECISION проставляем нужный тип
        if dt_type == 'float':
            dt_type = get_correctly_float(params)
            params = False

        # Проверяем синонимы без явного указания параметров для типа
        # Например 'number': 'decimal'
        dt_type = check_synonym(dt_type, SYNONYMS_DICT)

        if not is_type_correct(dt_type):
            error_obj.append('Error at line ' + str(line_number) + ' data type: "' + dt_type + '" is not supported!')
            line_number += 1
            continue
        if dt_type == 'decimal':
            dt_length, prec, scale = split_parameters(params, is_decimal=True)
        else:
            dt_length, prec, scale = split_parameters(params)

        columns[column_name] = {}
        columns[column_name]['data_type'] = dt_type
        columns[column_name]['dt_length'] = dt_length
        columns[column_name]['precision'] = prec
        columns[column_name]['scale'] = scale
        columns[column_name]['is_nullable'] = is_nullable

        line_number += 1

    # Если были ошибки выводим на экран и завершаем приложение
    # if error_obj:
    #     err_str = '\n'.join(error_obj)
    #     return err_str, new_count_strings
    return columns, new_count_strings, error_obj


# Формирует массив сгенерированных данных для одной строки (return - result_arr: list)
def get_full_row_from_obj(table_object):
    """
    Создает массив сгенерированных данных для одной строки
    :param table_object:
    :return: result_arr: list
    """
    result_arr = []
    for key in table_object:
        column = table_object[key]
        col_data_type = column['data_type']

        result_arr.append(BASE_DATA_TYPES[col_data_type](column['dt_length'],
                                                         column['precision'],
                                                         column['scale'],
                                                         column['is_nullable']))
    return result_arr


def start_generation_for_single_file(file_name: str, out_dir_name='', in_dir_name=''):
    started_time = time.time()
    base_file_name = os.path.basename(file_name)
    print('\nGenerate for "{}"'.format(file_name))

    # Генерируем:
    #   1 - объект с типами для каждого поля (table_object)
    #   2 - параметр кол-ва строк, (new_cnt_str)
    #   3 - массив ошибок парсинга (err_arr)

    # Если это файлы из определенной директории, добавляем путь к имени файла
    if in_dir_name:
        in_file = os.path.normcase(in_dir_name + '/' + file_name)
        table_object, new_cnt_str, err_arr = get_object_from_ddl_file(in_file)
    else:
        table_object, new_cnt_str, err_arr = get_object_from_ddl_file(file_name)

    # Если была ошибка при парсинге файла, возвращаем текст ошибки и закрываем программу с кодом 1
    if err_arr:
        for err in err_arr:
            print(err)
        exit(1)

    # Если кольчество строк для файла прописанно именно в файле
    if new_cnt_str:
        count_strings_per_file = int(new_cnt_str) // COUNT_OUTPUT_FILE
    else:
        count_strings_per_file = COUNT_STRINGS // COUNT_OUTPUT_FILE

    # Если указана определенная директория для результирующих файлов, добавляем ее к названию итогового файла
    if out_dir_name:
        out_file_name = os.path.normcase(out_dir_name + '/' + 'data_for_' + os.path.splitext(base_file_name)[0])
    else:
        out_file_name = 'data_for_' + os.path.splitext(base_file_name)[0]

    # Счетчик готовых промежуточных файлов
    cnt_tmp_file_done = 0

    # Цикл создания процессов
    while cnt_tmp_file_done < COUNT_OUTPUT_FILE:
        # Если количество оставшихся необработанных промежуточных файлов меньше чем количество максимальных процессов,
        # приравниваем количество процессов к количеству оставшихся файлов
        if COUNT_OUTPUT_FILE - cnt_tmp_file_done < MAX_COUNT_SUBPROCESS:
            cnt_multiproc = COUNT_OUTPUT_FILE - cnt_tmp_file_done
        else:
            cnt_multiproc = MAX_COUNT_SUBPROCESS

        # Генерируем объект для всех процессов
        main_obj = make_multiprocess(out_file_name, cnt_tmp_file_done, cnt_multiproc, count_strings_per_file,
                                     table_object)

        # Запускаем процессы
        for key in main_obj:
            main_obj[key]['process_obj'].start()

        # Ждем завершение всех процессов
        for key in main_obj:
            main_obj[key]['process_obj'].join()

        cnt_tmp_file_done += cnt_multiproc

    end_generation_time = time.time()
    print('  Durations:')
    print('    Generating:  ', datetime.datetime.utcfromtimestamp(end_generation_time - started_time).time())

    # Заполняем массив со всеми временными файлами
    all_tmp_files_arr = []
    for i in range(cnt_tmp_file_done):
        all_tmp_files_arr.append(out_file_name + '_part_' + str(i) + OUTPUT_FILE_EXTENSIONS)

    # Если нужно объеденить все файлы в один
    if MERGE_ALL_FILE_TO_SINGLE:
        # Генерируем строку со всеми файлами для их объединения
        all_files_str = ''
        for i in all_tmp_files_arr:
            all_files_str += i + ' '

        os_platform = sys.platform

        if os_platform == 'darwin' or os_platform == 'linux':
            cmd = 'cat '
        else:
            cmd = 'type '

        command = cmd + all_files_str + '> ' + out_file_name + '_full' + OUTPUT_FILE_EXTENSIONS

        # Запускаем объединение файлов
        start = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
        start.wait()

        # print('End merge all files for "{}"'.format(file_name))
        print('    Merging:     ', datetime.datetime.utcfromtimestamp(time.time() - end_generation_time).time())

    if DEL_ALL_TMP_FILE:
        start_delete = time.time()
        # Удаляем временные файлы
        for f in all_tmp_files_arr:
            os.remove(f)
        print('    Deleting:    ', datetime.datetime.utcfromtimestamp(time.time() - start_delete).time())

    print('    Full:        ', datetime.datetime.utcfromtimestamp(time.time() - started_time).time())


def start_generation():

    # Проверяем наличие параметров, если не было переданно ни одного параметра - Выводим ошибку
    if len(sys.argv) == 1:
        print('Error')
        print(
            'The required parameter was not passed: a file or directory with files with a list of fields in the table')
        exit(1)

    if len(sys.argv) == 3:
        out_dir_name = sys.argv[2]
    else:
        out_dir_name = ''

    # Если в качестве параметра передана директория,
    # последовательно обрабатываем все файлы из этой директории
    if os.path.isdir(sys.argv[1]):
        list_files = os.listdir(sys.argv[1])

        # Проходим по всем файлам
        for file in list_files:
            start_generation_for_single_file(file, out_dir_name, sys.argv[1])

    else:
        # Иначе генерируем данные только для переданного файла
        start_generation_for_single_file(sys.argv[1], out_dir_name)


if __name__ == '__main__':
    start_time = time.time()
    print('Started at', datetime.datetime.utcfromtimestamp(start_time), 'UTC')

    start_generation()

    end_time = time.time()
    print('\nFinished at', datetime.datetime.utcfromtimestamp(end_time), 'UTC')

    duration = datetime.datetime.utcfromtimestamp(end_time - start_time).time()
    print('Duration of the entire generation: ', duration)
