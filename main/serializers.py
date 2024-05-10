from django.contrib.auth.models import User as AuthUser
from rest_framework.authtoken.models import Token as AuthToken

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Token, Major, User, Board, Board_Comment, Board_Like, Board_bookmark, Study, Study_Comment, Study_Like, Usedbooktrade, UsedbooktradeData, Usedbooktrade_Comment

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Frontend에서 더 필요한 정보가 있다면 여기에 추가적으로 작성
        token['username'] = user.username
        token['email'] = user.email
        return token

class AuthUserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    username = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = AuthUser
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        auth_user = AuthUser.objects.create(
            username=validated_data['username'],
            password=make_password(validated_data['password']),
            email=validated_data['email']
        )
        return auth_user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    # write_only=True 옵션을 통해 클라이언트->서버의 역직렬화는 가능하지만, 서버->클라이언트 방향의 직렬화는 불가능하도록 해준다.
    
    def validate(self, data):
        user = authenticate(**data)
        if user:
            try:
                token = Token.objects.get(auth_id=user.id)
                #token = AuthToken.objects.filter(user=user)
                return token
            except AuthToken.DoesNotExist:
                raise serializers.ValidationError(
                    {"error": "Token does not exist for this user."}
                )
        else:
            raise serializers.ValidationError(
                {"error": "Unable to log in with provided credentials."}
            )


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

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'major_id', 'user_name', 'school_name', 'major_name', 'student_id', 'home_id', 'home_password', 'email', 'phonenumber', 'admission_date']

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