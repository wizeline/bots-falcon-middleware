from wizeline.falcon.errors.http import (
    BotHTTPInternalServerError,
    BotHTTPNotFound,
    BotHTTPConflict,
    BotHTTPBadRequest
)


class PlatformRepresentation:
    def to_dict(self, obj_type=dict):
        obj = super(PlatformRepresentation, self).to_dict(obj_type)

        if self.platform_name is not None:
            obj['platform_name'] = self.platform_name

        return obj


class NLPEngineError(BotHTTPInternalServerError):
    def __init__(self, message=None, **kwargs):
        super(NLPEngineError, self).__init__(
            code='NLPEngineError',
            message=message,
            **kwargs
        )


class BotDoesNotExist(BotHTTPNotFound):
    def __init__(self, message=None, **kwargs):
        super(BotDoesNotExist, self).__init__(
            code='BotDoesNotExist',
            message=message,
            **kwargs
        )


class BotAlreadyExists(BotHTTPConflict):
    def __init__(self, message=None, **kwargs):
        super(BotAlreadyExists, self).__init__(
            code='BotAlreadyExists',
            message=message,
            **kwargs
        )


class PlatformNotAvailable(PlatformRepresentation, BotHTTPConflict):
    def __init__(self, platform_name, message=None, **kwargs):
        super(PlatformNotAvailable, self).__init__(
            code='PlatformNotAvailable',
            message=message,
            **kwargs
        )
        self.platform_name = platform_name


class PlatformAlreadySet(PlatformRepresentation, BotHTTPConflict):
    def __init__(self, platform_name, message=None, **kwargs):
        super(PlatformAlreadySet, self).__init__(
            code='PlatformAlreadySet',
            message=message,
            **kwargs
        )
        self.platform_name = platform_name


class PlatformNotSupported(PlatformRepresentation, BotHTTPConflict):
    def __init__(self, platform_name, message=None, **kwargs):
        super(PlatformNotSupported, self).__init__(
            code='PlatformNotSupported',
            message=message,
            **kwargs
        )
        self.platform_name = platform_name


class BotTrainingError(BotHTTPBadRequest):
    def __init__(self, message=None, **kwargs):
        super(BotTrainingError, self).__init__(
            code='BotTrainingError',
            message=message,
            **kwargs
        )


class CanNotSendMessage(BotHTTPInternalServerError):
    def __init__(self, message=None, **kwargs):
        super(CanNotSendMessage, self).__init__(
            code='CanNotSendMessage',
            message=message,
            **kwargs
        )
