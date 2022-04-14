from rest_framework import serializers
from posts.models import Post, Group, Comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('title', 'slug', 'description')
        model = Group


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment
        read_only_fields = ('post',)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    comments = CommentSerializer(read_only=True, many=True)

    def create(self, validated_data):
        if 'group' not in self.initial_data:
            post = Post.objects.create(**validated_data)
            return post
        group = validated_data.pop('group')
        post = Post.objects.create(**validated_data, group=group)
        return post

    class Meta:
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date', 'comments')
        model = Post
