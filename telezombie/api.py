from __future__ import unicode_literals

import json

from tornado import gen, httpclient, web, httputil

from . import types, util

_API_TEMPLATE = 'https://api.telegram.org/bot{api_token}/{api_method}'


class TeleZombie(object):
    def __init__(self, api_token):
        self._api_token = api_token
        if not self._api_token:
            raise TeleError('invalid API token')

    @gen.coroutine
    def get_updates(self, offset=0, limit=100, timeout=0):
        args = {
            'offset': offset,
            'limit': limit,
            'timeout': timeout,
        }
        data = yield self._get('getUpdates', args)
        raise gen.Return([types.Update(u) for u in data])

    @gen.coroutine
    def set_webhook(self, url=None):
        if url is None:
            args = None
        else:
            args = {
                'url': url
            }

        # TODO undocumented return type
        data = yield self._get('setWebhook', args)
        raise gen.Return(None)

    @gen.coroutine
    def get_me(self):
        data = yield self._get('getMe')
        raise gen.Return(types.User(data))

    @gen.coroutine
    def send_message(self, chat_id, text, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None):
        args = {
            'chat_id': chat_id,
            'text': text,
        }
        if disable_web_page_preview is not None:
            args['disable_web_page_preview'] = disable_web_page_preview
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = str(reply_markup)

        data = yield self._get('sendMessage', args)
        raise gen.Return(types.Message(data))

    @gen.coroutine
    def answer_callback_query(self, callback_query_id, text=None, show_alert=None, url=None, cache_time=None):
        args = {
            'callback_query_id': callback_query_id
        }
        if text is not None:
            args['text'] = text
        if show_alert is not None:
            args['show_alert'] = show_alert
        if url is not None:
            args['url'] = url
        if cache_time is not None:
            args['cache_time'] = cache_time

        data = yield self._get('answerCallbackQuery', args)
        raise gen.Return(data)

    @gen.coroutine
    def edit_message_text(self, text, chat_id=None, message_id=None, inline_message_id=None, parse_mode=None,
                          disable_web_page_preview=None, reply_markup=None):
        args = {
            'text': text
        }
        if chat_id is not None:
            args['chat_id'] = chat_id
        if message_id is not None:
            args['message_id'] = message_id
        if inline_message_id is not None:
            args['inline_message_id'] = inline_message_id
        if parse_mode is not None:
            args['parse_mode'] = parse_mode
        if disable_web_page_preview is not None:
            args['disable_web_page_preview'] = disable_web_page_preview
        if reply_markup is not None:
            args['reply_markup'] = reply_markup

        data = yield self._get('editMessageText', args)
        raise gen.Return(data)

    @gen.coroutine
    def edit_message_caption(self, caption, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        args = {
            'caption': caption
        }
        if chat_id is not None:
            args['chat_id'] = chat_id
        if message_id is not None:
            args['message_id'] = message_id
        if inline_message_id is not None:
            args['inline_message_id'] = inline_message_id
        if reply_markup is not None:
            args['reply_markup'] = reply_markup

        data = yield self._get('editMessageCaption', args)
        raise gen.Return(data)

    @gen.coroutine
    def edit_message_reply_markup(self, chat_id=None, message_id=None, inline_message_id=None,
                                  reply_markup=None):
        args = {}
        if chat_id is not None:
            args['chat_id'] = chat_id
        if message_id is not None:
            args['message_id'] = message_id
        if inline_message_id is not None:
            args['inline_message_id'] = inline_message_id
        if reply_markup is not None:
            args['reply_markup'] = reply_markup

        data = yield self._get('editMessageReplyMarkup', args)
        raise gen.Return(data)

    @gen.coroutine
    def forward_message(self, chat_id, from_chat_id, message_id):
        args = {
            'chat_id': chat_id,
            'from_chat_id': from_chat_id,
            'message_id': message_id,
        }

        data = yield self._get('forwardMessage', args)
        raise gen.Return(types.Message(data))

    @gen.coroutine
    def send_photo(self, chat_id, photo, caption=None, reply_to_message_id=None, reply_markup=None):
        args = {
            'chat_id': chat_id,
            'photo': photo,
        }
        if caption is not None:
            args['caption'] = caption
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = str(reply_markup)

        if isinstance(photo, str):
            data = yield self._get('sendPhoto', args)
        else:
            data = yield self._post('sendPhoto', args)

        raise gen.Return(types.Message(data))

    @gen.coroutine
    def send_audio(self, chat_id, audio, reply_to_message_id=None, reply_markup=None):
        args = {
            'chat_id': chat_id,
            'audio': audio,
        }
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = str(reply_markup)

        if isinstance(audio, str):
            data = yield self._get('sendAudio', args)
        else:
            data = yield self._post('sendAudio', args)

        raise gen.Return(types.Message(data))

    @gen.coroutine
    def send_document(self, chat_id, document, reply_to_message_id=None, reply_markup=None):
        args = {
            'chat_id': chat_id,
            'document': document,
        }
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = str(reply_markup)

        if isinstance(document, str):
            data = yield self._get('sendDocument', args)
        else:
            data = yield self._post('sendDocument', args)

        raise gen.Return(types.Message(data))

    @gen.coroutine
    def send_sticker(self, chat_id, sticker, reply_to_message_id=None, reply_markup=None):
        args = {
            'chat_id': chat_id,
            'sticker': sticker,
        }
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = str(reply_markup)

        if isinstance(sticker, str):
            data = yield self._get('sendSticker', args)
        else:
            data = yield self._post('sendSticker', args)

        raise gen.Return(types.Message(data))

    @gen.coroutine
    def send_video(self, chat_id, video, reply_to_message_id=None, reply_markup=None):
        args = {
            'chat_id': chat_id,
            'video': video,
        }
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = str(reply_markup)

        if isinstance(video, str):
            data = yield self._get('sendVideo', args)
        else:
            data = yield self._post('sendVideo', args)

        raise gen.Return(types.Message(data))

    @gen.coroutine
    def send_location(self, chat_id, latitude, longitude, reply_to_message_id=None, reply_markup=None):
        args = {
            'chat_id': chat_id,
            'latitude': latitude,
            'longitude': longitude,
        }
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = str(reply_markup)

        data = yield self._get('sendLocation', args)
        raise gen.Return(types.Message(data))

    @gen.coroutine
    def send_chat_action(self, chat_id, action):
        args = {
            'chat_id': chat_id,
            'action': action,
        }

        # TODO undocumented return type
        data = yield self._get('sendChatAction', args)
        raise gen.Return(None)

    @gen.coroutine
    def get_user_profile_photos(self, user_id, offset=0, limit=100):
        args = {
            'user_id': user_id,
            'offset': offset,
            'limit': limit,
        }

        data = yield self._get('getUserProfilePhotos', args)
        raise gen.Return(types.UserProfilePhotos(data))

    def _get_api_url(self, api_method):
        return _API_TEMPLATE.format(api_token=self._api_token, api_method=api_method)

    def _parse_response(self, response):
        data = response.body.decode('utf-8')
        data = json.loads(data)
        if not data['ok']:
            raise TeleError(data['description'])
        return data['result']

    @gen.coroutine
    def _get(self, api_method, args=None):
        url = self._get_api_url(api_method)
        if args is not None:
            url = httputil.url_concat(url, args)

        link = httpclient.AsyncHTTPClient()
        request = httpclient.HTTPRequest(url)
        response = yield link.fetch(request)

        raise gen.Return(self._parse_response(response))

    @gen.coroutine
    def _post(self, api_method, args):
        url = self._get_api_url(api_method)
        content_type, stream = util.generate_multipart_formdata(args.items())

        link = httpclient.AsyncHTTPClient()
        request = httpclient.HTTPRequest(url, method='POST', headers={
            'Content-Type': content_type,
        }, body_producer=stream, request_timeout=0.0)
        response = yield link.fetch(request)

        raise gen.Return(self._parse_response(response))


class _DispatcherMixin(object):
    def __init__(self, *args, **kwargs):
        super(_DispatcherMixin, self).__init__()

    @gen.coroutine
    def on_text(self, message):
        pass

    @gen.coroutine
    def on_audio(self, message):
        pass

    @gen.coroutine
    def on_document(self, message):
        pass

    @gen.coroutine
    def on_photo(self, message):
        pass

    @gen.coroutine
    def on_sticker(self, message):
        pass

    @gen.coroutine
    def on_video(self, message):
        pass

    @gen.coroutine
    def on_contact(self, message):
        pass

    @gen.coroutine
    def on_location(self, message):
        pass

    @gen.coroutine
    def on_new_chat_participant(self, message):
        pass

    @gen.coroutine
    def on_left_chat_participant(self, message):
        pass

    @gen.coroutine
    def on_new_chat_title(self, message):
        pass

    @gen.coroutine
    def on_new_chat_photo(self, message):
        pass

    @gen.coroutine
    def on_delete_chat_photo(self, message):
        pass

    @gen.coroutine
    def on_group_chat_created(self, message):
        pass

    @gen.coroutine
    def on_callback(self, callback):
        pass

    @gen.coroutine
    def _receive_message(self, message):
        if message.text is not None:
            yield self.on_text(message)
        elif message.audio is not None:
            yield self.on_audio(message)
        elif message.document is not None:
            yield self.on_document(message)
        elif message.photo is not None:
            yield self.on_photo(message)
        elif message.sticker is not None:
            yield self.on_sticker(message)
        elif message.video is not None:
            yield self.on_video(message)
        elif message.contact is not None:
            yield self.on_contact(message)
        elif message.location is not None:
            yield self.on_location(message)
        elif message.new_chat_participant is not None:
            yield self.on_new_chat_participant(message)
        elif message.left_chat_participant is not None:
            yield self.on_left_chat_participant(message)
        elif message.new_chat_title is not None:
            yield self.on_new_chat_title(message)
        elif message.new_chat_photo is not None:
            yield self.on_new_chat_photo(message)
        elif message.delete_chat_photo is not None:
            yield self.on_delete_chat_photo(message)
        elif message.group_chat_created is not None:
            yield self.on_group_chat_created(message)
        elif message.voice is not None:
            pass
        else:
            raise TeleError('unknown message type')

    @gen.coroutine
    def _receive_callback(self, callback):
        yield self.on_callback(callback)


class TeleLich(_DispatcherMixin):
    def __init__(self, api_token):
        self._api = TeleZombie(api_token)

    @property
    def zombie(self):
        return self._api

    @gen.coroutine
    def get_updates(self, timeout=0):
        offset = 0
        updates = []
        while True:
            us = yield self._api.get_updates(offset, timeout=timeout)
            updates.extend(us)
            if not us:
                break
            offset = us[-1].update_id + 1
        raise gen.Return(updates)

    @gen.coroutine
    def get_me(self):
        raise gen.Return((yield self._api.get_me()))

    @gen.coroutine
    def answer_callback_query(self, callback_query_id, text=None, show_alert=None, url=None, cache_time=None):
        raise gen.Return((yield self._api.answer_callback_query(callback_query_id, text, show_alert, url, cache_time)))

    @gen.coroutine
    def edit_message_text(self, text, chat_id=None, message_id=None, inline_message_id=None, parse_mode=None,
                          disable_web_page_preview=None, reply_markup=None):
        raise gen.Return((yield self._api.edit_message_text(text, chat_id, message_id, inline_message_id, parse_mode,
                                                            disable_web_page_preview, reply_markup)))

    @gen.coroutine
    def edit_message_caption(self, caption, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        raise gen.Return((yield self._api.edit_message_caption(caption, chat_id, message_id, inline_message_id,
                                                               reply_markup)))

    @gen.coroutine
    def edit_message_reply_markup(self, chat_id=None, message_id=None, inline_message_id=None,
                                  reply_markup=None):
        raise gen.Return((yield self._api.edit_message_reply_markup(chat_id, message_id, inline_message_id,
                                                                    reply_markup)))

    @gen.coroutine
    def send_message(self, chat_id, text, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None):
        raise gen.Return(
            (yield self._api.send_message(chat_id, text, disable_web_page_preview, reply_to_message_id, reply_markup)))

    @gen.coroutine
    def forward_message(self, chat_id, from_chat_id, message_id):
        raise gen.Return((yield self._api.forward_message(chat_id, from_chat_id, message_id)))

    @gen.coroutine
    def send_photo(self, chat_id, photo, caption=None, reply_to_message_id=None, reply_markup=None):
        raise gen.Return((yield self._api.send_photo(chat_id, photo, caption, reply_to_message_id, reply_markup)))

    @gen.coroutine
    def send_audio(self, chat_id, audio, reply_to_message_id=None, reply_markup=None):
        raise gen.Return((yield self._api.send_audio(chat_id, audio, reply_to_message_id, reply_markup)))

    @gen.coroutine
    def send_document(self, chat_id, document, reply_to_message_id=None, reply_markup=None):
        raise gen.Return((yield self._api.send_document(chat_id, document, reply_to_message_id, reply_markup)))

    @gen.coroutine
    def send_sticker(self, chat_id, sticker, reply_to_message_id=None, reply_markup=None):
        raise gen.Return((yield self._api.send_sticker(chat_id, sticker, reply_to_message_id, reply_markup)))

    @gen.coroutine
    def send_video(self, chat_id, video, reply_to_message_id=None, reply_markup=None):
        raise gen.Return((yield self._api.send_video(chat_id, video, reply_to_message_id, reply_markup)))

    @gen.coroutine
    def send_location(self, chat_id, latitude, longitude, reply_to_message_id=None, reply_markup=None):
        raise gen.Return(
            (yield self._api.send_location(chat_id, latitude, longitude, reply_to_message_id, reply_markup)))

    @gen.coroutine
    def send_chat_action(self, chat_id, action):
        raise gen.Return((yield self._api.send_chat_action(chat_id, action)))

    @gen.coroutine
    def get_user_profile_photos(self, user_id):
        offset = 0
        photos = []
        total = 0
        while True:
            ps = yield self._api.get_user_profile_photos(user_id, offset)
            total = ps.total_count
            photos.extend(ps.photos)
            if not ps:
                break
            offset = ps[-1][-1].file_id + 1

        raise gen.Return(types.UserProfilePhotos({
            'total_count': total,
            'photos': photos,
        }))

    @gen.coroutine
    def poll(self, timeout=1):
        # remove previous webhook first
        yield self._api.set_webhook()
        # forever
        while True:
            try:
                updates = yield self.get_updates(timeout)
                for u in updates:
                    yield self._receive_message(u.message)
            except httpclient.HTTPError as e:
                if e.code != 599:
                    raise

    @gen.coroutine
    def listen(self, hook_url):
        yield self._api.set_webhook(url=hook_url)

    @gen.coroutine
    def close(self):
        # remove webhook
        yield self._api.set_webhook()


class TeleHookHandler(web.RequestHandler, _DispatcherMixin):
    @gen.coroutine
    def post(self):
        data = self.request.body
        data = data.decode('utf-8')
        data = json.loads(data)
        if 'message' in data:
            update = types.Update(data)
            yield self._receive_message(update.message)
        elif 'callback_query' in data:
            callback = types.CallbackQuery(data['callback_query'])
            yield self._receive_callback(callback)


class TeleError(Exception):
    def __init__(self, description):
        self.description = description

    def __str__(self):
        return self.description
