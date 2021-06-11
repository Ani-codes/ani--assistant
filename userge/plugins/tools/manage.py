""" manage your userge :) """

# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.

import os

from userge import Config, Message, userge
from userge.plugins import ROOT
from userge.utils import get_import_path





@userge.on_cmd(
    "enable",
    about={
        "header": "enable plugins, commands, filters",
        "flags": {"-p": "plugin", "-c": "command", "-f": "filter"},
        "usage": "{tr}enable [flags] [name | names]",
        "examples": ["{tr}enable -p gdrive", "{tr}enable -c gls gup"],
    },
    del_pre=True,
    allow_channels=False,
)
async def enable(message: Message) -> None:
    """enable plugins, commands, filters"""
    if not message.flags:
        await message.err("flag required!")
        return
    if not message.filtered_input_str:
        await message.err("name required!")
        return
    await message.edit("`Enabling...`")
    names_ = message.filtered_input_str.split(" ")
    type_ = list(message.flags)
    if "p" in type_:
        found = set(names_).intersection(set(userge.manager.plugins))
        if found:
            out = await userge.manager.enable_plugins(list(found))
            if out:
                out_str = "**--Enabled Plugin(s)--**\n\n"
                for plg_name, cmds in out.items():
                    out_str += f"**{plg_name}** : `{'`,    `'.join(cmds)}`\n"
            else:
                out_str = f"already enabled! : `{'`,    `'.join(names_)}`"
        else:
            await message.err(f"plugins : {', '.join(names_)} not found!")
            return
    elif "c" in type_:
        for t_name in names_:
            if not t_name.startswith(Config.CMD_TRIGGER):
                names_.append(Config.CMD_TRIGGER + t_name)
        found = set(names_).intersection(set(userge.manager.commands))
        if found:
            out = await userge.manager.enable_commands(list(found))
            if out:
                out_str = "**--Enabled Command(s)--**\n\n"
                out_str += f"`{'`,    `'.join(out)}`"
            else:
                out_str = f"already enabled! : `{'`,    `'.join(names_)}`"
        else:
            await message.err(f"commands : {', '.join(names_)} not found!")
            return
    elif "f" in type_:
        found = set(names_).intersection(set(userge.manager.filters))
        if found:
            out = await userge.manager.enable_filters(list(found))
            if out:
                out_str = "**--Enabled Filter(s)--**\n\n"
                out_str += f"`{'`,    `'.join(out)}`"
            else:
                out_str = f"already enabled! : `{'`,    `'.join(names_)}`"
        else:
            await message.err(f"filters : {', '.join(names_)} not found!")
            return
    else:
        await message.err("invalid input flag!")
        return
    await message.edit(out_str, del_in=0, log=__name__)


@userge.on_cmd(
    "disable",
    about={
        "header": "disable plugins, commands, filters",
        "flags": {"-p": "plugin", "-c": "command", "-f": "filter"},
        "usage": "{tr}disable [flags] [name | names]",
        "examples": ["{tr}disable -p gdrive", "{tr}disable -c gls gup"],
    },
    del_pre=True,
    allow_channels=False,
)
async def disable(message: Message) -> None:
    """disable plugins, commands, filters"""
    if not message.flags:
        await message.err("flag required!")
        return
    if not message.filtered_input_str:
        await message.err("name required!")
        return
    await message.edit("`Disabling...`")
    names_ = message.filtered_input_str.split(" ")
    type_ = list(message.flags)
    if "p" in type_ and names_:
        found = set(names_).intersection(set(userge.manager.plugins))
        if found:
            out = await userge.manager.disable_plugins(list(found))
            if out:
                out_str = "**--Disabled Plugin(s)--**\n\n"
                for plg_name, cmds in out.items():
                    out_str += f"**{plg_name}** : `{'`,    `'.join(cmds)}`\n"
            else:
                out_str = f"already disabled! : `{'`,    `'.join(names_)}`"
        else:
            await message.err(f"plugins : {', '.join(names_)} not found!")
            return
    elif "c" in type_ and names_:
        for t_name in names_:
            if not t_name.startswith(Config.CMD_TRIGGER):
                names_.append(Config.CMD_TRIGGER + t_name)
        found = set(names_).intersection(set(userge.manager.commands))
        if found:
            out = await userge.manager.disable_commands(list(found))
            if out:
                out_str = "**--Disabled Command(s)--**\n\n"
                out_str += f"`{'`,    `'.join(out)}`"
            else:
                out_str = f"already disabled! : `{'`,    `'.join(names_)}`"
        else:
            await message.err(f"commands : {', '.join(names_)} not found!")
            return
    elif "f" in type_ and names_:
        found = set(names_).intersection(set(userge.manager.filters))
        if found:
            out = await userge.manager.disable_filters(list(found))
            if out:
                out_str = "**--Disabled Filter(s)--**\n\n"
                out_str += f"`{'`,    `'.join(out)}`"
            else:
                out_str = f"already disabled! : `{'`,    `'.join(names_)}`"
        else:
            await message.err(f"filters : {', '.join(names_)} not found!")
            return
    else:
        await message.err("invalid input flag!")
        return
    await message.edit(out_str, del_in=0, log=__name__)


