# from .admin_commands import
# from .clan_commands import
from .auth.auth_discord import auth_group
from .user_commands.user_commands import user_group

base_router = (user_group,)
