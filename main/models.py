from django.db import models
from django.contrib.auth.models import User as AuthUser
from rest_framework.authtoken.models import Token as AuthToken

from django.conf import settings
from django.utils import timezone


class Major(models.Model):
    id = models.BigAutoField(primary_key=True)
    major = models.CharField(max_length=100, null=True)
    major_category_name = models.CharField(max_length=10, null=True)

    def __str__(self) -> str:
        return str(self.id)


class User(models.Model):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    WARN = 'WARN'
    BLOCK = 'BLOCK'

    USER_STATUS = [
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
        (WARN, 'warn'),
        (BLOCK, 'block'),
    ]

    id = models.BigAutoField(primary_key=True)
    major_id = models.ForeignKey(Major, on_delete=models.CASCADE, db_column="major_id")
    user_name = models.CharField(max_length=10)
    school_name = models.CharField(max_length=20)
    major_name = models.CharField(max_length=15)
    student_id = models.BigIntegerField()
    home_id = models.CharField(max_length=15)
    home_password = models.CharField(max_length=20)
    home_password_check = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    phonenumber = models.CharField(max_length=15)
    admission_date = models.IntegerField()
    registration_date = models.DateField(auto_now_add=True)
    user_status = models.CharField(max_length=10, choices=USER_STATUS, default=ACTIVE)

    def __str__(self) -> str:
        return str(self.id)

class Token(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    auth_id = models.ForeignKey(AuthUser, on_delete=models.CASCADE, db_column="auth_id")
    refresh = models.CharField(max_length=500, null=True)
    access = models.CharField(max_length=500, null=True)

    def __str__(self) -> str:
        return str(self.id)
        
class Category(models.Model):
    COMMUNITY = 'COMMUNITY'
    STUDY = 'STUDY'

    POST_CATEGORY = [
        (COMMUNITY, 'community'),
        (STUDY, 'study'),
    ]
    id = models.BigAutoField(primary_key=True)
    category_of = models.CharField(max_length=10, choices=POST_CATEGORY)
    category_name = models.CharField(max_length=10, blank=False, null=False)

    def __str__(self) -> str:
        return str(self.id)


class Board(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, db_column="category_id")
    title = models.CharField(max_length=100, blank=False, null=False)
    contents = models.TextField(blank=False, null=False)
    imgfile = models.ImageField(null=True, upload_to="community/", blank=True, verbose_name='첨부 사진')
    post_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    delete_date = models.DateTimeField(null=True)
    comment = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    bookmark = models.IntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)

    @property
    def category_name(self):
        return self.category_id.category_name

    def __str__(self) -> str:
        return str(self.id)


class Board_Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    post_id = models.ForeignKey(Board, on_delete=models.CASCADE, db_column="post_id")
    parent_comment = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    contents = models.TextField(blank=False, null=False)
    comment_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    delete_date = models.DateTimeField(null=True)
    like = models.IntegerField(default=0)

    def __str__(self) -> str:
        return str(self.id)
    

