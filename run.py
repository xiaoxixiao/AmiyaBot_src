import os
import zipfile

from amiyabot.network.download import download_sync
from core.resource import remote_config
from core.util import create_dir, support_gbk
from core import log


class BotResource:
    @classmethod
    def download_bot_resource(cls):     # 下载机器人资源|cls是类方法|@classmethod是装饰器
        create_dir('resource')          # 创建目录|resource是目录名

        url = f'{remote_config.remote.cos}/resource/assets/Amiya-Bot-assets.zip'    # 资源地址
        print('url:', url)
        version = f'{remote_config.remote.cos}/resource/assets/version.txt'
        print('version:', version)
        lock_file = 'resource/assets-lock.txt'
        print('lock_file:', str(remote_config.remote.cos) + str(lock_file))
        pack_zip = 'resource/Amiya-Bot-assets.zip'
        print('pack_zip:', str(remote_config.remote.cos) + str(pack_zip))

        log.info('checking assets update...')

        flag = False
        latest_ver = download_sync(version, stringify=True)
        if os.path.exists(lock_file):
            if latest_ver:
                with open(lock_file, mode='r') as lf:
                    if lf.read() != latest_ver:
                        flag = True
        else:
            flag = True

        if flag:
            data = download_sync(url, progress=True)
            if data:
                with open(pack_zip, mode='wb+') as src:
                    src.write(data)

                pack = zipfile.ZipFile(pack_zip)
                for pack_file in support_gbk(pack).namelist():
                    pack.extract(pack_file, 'resource')
            else:
                if os.path.exists(lock_file):
                    os.remove(lock_file)
                raise Exception(f'assets download failed')

        if latest_ver:
            with open(lock_file, mode='w+') as v:
                v.write(latest_ver)
        else:
            log.error('assets version file request failed.')
