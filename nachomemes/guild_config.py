from dataclasses import dataclass
from typing import IO, List, Optional

from discord import Member, Role


@dataclass
class GuildConfig:
    """Stuff about the guild"""

    id: Optional[str]          # guild id
    name: str                  # guild name
    override: List[int]        # no bad-boy
    pariah: List[int]          # bad-boy timeout
    admin_role: Optional[int]  # guild role to administer the bot
    edit_role: Optional[int]   # guild role to edit templates

    def can_admin(self, member: Member) -> bool:
        return member.id in self.override or (member.id not in self.pariah and (member.guild_permissions.administrator or any(r for r in member.roles if r.id == self.admin_role)))

    def can_edit(self, member: Member) -> bool:
        return member.id in self.override or (member.id not in self.pariah and (member.guild_permissions.administrator or any(r for r in member.roles if r.id == self.edit_role)))

    def can_use(self, member: Member) -> bool:
        """Is the user a bad boy?"""
        return member.id in self.override or member.id not in self.pariah

    def set_admin_role(self, member: Member, role: Role=None) -> str:
        if not self.can_admin(member):
            return self.no_admin(member)
        self.admin_role = role.id
        return f"Members of '{role.name}' are now authorized to administer the memes."

    def set_edit_role(self, member: Member, role: Role) -> str:
        if not self.can_admin(member):
            return self.no_admin(member)
        self.edit_role = role.id
        return f"Members of '{role.name}' are now authorized to edit the memes."

    def shun(self, member: Member, victim: Member) -> str:
        if not self.can_admin(member):
            return self.no_admin(member)
        elif member == victim:
            self.pariah.append(victim.id)
            return "If that's what you really want to do."
        elif victim in self.override:
            self.pariah.append(member.id)
            return f"{self.member_nick(member)}. Your membership to The Continental has been, by thine own hand, revoked."
        elif not member.id in self.override and victim.guild_permissions.administrator:
            return "As fun as it sounds, it's probably not a good idea."
        else:
            self.pariah.append(victim.id)
            return f"{self.member_nick(victim)} is now excommunicado"

    def endorse(self, member: Member, victim: Member) -> str:
        if member == victim and victim in self.pariah and (member in self.override or member.guild_permissions.administrator):
            self.pariah.remove(victim.id)
            return "Wait, you can do that?"
        elif not self.can_admin(member):
            return self.no_admin(member)
        elif victim in self.pariah:
            self.pariah.remove(victim.id)
            return f"The contract on {self.member_nick(victim)} has been cancelled"
        else:
            return "/okay"

    def member_full_name(self, member: Member) -> str:
        return f"{member.nick} ({member.name}#{member.discriminator})" if member.nick else f"{member.name}#{member.discriminator}"

    def member_nick(self, member: Member) -> str:
        return f"{member.nick}" if member.nick else f"{member.name}"

    def no_admin(self, member: Member, action='administer', permission='admin') -> str:
        return f"Therapist: What do we do when we feel powerless and depressed?\n\n{self.member_nick(member)}: Try to {action} the bot without {permission} rights.\n\nTherapist: No."

    def no_memes(self, member: Member, action='administer', permission='admin') -> str:
        return "No memes for you!"
