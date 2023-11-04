from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from .models import User, Board, Board_Comment, Board_Like, Board_bookmark, Study, Study_Comment, Study_Like
from .serializers import UserSerializer, BoardSerializer, BoardCommentSerializer, BoardLikeSerializer, BoardBookmarkSerializer, StudySerializer, StudyCommentSerializer, StudyLikeSerializer

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
    serializer_class = UserSerializer


# 게시글 관련 API 모음

class BoardList(generics.ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

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

class BoardCreate(generics.CreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BoardUpdate(generics.UpdateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

class BoardDelete(generics.DestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


# 게시글 댓글 관련 API 모음

class BoardCommentList(generics.ListAPIView):
    queryset = Board_Comment.objects.all()
    serializer_class = BoardCommentSerializer

class BoardCommentListByUserId(generics.ListAPIView):
    serializer_class = BoardCommentSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Board_Comment.objects.filter(user_id=user_id)
    
class BoardCommentListByPostId(generics.ListAPIView):
    serializer_class = BoardCommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Board_Comment.objects.filter(post_id=post_id)

class BoardCommentListByParent(generics.ListAPIView):
    serializer_class = BoardCommentSerializer

    def get_queryset(self):
        parent_comment = self.kwargs['parent_comment']
        return Board_Comment.objects.filter(parent_comment=parent_comment)

class BoardCommentDetail(generics.RetrieveAPIView):
    queryset = Board_Comment.objects.all()
    serializer_class = BoardCommentSerializer

class BoardCommentCreate(generics.CreateAPIView):
    queryset = Board_Comment.objects.all()
    serializer_class = BoardCommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BoardCommentUpdate(generics.UpdateAPIView):
    queryset = Board_Comment.objects.all()
    serializer_class = BoardCommentSerializer

class BoardCommentDelete(generics.DestroyAPIView):
    queryset = Board_Comment.objects.all()
    serializer_class = BoardCommentSerializer

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

class BoardLikeDetail(generics.RetrieveAPIView):
    queryset = Board_Like.objects.all()
    serializer_class = BoardLikeSerializer

class BoardLikeCreate(generics.CreateAPIView):
    queryset = Board_Like.objects.all()
    serializer_class = BoardLikeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
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

class BoardBookmarkDetail(generics.RetrieveAPIView):
    queryset = Board_bookmark.objects.all()
    serializer_class = BoardBookmarkSerializer

class BoardBookmarkCreate(generics.CreateAPIView):
    queryset = Board_bookmark.objects.all()
    serializer_class = BoardBookmarkSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 스터디 관련 API 모음

class StudyList(generics.ListAPIView):
    queryset = Study.objects.all()
    serializer_class = StudySerializer

class StudyListByUserId(generics.ListAPIView):
    serializer_class = StudySerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Study.objects.filter(user_id=user_id)

class StudyDetail(generics.RetrieveAPIView):
    queryset = Study.objects.all()
    serializer_class = StudySerializer

class StudyCreate(generics.CreateAPIView):
    queryset = Study.objects.all()
    serializer_class = StudySerializer

    def create(self, request, *args, **kwargs):
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


# 스터디 댓글 관련 API 모음

class StudyCommentList(generics.ListAPIView):
    queryset = Study_Comment.objects.all()
    serializer_class = StudyCommentSerializer

class StudyCommentListByUserId(generics.ListAPIView):
    serializer_class = StudyCommentSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Study_Comment.objects.filter(user_id=user_id)
    
class StudyCommentListByPostId(generics.ListAPIView):
    serializer_class = StudyCommentSerializer

    def get_queryset(self):
        studypost_id = self.kwargs['studypost_id']
        return Study_Comment.objects.filter(studypost_id=studypost_id)

class StudyCommentListByParent(generics.ListAPIView):
    serializer_class = StudyCommentSerializer

    def get_queryset(self):
        parent_comment = self.kwargs['parent_comment']
        return Study_Comment.objects.filter(parent_comment=parent_comment)

class StudyCommentDetail(generics.RetrieveAPIView):
    queryset = Study_Comment.objects.all()
    serializer_class = StudyCommentSerializer

class StudyCommentCreate(generics.CreateAPIView):
    queryset = Study_Comment.objects.all()
    serializer_class = StudyCommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudyCommentUpdate(generics.UpdateAPIView):
    queryset = Study_Comment.objects.all()
    serializer_class = StudyCommentSerializer

class StudyCommentDelete(generics.DestroyAPIView):
    queryset = Study_Comment.objects.all()
    serializer_class = StudyCommentSerializer


# 스터디 좋아요 관련 API

class StudyLikeList(generics.ListAPIView):
    queryset = Study_Comment.objects.all()
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

class StudyLikeCreate(APIView):
    
    def post(self, request, post_id, user_id):
        # 우선은 누른 사람의 user_id를 파라미터로 주는 것으로 설정
        # user = request.user
        try:
            study_post = Study.objects.get(pk=post_id)
        except Study.DoesNotExist:
            return Response({"error": "Study post not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # 좋아요를 이미 눌렀는지 확인
        is_liked = Study_Like.objects.filter(user_id=user, studypost_id=study_post).exists()

        if is_liked:
            # 이미 좋아요를 누른 경우 좋아요를 취소
            like = Study_Like.objects.get(user_id=user, studypost_id=study_post)
            like.delete()
            study_post.like -= 1
            study_post.save()
            return Response({"message": "Like removed.", "likes": study_post.like}, status=status.HTTP_200_OK)
        else:
            # 좋아요를 누르지 않은 경우 좋아요 추가
            like = Study_Like(user_id=user, studypost_id=study_post)
            like.save()
            study_post.like += 1
            study_post.save()
            return Response({"message": "Liked.", "likes": study_post.like}, status=status.HTTP_201_CREATED)


# Create your views here.
def index(request):
    return render(request,'main/index.html')

def user_view(request):
    users = User.objects.all() # user 테이블의 모든 객체 불러와서 users 변수에 저장 
    return render(request,'main/user_view.html',{'users':users})

