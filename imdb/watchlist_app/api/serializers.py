from rest_framework import serializers
from watchlist_app.models import WatchList, StreamingPlatform

class StreamingPlatformSerializer(serializers.ModelSerializer):
    """
    Serializer for the StreamingPlatform model.
    """
    class Meta:
        model = StreamingPlatform
        fields = '__all__'
        read_only_fields = ('id',)
    
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

class WatchListSerializer(serializers.ModelSerializer):
    len_title = serializers.SerializerMethodField()
    
    """
    Serializer for the Movie model.
    """
    class Meta:
        model = WatchList
        fields = '__all__'
        read_only_fields = ('id', 'created_at')
    
    def get_len_title(self, obj):
        """
        Returns the length of the movie title.
        """
        return len(obj.title) if obj.title else 0
    
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