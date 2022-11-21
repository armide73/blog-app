from django.contrib.auth import get_user_model
from rest_framework import serializers

from blog.models import Comment, Post

User = get_user_model()
class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.first_name')
    likes = serializers.IntegerField(source='total_likes')
    class Meta:
        model = Post
        fields = "__all__"
            

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        # fields = "__all__"
        exclude = ("blog", "dateTime", )


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'error': 'Password doesn\'t match'})

        user_queryset = User.objects.filter(email=self.validated_data['email'])

        if user_queryset.exists():
            raise serializers.ValidationError(
                {'error': 'User email already exists'})

        account = User(
            email=self.validated_data['email'], username=self.validated_data['username'])

        account.set_password(password)
        account.save()

        return account
