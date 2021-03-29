from typing import Any, List, Optional, Union

from .mixins import Hashable
from discord import Member, Guild, role
from discord.abc import User

class Attachment:
    id: Any = ...
    size: Any = ...
    height: Any = ...
    width: Any = ...
    filename: Any = ...
    url: Any = ...
    proxy_url: Any = ...
    def __init__(self, data: Any, state: Any) -> None: ...
    def is_spoiler(self): ...
    async def save(self, fp: Any, *, seek_begin: bool = ..., use_cached: bool = ...): ...
    async def read(self, *, use_cached: bool = ...): ...
    async def to_file(self, *, use_cached: bool = ..., spoiler: bool = ...): ...

class DeletedReferencedMessage:
    def __init__(self, parent: Any) -> None: ...
    @property
    def id(self): ...
    @property
    def channel_id(self): ...
    @property
    def guild_id(self): ...

class MessageReference:
    resolved: Any = ...
    message_id: Any = ...
    channel_id: Any = ...
    guild_id: Any = ...
    def __init__(self, message_id: Any, channel_id: Any, *, guild_id: Optional[Any] = ...) -> None: ...
    @classmethod
    def with_state(cls, state: Any, data: Any): ...
    @classmethod
    def from_message(cls, message: Any): ...
    @property
    def cached_message(self): ...
    def to_dict(self): ...
    to_message_reference_dict: Any = ...

class Message(Hashable):
    id: int
    
    @property
    def mentions(self) -> List[User]: ...

    @property
    def author(self) -> Union[User, Member]: ...

    @property
    def content(self) -> str: ...

    @property
    def guild(self) -> Optional[Guild]: ...

    webhook_id: Any = ...
    reactions: Any = ...
    attachments: Any = ...
    embeds: Any = ...
    application: Any = ...
    activity: Any = ...
    channel: Any = ...
    type: Any = ...
    pinned: Any = ...
    flags: Any = ...
    mention_everyone: Any = ...
    tts: Any = ...
    nonce: Any = ...
    stickers: Any = ...
    reference: Any = ...
    def __init__(self, state: Any, channel: Any, data: Any) -> None: ...
    def raw_mentions(self): ...
    def raw_channel_mentions(self): ...
    def raw_role_mentions(self): ...
    def channel_mentions(self): ...
    def clean_content(self): ...
    @property
    def created_at(self): ...
    @property
    def edited_at(self): ...
    @property
    def jump_url(self): ...
    def is_system(self): ...
    def system_content(self): ...
    async def delete(self, *, delay: Optional[Any] = ...) -> None: ...
    async def edit(self, **fields: Any) -> None: ...
    async def publish(self) -> None: ...
    async def pin(self, *, reason: Optional[Any] = ...) -> None: ...
    async def unpin(self, *, reason: Optional[Any] = ...) -> None: ...
    async def add_reaction(self, emoji: Any) -> None: ...
    async def remove_reaction(self, emoji: Any, member: Any) -> None: ...
    async def clear_reaction(self, emoji: Any) -> None: ...
    async def clear_reactions(self) -> None: ...
    async def ack(self): ...
    async def reply(self, content: Optional[Any] = ..., **kwargs: Any): ...
    def to_reference(self): ...
    def to_message_reference_dict(self): ...

class PartialMessage(Hashable):
    channel: Any = ...
    id: Any = ...
    def __init__(self, channel: Any, id: Any) -> None: ...
    pinned: Any = ...
    @property
    def created_at(self): ...
    def guild(self): ...
    async def fetch(self): ...
