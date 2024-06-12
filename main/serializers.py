from django.contrib.auth.models import User as AuthUser
from rest_framework.authtoken.models import Token as AuthToken

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Token, Major, User, Category, Board, Board_Comment, Board_Like, Board_bookmark, Study, Study_Comment, Study_Like, Usedbooktrade, UsedbooktradeData, Usedbooktrade_Comment

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

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'major_id', 'user_name', 'school_name', 'major_name', 'student_id', 'home_id', 'email', 'phonenumber', 'admission_date', 'registration_date', 'user_status']

class UserRegisterSerializer(serializers.ModelSerializer):
    home_password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    home_password_check = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'major_id', 'user_name', 'school_name', 'major_name', 'student_id', 'home_id', 'home_password', 'home_password_check', 'email', 'phonenumber', 'admission_date']

    def validate(self, attrs):
        if attrs['home_password'] != attrs['home_password_check']:
            raise serializers.ValidationError(
                {"password": "비밀번호가 일치하지 않습니다."})

        return attrs

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_of', 'category_name']

class BoardSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(max_length=10)

    class Meta:
        model = Board
        fields = ['id', 'user_id', 'category_name', 'title', 'contents', 'imgfile', 'post_date', 'comment', 'like', 'bookmark']

    def create(self, validated_data):
        category_name = validated_data.pop('category_name')
        
        # category_name을 사용하여 Category 인스턴스 가져오기
        try:
            category = Category.objects.get(category_name=category_name)
        except Category.DoesNotExist:
            raise serializers.ValidationError("해당 카테고리가 존재하지 않습니다.")

        validated_data['category_id'] = category
        board = Board.objects.create(**validated_data)
        return board

class BoardProfileSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(max_length=10)

    class Meta:
        model = Board
        fields = [
            'id', 'user_id', 'category_name', 'title', 'contents', 'imgfile',
            'post_date', 'comment', 'like', 'bookmark'
        ]

class BoardCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board_Comment
        fields = ['id', 'user_id', 'post_id', 'parent_comment', 'contents', 'comment_date']

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
        fields = ['id', 'user_id', 'title', 'contents', 'hashtags', 'is_recruited', 'post_date', 'comment', 'like']

class StudyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Study_Comment
        fields = ['id', 'user_id', 'studypost_id', 'parent_comment', 'contents', 'comment_date']   

class StudyLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Study_Like
        fields = ['id', 'user_id', 'studypost_id'] 

class UsedbooktradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usedbooktrade
        fields = ['id', 'title', 'author', 'user_id', 'publisher', 'price', 'origin_imgfile', 'imgfile', 'description', 'damage_level', 'post_date', 'comment', 'is_sold']

class UsedbooktradeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsedbooktradeData
        fields = ['id', 'trade', 'user_id', 'sell_date']

class UsedbooktradeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usedbooktrade_Comment
        fields = ['id', 'user_id', 'Usedbookpost_id', 'parent_comment', 'contents', 'comment_date']    