"""
导入省份数据、区域数据、题库数据
用法: python manage.py import_data
"""
from django.core.management.base import BaseCommand
from api.models import Region, Province, QuizQuestion


class Command(BaseCommand):
    help = '导入省份、区域、题库数据'

    def handle(self, *args, **options):
        self._import_regions()
        self._import_provinces()
        self._import_quiz_questions()
        self.stdout.write(self.style.SUCCESS('数据导入完成 ✅'))

    def _import_regions(self):
        regions = [
            '华北', '东北', '华东', '华中', '华南',
            '西南', '西北', '港澳台',
        ]
        for name in regions:
            Region.objects.get_or_create(name=name)
        self.stdout.write(f'✓ 导入 {len(regions)} 个区域')

    def _import_provinces(self):
        region_map = {r.name: r for r in Region.objects.all()}

        provinces_data = [
            {'name': '北京', 'capital': '北京', 'abbr': '京', 'feature': '天安门、长城、故宫', 'emoji': '🏛️', 'region': '华北', 'fun_fact': '北京是中国的首都，有3000多年建城史！故宫有8707间房间。', 'image': 'images/image4.jpg'},
            {'name': '天津', 'capital': '天津', 'abbr': '津', 'feature': '狗不理包子、天津之眼', 'emoji': '🎡', 'region': '华北', 'fun_fact': '天津是中国北方最大的港口城市，天津之眼是世界上唯一建在桥上的摩天轮。', 'image': 'images/image7.jpg'},
            {'name': '河北', 'capital': '石家庄', 'abbr': '冀', 'feature': '承德避暑山庄、北戴河', 'emoji': '🏰', 'region': '华北', 'fun_fact': '河北是中华民族的发祥地之一，承德避暑山庄是世界文化遗产。', 'image': 'images/image10.jpg'},
            {'name': '山西', 'capital': '太原', 'abbr': '晋', 'feature': '平遥古城、云冈石窟', 'emoji': '⛩️', 'region': '华北', 'fun_fact': '山西是中华文明的重要发源地，平遥古城是中国保存最完整的古代县城。', 'image': 'images/image13.jpg'},
            {'name': '内蒙古', 'capital': '呼和浩特', 'abbr': '蒙', 'feature': '大草原、蒙古包', 'emoji': '🐎', 'region': '华北', 'fun_fact': '内蒙古是中国最大的草原牧区，面积118万平方公里！', 'image': 'images/image15.jpg'},
            {'name': '辽宁', 'capital': '沈阳', 'abbr': '辽', 'feature': '沈阳故宫、大连海滩', 'emoji': '❄️', 'region': '东北', 'fun_fact': '辽宁是新中国工业的摇篮，沈阳故宫是清朝入关前的皇宫。', 'image': 'images/image19.jpg'},
            {'name': '吉林', 'capital': '长春', 'abbr': '吉', 'feature': '长白山、雾凇', 'emoji': '⛄', 'region': '东北', 'fun_fact': '长白山天池是中国最深的湖泊，也是松花江的源头。', 'image': 'images/image21.jpg'},
            {'name': '黑龙江', 'capital': '哈尔滨', 'abbr': '黑', 'feature': '冰雪大世界、中央大街', 'emoji': '🧊', 'region': '东北', 'fun_fact': '黑龙江是中国最北和最东的省份，冬季的冰雪大世界美极了！', 'image': 'images/image25.jpg'},
            {'name': '上海', 'capital': '上海', 'abbr': '沪', 'feature': '东方明珠、外滩', 'emoji': '🗼', 'region': '华东', 'fun_fact': '上海是中国最大的城市，有"魔都"之称，外滩有"万国建筑博览群"。', 'image': 'images/image31.jpg'},
            {'name': '江苏', 'capital': '南京', 'abbr': '苏', 'feature': '苏州园林、中山陵', 'emoji': '🌸', 'region': '华东', 'fun_fact': '江苏有"鱼米之乡"的美称，苏州园林是世界文化遗产。', 'image': 'images/image33.jpg'},
            {'name': '浙江', 'capital': '杭州', 'abbr': '浙', 'feature': '西湖、乌镇', 'emoji': '🍵', 'region': '华东', 'fun_fact': '"上有天堂，下有苏杭"，杭州西湖是世界文化遗产。', 'image': 'images/image32.jpg'},
            {'name': '安徽', 'capital': '合肥', 'abbr': '皖', 'feature': '黄山、宏村', 'emoji': '🏔️', 'region': '华东', 'fun_fact': '黄山有"五岳归来不看山，黄山归来不看岳"的美誉。', 'image': 'images/image37.jpg'},
            {'name': '福建', 'capital': '福州', 'abbr': '闽', 'feature': '武夷山、鼓浪屿', 'emoji': '🍵', 'region': '华东', 'fun_fact': '福建是海上丝绸之路的起点，武夷山是世界文化与自然双重遗产。', 'image': 'images/image38.jpg'},
            {'name': '江西', 'capital': '南昌', 'abbr': '赣', 'feature': '滕王阁、庐山', 'emoji': '🐒', 'region': '华东', 'fun_fact': '"落霞与孤鹜齐飞，秋水共长天一色"就是描写滕王阁的！', 'image': 'images/image41.jpg'},
            {'name': '山东', 'capital': '济南', 'abbr': '鲁', 'feature': '泰山、曲阜三孔', 'emoji': '🏔️', 'region': '华东', 'fun_fact': '泰山是五岳之首，孔子是山东曲阜人，儒家文化的发源地。', 'image': 'images/image35.jpg'},
            {'name': '河南', 'capital': '郑州', 'abbr': '豫', 'feature': '少林寺、龙门石窟', 'emoji': '🥋', 'region': '华中', 'fun_fact': '河南是中华文明的摇篮，少林寺是天下功夫的源头！', 'image': 'images/image49.jpg'},
            {'name': '湖北', 'capital': '武汉', 'abbr': '鄂', 'feature': '黄鹤楼、武当山', 'emoji': '🌉', 'region': '华中', 'fun_fact': '"昔人已乘黄鹤去，此地空余黄鹤楼"，黄鹤楼是江南三大名楼之首。', 'image': 'images/image51.jpg'},
            {'name': '湖南', 'capital': '长沙', 'abbr': '湘', 'feature': '张家界、凤凰古城', 'emoji': '🐼', 'region': '华中', 'fun_fact': '张家界是中国第一个国家森林公园，电影《阿凡达》曾在此取景。', 'image': 'images/image55.jpg'},
            {'name': '广东', 'capital': '广州', 'abbr': '粤', 'feature': '早茶、广州塔', 'emoji': '🗼', 'region': '华南', 'fun_fact': '广东是中国的"南大门"，粤菜是中国八大菜系之一，早茶文化闻名世界。', 'image': 'images/image60.jpg'},
            {'name': '广西', 'capital': '南宁', 'abbr': '桂', 'feature': '桂林山水、阳朔', 'emoji': '🏝️', 'region': '华南', 'fun_fact': '"桂林山水甲天下"，广西有中国最美的喀斯特地貌。', 'image': 'images/image63.jpg'},
            {'name': '海南', 'capital': '海口', 'abbr': '琼', 'feature': '三亚海滩、椰子树', 'emoji': '🏖️', 'region': '华南', 'fun_fact': '海南是中国唯一的热带岛屿省份，有"东方夏威夷"之称。', 'image': 'images/image62.jpg'},
            {'name': '重庆', 'capital': '重庆', 'abbr': '渝', 'feature': '火锅、洪崖洞', 'emoji': '🌶️', 'region': '西南', 'fun_fact': '重庆被称为"山城"和"火锅之都"，轻轨穿楼是著名景观！', 'image': 'images/image73.jpg'},
            {'name': '四川', 'capital': '成都', 'abbr': '川', 'feature': '大熊猫、都江堰', 'emoji': '🐼', 'region': '西南', 'fun_fact': '四川是大熊猫的故乡，都江堰是2000多年前修建的伟大水利工程。', 'image': 'images/image75.jpg'},
            {'name': '贵州', 'capital': '贵阳', 'abbr': '黔', 'feature': '黄果树瀑布、千户苗寨', 'emoji': '💧', 'region': '西南', 'fun_fact': '黄果树瀑布是中国第一大瀑布，贵州有49个民族聚居。', 'image': 'images/image77.jpg'},
            {'name': '云南', 'capital': '昆明', 'abbr': '云', 'feature': '丽江古城、石林', 'emoji': '🌺', 'region': '西南', 'fun_fact': '云南有"彩云之南"的美称，是中国民族最多的省份（25个少数民族）。', 'image': 'images/image78.jpg'},
            {'name': '西藏', 'capital': '拉萨', 'abbr': '藏', 'feature': '布达拉宫、珠穆朗玛峰', 'emoji': '🏔️', 'region': '西南', 'fun_fact': '布达拉宫是世界上海拔最高的宫殿，珠穆朗玛峰是世界最高峰！', 'image': 'images/image81.jpg'},
            {'name': '陕西', 'capital': '西安', 'abbr': '陕', 'feature': '兵马俑、大雁塔', 'emoji': '🏯', 'region': '西北', 'fun_fact': '兵马俑被誉为"世界第八大奇迹"，西安是十三朝古都。', 'image': 'images/image87.jpg'},
            {'name': '甘肃', 'capital': '兰州', 'abbr': '甘', 'feature': '敦煌莫高窟、兰州拉面', 'emoji': '🏜️', 'region': '西北', 'fun_fact': '敦煌莫高窟是世界最大的佛教艺术宝库，有"东方卢浮宫"之称。', 'image': 'images/image90.jpg'},
            {'name': '青海', 'capital': '西宁', 'abbr': '青', 'feature': '青海湖、茶卡盐湖', 'emoji': '🌊', 'region': '西北', 'fun_fact': '青海湖是中国最大的内陆咸水湖，被誉为"高原蓝宝石"。', 'image': 'images/image92.jpg'},
            {'name': '宁夏', 'capital': '银川', 'abbr': '宁', 'feature': '西夏王陵、沙坡头', 'emoji': '🕌', 'region': '西北', 'fun_fact': '宁夏是回族自治区，西夏王陵被称为"东方金字塔"。', 'image': 'images/image94.jpg'},
            {'name': '新疆', 'capital': '乌鲁木齐', 'abbr': '新', 'feature': '吐鲁番葡萄、天山', 'emoji': '🍇', 'region': '西北', 'fun_fact': '新疆是中国面积最大的省级行政区，占全国面积的六分之一！', 'image': 'images/image97.jpg'},
            {'name': '台湾', 'capital': '台北', 'abbr': '台', 'feature': '日月潭、阿里山', 'emoji': '🏔️', 'region': '港澳台', 'fun_fact': '台湾是中国第一大岛，日月潭是台湾最大的天然湖泊。', 'image': 'images/image43.jpg'},
            {'name': '香港', 'capital': '香港', 'abbr': '港', 'feature': '迪士尼乐园、维多利亚港', 'emoji': '🎢', 'region': '港澳台', 'fun_fact': '香港是中国的特别行政区，有"东方之珠"的美称。', 'image': 'images/image66.jpg'},
            {'name': '澳门', 'capital': '澳门', 'abbr': '澳', 'feature': '大三巴牌坊、葡式蛋挞', 'emoji': '⛪', 'region': '港澳台', 'fun_fact': '澳门是中国的特别行政区，大三巴牌坊是澳门的标志性建筑。', 'image': 'images/image69.jpg'},
        ]

        for data in provinces_data:
            region_name = data.pop('region')
            region = region_map.get(region_name)
            Province.objects.update_or_create(
                name=data['name'],
                defaults={**data, 'region': region}
            )
        self.stdout.write(f'✓ 导入 {len(provinces_data)} 个省份')

    def _import_quiz_questions(self):
        """生成题库：省会、简称、特色三种类型"""
        provinces = Province.objects.all()
        count = 0
        for p in provinces:
            # 省会题
            QuizQuestion.objects.get_or_create(
                province=p, question_type='capital',
                defaults={
                    'question_text': f'{p.name}的省会是哪里？',
                    'correct_answer': p.capital,
                    'option_a': p.capital,
                    'option_b': self._wrong_answer(provinces, 'capital', p),
                    'option_c': self._wrong_answer(provinces, 'capital', p),
                    'option_d': self._wrong_answer(provinces, 'capital', p),
                }
            )
            count += 1

            # 简称题
            QuizQuestion.objects.get_or_create(
                province=p, question_type='abbr',
                defaults={
                    'question_text': f'{p.name}的简称是什么？',
                    'correct_answer': p.abbr,
                    'option_a': p.abbr,
                    'option_b': self._wrong_answer(provinces, 'abbr', p),
                    'option_c': self._wrong_answer(provinces, 'abbr', p),
                    'option_d': self._wrong_answer(provinces, 'abbr', p),
                }
            )
            count += 1

            # 特色题
            feature_short = p.feature.split('、')[0] if '、' in p.feature else p.feature
            QuizQuestion.objects.get_or_create(
                province=p, question_type='feature',
                defaults={
                    'question_text': f'{p.name}的特色是什么？',
                    'correct_answer': feature_short,
                    'option_a': feature_short,
                    'option_b': self._wrong_answer(provinces, 'feature', p),
                    'option_c': self._wrong_answer(provinces, 'feature', p),
                    'option_d': self._wrong_answer(provinces, 'feature', p),
                }
            )
            count += 1

        self.stdout.write(f'✓ 导入 {count} 道题目')

    @staticmethod
    def _wrong_answer(provinces, field, current):
        """随机返回一个错误答案"""
        others = [p for p in provinces if p.id != current.id]
        if not others:
            return '未知'
        import random
        other = random.choice(others)
        return getattr(other, field, '未知') or '未知'