@userge.on_cmd(
    "load",
    about={
        "header": "load plugins, commands, filters",
        "flags": {"-p": "plugin", "-c": "command", "-f": "filter"},
        "usage": "{tr}load [reply to plugin] to load from file\n"
        "{tr}load [flags] [name | names]",
        "examples": ["{tr}load -p gdrive", "{tr}load -c gls gup"],
    },
    del_pre=True,
    allow_channels=False,
)
async def load(message: Message) -> None:
    """load plugins, commands, filters"""
    if message.flags:
        if not message.filtered_input_str:
            await message.err("name required!")
            return
        await message.edit("`Loading...`")
        names_ = message.filtered_input_str.split(" ")
        type_ = list(message.flags)
        if "p" in type_:
            found = set(names_).intersection(set(userge.manager.plugins))
            if found:
                out = await userge.manager.load_plugins(list(found))
                if out:
                    out_str = "**--Loaded Plugin(s)--**\n\n"
                    for plg_name, cmds in out.items():
                        out_str += f"**{plg_name}** : `{'`,    `'.join(cmds)}`\n"
                else:
                    out_str = f"already loaded! : `{'`,    `'.join(names_)}`"
            else:
                await message.err(f"plugins : {', '.join(names_)} not found!")
                return
        elif "c" in type_:
            for t_name in names_:
                if not t_name.startswith(Config.CMD_TRIGGER):
                    names_.append(Config.CMD_TRIGGER + t_name)
            found = set(names_).intersection(set(userge.manager.commands))
            if found:
                out = await userge.manager.load_commands(list(found))
                if out:
                    out_str = "**--Loaded Command(s)--**\n\n"
                    out_str += f"`{'`,    `'.join(out)}`"
                else:
                    out_str = f"already loaded! : `{'`,    `'.join(names_)}`"
            else:
                await message.err(f"commands : {', '.join(names_)} not found!")
                return
        elif "f" in type_:
            found = set(names_).intersection(set(userge.manager.filters))
            if found:
                out = await userge.manager.load_filters(list(found))
                if out:
                    out_str = "**--Loaded Filter(s)--**\n\n"
                    out_str += f"`{'`,    `'.join(out)}`"
                else:
                    out_str = f"already loaded! : `{'`,    `'.join(names_)}`"
            else:
                await message.err(f"filters : {', '.join(names_)} not found!")
                return
        else:
            await message.err("invalid input flag!")
            return
        await message.edit(out_str, del_in=0, log=__name__)
    else:
        await message.edit("`Loading...`")
        replied = message.reply_to_message
        if replied and replied.document:
            file_ = replied.document
            if file_.file_name.endswith(".py") and file_.file_size < 2 ** 20:
                if not os.path.isdir(Config.TMP_PATH):
                    os.makedirs(Config.TMP_PATH)
                t_path = os.path.join(Config.TMP_PATH, file_.file_name)
                if os.path.isfile(t_path):
                    os.remove(t_path)
                await replied.download(file_name=t_path)
                plugin = get_import_path(ROOT, t_path)
                try:
                    await userge.load_plugin(plugin, reload_plugin=True)
                    await userge.finalize_load()
                except (ImportError, SyntaxError, NameError) as i_e:
                    os.remove(t_path)
                    await message.err(i_e)
                else:
                    await message.edit(f"`Loaded {plugin}`", del_in=3, log=__name__)
            else:
                await message.edit("`Plugin Not Found`")
        else:
            await message.edit(f"pls check `{Config.CMD_TRIGGER}help load` !")


