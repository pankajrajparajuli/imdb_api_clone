from rest_framework import serializers
from watchlist_app.models import Movie

class MovieSerializer(serializers.Serializer):
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
        return instance
