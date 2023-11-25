from rest_framework import serializers
from .models import User, Board, Board_Comment, Board_Like, Board_bookmark, Study, Study_Comment, Study_Like

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'user_id', 'category_id', 'title', 'contents']

class BoardCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board_Comment
        fields = ['id', 'user_id', 'post_id', 'contents']

class BoardLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board_Like
        fields = ['id', 'user_id', 'post_id']

class BoardBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board_bookmark
        fields = ['id', 'user_id', 'post_id']

class StudySerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = ['id', 'user_id', 'title', 'contents', 'hashtags', 'is_recruited']

class StudyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Study_Comment
        fields = ['id', 'user_id', 'studypost_id', 'contents']   

class StudyLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Study_Like
        fields = ['id', 'user_id', 'studypost_id']     