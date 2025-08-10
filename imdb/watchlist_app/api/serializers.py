from rest_framework import serializers
from watchlist_app.models import WatchList, StreamingPlatform, Review

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    """
    Serializer for the Review model.
    """
    class Meta:
        model = Review
        exclude = ('watchlist',)
        read_only_fields = ('id', 'created_at')
    
    def validate(self, attrs):
        if not attrs.get('review_text'):
            raise serializers.ValidationError("Review text is required.")
        if attrs.get('rating') is None:
            raise serializers.ValidationError("Rating is required.")
        return attrs
    
    def validate_rating(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Rating must be between 1 and 10.")
        return value
    
class WatchListSerializer(serializers.ModelSerializer):
    reviews= ReviewSerializer(many=True, read_only=True)
    len_title = serializers.SerializerMethodField()
    """
    Serializer for the Movie model.
    """
    class Meta:
        model = WatchList
        fields = ('__all__')
        read_only_fields = ('id', 'created_at')
    
    def get_len_title(self, obj):
        """
        Returns the length of the movie title.
        """
        return len(obj.title)
    
    def validate(self, attrs):
        if not attrs.get('title'):
            raise serializers.ValidationError("Title is required.")
        if not attrs.get('description'):
            raise serializers.ValidationError("Description is required.")
        if attrs.get('rating') is None:
            raise serializers.ValidationError("Rating is required.")
        if attrs.get('release_date') is None:
            raise serializers.ValidationError("Release date is required.")
        return attrs
    
    def validate(self,attrs):
        if attrs['title'] == attrs['description']:
            raise serializers.ValidationError("Title and description cannot be the same.")
        return attrs
    
    def validate_title(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        if len(value) > 100:
            raise serializers.ValidationError("Name must be at most 100 characters long.")
        return value
    
    def validate_description(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Description must be at least 10 characters long.")
        return value
    
    def validate_rating(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError("Rating must be between 0 and 10.")
        return value
    
    def validate_release_date(self, value):
        if value > serializers.DateField().today():
            raise serializers.ValidationError("Release date cannot be in the future.")
        return value
    
    def validate_active(self, value):
        if not isinstance(value, bool):
            raise serializers.ValidationError("Active must be a boolean value.")
        return value

class StreamingPlatformSerializer(serializers.ModelSerializer):
    """
    Serializer for the StreamingPlatform model.
    """
    watchlist = WatchListSerializer(many=True, read_only=True)
    
    class Meta:
        model = StreamingPlatform
        fields = ('__all__')
        read_only_fields = ('id', 'created_at')
    
    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        if len(value) > 100:
            raise serializers.ValidationError("Name must be at most 100 characters long.")
        return value
    
    def validate_website(self, value):
        if value and not value.startswith('http'):
            raise serializers.ValidationError("Website must start with 'http' or 'https'.")
        return value

""" class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    active = serializers.BooleanField()
    release_date = serializers.DateField()
    rating = serializers.DecimalField(max_digits=3, decimal_places=1)
    created_at = serializers.DateTimeField()
    
    def create(self, validated_data):
        Movie.objects.create(**validated_data)
        return validated_data
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.release_date = validated_data.get('release_date', instance.release_date)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance """
    
    