from api.command import Section, ContextExecute
import api.context as context
from message.kook.card import Card, CardList
import message.kook.card.module as modules
import message.kook.card.element as elements

_reply = lambda c, content: c.bot.send_message(target_id=c.channel_id, content=content)

_reply_func = lambda content: lambda c: _reply(c=c, content=content)


async def _add_candidate(c: ContextExecute):
    context.program.db.insert(
        "candidate",
        {"name": c.params[1], "url": c.params[2], "description": c.params[3]},
    )
    await _reply(c, "添加成功")


async def _show_candidates(c: ContextExecute):
    candidates = context.program.db.select("candidate")
    await c.bot.send_message(
        target_id=c.channel_id,
        type=10,
        content=CardList(
            [
                Card().append_module(
                    modules.Section(
                        elements.KMarkdown(
                            f"名称：{candidate["name"]} 链接：{candidate["url"]} 描述：{candidate["description"]}"
                        )
                    )
                )
                for candidate in candidates
            ]
        ).to_str(),
    )


root = (
    Section("root")
    .usage_supplier(lambda c: "错误的用法")
    .append(
        Section("添加待选")
        .usage_supplier(lambda c: "用法：添加待选 名称 链接 描述")
        .append(Section().append(Section().append(Section().executor(_add_candidate))))
        .append(Section("test").executor(_reply_func("hi")))
    )
    .append(
        Section("查看待选")
        .usage_supplier(lambda c: "用法：查看待选")
        .executor(_show_candidates)
    )
)
