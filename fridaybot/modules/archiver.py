"""
usage: reply with file : .rar , .7z  create archived file
unzip usage: reply with zipped file .unzipper
Coded by @furki
"""

import asyncio
import os
import shutil
import tarfile
import time
from datetime import datetime

import patoolib
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon.tl.types import DocumentAttributeVideo

from fridaybot import CMD_HELP
from fridaybot.Configs import Config as Var

from ..utils import admin_cmd, progress

thumb_image_path = Var.TEMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"
extracted = Var.TEMP_DOWNLOAD_DIRECTORY + "extracted/"
if not os.path.isdir(extracted):
    os.makedirs(extracted)


@borg.on(admin_cmd(pattern=("rar ?(.*)")))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    mone = await event.edit("Processing ...")
    if not os.path.isdir(Var.TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Var.TEMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:

            downloaded_file_name = await borg.download_media(
                reply_message, Var.TEMP_DOWNLOAD_DIRECTORY
            )
            directory_name = downloaded_file_name
            await event.edit("creating rar archive, please wait..")
            # patoolib.create_archive(directory_name + '.7z',directory_name)
            patoolib.create_archive(
                directory_name + ".rar", (directory_name, Var.TEMP_DOWNLOAD_DIRECTORY)
            )
            # patoolib.create_archive("/content/21.yy Avrupa (1).pdf.zip",("/content/21.yy Avrupa (1).pdf","/content/"))
            await borg.send_file(
                event.chat_id,
                directory_name + ".rar",
                caption="rarred By @VirtualUserbot",
                force_document=True,
                allow_cache=False,
                reply_to=event.message.id,
            )
            try:
                os.remove(directory_name + ".rar")
                os.remove(directory_name)
            except:
                pass
            await event.edit("Task Completed")
            await asyncio.sleep(3)
            await event.delete()
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
    elif input_str:
        directory_name = input_str

        await event.edit(
            "Local file compressed to `{}`".format(directory_name + ".rar")
        )


@borg.on(admin_cmd(pattern=("7z ?(.*)")))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    mone = await event.edit("Processing ...")
    if not os.path.isdir(Var.TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Var.TEMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:

            downloaded_file_name = await borg.download_media(
                reply_message, Var.TEMP_DOWNLOAD_DIRECTORY
            )
            directory_name = downloaded_file_name
            await event.edit("creating 7z archive, please wait..")
            # patoolib.create_archive(directory_name + '.7z',directory_name)
            patoolib.create_archive(
                directory_name + ".7z", (directory_name, Var.TEMP_DOWNLOAD_DIRECTORY)
            )
            # patoolib.create_archive("/content/21.yy Avrupa (1).pdf.zip",("/content/21.yy Avrupa (1).pdf","/content/"))
            await borg.send_file(
                event.chat_id,
                directory_name + ".7z",
                caption="7z archived By @VirtualUserbot",
                force_document=True,
                allow_cache=False,
                reply_to=event.message.id,
            )
            try:
                os.remove(directory_name + ".7z")
                os.remove(directory_name)
            except:
                pass
            await event.edit("Task Completed")
            await asyncio.sleep(3)
            await event.delete()
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
    elif input_str:
        directory_name = input_str

        await event.edit("Local file compressed to `{}`".format(directory_name + ".7z"))


@borg.on(admin_cmd(pattern=("tar ?(.*)")))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    mone = await event.edit("Processing ...")
    if not os.path.isdir(Var.TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Var.TEMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:

            downloaded_file_name = await borg.download_media(
                reply_message, Var.TEMP_DOWNLOAD_DIRECTORY
            )
            directory_name = downloaded_file_name
            await event.edit("Finish downloading to my local")
            to_upload_file = directory_name
            output = await create_archive(to_upload_file)
            is_zip = False
            if is_zip:
                check_if_file = await create_archive(to_upload_file)
                if check_if_file is not None:
                    to_upload_file = check_if_file
            await borg.send_file(
                event.chat_id,
                output,
                caption="TAR By @VirtualUserbot",
                force_document=True,
                allow_cache=False,
                reply_to=event.message.id,
            )
            try:
                os.remove(output)
                os.remove(output)
            except:
                pass
            await event.edit("Task Completed")
            await asyncio.sleep(3)
            await event.delete()
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
    elif input_str:
        directory_name = input_str

        await event.edit("Local file compressed to `{}`".format(output))


async def create_archive(input_directory):
    return_name = None
    if os.path.exists(input_directory):
        base_dir_name = os.path.basename(input_directory)
        compressed_file_name = f"{base_dir_name}.tar.gz"
        # suffix_extention_length = 1 + 3 + 1 + 2
        # if len(base_dir_name) > (64 - suffix_extention_length):
        #     compressed_file_name = base_dir_name[0:(64 - suffix_extention_length)]
        compressed_file_name += ".tar.gz"
        file_genertor_command = [
            "tar",
            "-zcvf",
            compressed_file_name,
            f"{input_directory}",
        ]
        process = await asyncio.create_subprocess_exec(
            *file_genertor_command,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # Wait for the subprocess to finish
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
        if os.path.exists(compressed_file_name):
            try:
                shutil.rmtree(input_directory)
            except:
                pass
            return_name = compressed_file_name
    return return_name


@borg.on(admin_cmd(pattern="unrar"))
async def _(event):
    if event.fwd_from:
        return
    mone = await event.edit("Processing ...")
    if not os.path.isdir(Var.TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Var.TEMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        reply_message = await event.get_reply_message()
        try:

            downloaded_file_name = await borg.download_media(
                reply_message, Var.TEMP_DOWNLOAD_DIRECTORY
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
        else:
            end = datetime.now()
            ms = (end - start).seconds
            await mone.edit(
                "Stored the rar to `{}` in {} seconds.".format(downloaded_file_name, ms)
            )

        patoolib.extract_archive(downloaded_file_name, outdir=extracted)
        filename = sorted(get_lst_of_files(extracted, []))
        # filename = filename + "/"
        await event.edit("Unraring now")
        # r=root, d=directories, f = files
        for single_file in filename:
            if os.path.exists(single_file):
                # https://stackoverflow.com/a/678242/4723940
                caption_rts = os.path.basename(single_file)
                force_document = True
                supports_streaming = False
                document_attributes = []
                if single_file.endswith((".mp4", ".mp3", ".flac", ".webm")):
                    metadata = extractMetadata(createParser(single_file))
                    duration = 0
                    width = 0
                    height = 0
                    if metadata.has("duration"):
                        duration = metadata.get("duration").seconds
                    if os.path.exists(thumb_image_path):
                        metadata = extractMetadata(createParser(thumb_image_path))
                        if metadata.has("width"):
                            width = metadata.get("width")
                        if metadata.has("height"):
                            height = metadata.get("height")
                    document_attributes = [
                        DocumentAttributeVideo(
                            duration=duration,
                            w=width,
                            h=height,
                            round_message=False,
                            supports_streaming=True,
                        )
                    ]
                try:
                    await borg.send_file(
                        event.chat_id,
                        single_file,
                        caption=f"UnRarred `{caption_rts}`",
                        force_document=force_document,
                        supports_streaming=supports_streaming,
                        allow_cache=False,
                        reply_to=event.message.id,
                        attributes=document_attributes,
                        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            progress(d, t, event, c_time, "trying to upload")
                        ),
                    )
                    await event.edit("DONE!!!")
                    await asyncio.sleep(5)
                    await event.delete()
                except Exception as e:
                    await borg.send_message(
                        event.chat_id,
                        "{} caused `{}`".format(caption_rts, str(e)),
                        reply_to=event.message.id,
                    )
                    # some media were having some issues
                    continue
                os.remove(single_file)
        os.remove(downloaded_file_name)


@borg.on(admin_cmd(pattern="untar"))
async def _(event):
    if event.fwd_from:
        return
    mone = await event.edit("Processing ...")
    if not os.path.isdir(Var.dTEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Var.TEMP_DOWNLOAD_DIRECTORY)
    extracted = Var.TEMP_DOWNLOAD_DIRECTORY + "extracted/"
    thumb_image_path = Var.TEMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"
    if not os.path.isdir(extracted):
        os.makedirs(extracted)
    if event.reply_to_msg_id:
        start = datetime.now()
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await borg.download_media(
                reply_message, Var.TEMP_DOWNLOAD_DIRECTORY
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
        else:
            end = datetime.now()
            ms = (end - start).seconds
            await mone.edit(
                "Stored the tar to `{}` in {} seconds.".format(downloaded_file_name, ms)
            )
        with tarfile.TarFile.open(downloaded_file_name, "r") as tar_file:
            tar_file.extractall(path=extracted)
        # tf = tarfile.open(downloaded_file_name)
        # tf.extractall(path=extracted)
        # tf.close()

        # with zipfile.ZipFile(downloaded_file_name, 'r') as zip_ref:
        #     zip_ref.extractall(extracted)
        filename = sorted(get_lst_of_files(extracted, []))
        # filename = filename + "/"
        await event.edit("Untarring now")
        # r=root, d=directories, f = files
        for single_file in filename:
            if os.path.exists(single_file):
                # https://stackoverflow.com/a/678242/4723940
                caption_rts = os.path.basename(single_file)
                force_document = False
                supports_streaming = True
                document_attributes = []
                if single_file.endswith((".mp4", ".mp3", ".flac", ".webm")):
                    metadata = extractMetadata(createParser(single_file))
                    duration = 0
                    width = 0
                    height = 0
                    if metadata.has("duration"):
                        duration = metadata.get("duration").seconds
                    if os.path.exists(thumb_image_path):
                        metadata = extractMetadata(createParser(thumb_image_path))
                        if metadata.has("width"):
                            width = metadata.get("width")
                        if metadata.has("height"):
                            height = metadata.get("height")
                    document_attributes = [
                        DocumentAttributeVideo(
                            duration=duration,
                            w=width,
                            h=height,
                            round_message=False,
                            supports_streaming=True,
                        )
                    ]
                try:
                    await borg.send_file(
                        event.chat_id,
                        single_file,
                        caption=f"Untared `{caption_rts}`",
                        force_document=force_document,
                        supports_streaming=supports_streaming,
                        allow_cache=False,
                        reply_to=event.message.id,
                        attributes=document_attributes,
                        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            progress(d, t, event, c_time, "trying to upload")
                        ),
                    )
                    await event.edit("DONE!!!")
                    await asyncio.sleep(5)
                    await event.delete()
                except Exception as e:
                    await borg.send_message(
                        event.chat_id,
                        "{} caused `{}`".format(caption_rts, str(e)),
                        reply_to=event.message.id,
                    )
                    # some media were having some issues
                    continue
                os.remove(single_file)
        os.remove(downloaded_file_name)


def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        output_lst.append(current_file_name)
    return output_lst


CMD_HELP.update(
    {
        "archive": ".zip reply to a file/media\
    \nUSEAGE: it will zip that file/media\
    \n\n.rar reply to a file/media\
    \nUSEAGE: it will rar that file/media\
    z\n\n. reply to a file/media\
    \nUSEAGE: it will make into .7z that hat file/media\
    \n\n.tar reply to a file/media\
    \nUSEAGE: it will tar that file/media\
    \n\n.unzip reply to a .zip file\
    \nUSEAGE: it will unzip that .zip file\
    \n\n.unrar reply to a .rar file\
    \nUSEAGE: it will unrar that .rar file\
    \n\n.untar reply to a .tar\
    \nUSEAGE: it will untar that .tar file\
"
    }
)