class Board_Like(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    post_id = models.ForeignKey(Board, on_delete=models.CASCADE, db_column="post_id")
    like_date = models.DateTimeField(auto_now_add=True)
    delete_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.id
    

class Board_bookmark(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    post_id = models.ForeignKey(Board, on_delete=models.CASCADE, db_column="post_id")
    bookmark_date = models.DateTimeField(auto_now_add=True)
    delete_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.id
    

class Study(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    title = models.CharField(max_length=100, blank=False, null=False)
    contents = models.TextField(blank=False, null=False)
    hashtags = models.TextField(blank=False, null=False)
    is_recruited = models.BooleanField(default=False, null=False)
    post_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    delete_date = models.DateTimeField(null=True)
    comment = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return str(self.id)
    

class Study_Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    studypost_id = models.ForeignKey(Study, on_delete=models.CASCADE, db_column="studypost_id")
    parent_comment = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    contents = models.TextField(blank=False, null=False)
    comment_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    delete_date = models.DateTimeField(null=True)
    like = models.IntegerField(default=0)

    def __str__(self) -> str:
        return str(self.id)
    

class Study_Like(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    studypost_id = models.ForeignKey(Study, on_delete=models.CASCADE, db_column="studypost_id")
    like_date = models.DateTimeField(auto_now_add=True)
    delete_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.id
    

class Usedbooktrade(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=False, null=False, verbose_name='상품명', help_text='* 책 제목은 정확하게 기입해주세요.')
    author = models.TextField(blank=False, null=False, verbose_name='저자')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id", verbose_name='판매자')
    publisher = models.CharField(max_length=100, null=False, verbose_name='출판사')
    price = models.TextField(blank=False, null=False, verbose_name='판매가')
    origin_imgfile = models.CharField(max_length=150, null=True, verbose_name='상품 사진')
    imgfile = models.ImageField(null=True, upload_to="book_covers/", blank=True, verbose_name='판매자 상품 사진')
    description = models.TextField(verbose_name='상품 설명')
    damage_level_choices = [
        ('없음', '손상도 없음'),
        ('조금있음', '손상도 조금있음'),
        ('많음', '손상도 많음'),
    ]
    damage_level = models.CharField(max_length=20, choices=damage_level_choices, default='없음', verbose_name='손상도')
    post_date = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    update_date = models.DateTimeField(auto_now=True, verbose_name='수정일')
    delete_date = models.DateTimeField(null=True)
    comment = models.IntegerField(default=0)
    is_sold = models.BooleanField(default=False, null=False)

    def __str__(self) -> str:
        return str(self.id)


class UsedbooktradeData(models.Model):
    id = models.BigAutoField(primary_key=True)
    trade = models.ForeignKey(Usedbooktrade, on_delete=models.CASCADE, db_column="trade_id")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    sell_date = models.DateTimeField(auto_now_add=True, verbose_name='판매일')

    def __str__(self) -> str:
        return str(self.id)


class Usedbooktrade_Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    Usedbookpost_id = models.ForeignKey(Usedbooktrade, on_delete=models.CASCADE, db_column="usedbookpost_id")
    parent_comment = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    contents = models.TextField(blank=False, null=False)
    comment_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    delete_date = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return str(self.id)


class MentorRegistrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=False, null=False, verbose_name='멘토링 제목')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='멘토 이름', db_column="user_id")
    mentoring_category_choices = [
        ('학습', '학습'),
        ('취업', '취업'),
        ('인간관계', '인간관계'),
    ]
    mentoring_category = models.CharField(max_length=20, choices=mentoring_category_choices, default='학습', verbose_name='멘토링 주제')
    description = models.TextField(verbose_name='멘토링 설명')
    place_type_choices = [
        ('온라인', '온라인'),
        ('오프라인', '오프라인'),
    ]
    place_type = models.CharField(max_length=10, choices=place_type_choices, default='온라인', verbose_name='진행 방식')
    period = models.TextField(verbose_name='멘토링 기간')
    day = models.TextField(verbose_name='가능 요일')
    mentee_num = models.IntegerField(blank=False, null=False, verbose_name='모집 인원')
    # mentoring_keyword = models.TextField(verbose_name='멘토링 키워드')
    # mood_type = models.TextField(verbose_name='멘토링 분위기')
    post_date = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    update_date = models.DateTimeField(auto_now=True, verbose_name='수정일')
    delete_date = models.DateTimeField(null=True, verbose_name='삭제일')
    admin_approval = models.BooleanField(default=False, null=False, verbose_name='관리자 승인 여부')
    status_choices = [
        ('모집중', '모집중'),
        ('모집완료', '모집완료'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='모집중', verbose_name='진행 상태')
    applicants_num = models.IntegerField(default=0, verbose_name='신청 인원')
    approval_num = models.IntegerField(default=0, verbose_name='승인 인원')

    def __str__(self) -> str:
        return str(self.id)


class MenteeApplications(models.Model):
    id = models.BigAutoField(primary_key=True)
    mentoring_id = models.ForeignKey(MentorRegistrations, on_delete=models.CASCADE, db_column="mentoring_id")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='멘티 이름', db_column="user_id")
    reason = models.TextField(verbose_name='지원 동기')
    add_text = models.TextField(verbose_name='멘토에게 하고 싶은 말')
    day = models.TextField(verbose_name='가능 요일')
    post_date = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    mentor_approval = models.BooleanField(default=False, null=False, verbose_name='멘토 승인 여부')

    def __str__(self) -> str:
        return str(self.id)


class MentoringData(models.Model):
    id = models.BigAutoField(primary_key=True)
    mentoring_id = models.ForeignKey(MentorRegistrations, on_delete=models.CASCADE, db_column="mentoring_id")
    mentee_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="mentee_id")
    start_date = models.DateTimeField(auto_now_add=True, verbose_name='시작일')
    end_date = models.DateTimeField(auto_now=True, verbose_name='종료일')
    status_choices = [
        ('진행중', '진행중'),
        ('진행완료', '진행완료'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='진행중', verbose_name='진행 상태')

    def __str__(self) -> str:
        return str(self.id)


class MentoringReview(models.Model):
    id = models.BigAutoField(primary_key=True)
    mentoringdata_id = models.ForeignKey(MentoringData, on_delete=models.CASCADE, db_column="mentoringdata_id")
    rating = models.IntegerField(verbose_name='평점')
    review_text = models.TextField(verbose_name='리뷰 내용')
    recommend = models.BooleanField(default=False, null=False, verbose_name='추천 여부')
    post_date = models.DateTimeField(auto_now_add=True, verbose_name='리뷰 날짜')

    def __str__(self) -> str:
        return str(self.id)


class ChatHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    is_bot = models.BooleanField(default=False)
    message = models.TextField()
    question_index = models.IntegerField(null=True, blank=True)  # 현재 질문 인덱스
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.id)