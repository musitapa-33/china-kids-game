from django.db import models


class Region(models.Model):
    """地理区域（华北、东北等）"""
    name = models.CharField('区域名称', max_length=20, unique=True)

    class Meta:
        db_table = 'regions'
        verbose_name = '区域'
        verbose_name_plural = '区域'

    def __str__(self):
        return self.name


class Province(models.Model):
    """省份/行政区"""
    name = models.CharField('省份名称', max_length=20, unique=True)
    capital = models.CharField('省会/首府', max_length=20, default='')
    abbr = models.CharField('简称', max_length=4, default='')
    feature = models.CharField('特色', max_length=100, default='', blank=True)
    emoji = models.CharField('Emoji', max_length=4, default='', blank=True)
    region = models.ForeignKey(
        Region, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='provinces', verbose_name='所属区域'
    )
    fun_fact = models.TextField('趣味知识', default='', blank=True)
    description = models.TextField('描述', default='', blank=True)
    image = models.CharField('主图路径', max_length=200, default='', blank=True)
    visited_count = models.IntegerField('访问次数', default=0)

    class Meta:
        db_table = 'provinces'
        verbose_name = '省份'
        verbose_name_plural = '省份'
        ordering = ['name']

    def __str__(self):
        return self.name


class QuizQuestion(models.Model):
    """题库"""
    TYPE_CHOICES = [
        ('capital', '省会'),
        ('abbr', '简称'),
        ('feature', '特色'),
    ]
    province = models.ForeignKey(
        Province, on_delete=models.CASCADE, related_name='questions',
        verbose_name='关联省份'
    )
    question_type = models.CharField('题目类型', max_length=20, choices=TYPE_CHOICES)
    question_text = models.CharField('题目内容', max_length=200)
    correct_answer = models.CharField('正确答案', max_length=50)
    option_a = models.CharField('选项A', max_length=50)
    option_b = models.CharField('选项B', max_length=50)
    option_c = models.CharField('选项C', max_length=50)
    option_d = models.CharField('选项D', max_length=50)

    class Meta:
        db_table = 'quiz_questions'
        verbose_name = '题目'
        verbose_name_plural = '题目'

    def __str__(self):
        return f'{self.province.name} - {self.get_question_type_display()}'
