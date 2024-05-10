import logging
import random
import shelve

from datetime import datetime
from Task import Task
from constants import SHELVE_NAME

# logging.basicConfig(filename='organic.log', level=logging.INFO)
WORK_TASKS_SHELVE_NAME = "work_tasks"
COMPLETED_WORK_SHELVE_NAME = "completed_work"


def add_task(task):
    with shelve.open(SHELVE_NAME) as storage:
        name = task
        storage[task] = Task(name)


def get_task_list(shelve_name):
    with shelve.open(shelve_name) as storage:
        return [str(task) + ': ' + str(storage[task].wage) for task in storage.keys()]


def get_prepared_task_list(shelve_name):
    with shelve.open(shelve_name) as storage:
        task_list = []
        for task in storage.keys():
            for _ in range(storage[task].wage):
                task_list.append(storage[task])
    return task_list


def get_task():
    task_list = get_prepared_task_list(SHELVE_NAME)
    task = random.choice(task_list)
    return task.name + " : " + str(task.time) + " min"


def delete_task(shelve_name, task):
    with shelve.open(shelve_name) as storage:
        del storage[task]


def task_done(task):
    with shelve.open(SHELVE_NAME) as storage:
        temp_task = storage[task].complete()
        delete_task(SHELVE_NAME, task)
        storage[task] = temp_task
        logging.info("Done: " + task)


def save_magnet_link(link):
    with open("/home/zu/torrents/magnet.magnet", "w") as fh:
        fh.write(link)


def get_sport():
    activity = random.choice(('capoeira', 'gym', 'cardio'))
    available_sups = ('protein', 'alpha-gpc', 'l-tyrosine', 'gel', 'taurine')
    available_sups = available_sups + tuple([None for sup in available_sups])
    sups = random.sample(available_sups, k=len(available_sups)//2)
    sups = [sup for sup in sups if sup is not None]
    return activity + ' with ' + ' and '.join(sups)

def add_work(priority=0, title='dummy_work'):
    with shelve.open(WORK_TASKS_SHELVE_NAME) as work_storage:
        wage = 5 - int(priority)
        work_storage[title] = Task(title, wage)


def get_work():
    task_list = get_prepared_task_list(WORK_TASKS_SHELVE_NAME)
    if len(task_list) == 0:
        return "There is nothing"
    task = random.choice(task_list)
    return task.name


def delete_work(work):
    delete_task(WORK_TASKS_SHELVE_NAME, work)
    today = get_todays_date()
    with shelve.open(COMPLETED_WORK_SHELVE_NAME) as completed_log:
        if not today in completed_log.keys():
            completed_log[today] = 1
        else:
            completed_log[today] += 1


def get_work_stats():
    with shelve.open(COMPLETED_WORK_SHELVE_NAME) as completed_log:
        today = get_todays_date()
        sum = 0
        for date in completed_log.keys():
            sum += completed_log[date]
        average = sum / len(completed_log.keys())
        task_list = get_task_list(WORK_TASKS_SHELVE_NAME)

        return 'Today: ' + str(completed_log[today]) + ', Average: ' + str(average) + '\n' + str(task_list)

def get_works():
    with shelve.open(WORK_TASKS_SHELVE_NAME) as storage:
        return [str(task) + ': ' + str(storage[task].wage) for task in storage.keys()]



def get_todays_date():
    today = datetime.today().strftime('%Y-%m-%d')
    return today
