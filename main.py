import time

from LitParser import get_stats_day
from db_writer import init_db, write_to_db
from MarketParser import parse_stats_day_litmarket
from logger_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

genres = {'477': 'Бытовое фэнтези',
    # '463': 'Попаданки в другие',
    '349': 'Любовное фэнтези',
    '352': 'Магические академии',}
    # '467': 'Попаданки в академии'}


if __name__ == '__main__':
    logger.info('start')
    init_db(logger)

    file_path_litmarket = r'C:\Users\1\Desktop\bookdaystats\lit1.xlsx'
    # file_path = r'C:\Users\1\Desktop\bookdaystats\main.xlsx'
    # url_litnet = r'https://litnet.com/ru/lada-orfeeva-u3419385'
    for key, genre in genres.items():
        base_url_litmarket = f'https://litmarket.ru/books?page=1&genres={key}'
        data = parse_stats_day_litmarket(base_url_litmarket)
        write_to_db(data, genre, logger)
        time.sleep(1)

    # day_dict = get_stats_day(url_litnet)
    # write_file(day_dict, file_path, logger, 'book')
    logger.info('Done')