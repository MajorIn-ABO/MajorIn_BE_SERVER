from rest_framework import generics
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.utils import timezone  # 필요한 경우 추가
from django.http import JsonResponse
from .models import Token, Major, User, Category, Board, Board_Comment, Board_Like, Board_bookmark, Study, Study_Comment, Study_Like, Usedbooktrade, UsedbooktradeData, Usedbooktrade_Comment
from .serializers import MyTokenObtainPairSerializer, AuthUserRegisterSerializer, LoginSerializer,MajorSerializer, MajorCheckSerializer, UserSerializer, UserRegisterSerializer, CategorySerializer, BoardSerializer, BoardCommentSerializer, BoardLikeSerializer, BoardBookmarkSerializer, StudySerializer, StudyCommentSerializer, StudyLikeSerializer, UsedbooktradeSerializer, UsedbooktradeDataSerializer, UsedbooktradeCommentSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User as AuthUser
from rest_framework.authtoken.models import Token as AuthToken
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
import json
import requests
from django.db import transaction
from django.db.models import Q
from django.db.models import Prefetch
from urllib.parse import quote
from dotenv import load_dotenv
import os 
from django.core.files.storage import default_storage
from django.conf import settings

# load .env
load_dotenv()

NAVER_Client_ID = os.environ.get('Client_ID')
NAVER_Client_Secret = os.environ.get('Client_Secret')


# 로그인 관련 API 모음

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = AuthUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AuthUserRegisterSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/users/register/',
        '/api/token/refresh/'
    ]
    return Response(routes)

# 로그인 API
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data # validate()의 리턴값인 token을 받아온다.
        
        # 사용자 객체 조회
        user = get_object_or_404(User, id=token.user_id.id)

        token_data = {
            'user_id': token.user_id.id,
            'user_name': user.user_name,
            'school_name': user.school_name,
            'major_name': user.major_name,
            'admission_date': user.admission_date,
            'auth_id': token.auth_id.id,
            'refresh': token.refresh,
            'access': token.access
        }

        return Response({"message": "로그인에 성공했습니다.", "token": token_data}, status=status.HTTP_200_OK)

# 학과 관련 API 모음
class MajorList(generics.ListAPIView):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer

class MajorDetail(generics.RetrieveAPIView):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer

class MajorCreate(generics.CreateAPIView):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MajorUpdate(generics.UpdateAPIView):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer


# 유저 관련 API 모음
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

