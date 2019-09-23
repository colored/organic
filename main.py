import sys

from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

from Engine import *

SHELVE_NAME = "tasks"

if __name__ == "__main__":
    import time
    import telepot

    BOT_TOKEN = sys.argv[1]

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
        keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=" ".join(params))]])
        tg_bot.sendMessage(chat_id, 'keyboardtest', reply_markup=keyboard)


    def cmd_start(chat_id, params):
        msg = "/add_task \n /get_task \n /delete_task \n /display_all_tasks \n /task_done"
        tg_bot.sendMessage(chat_id, msg)


    def cmd_add_task(chat_id, params):
        tg_bot.sendMessage(chat_id, "Task " + params[0] + " added.")
        add_task(params[0])


    def cmd_get_task(chat_id, params):
        tg_bot.sendMessage(chat_id, get_task())


    def cmd_delete_task(chat_id, params):
        delete_task(SHELVE_NAME, params[0])
        tg_bot.sendMessage(chat_id, "Task " + params[0] + " was deleted.")


    def cmd_display_all_tasks(chat_id, params):
        tg_bot.sendMessage(chat_id, get_task_list())


    def cmd_task_done(chat_id, params):
        task_done(params[0])
        tg_bot.sendMessage(chat_id, "Task " + params[0] + " is done.")


    def cmd_magnet(chat_id, params):
        save_magnet_link(params[0])
        tg_bot.sendMessage(chat_id, "Magnet added")


    def cmd_getsport(chat_id, params):
        tg_bot.sendMessage(chat_id, get_sport())


    def cmd_addwork(chat_id, params):
        add_work(priority=params[0], title=params[1])
        tg_bot.sendMessage(chat_id, "work task " + params[1] + " added with priority " + params[0])


    def cmd_getwork(chat_id, params):
        tg_bot.sendMessage(chat_id, get_work())


    def cmd_delete_work(chat_id, params):
        delete_work(params[0])
        tg_bot.sendMessage(chat_id, 'Task ' + params[0] + ' was deleted')

    def cmd_work_stats(chat_id, params):
        tg_bot.sendMessage(chat_id, get_work_stats())


    def cmd_getworks(chat_id, params):
        tg_bot.sendMessage(chat_id, get_works())


    def main():
        global tg_bot
        tg_bot = telepot.Bot(BOT_TOKEN)
        add_command("/echo", cmd_echo)
        add_command("/start", cmd_start)
        add_command("/addtask", cmd_add_task)
        add_command("/get_task", cmd_get_task)
        add_command("/deletetask", cmd_delete_task)
        add_command("/displaytasks", cmd_display_all_tasks)
        add_command("/taskdone", cmd_task_done)
        add_command("/magnet", cmd_magnet)
        add_command("/getsport", cmd_getsport)
        add_command("/addwork", cmd_addwork)
        add_command("/getwork", cmd_getwork)
        add_command("/getworks", cmd_getworks)
        add_command("/deletework", cmd_delete_work)
        add_command("/workstats", cmd_work_stats)
        MessageLoop(tg_bot, on_message).run_as_thread()
        print("Listening messages")


    if __name__ == "__main__":
        main()
        while True:
            time.sleep(10)
