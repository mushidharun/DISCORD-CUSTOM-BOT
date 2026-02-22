# =========================================================
#  ZETRA DISCORD FIVEM BOT – COMMERCIAL EDITION
#
#  COPYRIGHT OWNER : MUSHI DHARUN (ZETRA)
#  PRICE : DM ME DIRECTLY OR CONTACT IN MY SERVER
#  SERVER : https://discord.gg/uxMjPz749k
#
#  This software is proprietary and confidential.
#  Unauthorized copying, modification, resale,
#  redistribution, or sharing is strictly prohibited.
#
#  Legal action may be taken for violations.
# =========================================================


import config

def is_owner(ctx_or_interaction):
    user = getattr(ctx_or_interaction, "author", None) or getattr(ctx_or_interaction, "user", None)
    return user and user.id == config.OWNER_ID


def has_any_role(ctx_or_interaction, role_ids):
    user = getattr(ctx_or_interaction, "author", None) or getattr(ctx_or_interaction, "user", None)

    if not user or not hasattr(user, "roles"):
        return False

    return any(role.id in role_ids for role in user.roles)


def is_management(ctx_or_interaction):
    return (
        is_owner(ctx_or_interaction) or
        has_any_role(ctx_or_interaction, [
            config.LEAD_ADMIN_ROLE,
            config.ADMIN_ROLE,
            config.MOD_ROLE,
            config.STAFF_ROLE
        ])
    )
