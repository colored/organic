import datetime
import random
import shelve

import telepot
from telepot.loop import MessageLoop

from Task import Task

SHELVE_NAME = "tasks"
TOKEN = '595325421:AAFCfc5pOjpAc7I_eFd-UVCG0M_6FY6VMXQ'
bot = telepot.Bot(TOKEN)

def add_task(task):
    with shelve.open(SHELVE_NAME) as storage:
        name = task
        times = receive_message('times: ')
        per_day = receive_message('per_day: ')
        from_time = receive_message('from time: ')
        till_time = receive_message('till time: ')
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


def display(text):
    bot.sendMessage(999999999, text)


def receive_message(param):
    pass


if __name__ == "__main__":
    # while True:
    #     display("1: Add task")
    #     display("2: Get task")
    #     display("3: Delete task")
    #     display("4: Display all tasks")
    #     inp = int(receive_message("Your choice:"))
    #     if inp == 1:
    #         task = receive_message("Task name: ")
    #         add_task(task)
    #     elif inp == 2:
    #         task = get_task()
    #         print(task)
    #         answer = receive_message("Is it done? y/n: ")
    #         if answer == "y" or answer == "yes":
    #             task_done(task)
    #             print("Task is done!!!")
    #         else:
    #             print("Next time")
    #     elif inp == 3:
    #         delete_task(receive_message("delete task: "))
    #     elif inp == 4:
    #         print(get_task_list())
    #
    #     else:
    #         print("Unknown command")


    import time
    import telepot

    BOT_TOKEN = "595325421:AAFCfc5pOjpAc7I_eFd-UVCG0M_6FY6VMXQ"

    tg_bot = 0

    tg_commands = {}


    # return cmd, params
    def parse_cmd(cmd_string):
        text_split = cmd_string.split()
        return text_split[0], text_split[1:]


    def add_command(cmd, func):
        global tg_commands
        tg_commands[cmd] = func


    def remove_command(cmd):
        global tg_commands
        del tg_commands[cmd]


    def on_message(message):
        global tg_bot
        content_type, chat_type, chat_id = telepot.glance(message)

        if content_type == "text":
            msg_text = message['text']
            chat_id = message['chat']['id']

            print("[MSG] {uid} : {msg}".format(uid=message['from']['id'], msg=msg_text))

            if msg_text[0] == '/':
                cmd, params = parse_cmd(msg_text)
                try:
                    tg_commands[cmd](chat_id, params)
                except KeyError:
                    tg_bot.sendMessage(chat_id, "Unknown command: {cmd}".format(cmd=cmd))
            else:
                tg_bot.sendMessage(chat_id, "Message is a plain text")


    def cmd_echo(chat_id, params):
        tg_bot.sendMessage(chat_id, "[ECHO] {text}".format(text=" ".join(params)))


    def cmd_start(chat_id, params):
        msg = "/add_task \n /get_task \n /delete_task \n /display_all_tasks \n /task_done"
        tg_bot.sendMessage(chat_id, msg)


    def cmd_add_task(chat_id, params):
        tg_bot.sendMessage(chat_id, "Task " + params[0] + " added.")
        add_task(params[0])


    def cmd_get_task(chat_id, params):
        tg_bot.sendMessage(chat_id, get_task())


    def cmd_delete_task(chat_id, params):
        delete_task(params[0])
        tg_bot.sendMessage(chat_id, "Task " + params[0] + " was removed.")


    def cmd_display_all_tasks(chat_id, params):
        tg_bot.sendMessage(chat_id, get_task_list())


    def cmd_task_done(chat_id, params):
        task_done(params[0])
        tg_bot.sendMessage(chat_id, "Task " + params[0] + " is done.")


    def main():
        global tg_bot
        tg_bot = telepot.Bot(BOT_TOKEN)
        add_command("/echo", cmd_echo)
        add_command("/start", cmd_start)
        add_command("/add_task", cmd_add_task)
        add_command("/get_task", cmd_get_task)
        add_command("/delete_task", cmd_delete_task)
        add_command("/display_all_tasks", cmd_display_all_tasks)
        add_command("/task_done", cmd_task_done)
        MessageLoop(tg_bot, on_message).run_as_thread()
        print("Listening messages")


    if __name__ == "__main__":
        main()
        while True:
            time.sleep(10)
