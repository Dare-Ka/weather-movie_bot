from random import choice

from aiogram import Router
from aiogram.types import MessageReactionUpdated, Message, ReactionTypeEmoji

from events.reactions.text import reactions, answer_emoji

router = Router(name=__name__)


@router.message()
async def set_reaction(message: Message) -> None:
    await message.react(reaction=[ReactionTypeEmoji(emoji=choice(reactions))])


@router.message_reaction()
async def reactions_handler(reaction: MessageReactionUpdated) -> None:
    emoji = reaction.new_reaction
    if len(emoji) != 0:
        await reaction.bot.send_message(
            chat_id=reaction.chat.id, text=choice(answer_emoji)
        )

