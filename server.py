#!/usr/bin/python3

import cherrypy
import json

import answers
from people import users_map, api_keys

cherrypy.config.update({'server.socket_port': 5050,})
cherrypy.config.update({'request.show_tracebacks': False})


use_led = False
if use_led:
    import controller
    serial_connector = controller.SerialConnector()


class TaskServer(object):
    def _cp_dispatch(self, vpath):
        cherrypy.request.params['login'] = vpath.pop(0)
        if len(vpath) == 0:
            return self

        return self

    @cherrypy.expose
    def index(self, login=None):
        if login is None:
            raise cherrypy.HTTPError(404)
        return 'Generic help for {}'.format(login)

    @cherrypy.expose
    def github(self, login, **kwargs):
        return GithubTask.handle(login, **kwargs)

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def krs(self, login, **kwargs):
        return KrsTask.handle(login, **kwargs)

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def wiki(self, login, **kwargs):
        return WikiTask.handle(login, **kwargs)



class Task(object):
    color = '000000'
    password = None
    previous = None

    @classmethod
    def handle(cls, login, **kwargs):
        cls.check_login(login)
        cls.verify_secret(login, **kwargs)
        cls.verify_previous(login, **kwargs)
        if cls.verify_success(login, **kwargs):
            cls.do_lamp(login)
            return cls.output_success()
        else:
            return cls.output_failure()

    @classmethod
    def verify_success(cls, login, **kwargs):
        raise NotImplemented()

    @classmethod
    def check_login(cls, login):
        if login not in users_map:
            raise cherrypy.HTTPError(404)

    @classmethod
    def verify_secret(cls, login, **kwargs):
        if 'api_key' not in kwargs:
            raise cherrypy.HTTPError(403)
        if not api_keys[login] == kwargs['api_key']:
            raise cherrypy.HTTPError(403)

    @classmethod
    def verify_previous(cls, login, **kwargs):
        body = cherrypy.request.json
        if not cls.previous:
            return
        if 'prev' not in body:
            raise cherrypy.HTTPError(403)
        if cls.previous.password != body['prev']:
            raise cherrypy.HTTPError(403)

    @classmethod
    def do_lamp(cls, login):
        if use_led:
            serial_connector.set_hex_color(users_map[login], cls.color)

    @classmethod
    def output_success(cls):
        result = {'result': 'Success', 'info': 'Gratulacje!'}
        if cls.password:
            result['password'] = cls.password
        return json.dumps(result)

    @classmethod
    def output_failure(cls):
        return json.dumps({'result': 'Failure', 'info': 'Nie udało się'})


class GithubTask(Task):
    color = '00ff00'

    @classmethod
    def verify_success(cls, login, **kwargs):
        return True


class KrsTask(Task):
    color = 'ff0000'
    password = 'wybitnie_trudny_klucz'

    @classmethod
    def verify_success(cls, login, **kwargs):
        body = cherrypy.request.json
        if 'postal' not in body or body['postal'] != answers.postal:
            return False
        return True


class WikiTask(Task):
    color = '0000ff'
    previous = KrsTask

    @classmethod
    def verify_success(cls, login, **kwargs):
        body = cherrypy.request.json
        print(body)
        if 'battle_url' not in body or body['battle_url'] != answers.battle_url:
            return False
        return True


if __name__ == '__main__':
    cherrypy.quickstart(TaskServer())

