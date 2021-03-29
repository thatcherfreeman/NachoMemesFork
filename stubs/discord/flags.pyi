from typing import Any

class flag_value:
    flag: Any = ...
    __doc__: Any = ...
    def __init__(self, func: Any) -> None: ...
    def __get__(self, instance: Any, owner: Any): ...
    def __set__(self, instance: Any, value: Any) -> None: ...

class alias_flag_value(flag_value): ...

class BaseFlags:
    value: Any = ...
    def __init__(self, **kwargs: Any) -> None: ...
    def __eq__(self, other: Any) -> Any: ...
    def __ne__(self, other: Any) -> Any: ...
    def __hash__(self) -> Any: ...
    def __iter__(self) -> Any: ...

class SystemChannelFlags(BaseFlags):
    def join_notifications(self): ...
    def premium_subscriptions(self): ...

class MessageFlags(BaseFlags):
    def crossposted(self): ...
    def is_crossposted(self): ...
    def suppress_embeds(self): ...
    def source_message_deleted(self): ...
    def urgent(self): ...

class PublicUserFlags(BaseFlags):
    def staff(self): ...
    def partner(self): ...
    def hypesquad(self): ...
    def bug_hunter(self): ...
    def hypesquad_bravery(self): ...
    def hypesquad_brilliance(self): ...
    def hypesquad_balance(self): ...
    def early_supporter(self): ...
    def team_user(self): ...
    def system(self): ...
    def bug_hunter_level_2(self): ...
    def verified_bot(self): ...
    def verified_bot_developer(self): ...
    def early_verified_bot_developer(self): ...
    def all(self): ...

class Intents(BaseFlags):
    value: Any = ...
    def __init__(self, **kwargs: Any) -> None: ...
    @classmethod
    def all(cls): ...
    @classmethod
    def none(cls): ...
    @classmethod
    def default(cls): ...
    def guilds(self): ...
    def members(self): ...
    def bans(self): ...
    def emojis(self): ...
    def integrations(self): ...
    def webhooks(self): ...
    def invites(self): ...
    def voice_states(self): ...
    def presences(self): ...
    def messages(self): ...
    def guild_messages(self): ...
    def dm_messages(self): ...
    def reactions(self): ...
    def guild_reactions(self): ...
    def dm_reactions(self): ...
    def typing(self): ...
    def guild_typing(self): ...
    def dm_typing(self): ...

class MemberCacheFlags(BaseFlags):
    value: Any = ...
    def __init__(self, **kwargs: Any) -> None: ...
    @classmethod
    def all(cls): ...
    @classmethod
    def none(cls): ...
    def online(self): ...
    def voice(self): ...
    def joined(self): ...
    @classmethod
    def from_intents(cls, intents: Any): ...
