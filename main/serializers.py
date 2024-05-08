from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework import serializers
from .models import Token, Major, User, Board, Board_Comment, Board_Like, Board_bookmark, Study, Study_Comment, Study_Like, Usedbooktrade, UsedbooktradeData, Usedbooktrade_Comment

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Frontend에서 더 필요한 정보가 있다면 여기에 추가적으로 작성하면 됩니다. token["is_superuser"] = user.is_superuser 이런식으로요.
        token['username'] = user.username
        token['email'] = user.email
        return token

class RegisterSerializer(serializers.ModelSerializer):
    home_password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    home_password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('user_name', 'home_password', 'home_password2')

    def validate(self, attrs):
        if attrs['home_password'] != attrs['home_password2']:
            raise serializers.ValidationError(
                {"home_password": "home_password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            user_name=validated_data['user_name']
        )

        user.set_password(validated_data['home_password'])
        user.save()

class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = '__all__'

class MajorCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ['id', 'major', 'major_category_name']
        
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

class UsedbooktradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usedbooktrade
        fields = ['id', 'title', 'author', 'seller', 'publisher', 'price', 'imgfile', 'description', 'damage_level', 'post_date', 'is_sold']

class UsedbooktradeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsedbooktradeData
        fields = ['id', 'trade', 'sellerid', 'sell_date']

class UsedbooktradeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usedbooktrade_Comment
        fields = ['id', 'user_id', 'Usedbookpost_id', 'contents']    