@userge.on_cmd(
    "unload",
    about={
        "header": "unload plugins, commands, filters",
        "flags": {"-p": "plugin", "-c": "command", "-f": "filter"},
        "usage": "{tr}unload [flags] [name | names]",
        "examples": ["{tr}unload -p gdrive", "{tr}unload -c gls gup"],
    },
    del_pre=True,
    allow_channels=False,
)
async def unload(message: Message) -> None:
    """unload plugins, commands, filters"""
    if not message.flags:
        await message.err("flag required!")
        return
    if not message.filtered_input_str:
        await message.err("name required!")
        return
    await message.edit("`UnLoading...`")
    names_ = message.filtered_input_str.split(" ")
    type_ = list(message.flags)
    if "p" in type_ and names_:
        found = set(names_).intersection(set(userge.manager.plugins))
        if found:
            out = await userge.manager.unload_plugins(list(found))
            if out:
                out_str = "**--Unloaded Plugin(s)--**\n\n"
                for plg_name, cmds in out.items():
                    out_str += f"**{plg_name}** : `{'`,    `'.join(cmds)}`\n"
            else:
                out_str = f"already unloaded! : `{'`,    `'.join(names_)}`"
        else:
            await message.err(f"plugins : {', '.join(names_)} not found!")
            return
    elif "c" in type_ and names_:
        for t_name in names_:
            if not t_name.startswith(Config.CMD_TRIGGER):
                names_.append(Config.CMD_TRIGGER + t_name)
        found = set(names_).intersection(set(userge.manager.commands))
        if found:
            out = await userge.manager.unload_commands(list(found))
            if out:
                out_str = "**--Unloaded Command(s)--**\n\n"
                out_str += f"`{'`,    `'.join(out)}`"
            else:
                out_str = f"already unloaded! : `{'`,    `'.join(names_)}`"
        else:
            await message.err(f"commands : {', '.join(names_)} not found!")
            return
    elif "f" in type_ and names_:
        found = set(names_).intersection(set(userge.manager.filters))
        if found:
            out = await userge.manager.unload_filters(list(found))
            if out:
                out_str = "**--Unloaded Filter(s)--**\n\n"
                out_str += f"`{'`,    `'.join(out)}`"
            else:
                out_str = f"already unloaded! : `{'`,    `'.join(names_)}`"
        else:
            await message.err(f"filters : {', '.join(names_)} not found!")
            return
    else:
        await message.err("invalid input flag!")
        return
    await message.edit(out_str, del_in=0, log=__name__)


@userge.on_cmd("reload", about={"header": "Reload all plugins"}, allow_channels=False)
async def reload_(message: Message) -> None:
    """Reload all plugins"""
    await message.edit("`Reloading All Plugins`")
    await message.edit(
        f"`Reloaded {await userge.reload_plugins()} Plugins`", del_in=3, log=__name__
    )


@userge.on_cmd(
    "clear", about={"header": "clear all save filters in DB"}, allow_channels=False
)
async def clear_(message: Message) -> None:
    """clear all save filters in DB"""
    await message.edit("`Clearing DB...`")
    await message.edit(
        f"**Cleared Filters** : `{await userge.manager.clear()}`",
        del_in=3,
        log=__name__,
    )
