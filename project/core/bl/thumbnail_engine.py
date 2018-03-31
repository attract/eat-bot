# -*- coding: utf-8 -*-
import os

import shutil
#from PIL import Image, ImageColor
from django.conf import settings

from sorl.thumbnail.base import ThumbnailBackend
from sorl.thumbnail.engines.pil_engine import Engine
from sorl.thumbnail.images import DummyImageFile, BaseImageFile, ImageFile
from sorl.thumbnail.conf import settings, defaults as default_settings
from sorl.thumbnail import default

from core.bl.utils_helper import prn, translit_ru_to_en, check_path_dirs


class BackgroundEngine(Engine):
    """ sorl.thumbnail engine, that replaces transparent background in png to white color.
        This is needed, because, by default, when PNG converted to JPG, it's background becames black.
    """
    def create(self, image, geometry, options):
        thumb = super(Engine, self).create(image, geometry, options)

        # try:
        #     background = Image.new('RGB', thumb.size, ImageColor.getrgb('white'))
        #     background.paste(thumb, mask=thumb.split()[3])  # 3 is the alpha of an RGBA image.
        #     return background
        # except Exception as e:
        #
        return thumb


class DynamicDummyImageFile(BaseImageFile):
    def __init__(self, dummy_image_file):
        self.size = dummy_image_file.size

    def exists(self):
        return True

    @property
    def url(self):
        return settings.THUMBNAIL_DUMMY_SOURCE


