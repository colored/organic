import logging
import random
import shelve

from Task import Task
from main import SHELVE_NAME


# logging.basicConfig(filename='organic.log', level=logging.INFO)
WORK_TASKS_SHELVE_NAME = "work_tasks"


def add_task(task):
    with shelve.open(SHELVE_NAME) as storage:
        name = task
        storage[task] = Task(name)


def get_task_list():
    with shelve.open(SHELVE_NAME) as storage:
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
    return random.choice(('capoeira','capoeira','capoeira', 'gym', 'gym', 'bike'))

def add_work(priority=0, title='dummy_work'):
    with shelve.open(WORK_TASKS_SHELVE_NAME) as work_storage:
        wage = 4 - int(priority)
        work_storage[title] = Task(title, wage)

def get_work():
    task_list = get_prepared_task_list(WORK_TASKS_SHELVE_NAME)
    task = random.choice(task_list)
    return task.name

def delete_work(work):
    with shelve.open(WORK_TASKS_SHELVE_NAME) as work_storage:
        delete_task(WORK_TASKS_SHELVE_NAME, work)
