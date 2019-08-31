import json
from datetime import datetime
from typing import Optional

import ujson
from guillotina import configure
from guillotina.interfaces import IResponse
from guillotina.interfaces.security import PermissionSetting
from guillotina.profile import profilable
from guillotina.response import RawResponse

from zope.interface.interface import InterfaceClass


class GuillotinaJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, complex):
            return [obj.real, obj.imag]
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, type):
            return obj.__module__ + '.' + obj.__name__
        elif isinstance(obj, InterfaceClass):
            return [x.__module__ + '.' + x.__name__ for x in obj.__iro__]  # noqa
        try:
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)

        if isinstance(obj, PermissionSetting):
            return obj.get_name()
        if callable(obj):
            return obj.__module__ + '.' + obj.__name__
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class Renderer:
    content_type: str

    def __init__(self, view, request):
        self.view = view
        self.request = request

    def get_body(self, value) -> Optional[bytes]:
        return str(value).encode('utf-8')

    @profilable
    async def __call__(self, value) -> IResponse:
        '''
        Value can be:
        - Guillotina response object
        - serializable value
        '''
        if not IResponse.providedBy(value):
            body = self.get_body(value)
            resp = RawResponse(content=body)
        else:
            resp = value

        resp.headers.update({
            'Content-Type': self.content_type
        })

        return resp


@configure.renderer(name='application/json')
@configure.renderer(name='*/*')
class RendererJson(Renderer):
    content_type = 'application/json'

    def get_body(self, value) -> Optional[bytes]:
        if value is not None:
            value = json.dumps(value, cls=GuillotinaJSONEncoder)
            return value.encode('utf-8')
        return None


class StringRenderer(Renderer):
    content_type = 'text/plain'

    def get_body(self, value) -> bytes:
        if not isinstance(value, bytes):
            if not isinstance(value, str):
                value = ujson.dumps(value)
            value = value.encode('utf8')
        return value


@configure.renderer(name='text/html')
@configure.renderer(name='text/*')
class RendererHtml(Renderer):
    content_type = 'text/html'

    def get_body(self, value: IResponse) -> Optional[bytes]:
        body = super().get_body(value)
        if body is not None:
            if b'<html' not in body:
                body = b'<html><body>' + body + b'</body></html>'
        return body


@configure.renderer(name='text/plain')
class RendererPlain(StringRenderer):
    content_type = 'text/plain'
