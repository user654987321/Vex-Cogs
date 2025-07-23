from datetime import datetime
from typing import TYPE_CHECKING

from redbot.core.commands import BadArgument, Context, Converter

from .vexutils import get_vex_logger

log = get_vex_logger(__name__)

if TYPE_CHECKING:
    BirthdayConverter = datetime
    TimeConverter = datetime
else:

    class BirthdayConverter(Converter):
        async def convert(self, ctx: Context, argument: str) -> datetime:
            log.trace("attempting to parse birthday: %s", argument)
            try:
                parts = argument.strip().split(".")
                if len(parts) == 2:
                    # Format: dd.mm
                    day, month = map(int, parts)
                    result = datetime(year=1, month=month, day=day)
                elif len(parts) == 3:
                    # Format: dd.mm.yyyy
                    result = datetime.strptime(argument, "%d.%m.%Y")
                else:
                    raise ValueError

                log.trace("parsed birthday: %s", result)
                return result.replace(hour=0, minute=0, second=0, microsecond=0)

            except ValueError:
                raise BadArgument(
                    "Ungültiges Datum. Bitte nutze das Format `TT.MM` oder `TT.MM.JJJJ`."
                )

    class TimeConverter(Converter):
        async def convert(self, ctx: Context, argument: str) -> datetime:
            log.trace("attempting to parse time: %s", argument)
            try:
                if argument.count(":") == 1:
                    # Format: HH:MM
                    result = datetime.strptime(argument, "%H:%M")
                elif argument.count(":") == 2:
                    # Format: HH:MM:SS
                    result = datetime.strptime(argument, "%H:%M:%S")
                else:
                    raise ValueError

                result = result.replace(year=1, month=1, day=1)
                log.trace("parsed time: %s", result)
                return result

            except ValueError:
                raise BadArgument(
                    "Ungültige Zeit. Bitte nutze das 24h-Format: `HH:MM` oder `HH:MM:SS`."
                )
