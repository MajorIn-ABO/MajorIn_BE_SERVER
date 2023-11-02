from django.db import models

from django.conf import settings
from django.utils import timezone


class Major(models.Model):
    id = models.BigAutoField(primary_key=True)
    major = models.CharField(max_length=15, null=True)
    major_category_name = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.id


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
    email = models.EmailField(unique=True)
    phonenumber = models.CharField(max_length=15)
    admission_date = models.DateField()
    registration_date = models.DateField(auto_now_add=True)
    user_status = models.CharField(max_length=10, choices=USER_STATUS)

    def __str__(self):
        return self.id


class Category(models.Model):
    QUESTION_MAJOR = 'QUESTION'
    TALK = 'TALK'
    INTERN_REVIEW = 'INTERN'
    EXTERNAL_ACTIVITY = 'EXTERNAL'
    SCHOOL_STROY = 'SCHOOL'

    POST_CATEGORY = [
        (QUESTION_MAJOR, 'question_major'),
        (TALK, 'talk'),
        (INTERN_REVIEW, 'intern_review'),
        (EXTERNAL_ACTIVITY, 'external_activity'),
        (SCHOOL_STROY, 'school_story'),
    ]
    id = models.BigAutoField(primary_key=True)
    category_name = models.CharField(max_length=10, choices=POST_CATEGORY)

    def __str__(self):
        return self.id


class Board(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, db_column="category_id")
    title = models.CharField(max_length=100, blank=False, null=False)
    contents = models.TextField(blank=False, null=False)
    post_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    delete_date = models.DateTimeField(null=True)
    like = models.IntegerField(default=0)
    keep = models.IntegerField(default=0)

    def __str__(self):
        return self.id


# 게시글, 스터디 댓글을 테이블을 나눠서 저장할지 -> 현재 상태
# 함께 저장 : 카테고리 str 을 id 에 붙여서 저장하는 방법 or 카테고리 컬럼을 넣고 따로 id 값은 같아도 상관없도록 (고려)
class Board_Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    post_id = models.ForeignKey(Board, on_delete=models.CASCADE, db_column="post_id")
    parent_comment = models.BigIntegerField(default=id, db_column="parent_comment")
    contents = models.TextField(blank=False, null=False)
    comment_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    delete_date = models.DateTimeField(null=True)
    like = models.IntegerField(default=0)

    def __str__(self):
        return self.id
    

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