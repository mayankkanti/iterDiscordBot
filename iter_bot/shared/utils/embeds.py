from datetime import datetime
from enum import Enum
from typing import Optional, Tuple
from discord import Embed, File


class EmbedColor(int, Enum):
    NORMAL = 0x6A1B9A
    INFORMATION = 0x546E7A
    WARNING = 0xE67E22
    ERROR = 0xE74C3C

class EmbedType(Enum):
    NORMAL = EmbedColor.NORMAL
    INFORMATION = EmbedColor.INFORMATION
    WARNING = EmbedColor.WARNING
    ERROR = EmbedColor.ERROR

async def get_embed(
    type: EmbedType, title: str, description: str, thumbnail_path: Optional[str] = None
    ) -> Tuple[Embed, Optional[File]]:
    embed = Embed(
        title=title,
        description=description,
        color=type.value.value,
        timestamp=datetime.now(),
    )
    file = File("static/iter_bot.png", filename="iter_bot.png")
    return embed, file