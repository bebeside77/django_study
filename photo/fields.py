__author__ = 'NAVER'

import os

from django.db.models.fields.files import ImageField, ImageFieldFile
from PIL import Image


def _add_thumb(s):
    parts = s.split(".")
    parts.insert(-1, "thumb")  # 뒤에서 두번째에 thumb을 넣음
    if parts[-1].lower() not in ['jpeg', 'jpg']:
        parts[-1] = 'jpg'
    return ".".join(parts)


class ThumbnailImageFieldFile(ImageFieldFile):
    def _get_thumb_path(self):  # 썸네일 파일경로를 가져옴
        return _add_thumb(self.path)

    thumb_path = property(_get_thumb_path)

    def _get_thumb_url(self):  # 썸네일 url 주소를 가져옴
        return _add_thumb(self.url)

    thumb_url = property(_get_thumb_url)

    def save(self, name, content, save=True):  # 파일 시스템에 파일 저장
        super(ThumbnailImageFieldFile, self).save(name, content, save)
        img = Image.open(self.path)

        size = (128, 128)
        img.thumbnail(size, Image.ANTIALIAS)  # 원본이미지로부터 썸네일 이미지 생성
        background = Image.new("RGBA", size, (255, 255, 255, 0))  # 흰색 배경용 이미지 생성
        background.paste(img, (int((size[0] - img.size[0]) / 2), int((size[1] - img.size[1]) / 2)))  # 썸네일 + 백그라운드
        background.save(self.thumb_path, 'JPEG')

    def delete(self, save=True):
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)  # 원본 뿐만아니라 썸네일 이미지도 삭제
        super(ThumbnailImageFieldFile, self).delete(save)


class ThumbnailImageField(ImageField):
    attr_class = ThumbnailImageFieldFile

    def __init__(self, thumb_width=128, thumb_height=128, *args, **kwargs):
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height
        super(ThumbnailImageField, self).__init__(*args, **kwargs)
