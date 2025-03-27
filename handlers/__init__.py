async def register_commands_handlers() -> None:
    from handlers.commands import (  # noqa
        CommandStart,
    )


async def register_messages_handlers() -> None:
    from handlers.messages import (  # noqa
    handle_document,
    )


async def register_handlers() -> None:
    await register_commands_handlers()
    await register_messages_handlers()
