from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AudioChunk(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class AudioResponse(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class ServerRequest(_message.Message):
    __slots__ = ["mycheck"]
    MYCHECK_FIELD_NUMBER: _ClassVar[int]
    mycheck: str
    def __init__(self, mycheck: _Optional[str] = ...) -> None: ...

class ServerResponse(_message.Message):
    __slots__ = ["isonline"]
    ISONLINE_FIELD_NUMBER: _ClassVar[int]
    isonline: bool
    def __init__(self, isonline: bool = ...) -> None: ...
