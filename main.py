import random
import shelve

import datetime

from Task import Task


SHELVE_NAME = "tasks"


def add_task(task):
    with shelve.open(SHELVE_NAME) as storage:
        name = task
        times = input('times: ')
        per_day = input('per_day: ')
        from_time = input('from time: ')
        till_time = input('till time: ')
        storage[task] = Task(name, times, per_day, from_time_hrs=from_time, till_time_hrs=till_time)


def get_task_list():
    with shelve.open(SHELVE_NAME) as storage:
        return [str(task) + ': ' + str(storage[task].wage) for task in storage.keys()]


def to_datetime_format(time):
    return datetime.datetime.now().replace(hour=time, minute=0, second=0, microsecond=0)


def get_prepared_task_list():
    with shelve.open(SHELVE_NAME) as storage:
        task_list = []
        current_time = datetime.datetime.now()
        for task in storage.keys():
            if to_datetime_format(storage[task].from_time) < current_time < to_datetime_format(storage[task].till_time):
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

def convert():
    with shelve.open(SHELVE_NAME) as storage:
        for task in storage.keys():
            temp_task = storage[task]
            temp_task.from_time = 1
            temp_task.till_time = 23
            delete_task(task)
            storage[task] = temp_task

if __name__ == "__main__":
    while True:
        print("1: Add task")
        print("2: Get task")
        print("3: Delete task")
        print("4: Display all tasks")
        inp = int(input("Your choice:"))
        if inp == 1:
            task = input("Task name: ")
            add_task(task)
        elif inp == 2:
            task = get_task()
            print(task)
            answer = input("Is it done? y/n: ")
            if answer == "y" or answer == "yes":
                task_done(task)
                print("Task is done!!!")
            else:
                print("Next time")
        elif inp == 3:
            delete_task(input("delete task: "))
        elif inp == 4:
            print(get_task_list())

        else:
            print("Unknown command")
