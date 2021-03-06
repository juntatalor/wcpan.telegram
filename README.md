# TeleZombie

Telegram Bot API with Tornado.

## High Level API Example

`TeleLich` is a high level undead, you can demand it to send requests:

```python
from tornado import gen, ioloop
from telezombie import api, types


@gen.coroutine
def main():
    API_TOKEN = 'your_token'
    lich = api.TeleLich(API_TOKEN)
    talk_to = 42

    # getMe
    user = yield lich.get_me()
    print(user)

    # getUpdates
    updates = yield lich.get_updates()
    print(updates)

    # sendMessage
    message = yield lich.send_message(talk_to, 'hello')
    print(message)

    # sendPhoto
    photo = types.InputFile('path_to_your_phoho.png')
    message = yield lich.send_photo(talk_to, photo)
    print(message)

    # sendAudio
    audio = types.InputFile('path_to_your_audio.ogg')
    message = yield lich.send_audio(talk_to, audio)
    print(message)

    # sendVideo
    video = types.InputFile('path_to_your_video.mp4')
    message = yield lich.send_video(talk_to, video)
    print(message)

    # sendDocument
    document = types.InputFile('path_to_your_file.zip')
    message = yield lich.send_document(talk_to, document)
    print(message)


main_loop = ioloop.IOLoop.instance()
main_loop.run_sync(main)
```

And let it handles updates:

```python
from tornado import gen, ioloop
from telezombie import api


class KelThuzad(api.TeleLich):

    def __init__(self, api_token):
        super(KelThuzad, self).__init__(api_token)

    @gen.coroutine
    def on_text(self, message):
        id_ = message.message_id
        chat = message.chat
        text = message.text
        # echo same text
        yield self.send_message(chat.id_, text, reply_to_message_id=id_)

    @gen.coroutine
    def on_video(self, message):
        chat = message.chat
        video = message.video
        # echo video without upload again
        yield self.send_video(chat.id_, video.file_id, reply_to_message_id=id_)


@gen.coroutine
def forever():
    API_TOKEN = 'your_token'
    lich = api.KelThuzad(API_TOKEN)

    yield lich.poll()


main_loop = ioloop.IOLoop.instance()
main_loop.run_sync(forever)
```

Or handles updates by webhook:

```python
from tornado import gen, ioloop, web
from telezombie import api


class HookHandler(api.TeleHookHandler):

    @gen.coroutine
    def on_text(self, message):
        lich = self.application.settings['lich']
        id_ = message.message_id
        chat = message.chat
        text = message.text
        # echo same text
        yield lich.send_message(chat.id_, text, reply_to_message_id=id_)


@gen.coroutine
def create_lich():
    API_TOKEN = 'your_token'
    lich = api.TeleLich(API_TOKEN)

    yield lich.listen('https://your.host/hook')

    return lich


main_loop = ioloop.IOLoop.instance()

lich = main_loop.run_sync(create_lich)
application = web.Application([
    (r"/hook", HookHandler),
], lich=lich)
# please configure your own SSL proxy
application.listen(8000)

main_loop.start()
```

## Low Level API Example

Although the `TeleLich` is handy, sometimes you just need a ghoul to collect
lumber for you, so you can use it to build your own Ziggurat.

`TeleZombie` provides simple and direct API mapping:

```python
from tornado import gen, ioloop
from telezombie import api, types


@gen.coroutine
def main():
    API_TOKEN = 'your_token'
    ghoul = api.TeleZombie(API_TOKEN)
    talk_to = 42

    # getMe
    user = yield ghoul.get_me()
    print(user)

    # getUpdates
    offset = 0
    updates = []
    while True:
        us = yield ghoul.get_updates(offset)
        updates.extend(us)
        if not us:
            break
        offset = us[-1].update_id + 1
    print(updates)

    # sendMessage
    message = yield ghoul.send_message(talk_to, 'hello')
    print(message)

    # sendDocument
    document = types.InputFile('path_to_your_file.zip')
    message = yield lich.send_document(talk_to, document)
    print(message)


main_loop = ioloop.IOLoop.instance()
main_loop.run_sync(main)
```
