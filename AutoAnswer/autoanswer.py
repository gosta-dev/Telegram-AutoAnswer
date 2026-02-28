#Значения по умолчанию
dataget = ''
sleep = 1
user = ''
get_message = ''
check_message = ''
get_message2 = ''
check_message2 = ''
cai = open('config.txt', 'r').read().splitlines()[0]
user_prompt = open('config.txt', 'r').read().splitlines()[1]
auto_server_up_tick = 0
help_command = '''
Чтобы указать доп. параметры используй командную строку и следующие команды:
/sleep=                                                  ---Устанавливает период обновления содержания чата(По умолчанию: 1 секунда)
/help                                                    ---Показывает эту подсказку
/start                                                   ---Запустить автоответчик
/chat-gpt                                                ---Запустить автоответчик с режимом ответа с AI
/cai                                                     ---Изменить бота для ответа(Укажи юз)
Пример:
/cai @username
/sleep=5
                        '''
import time
try:
    from pyrogram import *
except:
    pass

app = Client("session")
app.start()
def from_bot_to_user():
    global get_message
    global check_message
    global get_message2
    global check_message2
    global user
    bot_chat_history2 = app.get_chat_history(cai, 1)
    for i in bot_chat_history2:
        get_message2 = i.text
    check_message2 = get_message2
    def prom_func2():
        time.sleep(sleep)
        bot_chat_history1 = app.get_chat_history(cai, 1)
        for i in bot_chat_history1:
            get_message2 = i.text
        print(check_message2)
        if check_message2 == get_message2:
            time.sleep(sleep)
            prom_func2()
        else:
            app.send_message(user, get_message2)
            from_user_to_bot()
    prom_func2()


def from_user_to_bot():
    global get_message
    global check_message
    global user
    user_chat_history2 = app.get_chat_history(user, 1)
    for i in user_chat_history2:
        get_message = i.text
    check_message = get_message
    def prom_func():
        global auto_server_up_tick
        time.sleep(sleep)
        auto_server_up_tick += 1
        if auto_server_up_tick >= 600:
            app.send_message(app.get_me().id, 'Сообщение для поддержания работоспособности')
            auto_server_up_tick = 0
        user_chat_history1 = app.get_chat_history(user, 1)
        for i in user_chat_history1:
            get_message = i.text
        if check_message == get_message:
            time.sleep(sleep)
            prom_func()
        else:
            app.send_message(cai, get_message)
            from_bot_to_user()
    prom_func()
print(help_command)
def main():
    session_chats = app.get_dialogs()
    show_chat_checkbocks = input('Показать список чатов? (+/-): ')
    def show_chat(show_chat_checkbocks):
        for chat in session_chats:
            private_chat = chat.chat.first_name
            if private_chat != None:
                print(private_chat, chat.chat.id)
    if show_chat_checkbocks == '+':
        show_chat(show_chat_checkbocks)
    elif show_chat_checkbocks == '-':
        pass

    set_chat = int(input('Введи ID чата: '))
    set_message_trigger = input("Введи сообщение на которое надо ответить?: ").lower()
    set_message_answer = input('Что на него надо ответить?: ')

    while True:
        time.sleep(sleep)
        data = app.get_chat_history(set_chat, 1)
        for item in data:
            data = item.text.lower()
            if set_message_trigger == data:
                app.send_message(set_chat, set_message_answer)
                print('Сообщение было отправлено')

def chat_gpt():
    global user
    print('Для более корректной работы AI, напиши небольшой рассказ о себе. Можешь указать данные которые будут использоваться для ответа. Оставь поле пустым, чтобы пропустить этот этап. ОБЯЗАТЕЛЬНО!!!: Используй свой привычный стиль общения, будто пишешь это другу')
    prompt = input('Ввод: ').lower()
    app.send_message(cai, 'Обнули контекст. Представь что ты - человек который общается в Telegram. Не используй точки. Не используй эмодзи. Общайся как в следующем тексте, используй данные из него и интерпритируй их на себя: ' + prompt)
    def check_right():
        global user
        global dataget
        global sleep
        data = app.get_chat_history(cai, 1)
        for i in data:
            message = i.text
        #ПРОМПТ
        if 'Обнули контекст. Представь что ты - человек который общается в Telegram. Не используй эмодзи. Можешь указать в круглых скобках что сделать с сообщением дополнительно(к примеру, поставить реакцию). Общайся как в следующем тексте, используй данные из него и интерпритируй их на себя: ' in message:
            time.sleep(sleep)
            data = app.get_chat_history(cai, 1)
            for i in data:
                dataget = i.text
            check_right()
        else:
            check_box = input(f'{dataget} \n Все верно? (+/-): ')
            if check_box == '+':
                user = input('Тогда идем дальше. Укажи юзернейм пользователя/ID чата от которого будем ждать сообщения: ')
                print('Обрабатываю все новые сообщения...')
                from_user_to_bot()

            elif check_box == '-':
                print('Пройдем персонализацию AI еще раз')
                chat_gpt()

    check_right()
#Пользовательские настройки
def mr_settings():
    global user_prompt
    global sleep
    spec = input('Введите команду: ')
    #Настройка слип
    if '/sleep=' in spec and float(str(spec)[7:]) > 0.4:
        try:
            sleep = float(str(spec)[7:])
        except:
            print('Введите верное значение(Только числа)')
            mr_settings()
        print(f'Период обновления обновлен. Текущее значение: {sleep}')
        answer = input('Хотите продолжить настройку?(+/-): ')
        if answer == '+':
            mr_settings()
        elif answer == '-':
            print(f'Текущие настройки: sleep={sleep}')
        else:
            print('Невариативный ответ')
    #Хелп лист
    elif '/help' in spec:
        print(help_command)
        mr_settings()
    elif '/start' in spec:
        main()
    elif '/chat-gpt' in spec:
        chat_gpt()
    elif '/cai' in spec:
        cai = spec[5:]
        print(cai)
        mr_settings()
    else:
        print('Введена неверная команда/ошибка синтаксиза команды')
        mr_settings()
mr_settings()
