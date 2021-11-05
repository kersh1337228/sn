from user_media.models import Image, Video, Audio, File


'''Function helping to attach multiple media files to one note'''
def attach_media(media, owner_type, owner, object):
    '''Attach inner function for one of media types'''
    def attach(type, object_model):
        for file in media[f'{type}']:
            obj = object_model(**{
                f'{type[:-1]}': file,
                f'{owner_type}': owner
            })
            obj.save()
            if type == 'images':
                owner.images.add(obj)
            elif type == 'videos':
                owner.videos.add(obj)
            elif type == 'audios':
                owner.audios.add(obj)
            elif type == 'files':
                owner.files.add(obj)
    if media:
        attach('images', Image)
        attach('videos', Video)
        attach('audios', Audio)
        attach('files', File)
    return object
