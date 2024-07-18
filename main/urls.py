from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', views.index, name='index'),
    path('user/', views.user_view, name='user'),

    path('api/request-info/', views.RequestInfoView.as_view(), name='request-info'),

    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/users/register/', views.RegisterView.as_view(), name='auth_register'),
    path('api/list/', views.getRoutes),
    path('api/login/', views.LoginView.as_view(), name='major-login'),

    # 홈화면 학과 카테고리 관련 API
    path('api/majors/', views.MajorList.as_view(), name='major-list'),
    path('api/majors/<int:pk>/', views.MajorDetail.as_view(), name='major-detail'),
    path('api/majors/search/', views.MajorSearchAPIView.as_view(), name='major-search'),
    path('api/majors/create/', views.MajorCreate.as_view(), name='major-create'),
    path('api/majors/<int:pk>/update/', views.MajorUpdate.as_view(), name='major-update'),

    path('api/profile/users/<int:pk>/', views.UserProfile.as_view(), name='user-profile'),
    path('api/profile/boards/<int:user_id>/', views.BoardListProfileByUserId.as_view(), name='board-list-profile-by-userid'),
    path('api/profile/studys/<int:user_id>/', views.StudyListProfileByUserId.as_view(), name='study-list-profile-by-userid'),
    path('api/profile/usedbooktrades/<int:user_id>/', views.UsedbooktradeListProfileByUserId.as_view(), name='usedbook-list-profile-by-userid'),

    path('api/users/', views.UserList.as_view(), name='user-list'),
    path('api/users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('api/users/<int:pk>/update/', views.UserUpdate.as_view(), name='user-update'),
    path('api/users/register/', views.UserRegisterAPIView.as_view(), name='user-register'),

    path('api/check_major/', views.MajorCheckAPIView.as_view(), name='check_major'),

    path('api/category/', views.CategoryList.as_view(), name='category-list'),
    path('api/category/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('api/category/create/', views.CategoryCreate.as_view(), name='category-create'),
    path('api/category/<int:pk>/', views.CategoryUpdate.as_view(), name='category-update'),

    # 학과 페이지별 커뮤니티 글 API
    path('api/<int:major_id>/boards/posts/', views.BoardList.as_view(), name='board-list'),
    path('api/<int:major_id>/boards/posts/<int:pk>/', views.BoardDetail.as_view(), name='board-detail'),
    path('api/<int:major_id>/boards/posts/search/', views.BoardSearchAPIView.as_view(), name='board-search'),
    # path('api/boards/posts-by-userid/<int:user_id>/', views.BoardListByUserId.as_view(), name='board-list-by-userid'),
    # path('api/boards/posts-by-category/<str:category_id>/', views.BoardListByCategory.as_view(), name='board-list-by-category'),
    path('api/boards/posts/create/', views.BoardCreate.as_view(), name='board-create'),
    path('api/boards/posts/<int:pk>/update/', views.BoardUpdate.as_view(), name='board-update'),
    path('api/boards/posts/<int:pk>/delete/', views.BoardDelete.as_view(), name='board-delete'),

    # 학과 페이지별 커뮤니티 댓글 API
    path('api/<int:major_id>/boards/posts/comments/', views.BoardCommentList.as_view(), name='board-comment-list'),
    path('api/<int:major_id>/boards/posts/comments/<int:pk>/', views.BoardCommentDetail.as_view(), name='board-comment-detail'),
    path('api/<int:major_id>/boards/posts/comments-by-userid/<int:user_id>/', views.BoardCommentListByUserId.as_view(), name='board-comment-list-by-userid'),
    path('api/<int:major_id>/boards/posts/comments-by-postid/<int:post_id>/', views.BoardCommentListByPostId.as_view(), name='board-comment-list-by-postid'),
    # path('api/boards/posts/comments-by-parent/<int:parent_comment>/', views.BoardCommentListByParent.as_view(), name='board-comment-list-by-parent'),
    path('api/boards/posts/comments/create/', views.BoardCommentCreate.as_view(), name='board-comment-create'),
    path('api/boards/posts/comments/<int:pk>/update/', views.BoardCommentUpdate.as_view(), name='board-comment-update'),
    path('api/boards/posts/comments/<int:pk>/delete/', views.BoardCommentDelete.as_view(), name='board-comment-delete'),

    path('api/boards/posts/likes/', views.BoardLikeList.as_view(), name='board-like-list'),
    path('api/boards/posts/likes-by-userid/<int:user_id>/', views.BoardLikeListByUserId.as_view(), name='board-like-list-by-userid'),
    path('api/boards/posts/likes-by-postid/<int:post_id>/', views.BoardLikeListByPostId.as_view(), name='board-like-list-by-postid'),
    path('api/boards/posts/likes/create/', views.BoardLikeCreate.as_view(), name='board-like-create'),

    path('api/boards/posts/bookmarks/', views.BoardBookmarkList.as_view(), name='board-bookmark-list'),
    path('api/boards/posts/bookmarks-by-userid/<int:user_id>/', views.BoardBookmarkListByUserId.as_view(), name='board-bookmark-list-by-userid'),
    path('api/boards/posts/bookmarks-by-postid/<int:post_id>/', views.BoardBookmarkListByPostId.as_view(), name='board-bookmark-list-by-postid'),
    path('api/boards/posts/bookmarks/create/', views.BoardBookmarkCreate.as_view(), name='board-bookmark-create'),

    # 학과 페이지별 스터디 글 API
    path('api/<int:major_id>/studys/posts/', views.StudyList.as_view(), name='study-list'),
    path('api/<int:major_id>/studys/posts/<int:pk>/', views.StudyDetail.as_view(), name='study-detail'),
    path('api/<int:major_id>/studys/posts/search/', views.StudySearchAPIView.as_view(), name='study-search'),
    # path('api/studys/posts-by-userid/<int:user_id>/', views.StudyListByUserId.as_view(), name='study-list-by-userid'),
    path('api/studys/posts/create/', views.StudyCreate.as_view(), name='study-create'),
    path('api/studys/posts/<int:pk>/update/', views.StudyUpdate.as_view(), name='study-update'),
    path('api/studys/posts/<int:pk>/delete/', views.StudyDelete.as_view(), name='study-delete'),

    # 학과 페이지별 스터디 댓글 API
    path('api/<int:major_id>/studys/posts/comments/', views.StudyCommentList.as_view(), name='study-comment-list'),
    path('api/<int:major_id>/studys/posts/comments/<int:pk>/', views.StudyCommentDetail.as_view(), name='study-comment-detail'),
    path('api/<int:major_id>/studys/posts/comments-by-userid/<int:user_id>/', views.StudyCommentListByUserId.as_view(), name='study-comment-list-by-userid'),
    path('api/<int:major_id>/studys/posts/comments-by-postid/<int:studypost_id>/', views.StudyCommentListByPostId.as_view(), name='study-comment-list-by-postid'),
    # path('api/studys/posts/comments-by-parent/<int:parent_comment>/', views.StudyCommentListByParent.as_view(), name='study-comment-list-by-parent'),
    path('api/studys/posts/comments/create/', views.StudyCommentCreate.as_view(), name='study-comment-create'),
    path('api/studys/posts/comments/<int:pk>/update/', views.StudyCommentUpdate.as_view(), name='study-comment-update'),
    path('api/studys/posts/comments/<int:pk>/delete/', views.StudyCommentDelete.as_view(), name='study-comment-delete'),

    path('api/studys/posts/likes/', views.StudyLikeList.as_view(), name='study-like-list'),
    path('api/studys/posts/likes-by-userid/<int:user_id>/', views.StudyLikeListByUserId.as_view(), name='study-like-list-by-userid'),
    path('api/studys/posts/likes-by-postid/<int:studypost_id>/', views.StudyLikeListByPostId.as_view(), name='study-like-list-by-postid'),
    path('api/studys/posts/likes/create/', views.StudyLikeCreate.as_view(), name='study-like-create'),

    path('api/usedbooktrades/book/search/', views.BookSearchAPIView.as_view(), name='book-search-api'),
    # path('api/usedbooktrades/book/search/select/', views.BookSelectAPIView.as_view(), name='book-select-api'),
    # path('api/usedbooktrades/book/search/select/post/', views.SaveUsedBookAPIView.as_view(), name='book-post-api'),
    path('api/usedbooktrades/book/create/', views.UsedbooktradeCreate.as_view(), name='usedbook-create-api'),
    path('api/usedbooktrades/book/<int:usedbooktrade_id>/sold/', views.UsedbooktradeSold.as_view(), name='usedbook-sold-api'),

    # 학과 페이지별 중고거래 글 API
    path('api/<int:major_id>/usedbooktrades/posts/', views.UsedbooktradeList.as_view(), name='usedbooktrade-list'),
    path('api/<int:major_id>/usedbooktrades/posts/<int:pk>/', views.UsedbooktradeDetail.as_view(), name='usedbooktrade-detail'),
    path('api/<int:major_id>/usedbooktrades/posts/search/', views.UsedbooktradeSearchAPIView.as_view(), name='usedbooktrade-search'),
    # path('api/usedbooktrades/posts-by-userid/<int:user_id>/', views.UsedbooktradeListByUserId.as_view(), name='usedbooktrade-list-by-userid'),
    # path('api/usedbooktrades/posts/create/', views.UsedbooktradeCreate.as_view(), name='usedbooktrade-create'),
    path('api/usedbooktrades/posts/<int:pk>/update/', views.UsedbooktradeUpdate.as_view(), name='usedbooktrade-update'),
    path('api/usedbooktrades/posts/<int:pk>/delete/', views.UsedbooktradeDelete.as_view(), name='usedbooktrade-delete'),

    path('api/usedbooktrades/data/', views.UsedbooktradedataList.as_view(), name='usedbooktradedata-list'),
    path('api/usedbooktrades/datas/<int:pk>/', views.UsedbooktradedataDetail.as_view(), name='usedbooktradedata-detail'),
    path('api/usedbooktrades/datas-by-tradeid/<int:trade_id>/', views.UsedbooktradedataListByTradeId.as_view(), name='usedbooktradedata-list-by-tradeid'),
    path('api/usedbooktrades/datas-by-sellerid/<int:seller_id>/', views.UsedbooktradedataListBySellerId.as_view(), name='usedbooktradedata-list-by-sellerid'),
    # path('api/usedbooktrades/datas/create/', views.UsedbooktradedataCreate.as_view(), name='usedbooktradedata-create'),
    path('api/usedbooktrades/datas/<int:pk>/update/', views.UsedbooktradedataUpdate.as_view(), name='usedbooktradedata-update'),
    path('api/usedbooktrades/datas/<int:pk>/delete/', views.UsedbooktradedataDelete.as_view(), name='usedbooktradedata-delete'),

    # 학과 페이지별 중고거래 댓글 API
    path('api/<int:major_id>/usedbooktrades/posts/comments/', views.UsedbooktradeCommentList.as_view(), name='usedbooktrade-comment-list'),
    path('api/<int:major_id>/usedbooktrades/posts/comments/<int:pk>/', views.UsedbooktradeCommentDetail.as_view(), name='usedbooktrade-comment-detail'),
    path('api/<int:major_id>/usedbooktrades/posts/comments-by-userid/<int:user_id>/', views.UsedbooktradeCommentListByUserId.as_view(), name='usedbooktrade-comment-list-by-userid'),
    path('api/<int:major_id>/usedbooktrades/posts/comments-by-postid/<int:Usedbookpost_id>/', views.UsedbooktradeCommentListByPostId.as_view(), name='usedbooktrade-comment-list-by-postid'),
    # path('api/usedbooktrades/posts/comments-by-parent/<int:parent_comment>/', views.UsedbooktradeCommentListByParent.as_view(), name='usedbooktrade-comment-list-by-parent'),
    path('api/usedbooktrades/posts/comments/create/', views.UsedbooktradeCommentCreate.as_view(), name='usedbooktrade-comment-create'),
    path('api/usedbooktrades/posts/comments/<int:pk>/update/', views.UsedbooktradeCommentUpdate.as_view(), name='usedbooktrade-comment-update'),
    path('api/usedbooktrades/posts/comments/<int:pk>/delete/', views.UsedbooktradeCommentDelete.as_view(), name='usedbooktrade-comment-delete'),

    # 멘토링 멘토 관련 API
    path('api/<int:major_id>/mentorings/mentor/posts/', views.MentoringList.as_view(), name='mentoring-list'),
    path('api/profile/mentorings/<int:user_id>/', views.MentoringListByUserId.as_view(), name='mentoring-list-profile-by-userid'),
    path('api/mentorings/mentor/posts/create/', views.MentoringCreate.as_view(), name='mentoring-create'),

    path('api/mentorings/mentee/approvals/create/', views.MenteeApprovalCreate.as_view(), name='mentee-aapproval-create'),

    # 멘토링 멘티 관련 API
    path('api/<int:major_id>/mentorings/mentee/posts/', views.MenteeList.as_view(), name='mentee-list'),
    path('api/profile/mentee/<int:user_id>/', views.MenteeListByUserId.as_view(), name='mentee-list-profile-by-userid'),
    path('api/mentorings/mentee/posts/create/', views.MenteeCreate.as_view(), name='mentee-create'),

    # 멘토링 내역 관련 API

    # 멘토링 리뷰 관련 API

    
]
