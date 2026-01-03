import asyncio
import contextlib
import math
import os
import shlex
import shutil
import time

from pyrogram.types import Message

from Pbxbot.core import Config, Symbols
from .formatter import humanbytes, readable_time


# ===================== PROGRESS =====================

async def progress(
    current: int, total: int, message: Message, start: float, process: str
):
    now = time.time()
    diff = now - start
    if diff <= 0:
        diff = 1

    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total if total else 0
        speed = current / diff if diff else 0
        elapsed_time = round(diff) * 1000
        complete_time = (
            round((total - current) / speed) * 1000 if speed > 0 else 0
        )
        estimated_total_time = elapsed_time + complete_time

        progress_str = "**[{0}{1}] : {2}%\n**".format(
            "".join(["●" for _ in range(math.floor(percentage / 10))]),
            "".join(["○" for _ in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2),
        )

        msg = (
            progress_str
            + "__{0}__ **𝗈𝖿** __{1}__\n"
              "**𝖲𝗉𝖾𝖾𝖽:** __{2}/s__\n"
              "**𝖤𝖳𝖠:** __{3}__".format(
                humanbytes(current),
                humanbytes(total),
                humanbytes(speed),
                readable_time(estimated_total_time / 1000),
            )
        )

        await message.edit_text(f"**{process} ...**\n\n{msg}")


# ===================== FILE UTILS =====================

async def get_files_from_directory(directory: str) -> list:
    all_files = []
    for path, _, files in os.walk(directory):
        for file in files:
            all_files.append(os.path.join(path, file))
    return all_files


# ===================== RUN CMD =====================

async def runcmd(cmd: str) -> tuple[str, str, int, int]:
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


# ===================== ENV UPDATE =====================

async def update_dotenv(key: str, value: str) -> None:
    if not os.path.exists(".env"):
        return

    with open(".env", "r") as file:
        data = file.readlines()

    updated = False
    for index, line in enumerate(data):
        if line.startswith(f"{key}="):
            data[index] = f"{key}={value}\n"
            updated = True
            break

    if not updated:
        data.append(f"{key}={value}\n")

    with open(".env", "w") as file:
        file.writelines(data)


# ===================== RESTART =====================

async def restart(
    update: bool = False,
    clean_up: bool = False,
    shutdown: bool = False,
):
    # cleanup temp folders
    for folder in (Config.DWL_DIR, Config.TEMP_DIR):
        with contextlib.suppress(Exception):
            shutil.rmtree(folder)

    if clean_up:
        os.makedirs(Config.DWL_DIR, exist_ok=True)
        os.makedirs(Config.TEMP_DIR, exist_ok=True)
        return

    if shutdown:
        os._exit(0)

    # ❌ git pull REMOVED (cloud safe)
    cmd = "bash start.sh"

    os.execvp("bash", ["bash", "-c", cmd])


# ===================== GIT STUBS (SAFE) =====================

async def gen_changelogs(*args, **kwargs) -> str:
    # git disabled on cloud platforms
    return f"**{Symbols.triangle_right} Updates disabled on this platform**"


async def initialize_git(*args, **kwargs):
    # git intentionally disabled (Choreo / Heroku safe)
    return True, None, False
