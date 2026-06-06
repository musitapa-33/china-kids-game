"""
等待数据库就绪的 management command。
用法: python manage.py wait_for_db
"""
import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '等待数据库连接就绪'

    def add_arguments(self, parser):
        parser.add_argument('--timeout', type=int, default=60, help='超时秒数')

    def handle(self, *args, **options):
        timeout = options['timeout']
        db_conn = connections['default']
        start = time.time()

        self.stdout.write('等待数据库就绪...')
        while time.time() - start < timeout:
            try:
                db_conn.ensure_connection()
                self.stdout.write(self.style.SUCCESS('✅ 数据库已就绪！'))
                return
            except OperationalError:
                self.stdout.write('.', ending='')
                time.sleep(2)

        self.stdout.write(self.style.ERROR(f'❌ 数据库连接超时（{timeout}秒）'))
        raise SystemExit(1)