# 유저 회원가입 + 토큰 발급 API
class UserRegisterAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                # UserRegisterSerializer를 통해 유저 데이터 저장
                user = serializer.save()

                # AuthUserRegisterSerializer를 통해 AuthUser 생성
                auth_user_serializer = AuthUserRegisterSerializer(data={
                    'username': serializer.validated_data['home_id'],
                    'password': serializer.validated_data['home_password'],
                    'email': serializer.validated_data['email']
                })
                if auth_user_serializer.is_valid():
                    auth_user = auth_user_serializer.save()

                    # MyTokenObtainPairSerializer를 사용하여 토큰 발급
                    token_serializer = MyTokenObtainPairSerializer()
                    token = token_serializer.get_token(auth_user)
                    refresh_token = str(token)
                    access_token = str(token.access_token)

                    # 토큰 저장
                    token_data = {
                        'user_id': user,
                        'auth_id': auth_user,
                        'refresh': refresh_token,
                        'access': access_token
                    }

                    token = Token.objects.create(**token_data)

                    # user와 auth_user와 토큰 데이터를 하나의 응답 데이터로 묶어서 반환
                    res = Response(
                        {
                            "user_id": user.id,  # serializer.data
                            "auth_id": auth_user.id,
                            "message": "회원가입에 성공했습니다.",
                            "token": {
                                "access": access_token,
                                "refresh": refresh_token,
                            },
                        },
                        status=status.HTTP_200_OK,
                    )

                    # jwt 토큰 => 쿠키에 저장
                    res.set_cookie("access", access_token, httponly=True)
                    res.set_cookie("refresh", refresh_token, httponly=True)

                    return res
                else:
                    # AuthUser 등록 실패 시 User 데이터 롤백
                    user.delete()
                    return Response({'message': "등록할 수 없는 아이디 혹은 비밀번호 입니다."}, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                # 토큰 발급 및 저장 중에 오류가 발생한 경우
                user.delete()
                return Response({'message': "회원가입에 실패하였습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 사용자가 선택한 학과 카테고리가 올바른지 확인하는 API
class MajorCheckAPIView(APIView):
    queryset = Major.objects.all()
    serializer_class = MajorCheckSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        # serializer = MajorCheckSerializer(data=request.data)
        if serializer.is_valid():
            major_name = serializer.validated_data['major']
            major_category_name = serializer.validated_data['major_category_name']

            # 주어진 학과 카테고리에 해당하는 모든 Major 객체 가져오기
            major_data = Major.objects.filter(major_category_name=major_category_name)

            # 주어진 학과가 포함되어 있는지 확인
            for category in major_data:
                if major_name in category.major:
                    major_id = category.id
                    return Response({'message': True, 'major_id': major_id, 'major_category': major_category_name}, status=status.HTTP_201_CREATED)

            # 주어진 학과가 없는 경우
            return Response({'message': False}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 카테고리 관련 API 모음
class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetail(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryCreate(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryUpdate(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# 게시글 관련 API 모음

class BoardList(generics.ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        # 사용자 정보를 응답 데이터에 추가
        for data in response_data:
            user_id = data['user_id']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
            
            user_data = UserSerializer(user).data
            data['school_name'] = user_data['school_name']
            data['major_name'] = user_data['major_name']
            data['admission_date'] = user_data['admission_date']

        return Response(response_data, status=status.HTTP_200_OK)

class BoardListByUserId(generics.ListAPIView):
    serializer_class = BoardSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Board.objects.filter(user_id=user_id)
    
class BoardListByCategory(generics.ListAPIView):
    serializer_class = BoardSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Board.objects.filter(category_id=category_id)

class BoardDetail(generics.RetrieveAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # request 객체의 유저 속성들
        request_user_info = {
            "user": {
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email
            } if request.user.is_authenticated else None
        }
        
        # 게시글 작성자의 정보를 가져와 응답 데이터에 추가
        user_id = instance.user_id.id
        try:
            user_data = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        response_data = serializer.data
        response_data['school_name'] = user_data.school_name
        response_data['major_name'] = user_data.major_name
        response_data['admission_date'] = user_data.admission_date

        # 로그인된 사용자가 해당 게시글에 좋아요를 눌렀는지 확인
        # auth_user = request.user
        
        auth_id = request.user.id
        token = get_object_or_404(Token, auth_id=auth_id)
        login_user_id = token.user_id.id
        has_liked = Board_Like.objects.filter(user_id=login_user_id, post_id=instance.id, delete_date__isnull=True).exists()
        response_data['has_liked'] = has_liked

        # 로그인한 유저 객체의 속성들
        login_user_info = {
            "auth_id": auth_id,
            "user_id": login_user_id,
            "has_liked": has_liked
        }
        
        return Response(response_data, status=status.HTTP_200_OK)

class BoardCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # 이미지 파일 서버에 저장
            image_file = request.FILES.get('imgfile')
            if image_file:
                file_path = os.path.join(settings.MEDIA_ROOT, image_file.name)
                # file_path = default_storage.save(f"{settings.MEDIA_ROOT}/{image_file.name}", image_file)
                # 파일 경로를 serializer data에 추가
                request.data['imgfile'] = file_path
                
            # 게시글 생성
            self.perform_create(serializer)
            # 응답 데이터 준비
            response_data = serializer.data
            
            # 사용자 정보 가져오기
            user_id = response_data['user_id']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
            
            # 사용자 정보를 응답 데이터에 추가
            user_data = UserSerializer(user).data
            response_data['school_name'] = user_data['school_name']
            response_data['major_name'] = user_data['major_name']
            response_data['admission_date'] = user_data['admission_date']

            headers = self.get_success_headers(serializer.data)
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BoardUpdate(generics.UpdateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

class BoardDelete(generics.DestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

# api/boards/posts/search/?keyword=example
class BoardSearchAPIView(generics.ListAPIView):
    serializer_class = BoardSerializer
    queryset = Board.objects.all()  # 모든 커뮤니티게시판을 기본 queryset으로 설정

    def get_queryset(self):
        queryset = self.queryset

        keyword = self.request.query_params.get('keyword')

        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(contents__icontains=keyword)
            )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response({"message": "해당하는 글이 없습니다."})

        serializer = self.get_serializer(queryset, many=True)

        response_data = serializer.data

        # 사용자 정보를 응답 데이터에 추가
        for data in response_data:
            user_id = data['user_id']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
            
            user_data = UserSerializer(user).data
            data['school_name'] = user_data['school_name']
            data['major_name'] = user_data['major_name']
            data['admission_date'] = user_data['admission_date']

        return Response(response_data, status=status.HTTP_200_OK)

# 게시글 댓글 관련 API 모음

class BoardCommentList(generics.ListAPIView):
    queryset = Board_Comment.objects.all()
    serializer_class = BoardCommentSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        # 사용자 정보를 응답 데이터에 추가
        for data in response_data:
            user_id = data['user_id']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
            
            user_data = UserSerializer(user).data
            data['school_name'] = user_data['school_name']
            data['major_name'] = user_data['major_name']
            data['admission_date'] = user_data['admission_date']

        return Response(response_data, status=status.HTTP_200_OK)

class BoardCommentListByUserId(generics.ListAPIView):
    serializer_class = BoardCommentSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Board_Comment.objects.filter(user_id=user_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        # 사용자 정보를 응답 데이터에 추가
        for data in response_data:
            user_id = data['user_id']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
            
            user_data = UserSerializer(user).data
            data['school_name'] = user_data['school_name']
            data['major_name'] = user_data['major_name']
            data['admission_date'] = user_data['admission_date']

        return Response(response_data, status=status.HTTP_200_OK)
    
class BoardCommentListByPostId(generics.ListAPIView):
    serializer_class = BoardCommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Board_Comment.objects.filter(post_id=post_id).prefetch_related(
            Prefetch('replies', queryset=Board_Comment.objects.all())
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        # Cache for user info
        user_info_cache = {}

        def get_user_info(user_id):
            if user_id not in user_info_cache:
                try:
                    user = User.objects.get(id=user_id)
                    user_data = UserSerializer(user).data
                    user_info_cache[user_id] = {
                        "school_name": user_data['school_name'],
                        "major_name": user_data['major_name'],
                        "admission_date": user_data['admission_date']
                    }
                except User.DoesNotExist:
                    return None
            return user_info_cache[user_id]

        # Dictionary to hold parent comments and their replies
        comments_dict = {}

        for comment in response_data:
            user_info = get_user_info(comment['user_id'])
            if not user_info:
                continue

            comment_data = {
                "id": comment['id'],
                "user_id": comment['user_id'],
                "post_id": comment['post_id'],
                "parent_comment": comment['parent_comment'],
                "contents": comment['contents'],
                "comment_date": comment['comment_date'],
                "school_name": user_info['school_name'],
                "major_name": user_info['major_name'],
                "admission_date": user_info['admission_date'],
                "comments": []
            }

            if comment['parent_comment'] is None:
                comments_dict[comment['id']] = comment_data
            else:
                parent_id = comment['parent_comment']
                if parent_id in comments_dict:
                    parent_comment = comments_dict[parent_id]
                    parent_comment['comments'].append({
                        "commentId": comment['id'],
                        "user_id": comment['user_id'],
                        "school_name": user_info['school_name'],
                        "major_name": user_info['major_name'],
                        "admission_date": user_info['admission_date'],
                        "comment_date": comment['comment_date'],
                        "contents": comment['contents']
                    })

        final_response_data = list(comments_dict.values())

        return Response(final_response_data, status=status.HTTP_200_OK)

class BoardCommentListByParent(generics.ListAPIView):
    serializer_class = BoardCommentSerializer

    def get_queryset(self):
        parent_comment = self.kwargs['parent_comment']
        return Board_Comment.objects.filter(parent_comment=parent_comment)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        # 사용자 정보를 응답 데이터에 추가
        for data in response_data:
            user_id = data['user_id']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
            
            user_data = UserSerializer(user).data
            data['school_name'] = user_data['school_name']
            data['major_name'] = user_data['major_name']
            data['admission_date'] = user_data['admission_date']

        return Response(response_data, status=status.HTTP_200_OK)

class BoardCommentDetail(generics.RetrieveAPIView):
    queryset = Board_Comment.objects.all()
    serializer_class = BoardCommentSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # 스터디 작성자의 정보를 가져와 응답 데이터에 추가
        user_id = instance.user_id.id
        try:
            user_data = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        response_data = serializer.data

        response_data['school_name'] = user_data.school_name
        response_data['major_name'] = user_data.major_name
        response_data['admission_date'] = user_data.admission_date

        return Response(response_data, status=status.HTTP_200_OK)

class BoardCommentCreate(generics.CreateAPIView):
    queryset = Board_Comment.objects.all()
    serializer_class = BoardCommentSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # 저장 전 데이터 유효성 검사
            try:
                # 이미 `validated_data`에 외래 키 객체가 포함되어 있습니다.
                board_post = serializer.validated_data['post_id']
                user = serializer.validated_data['user_id']
                
                # 댓글 저장
                # comment = serializer.save()
                self.perform_create(serializer)

                # Board 게시글의 댓글 수 증가
                board_post.comment += 1
                board_post.save(update_fields=['comment'])
                
                # return Response({"message": "Comment created successfully.", "comments": board_post.comment}, status=status.HTTP_201_CREATED)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

            except Board.DoesNotExist:
                return Response({"error": "Board post not found."}, status=status.HTTP_404_NOT_FOUND)
            
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardCommentUpdate(generics.UpdateAPIView):
    queryset = Board_Comment.objects.all()
    serializer_class = BoardCommentSerializer

class BoardCommentDelete(generics.DestroyAPIView):
    queryset = Board_Comment.objects.all()

    def destroy(self, request, *args, **kwargs):

        # 우선은 누른 사람의 user_id를 파라미터로 주는 것으로 설정
        # user = request.user

        # user_id = request.data.get("user_id")
        # post_id = request.data.get("post_id")
        comment_id = kwargs.get("pk")  # pk는 URL에서 가져온 댓글의 기본 키 값
        
        try:
            board_comment = Board_Comment.objects.get(pk=comment_id)
        except Board_Comment.DoesNotExist:
            return Response({"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        '''
        # 댓글을 작성한 사용자와 요청한 사용자가 일치하는지 확인
        if user_id != board_comment.user_id.id:
            return Response({"error": "Unauthorized. You don't have permission to delete this comment."},
                            status=status.HTTP_403_FORBIDDEN)

        # 댓글이 속한 게시물과 요청한 게시물이 일치하는지 확인
        if post_id != board_comment.post_id.id:
            return Response({"error": "Invalid request. The comment does not belong to the specified post."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        '''

        board_comment.delete()

        # 게시물의 댓글 수 업데이트
        try:
            board_post = Board.objects.get(pk=board_comment.post_id.id)
        except Board.DoesNotExist:
            return Response({"error": "Board post not found."}, status=status.HTTP_404_NOT_FOUND)

        board_post.comment -= 1
        board_post.save(update_fields=['comment'])

        return Response({"message": "Comment deleted successfully.", "comments": board_post.comment}, status=status.HTTP_204_NO_CONTENT)

# 게시글 좋아요 관련 API

class BoardLikeList(generics.ListAPIView):
    queryset = Board_Comment.objects.all()
    serializer_class = BoardLikeSerializer

class BoardLikeListByUserId(generics.ListAPIView):
    serializer_class = BoardLikeSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Board_Like.objects.filter(user_id=user_id)
    
class BoardLikeListByPostId(generics.ListAPIView):
    serializer_class = BoardLikeSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Board_Like.objects.filter(post_id=post_id)


class BoardLikeCreate(generics.CreateAPIView):
    queryset = Board_Like.objects.all()
    serializer_class = BoardLikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        '''
        auth_id = request.user.id
        token = get_object_or_404(Token, auth_id=auth_id)
        login_user_id = token.user_id.id

        request_data = request.data.copy()
        request_data['user_id'] = login_user_id

        serializer = self.get_serializer(data=request_data)
        '''
        serializer = self.get_serializer(data=request.data)

        '''
        user = request.user
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Board, id=post_id)
        '''
        if serializer.is_valid():
            # 저장 전 데이터 유효성 검사
            try:
                # 이미 `validated_data`에 외래 키 객체가 포함되어 있습니다.
                board_post = serializer.validated_data['post_id']
                user = serializer.validated_data['user_id']
                
                with transaction.atomic():
                    existing_like = Board_Like.objects.filter(user_id=user, post_id=board_post).first()
                    if existing_like:
                        # 좋아요 취소
                        existing_like.delete()
                        board_post.like = max(0, board_post.like - 1)
                        board_post.save(update_fields=['like'])
                        return Response({"detail": "좋아요가 취소되었습니다.", "likes": board_post.like}, status=status.HTTP_200_OK)
                    else:
                        # 좋아요 추가
                        serializer = self.get_serializer(data={'user_id': user.id, 'post_id': board_post.id})
                        serializer.is_valid(raise_exception=True)
                        self.perform_create(serializer)
                        board_post.like += 1
                        board_post.save(update_fields=['like'])
                        headers = self.get_success_headers(serializer.data)
                        return Response({"detail": "좋아요가 추가되었습니다.", "likes": board_post.like}, status=status.HTTP_201_CREATED, headers=headers)

            except Board.DoesNotExist:
                return Response({"error": "Board post not found."}, status=status.HTTP_404_NOT_FOUND)
            
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# 게시글 북마크 관련 API

class BoardBookmarkList(generics.ListAPIView):
    queryset = Board_bookmark.objects.all()
    serializer_class = BoardBookmarkSerializer

class BoardBookmarkListByUserId(generics.ListAPIView):
    serializer_class = BoardBookmarkSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Board_bookmark.objects.filter(user_id=user_id)
    
class BoardBookmarkListByPostId(generics.ListAPIView):
    serializer_class = BoardBookmarkSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Board_bookmark.objects.filter(post_id=post_id)

class BoardBookmarkCreate(APIView):
    
    def post(self, request, post_id, user_id):
        # 우선은 누른 사람의 user_id를 파라미터로 주는 것으로 설정
        # user = request.user
        try:
            board_post = Board.objects.get(pk=post_id)
        except Board.DoesNotExist:
            return Response({"error": "Board post not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # 북마크를 이미 눌렀는지 확인
        is_kept = Board_bookmark.objects.filter(user_id=user, post_id=board_post).exists()

        if is_kept:
            # 이미 북마크를 누른 경우 북마크를 취소
            keep = Board_bookmark.objects.get(user_id=user, post_id=board_post)
            keep.delete()
            # keep.delete_date = timezone.now()  # delete_date 필드에 현재 시간 설정
            # keep.save()
            board_post.keep -= 1
            board_post.save(update_fields=['keep'])
            return Response({"message": "keep removed successfully.", "keeps": board_post.keep}, status=status.HTTP_200_OK)
        else:
            # 북마크를 누르지 않은 경우 북마크 추가
            keep = Board_bookmark(user_id=user, post_id=board_post)
            keep.save()
            board_post.keep += 1
            board_post.save(update_fields=['keep'])
            return Response({"message": "Keep created successfully.", "keeps": board_post.keep}, status=status.HTTP_201_CREATED)
    
# 스터디 관련 API 모음

class StudyList(generics.ListAPIView):
    queryset = Study.objects.all()
    serializer_class = StudySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        # 사용자 정보를 응답 데이터에 추가
        for data in response_data:
            # 해시태그 데이터를 문자열에서 리스트로 변환하여 추가합니다.
            hashtags_str = data['hashtags']
            data['hashtags'] = eval(hashtags_str)

            user_id = data['user_id']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
            
            user_data = UserSerializer(user).data
            data['school_name'] = user_data['school_name']
            data['major_name'] = user_data['major_name']
            data['admission_date'] = user_data['admission_date']

        return Response(response_data, status=status.HTTP_200_OK)

class StudyListByUserId(generics.ListAPIView):
    serializer_class = StudySerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Study.objects.filter(user_id=user_id)

class StudyDetail(generics.RetrieveAPIView):
    queryset = Study.objects.all()
    serializer_class = StudySerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # 스터디 작성자의 정보를 가져와 응답 데이터에 추가
        user_id = instance.user_id.id
        try:
            user_data = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        response_data = serializer.data

        # 해시태그 데이터를 문자열에서 리스트로 변환하여 추가합니다.
        hashtags_str = response_data['hashtags']
        response_data['hashtags'] = eval(hashtags_str)

        response_data['school_name'] = user_data.school_name
        response_data['major_name'] = user_data.major_name
        response_data['admission_date'] = user_data.admission_date

        # 로그인된 사용자가 해당 게시글에 좋아요를 눌렀는지 확인
        # auth_user = request.user
        
        auth_id = request.user.id
        token = get_object_or_404(Token, auth_id=auth_id)
        login_user_id = token.user_id.id
        has_liked = Study_Like.objects.filter(user_id=login_user_id, studypost_id=instance.id, delete_date__isnull=True).exists()
        response_data['has_liked'] = has_liked

        return Response(response_data, status=status.HTTP_200_OK)

class StudyCreate(generics.CreateAPIView):
    queryset = Study.objects.all()
    serializer_class = StudySerializer

    def create(self, request, *args, **kwargs):
        # hashtags 데이터를 문자열로 변환
        if 'hashtags' in request.data:
            hashtags = request.data['hashtags']
            if isinstance(hashtags, list):
                request.data['hashtags'] = str(hashtags)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudyUpdate(generics.UpdateAPIView):
    queryset = Study.objects.all()
    serializer_class = StudySerializer

class StudyDelete(generics.DestroyAPIView):
    queryset = Study.objects.all()
    serializer_class = StudySerializer

# api/studys/posts/search/?hashtag=원하는해시태그
# api/studys/posts/search/?keyword=example
# api/studys/posts/search/?hashtag=example1,example2&keyword=example
class StudySearchAPIView(generics.ListAPIView):
    serializer_class = StudySerializer
    queryset = Study.objects.all()  # 모든 스터디를 기본 queryset으로 설정

    def encode_hashtags(self, hashtags):
        encoded_hashtags = [quote(tag.strip()) for tag in hashtags]
        return encoded_hashtags

    def get_queryset(self):
        queryset = self.queryset

        hashtag = self.request.query_params.get('hashtag')
        keyword = self.request.query_params.get('keyword')

        if hashtag:
            # '#' 기호를 제거하고 쉼표(,)를 기준으로 문자열을 분리하여 리스트로 변환
            hashtags = hashtag.strip('#').split(',')

            # 검색된 해시태그를 URL 인코딩합니다.
            encoded_hashtags = self.encode_hashtags(hashtags)

            # 각 해시태그에 대해 필터링합니다.
            for tag in hashtags:
                queryset = queryset.filter(hashtags__contains=tag.strip())

        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(contents__icontains=keyword)
            )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response({"message": "해당하는 글이 없습니다."})

        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        for data in response_data:
            # 사용자 정보를 응답 데이터에 추가
            user_id = data['user_id']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
            
            user_data = UserSerializer(user).data
            data['school_name'] = user_data['school_name']
            data['major_name'] = user_data['major_name']
            data['admission_date'] = user_data['admission_date']

            # 각 스터디의 hashtags를 리스트화하여 반환
            hashtags_str = data['hashtags']
            data['hashtags'] = eval(hashtags_str)

        return Response(response_data, status=status.HTTP_200_OK)

# 스터디 댓글 관련 API 모음

class StudyCommentList(generics.ListAPIView):
    queryset = Study_Comment.objects.all()
    serializer_class = StudyCommentSerializer

    def list(self, request, *args, **kwargs):
        comments_with_replies = self.queryset.prefetch_related(
            Prefetch('replies', queryset=Study_Comment.objects.all())
        )

        serializer = self.get_serializer(comments_with_replies, many=True)
        response_data = serializer.data

        # Cache for user info
        user_info_cache = {}

        def get_user_info(user_id):
            if user_id not in user_info_cache:
                try:
                    user = User.objects.get(id=user_id)
                    user_data = UserSerializer(user).data
                    user_info_cache[user_id] = {
                        "school_name": user_data['school_name'],
                        "major_name": user_data['major_name'],
                        "admission_date": user_data['admission_date']
                    }
                except User.DoesNotExist:
                    return None
            return user_info_cache[user_id]

        # Dictionary to hold parent comments and their replies
        comments_dict = {}

        for comment in response_data:
            user_info = get_user_info(comment['user_id'])
            if not user_info:
                continue

            comment_data = {
                "id": comment['id'],
                "user_id": comment['user_id'],
                "studypost_id": comment['studypost_id'],
                "parent_comment": comment['parent_comment'],
                "contents": comment['contents'],
                "comment_date": comment['comment_date'],
                "school_name": user_info['school_name'],
                "major_name": user_info['major_name'],
                "admission_date": user_info['admission_date'],
                "comments": []
            }

            if comment['parent_comment'] is None:
                comments_dict[comment['id']] = comment_data
            else:
                parent_id = comment['parent_comment']
                if parent_id in comments_dict:
                    parent_comment = comments_dict[parent_id]
                    parent_comment['comments'].append({
                        "commentId": comment['id'],
                        "writer": f"{comment['user_id']} {user_info['school_name']} {user_info['major_name']} {user_info['admission_date']}학번",
                        "date": comment['comment_date'],
                        "content": comment['contents']
                    })

        final_response_data = list(comments_dict.values())

        return Response(final_response_data, status=status.HTTP_200_OK)

class StudyCommentListByUserId(generics.ListAPIView):
    serializer_class = StudyCommentSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Study_Comment.objects.filter(user_id=user_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        # 사용자 정보를 응답 데이터에 추가
        for data in response_data:
            user_id = data['user_id']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
            
            user_data = UserSerializer(user).data
            data['school_name'] = user_data['school_name']
            data['major_name'] = user_data['major_name']
            data['admission_date'] = user_data['admission_date']

        return Response(response_data, status=status.HTTP_200_OK)
    
class StudyCommentListByPostId(generics.ListAPIView):
    serializer_class = StudyCommentSerializer

    def get_queryset(self):
        studypost_id = self.kwargs['studypost_id']
        return Study_Comment.objects.filter(studypost_id=studypost_id).prefetch_related(
            Prefetch('replies', queryset=Study_Comment.objects.all())
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        # Cache for user info
        user_info_cache = {}

        def get_user_info(user_id):
            if user_id not in user_info_cache:
                try:
                    user = User.objects.get(id=user_id)
                    user_data = UserSerializer(user).data
                    user_info_cache[user_id] = {
                        "school_name": user_data['school_name'],
                        "major_name": user_data['major_name'],
                        "admission_date": user_data['admission_date']
                    }
                except User.DoesNotExist:
                    return None
            return user_info_cache[user_id]

        # Dictionary to hold parent comments and their replies
        comments_dict = {}

        for comment in response_data:
            user_info = get_user_info(comment['user_id'])
            if not user_info:
                continue

            comment_data = {
                "id": comment['id'],
                "user_id": comment['user_id'],
                "studypost_id": comment['studypost_id'],
                "parent_comment": comment['parent_comment'],
                "contents": comment['contents'],
                "comment_date": comment['comment_date'],
                "school_name": user_info['school_name'],
                "major_name": user_info['major_name'],
                "admission_date": user_info['admission_date'],
                "comments": []
            }

            if comment['parent_comment'] is None:
                comments_dict[comment['id']] = comment_data
            else:
                parent_id = comment['parent_comment']
                if parent_id in comments_dict:
                    parent_comment = comments_dict[parent_id]
                    parent_comment['comments'].append({
                        "commentId": comment['id'],
                        "user_id": comment['user_id'],
                        "school_name": user_info['school_name'],
                        "major_name": user_info['major_name'],
                        "admission_date": user_info['admission_date'],
                        "comment_date": comment['comment_date'],
                        "contents": comment['contents']
                    })

        final_response_data = list(comments_dict.values())

        return Response(final_response_data, status=status.HTTP_200_OK)

class StudyCommentListByParent(generics.ListAPIView):
    serializer_class = StudyCommentSerializer

    def get_queryset(self):
        parent_comment = self.kwargs['parent_comment']
        return Study_Comment.objects.filter(parent_comment=parent_comment)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        # 사용자 정보를 응답 데이터에 추가
        for data in response_data:
            user_id = data['user_id']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
            
            user_data = UserSerializer(user).data
            data['school_name'] = user_data['school_name']
            data['major_name'] = user_data['major_name']
            data['admission_date'] = user_data['admission_date']

        return Response(response_data, status=status.HTTP_200_OK)

class StudyCommentDetail(generics.RetrieveAPIView):
    queryset = Study_Comment.objects.all()
    serializer_class = StudyCommentSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # 스터디 작성자의 정보를 가져와 응답 데이터에 추가
        user_id = instance.user_id.id
        try:
            user_data = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        response_data = serializer.data

        response_data['school_name'] = user_data.school_name
        response_data['major_name'] = user_data.major_name
        response_data['admission_date'] = user_data.admission_date

        return Response(response_data, status=status.HTTP_200_OK)

class StudyCommentCreate(generics.CreateAPIView):
    queryset = Study_Comment.objects.all()
    serializer_class = StudyCommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # 저장 전 데이터 유효성 검사
            try:
                # 이미 `validated_data`에 외래 키 객체가 포함되어 있습니다.
                study_post = serializer.validated_data['studypost_id']
                user = serializer.validated_data['user_id']
                
                # 댓글 저장
                # comment = serializer.save()
                self.perform_create(serializer)

                # Study 게시글의 댓글 수 증가
                study_post.comment += 1
                study_post.save(update_fields=['comment'])
                
                # return Response({"message": "Comment created successfully.", "comments": study_post.comment}, status=status.HTTP_201_CREATED)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

            except Study.DoesNotExist:
                return Response({"error": "Study post not found."}, status=status.HTTP_404_NOT_FOUND)
            
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudyCommentUpdate(generics.UpdateAPIView):
    queryset = Study_Comment.objects.all()
    serializer_class = StudyCommentSerializer

class StudyCommentDelete(generics.DestroyAPIView):
    queryset = Study_Comment.objects.all()

    def destroy(self, request, *args, **kwargs):

        # 우선은 누른 사람의 user_id를 파라미터로 주는 것으로 설정
        # user = request.user

        # user_id = request.data.get("user_id")
        # studypost_id = request.data.get("studypost_id")
        comment_id = kwargs.get("pk")  # pk는 URL에서 가져온 댓글의 기본 키 값
        
        try:
            study_comment = Study_Comment.objects.get(pk=comment_id)
        except Study_Comment.DoesNotExist:
            return Response({"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        '''
        # 댓글을 작성한 사용자와 요청한 사용자가 일치하는지 확인
        if user_id != study_comment.user_id.id:
            return Response({"error": "Unauthorized. You don't have permission to delete this comment."},
                            status=status.HTTP_403_FORBIDDEN)

        # 댓글이 속한 스터디 게시물과 요청한 스터디 게시물이 일치하는지 확인
        if studypost_id != study_comment.studypost_id.id:
            return Response({"error": "Invalid request. The comment does not belong to the specified post."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        '''

        study_comment.delete()

        # 스터디 게시물의 댓글 수 업데이트
        try:
            study_post = Study.objects.get(pk=study_comment.studypost_id.id)
        except Study.DoesNotExist:
            return Response({"error": "Study post not found."}, status=status.HTTP_404_NOT_FOUND)

        study_post.comment -= 1
        study_post.save(update_fields=['comment'])

        return Response({"message": "Comment deleted successfully.", "comments": study_post.comment}, status=status.HTTP_204_NO_CONTENT)


# 스터디 좋아요 관련 API

class StudyLikeList(generics.ListAPIView):
    queryset = Study_Like.objects.all()
    serializer_class = StudyLikeSerializer

class StudyLikeListByUserId(generics.ListAPIView):
    serializer_class = StudyLikeSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Study_Like.objects.filter(user_id=user_id)
    
class StudyLikeListByPostId(generics.ListAPIView):
    serializer_class = StudyLikeSerializer

    def get_queryset(self):
        studypost_id = self.kwargs['studypost_id']
        return Study_Like.objects.filter(studypost_id=studypost_id)

class StudyLikeCreate(generics.CreateAPIView):
    queryset = Study_Like.objects.all()
    serializer_class = StudyLikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        '''
        auth_id = request.user.id
        token = get_object_or_404(Token, auth_id=auth_id)
        login_user_id = token.user_id.id

        request_data = request.data.copy()
        request_data['user_id'] = login_user_id

        serializer = self.get_serializer(data=request_data)
        '''
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # 저장 전 데이터 유효성 검사
            try:
                # 이미 `validated_data`에 외래 키 객체가 포함되어 있습니다.
                study_post = serializer.validated_data['studypost_id']
                user = serializer.validated_data['user_id']
                
                with transaction.atomic():
                    existing_like = Study_Like.objects.filter(user_id=user, studypost_id=study_post).first()
                    if existing_like:
                        # 좋아요 취소
                        existing_like.delete()
                        study_post.like = max(0, study_post.like - 1)
                        study_post.save(update_fields=['like'])
                        return Response({"detail": "좋아요가 취소되었습니다.", "likes": study_post.like}, status=status.HTTP_200_OK)
                    else:
                        # 좋아요 추가
                        serializer = self.get_serializer(data={'user_id': user.id, 'studypost_id': study_post.id})
                        serializer.is_valid(raise_exception=True)
                        self.perform_create(serializer)
                        study_post.like += 1
                        study_post.save(update_fields=['like'])
                        headers = self.get_success_headers(serializer.data)
                        return Response({"detail": "좋아요가 추가되었습니다.", "likes": study_post.like}, status=status.HTTP_201_CREATED, headers=headers)
                    
            except Study.DoesNotExist:
                return Response({"error": "Study post not found."}, status=status.HTTP_404_NOT_FOUND)
            
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 중고거래 관련 API 모음

class UsedbooktradeList(generics.ListAPIView):
    queryset = Usedbooktrade.objects.all()
    serializer_class = UsedbooktradeSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        # 사용자 정보를 응답 데이터에 추가
        for data in response_data:
            user_id = data['user_id']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
            
            user_data = UserSerializer(user).data
            data['school_name'] = user_data['school_name']
            data['major_name'] = user_data['major_name']
            data['admission_date'] = user_data['admission_date']

        return Response(response_data, status=status.HTTP_200_OK)

class UsedbooktradeListByUserId(generics.ListAPIView):
    serializer_class = UsedbooktradeSerializer

    def get_queryset(self):
        seller_id = self.kwargs['seller']
        return Usedbooktrade.objects.filter(seller=seller_id)

class UsedbooktradeDetail(generics.RetrieveAPIView):
    queryset = Usedbooktrade.objects.all()
    serializer_class = UsedbooktradeSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # 게시글 작성자의 정보를 가져와 응답 데이터에 추가
        user_id = instance.user_id.id
        try:
            user_data = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        response_data = serializer.data
        response_data['school_name'] = user_data.school_name
        response_data['major_name'] = user_data.major_name
        response_data['admission_date'] = user_data.admission_date

        return Response(response_data, status=status.HTTP_200_OK)


# 중고거래 글 작성

class UsedbooktradeCreate(generics.CreateAPIView):
    queryset = Usedbooktrade.objects.all()
    serializer_class = UsedbooktradeSerializer

    def create(self, request, *args, **kwargs):
        try:
            # 사용자 입력 데이터 추출
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # 이미지 파일 서버에 저장
            image_file = request.FILES.get('imgfile')
            if image_file:
                file_path = os.path.join(settings.MEDIA_ROOT, image_file.name)
                # file_path = default_storage.save(f"{settings.MEDIA_ROOT}/{image_file.name}", image_file)
                # 파일 경로를 serializer data에 추가
                request.data['imgfile'] = file_path

            self.perform_create(serializer)
            # 생성된 인스턴스 데이터 반환
            return Response({"message": "Usedbooktrade post created successfully.", "results": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UsedbooktradeUpdate(generics.UpdateAPIView):
    queryset = Usedbooktrade.objects.all()
    serializer_class = UsedbooktradeSerializer

class UsedbooktradeDelete(generics.DestroyAPIView):
    queryset = Usedbooktrade.objects.all()
    serializer_class = UsedbooktradeSerializer


# 데이터 임시 저장을 위한 클래스 

class SharedBookInfo:
    cached_book_info = {}

# 중고거래 도서 검색 API
# http://127.0.0.1:8000/api/usedbooktrades/book/search/?book_title=검색어

@method_decorator(csrf_exempt, name='dispatch')
class BookSearchAPIView(APIView):
    
    def get(self, request, *args, **kwargs):
        # 우선은 누른 사람의 user_id를 파라미터로 주는 것으로 설정
        # user = request.user
        try:
            # GET 요청에서 도서 이름 추출
            book_title = request.GET.get('book_title', '')

            book_data = search_books_by_title(book_title, NAVER_Client_ID, NAVER_Client_Secret)

            # 결과가 있는지 확인
            if 'items' in book_data and book_data['items']:
                # 검색 결과 반환
                # 전체 도서 정보를 클래스 변수에 저장
                '''
                SharedBookInfo.cached_book_info[book_title] = {
                    'title': book_data['items'][0].get('title', ''),
                    'author': book_data['items'][0].get('author', ''),
                    'publisher': book_data['items'][0].get('publisher', ''),
                    'price': book_data['items'][0].get('discount', ''),
                    'imgfile': book_data['items'][0].get('image', ''),
                }
                '''

                # JsonResponse를 사용하여 검색 결과 데이터를 응답으로 반환
                return JsonResponse({'success': True, 'book_data_list': book_data['items']})

                # return render(request, 'main/book_search_result.html', {'book_data_list': book_data['items']})
                # return JsonResponse(SharedBookInfo.cached_book_info[book_title])
                # return JsonResponse({'success': True, 'data': book_data['items'][0]})
            else:
                # 검색 결과가 없을 경우
                return JsonResponse({'success': False, 'message': '도서를 찾을 수 없습니다.'}, status=404)
                # return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
              
        except Exception as e:
            # 예외 처리
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
        

# 네이버 API 사용 외부 데이터 가져오는 코드

def search_books_by_title(book_title, client_id, client_secret):
    # 네이버 도서 검색 API 엔드포인트
    naver_api_url = f'https://openapi.naver.com/v1/search/book.json'

    # API에 전송할 파라미터 설정
    params = {'query': book_title, 'display': 15}

    # 네이버 API 요청에 필요한 헤더 설정
    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret}

    # API 요청 보내기
    response = requests.get(naver_api_url, params=params, headers=headers)

    # 응답 확인
    if response.status_code == 200:
        # JSON 형태로 반환된 응답 데이터를 파이썬 딕셔너리로 변환
        
        return response.json()

    else:
        # API 요청이 실패한 경우 에러 코드 출력
        return JsonResponse({'success': False, 'message': f'API 요청 실패 - 상태 코드: {response.status_code}'}, status=500)


# 중고거래 거래내역 관련 API 모음

class UsedbooktradeSold(APIView):
    def post(self, request, usedbooktrade_id):
        # 해당 책 모델 조회
        usedbooktrade = get_object_or_404(Usedbooktrade, id=usedbooktrade_id)

        # 판매자 확인 (현재 로그인한 사용자를 판매자로 설정)
        # seller = request.user

        user_id = usedbooktrade.user_id

        # 책이 판매되지 않았다면
        if usedbooktrade.is_sold == False:
            # is_sold 컬럼을 True로 업데이트
            usedbooktrade.is_sold = True
            usedbooktrade.save()

            # UsedbooktradeData에 판매된 책 데이터 등록
            UsedbooktradeData.objects.create(trade=usedbooktrade, user_id=user_id)

            return Response({"message": "책이 성공적으로 판매되었습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "이미 판매된 책입니다."}, status=status.HTTP_400_BAD_REQUEST)

class UsedbooktradedataList(generics.ListAPIView):
    queryset = UsedbooktradeData.objects.all()
    serializer_class = UsedbooktradeDataSerializer

class UsedbooktradedataListByTradeId(generics.ListAPIView):
    serializer_class = UsedbooktradeDataSerializer

    def get_queryset(self):
        trade_id = self.kwargs['trade']
        return UsedbooktradeData.objects.filter(trade=trade_id)
    
class UsedbooktradedataListBySellerId(generics.ListAPIView):
    serializer_class = UsedbooktradeDataSerializer

    def get_queryset(self):
        sellerid = self.kwargs['sellerid']
        return UsedbooktradeData.objects.filter(sellerid=sellerid)

class UsedbooktradedataDetail(generics.RetrieveAPIView):
    queryset = UsedbooktradeData.objects.all()
    serializer_class = UsedbooktradeDataSerializer

'''
class UsedbooktradedataCreate(generics.CreateAPIView):
    queryset = UsedbooktradeData.objects.all()
    serializer_class = UsedbooktradeDataSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''

class UsedbooktradedataUpdate(generics.UpdateAPIView):
    queryset = UsedbooktradeData.objects.all()
    serializer_class = UsedbooktradeDataSerializer

class UsedbooktradedataDelete(generics.DestroyAPIView):
    queryset = UsedbooktradeData.objects.all()
    serializer_class = UsedbooktradeDataSerializer

# 중고거래 글 검색
# api/usedbooktrades/posts/search/?keyword=example
class UsedbooktradeSearchAPIView(generics.ListAPIView):
    serializer_class = UsedbooktradeSerializer
    queryset = Usedbooktrade.objects.all()  # 모든 중고거래게시판을 기본 queryset으로 설정

    def get_queryset(self):
        queryset = self.queryset

        keyword = self.request.query_params.get('keyword')

        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(author__icontains=keyword) | Q(publisher__icontains=keyword) | Q(description__icontains=keyword)
            )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response({"message": "해당하는 글이 없습니다."})

        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        for data in response_data:
            # 사용자 정보를 응답 데이터에 추가
            user_id = data['user_id']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
            
            user_data = UserSerializer(user).data
            data['school_name'] = user_data['school_name']
            data['major_name'] = user_data['major_name']
            data['admission_date'] = user_data['admission_date']

        return Response(response_data, status=status.HTTP_200_OK)



# 중고거래 댓글 관련 API 모음

class UsedbooktradeCommentList(generics.ListAPIView):
    queryset = Usedbooktrade_Comment.objects.all()
    serializer_class = UsedbooktradeCommentSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        # 사용자 정보를 응답 데이터에 추가
        for data in response_data:
            user_id = data['user_id']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
            
            user_data = UserSerializer(user).data
            data['school_name'] = user_data['school_name']
            data['major_name'] = user_data['major_name']
            data['admission_date'] = user_data['admission_date']

        return Response(response_data, status=status.HTTP_200_OK)

class UsedbooktradeCommentListByUserId(generics.ListAPIView):
    serializer_class = UsedbooktradeCommentSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Usedbooktrade_Comment.objects.filter(user_id=user_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        # 사용자 정보를 응답 데이터에 추가
        for data in response_data:
            user_id = data['user_id']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
            
            user_data = UserSerializer(user).data
            data['school_name'] = user_data['school_name']
            data['major_name'] = user_data['major_name']
            data['admission_date'] = user_data['admission_date']

        return Response(response_data, status=status.HTTP_200_OK)
    
class UsedbooktradeCommentListByPostId(generics.ListAPIView):
    serializer_class = UsedbooktradeCommentSerializer

    def get_queryset(self):
        Usedbookpost_id = self.kwargs['Usedbookpost_id']
        return Usedbooktrade_Comment.objects.filter(Usedbookpost_id=Usedbookpost_id).prefetch_related(
            Prefetch('replies', queryset=Usedbooktrade_Comment.objects.all())
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        # Cache for user info
        user_info_cache = {}

        def get_user_info(user_id):
            if user_id not in user_info_cache:
                try:
                    user = User.objects.get(id=user_id)
                    user_data = UserSerializer(user).data
                    user_info_cache[user_id] = {
                        "school_name": user_data['school_name'],
                        "major_name": user_data['major_name'],
                        "admission_date": user_data['admission_date']
                    }
                except User.DoesNotExist:
                    return None
            return user_info_cache[user_id]

        # Dictionary to hold parent comments and their replies
        comments_dict = {}

        for comment in response_data:
            user_info = get_user_info(comment['user_id'])
            if not user_info:
                continue

            comment_data = {
                "id": comment['id'],
                "user_id": comment['user_id'],
                "Usedbookpost_id": comment['Usedbookpost_id'],
                "parent_comment": comment['parent_comment'],
                "contents": comment['contents'],
                "comment_date": comment['comment_date'],
                "school_name": user_info['school_name'],
                "major_name": user_info['major_name'],
                "admission_date": user_info['admission_date'],
                "comments": []
            }

            if comment['parent_comment'] is None:
                comments_dict[comment['id']] = comment_data
            else:
                parent_id = comment['parent_comment']
                if parent_id in comments_dict:
                    parent_comment = comments_dict[parent_id]
                    parent_comment['comments'].append({
                        "commentId": comment['id'],
                        "user_id": comment['user_id'],
                        "school_name": user_info['school_name'],
                        "major_name": user_info['major_name'],
                        "admission_date": user_info['admission_date'],
                        "comment_date": comment['comment_date'],
                        "contents": comment['contents']
                    })

        final_response_data = list(comments_dict.values())

        return Response(final_response_data, status=status.HTTP_200_OK)

class UsedbooktradeCommentListByParent(generics.ListAPIView):
    serializer_class = UsedbooktradeCommentSerializer

    def get_queryset(self):
        parent_comment = self.kwargs['parent_comment']
        return Usedbooktrade_Comment.objects.filter(parent_comment=parent_comment)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        # 사용자 정보를 응답 데이터에 추가
        for data in response_data:
            user_id = data['user_id']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
            
            user_data = UserSerializer(user).data
            data['school_name'] = user_data['school_name']
            data['major_name'] = user_data['major_name']
            data['admission_date'] = user_data['admission_date']

        return Response(response_data, status=status.HTTP_200_OK)

class UsedbooktradeCommentDetail(generics.RetrieveAPIView):
    queryset = Usedbooktrade_Comment.objects.all()
    serializer_class = UsedbooktradeCommentSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # 스터디 작성자의 정보를 가져와 응답 데이터에 추가
        user_id = instance.user_id.id
        try:
            user_data = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        response_data = serializer.data

        response_data['school_name'] = user_data.school_name
        response_data['major_name'] = user_data.major_name
        response_data['admission_date'] = user_data.admission_date

        return Response(response_data, status=status.HTTP_200_OK)

class UsedbooktradeCommentCreate(generics.CreateAPIView):
    queryset = Usedbooktrade_Comment.objects.all()
    serializer_class = UsedbooktradeCommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # 저장 전 데이터 유효성 검사
            try:
                # 이미 `validated_data`에 외래 키 객체가 포함되어 있습니다.
                Usedbookpost = serializer.validated_data['Usedbookpost_id']
                user = serializer.validated_data['user_id']
                
                # 댓글 저장
                # comment = serializer.save()
                self.perform_create(serializer)

                # Usedbookpost 게시글의 댓글 수 증가
                Usedbookpost.comment += 1
                Usedbookpost.save(update_fields=['comment'])
                
                # return Response({"message": "Comment created successfully.", "comments": Usedbookpost.comment}, status=status.HTTP_201_CREATED)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

            except Usedbooktrade.DoesNotExist:
                return Response({"error": "Usedbookpost not found."}, status=status.HTTP_404_NOT_FOUND)
            
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsedbooktradeCommentUpdate(generics.UpdateAPIView):
    queryset = Usedbooktrade_Comment.objects.all()
    serializer_class = UsedbooktradeCommentSerializer

class UsedbooktradeCommentDelete(generics.DestroyAPIView):
    queryset = Usedbooktrade_Comment.objects.all()

    def destroy(self, request, *args, **kwargs):

        # 우선은 누른 사람의 user_id를 파라미터로 주는 것으로 설정
        # user = request.user

        # user_id = request.data.get("user_id")
        # Usedbookpost_id = request.data.get("Usedbookpost_id")
        comment_id = kwargs.get("pk")  # pk는 URL에서 가져온 댓글의 기본 키 값
        
        try:
            Usedbooktrade_comment = Usedbooktrade_Comment.objects.get(pk=comment_id)
        except Usedbooktrade_Comment.DoesNotExist:
            return Response({"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        '''
        # 댓글을 작성한 사용자와 요청한 사용자가 일치하는지 확인
        if user_id != study_comment.user_id.id:
            return Response({"error": "Unauthorized. You don't have permission to delete this comment."},
                            status=status.HTTP_403_FORBIDDEN)

        # 댓글이 속한 스터디 게시물과 요청한 스터디 게시물이 일치하는지 확인
        if studypost_id != study_comment.studypost_id.id:
            return Response({"error": "Invalid request. The comment does not belong to the specified post."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        '''

        Usedbooktrade.delete()

        # 중고거래 게시물의 댓글 수 업데이트
        try:
            usedbook_post = Usedbooktrade.objects.get(pk=Usedbooktrade_comment.Usedbookpost_id.id)
        except Usedbooktrade.DoesNotExist:
            return Response({"error": "Usedbooktrade post not found."}, status=status.HTTP_404_NOT_FOUND)

        usedbook_post.comment -= 1
        usedbook_post.save(update_fields=['comment'])

        return Response({"message": "Comment deleted successfully.", "comments": usedbook_post.comment}, status=status.HTTP_204_NO_CONTENT)


# 유저 request data 받아오는 api

class RequestInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # request 객체의 주요 속성들
        request_info = {
            "method": request.method,
            "headers": dict(request.headers),
            "GET_params": request.GET.dict(),
            "POST_params": request.POST.dict(),
            "body": request.body.decode('utf-8'),  # request body (json이나 form data 등)
            "user": {
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email
            } if request.user.is_authenticated else None,
            "META": {
                "REMOTE_ADDR": request.META.get("REMOTE_ADDR"),
                "HTTP_USER_AGENT": request.META.get("HTTP_USER_AGENT")
            }
        }
        return Response(request_info)

# Create your views here.
def index(request):
    return render(request,'main/index.html')

def user_view(request):
    users = User.objects.all() # user 테이블의 모든 객체 불러와서 users 변수에 저장 
    return render(request,'main/user_view.html',{'users':users})

