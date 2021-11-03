from user_media.models import Image, Video, Audio, File


'''Function helping to attach multiple media files to one note'''
def note_attach_media(objects, type, owner_type, owner, note):
    if objects:
        if type == 'image':
            if owner_type == 'user':
                for image in objects:
                    img = Image(
                        image=image,
                        user=owner,
                    )
                    img.save()
                    note.images.add(img)
            elif owner_type == 'community':
                for image in objects:
                    img = Image(
                        image=image,
                        community=owner,
                    )
                    img.save()
                    note.images.add(img)
        elif type == 'video':
            if owner_type == 'user':
                for video in objects:
                    vid = Video(
                        video=video,
                        user=owner,
                    )
                    vid.save()
                    note.videos.add(vid)
            elif owner_type == 'community':
                for video in objects:
                    vid = Image(
                        video=video,
                        community=owner,
                    )
                    vid.save()
                    note.images.add(vid)
        elif type == 'audio':
            if owner_type == 'user':
                for audio in objects:
                    aud = Audio(
                        audio=audio,
                        user=owner,
                    )
                    aud.save()
                    note.audios.add(aud)
            elif owner_type == 'community':
                for audio in objects:
                    aud = Audio(
                        audio=audio,
                        community=owner,
                    )
                    aud.save()
                    note.audios.add(aud)
        elif type == 'file':
            if owner_type == 'user':
                for file in objects:
                    fil = File(
                        file=file,
                        user=owner,
                    )
                    fil.save()
                    note.images.add(fil)
            elif owner_type == 'community':
                for file in objects:
                    fil = File(
                        file=file,
                        community=owner,
                    )
                    fil.save()
                    note.images.add(fil)
    return note
