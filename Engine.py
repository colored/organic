import random
import shelve

from Task import Task
from main import SHELVE_NAME


def add_task(task):
    with shelve.open(SHELVE_NAME) as storage:
        name = task
        storage[task] = Task(name)


def get_task_list():
    with shelve.open(SHELVE_NAME) as storage:
        return [str(task) + ': ' + str(storage[task].wage) for task in storage.keys()]


def get_prepared_task_list():
    with shelve.open(SHELVE_NAME) as storage:
        task_list = []
        for task in storage.keys():
            for _ in range(storage[task].wage):
                task_list.append(task)
    return task_list


def get_task():
    task_list = get_prepared_task_list()
    return random.choice(task_list)


def delete_task(task):
    with shelve.open(SHELVE_NAME) as storage:
        del storage[task]


def task_done(task):
    with shelve.open(SHELVE_NAME) as storage:
        temp_task = storage[task].complete()
        delete_task(task)
        storage[task] = temp_task