class DummyThumbnailBackend(ThumbnailBackend):
    def get_thumbnail(self, file_, geometry_string, **options):
        #try:
        image = self.get_thumbnail_custom(file_, geometry_string, **options)
        if isinstance(image, DummyImageFile):
            image = DynamicDummyImageFile(image)
        # except UnicodeEncodeError as error:
        #     print 'Error for file: %s, error: %s' % (file_, error)
        #     image = ImageFile(file_)

        return image

    def get_thumbnail_custom(self, file_, geometry_string, **options):
        """
        Returns thumbnail as an ImageFile instance for file with geometry and
        options given. First it will try to get it from the key value store,
        secondly it will create it.
        """
        from sorl.thumbnail import delete
        dummy_source = settings.THUMBNAIL_DUMMY_SOURCE

        if 'dummy_source_size' in options:
            if options['dummy_source_size'] == 'small':
                dummy_source = settings.THUMBNAIL_DUMMY_SOURCE_SMALL

        if file_:
            source = ImageFile(file_)
        elif settings.THUMBNAIL_DUMMY:
            source = ImageFile(dummy_source)
            #return DummyImageFile(geometry_string)
        else:
            return None
        # preserve image filetype
        if settings.THUMBNAIL_PRESERVE_FORMAT:
            options.setdefault('format', self._get_format(source))

        for key, value in self.default_options.items():
            options.setdefault(key, value)

        # For the future I think it is better to add options only if they
        # differ from the default settings as below. This will ensure the same
        # filenames being generated for new options at default.
        for key, attr in self.extra_options:
            value = getattr(settings, attr)
            if value != getattr(default_settings, attr):
                options.setdefault(key, value)

        cache_name = self._get_thumbnail_filename(source, geometry_string, options)
        thumbnail = ImageFile(cache_name, default.storage)
        cached = default.kvstore.get(thumbnail)
        if cached:
            if not thumbnail.exists():
                # CHECK IF CACHED FILE WAS DELETED MANUAL
                delete(cached)
                return self.get_thumbnail_custom(file_, geometry_string, **options)
            return cached
        media_folder = settings.MEDIA_URL
        # We have to check exists() because the Storage backend does not
        # overwrite in some implementations.
        if not self.check_exists(thumbnail):
            # TRY WITH SORL default.engine
            if source.name.startswith(media_folder):
                source.name = source.name.replace(media_folder, '')
            try:
                source_image = default.engine.get_image(source)
            except (IOError, UnicodeEncodeError) as error:
                if type(error) == UnicodeEncodeError:
                    thumbnail = self.create_translit_cache(source, geometry_string, options, cache_name)
                    if thumbnail:
                        return thumbnail
                #print "GET_THUMBNAIL[1]: %s, URL= '%s', CREATING CACHE FILE" % (error, source.url)
                #return self.create_dummy_cache(source, cache_name, media_folder, dummy_source)

                options['level'] = options['level'] if 'level' in options else 1
                if options['level'] == 1:
                    options['level'] += 1
                    return self.get_thumbnail_custom(dummy_source, geometry_string, **options)
                else:
                    return DummyImageFile(geometry_string)

            # We might as well set the size since we have the image in memory
            image_info = default.engine.get_image_info(source_image)
            options['image_info'] = image_info
            size = default.engine.get_image_size(source_image)
            source.set_size(size)
            try:
                self._create_thumbnail(source_image, geometry_string, options, thumbnail)
                self._create_alternative_resolutions(source_image, geometry_string,
                                                     options, thumbnail.name)
            except SystemError as error:
                # when image transparent, can't create thumbnail for it
                print(error)
                # return DummyImageFile(geometry_string)
            finally:
                default.engine.cleanup(source_image)

        # If the thumbnail exists we don't create it, the other option is
        # to delete and write but this could lead to race conditions so I
        # will just leave that out for now.
        try:
            default.kvstore.get_or_set(source)
        except IOError as error:
            #print "GET_THUMBNAIL[2]: %s, URL= '%s'. CREATING CACHE FILE" % (error, cache_name)
            #return self.create_dummy_cache(source, cache_name, media_folder, dummy_source)
            #return self.get_thumbnail_custom(dummy_source, geometry_string, **options)
            return DummyImageFile(geometry_string)
        try:
            default.kvstore.set(thumbnail, source)
        except IOError as error:
            #print "GET_THUMBNAIL[3]: %s, URL= '%s'. CREATING CACHE FILE" % (error, cache_name)
            #return self.create_dummy_cache(source, cache_name, media_folder, dummy_source)
            #return self.get_thumbnail_custom(dummy_source, geometry_string, **options)
            return DummyImageFile(geometry_string)

        return thumbnail

    def create_dummy_cache(self, source, cache_name, media_folder, dummy_source):
        # CREATING CACHE DUMMY FILE FOR URL THAT CAN'T DOWNLOAD
        #dummy_image = dummy_source
        dummy_image = dummy_source.split(media_folder)[-1]
        if dummy_image.startswith(media_folder):
            dummy_image = dummy_image.replace(media_folder, '')
        dummy_image_full_path = '%s%s' % (settings.MEDIA_ROOT, dummy_image)
        cache_dummy_image = '%s%s' % (settings.MEDIA_ROOT, cache_name)
        check_path_dirs(cache_dummy_image)
        shutil.copy(dummy_image_full_path, cache_dummy_image)

        thumbnail = ImageFile(cache_name, default.storage)
        #source.name = '%s%s%s' % (settings.SITE_URL_FULL, settings.MEDIA_URL, dummy_image)
        source.name = dummy_source

        try:
            default.kvstore.get_or_set(source)
        except IOError as error:
            print('create_dummy_cache %s' % error)
            source.name = dummy_image
            default.kvstore.get_or_set(source)

        default.kvstore.set(thumbnail, source)
        return thumbnail

    def check_exists(self, thumbnail):
        if thumbnail.exists():
            if thumbnail.name.startswith('cache/'):
                return os.path.isfile("%s%s" % (settings.MEDIA_ROOT, thumbnail.name))
            else:
                return True
        return False

    def create_translit_cache(self, source, geometry_string, options, cache_name):
        full_path = "%s%s" % (settings.MEDIA_ROOT, source.name.encode('utf-8'))
        file_name = source.name.split('/')[-1]
        if os.path.isfile(full_path):
            file_name_translit = source.name.replace(file_name, translit_ru_to_en(file_name))
            full_path_translit = "%s%s" % (settings.MEDIA_ROOT, file_name_translit)
            shutil.copy(full_path, full_path_translit)

            # creating file with exact size
            file_resized = self.get_thumbnail_custom(file_name_translit, geometry_string, **options)
            os.remove(full_path_translit)

            # creating cache file for original filename
            resized_file_full_path = "%s%s" % (settings.MEDIA_ROOT, file_resized.name)
            cache_file_full_path = "%s%s" % (settings.MEDIA_ROOT, cache_name)
            check_path_dirs(cache_file_full_path)
            shutil.copy(resized_file_full_path, cache_file_full_path)
            os.remove(resized_file_full_path)

            source.name = file_resized.name
            thumbnail = ImageFile(cache_name, default.storage)
            default.kvstore.get_or_set(source)
            default.kvstore.set(thumbnail, source)
            return thumbnail

        return False
