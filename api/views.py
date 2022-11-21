from api.permissions import IsBlogUserOrReadOnly, IsCommentUserOrReadOnly
from blog.models import Comment, Post
from api.serializers import CommentSerializer, PostSerializer, RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view

from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.validators import ValidationError

# Create your views here.

class PostList(APIView):
    permission_classes = [IsBlogUserOrReadOnly]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class PostDetail(APIView):
    permission_classes = [IsBlogUserOrReadOnly]

    def get(self, request, pk):
        try:
            movie = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = Post.objects.get(pk=pk)
        serializer = PostSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        movie = Post.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentCreate(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        post = Post.objects.get(pk=pk)

        comment_user = self.request.user
        Comment_queryset = Comment.objects.filter(
            blog=post, user=comment_user)

        if Comment_queryset.exists():
            raise ValidationError(
                "This action cannot be done, You have already Commented this Movie")

        serializer.save(blog=post, user=comment_user)

class CommentList(generics.ListAPIView):
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Comment.objects.filter(blog=pk)

class CommentDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentUserOrReadOnly]

@api_view(['POST', ])
def register_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            account = serializer.save()

            data['response'] = "Account has been created successfully"
            data['username'] = account.username
            data['email'] = account.email

            token = Token.objects.get(user=account).key

            data['token'] = token

        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED)


@api_view(['POST', ])
def logout_view(request):

    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
