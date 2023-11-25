from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.utils import timezone  # 필요한 경우 추가
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
        # serializer = BoardCommentSerializer(data=request.data)

        if serializer.is_valid():
            # 우선은 누른 사람의 user_id를 파라미터로 주는 것으로 설정
            # user = request.user

            user_id = serializer.validated_data["user_id"].id
            post_id = serializer.validated_data["post_id"].id
            contents = serializer.validated_data["contents"]
            
            try:
                board_post = Board.objects.get(pk=post_id)
            except Board.DoesNotExist:
                return Response({"error": "Board post not found."}, status=status.HTTP_404_NOT_FOUND)

            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            
            # serializer.save()  # 댓글을 저장하고
        
            comment = Board_Comment(user_id=user, post_id=board_post, contents=contents)
            comment.save()

            board_post.comment += 1
            board_post.save(update_fields=['comment'])
            return Response({"message": "Commented.", "comments": board_post.comment}, status=status.HTTP_201_CREATED)
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

class BoardLikeCreate(APIView):
    
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
        
        # 좋아요를 이미 눌렀는지 확인
        is_liked = Board_Like.objects.filter(user_id=user, post_id=board_post).exists()

        if is_liked:
            # 이미 좋아요를 누른 경우 좋아요를 취소
            like = Board_Like.objects.get(user_id=user, post_id=board_post)
            like.delete()
            # like.delete_date = timezone.now()  # delete_date 필드에 현재 시간 설정
            # like.save()
            board_post.like -= 1
            board_post.save(update_fields=['like'])
            return Response({"message": "Like removed.", "likes": board_post.like}, status=status.HTTP_200_OK)
        else:
            # 좋아요를 누르지 않은 경우 좋아요 추가
            like = Board_Like(user_id=user, post_id=board_post)
            like.save()
            board_post.like += 1
            board_post.save(update_fields=['like'])
            return Response({"message": "Liked.", "likes": board_post.like}, status=status.HTTP_201_CREATED)

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
            return Response({"message": "keep removed.", "keeps": board_post.keep}, status=status.HTTP_200_OK)
        else:
            # 북마크를 누르지 않은 경우 북마크 추가
            keep = Board_bookmark(user_id=user, post_id=board_post)
            keep.save()
            board_post.keep += 1
            board_post.save(update_fields=['keep'])
            return Response({"message": "Keep successed.", "keeps": board_post.keep}, status=status.HTTP_201_CREATED)
    
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
            # like.delete_date = timezone.now()  # delete_date 필드에 현재 시간 설정
            # like.save()
            study_post.like -= 1
            study_post.save(update_fields=['like'])
            return Response({"message": "Like removed.", "likes": study_post.like}, status=status.HTTP_200_OK)
        else:
            # 좋아요를 누르지 않은 경우 좋아요 추가
            like = Study_Like(user_id=user, studypost_id=study_post)
            like.save()
            study_post.like += 1
            study_post.save(update_fields=['like'])
            return Response({"message": "Liked.", "likes": study_post.like}, status=status.HTTP_201_CREATED)


# Create your views here.
def index(request):
    return render(request,'main/index.html')

def user_view(request):
    users = User.objects.all() # user 테이블의 모든 객체 불러와서 users 변수에 저장 
    return render(request,'main/user_view.html',{'users':users})

