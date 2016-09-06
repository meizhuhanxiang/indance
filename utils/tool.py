# -*- coding: utf-8 -*-
import qrcode
import base64
import uuid
import functools
from utils.code import *
import traceback
from utils.logger import runtime_logger
from StringIO import StringIO

__author__ = 'guoguangchuan'


def get_qrcode(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    img_io = StringIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return img_io.getvalue()


def get_uuid():
    return str(uuid.uuid1()).replace('-', '')


def excetion(method):
    @functools.wraps(method)
    def warpper(self, *args, **kwargs):
        try:
            method(self, *args, **kwargs)
        except Exception, e:
            runtime_logger().error(traceback.format_exc())
            self.write_res(INTERNAL_ERROR, msg=str(e))

    return warpper
