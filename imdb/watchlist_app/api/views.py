from watchlist_app.models import WatchList, StreamingPlatform, Review
#from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from watchlist_app.api.serializers import WatchListSerializer, StreamingPlatformSerializer, ReviewSerializer
from rest_framework import status, generics, mixins

class WatchListView(APIView):
    """ 
    List all movies or create a new movie.
    """
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WatchListDetailView(APIView):
    """ 
    Retrieve, update or delete a movie instance.
    """
    def get_object(self, pk):
        try:
            return WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return None

    def get(self, request, pk):
        movie = self.get_object(pk)
        if movie is None:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        movie = self.get_object(pk)
        if movie is None:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = self.get_object(pk)
        if movie is None:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ReviewCreateView(generics.CreateAPIView):
    """
    Create a new review for a movie one user one review.
    """
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        watchlist_id = self.kwargs.get('pk')
        return Review.objects.filter(watchlist=watchlist_id)
    
    def perform_create(self, serializer):
        watchlist_id = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk = watchlist_id)
        review_user = self.request.user
        review_queryset = Review.objects.filter(review_user=review_user, watchlist=watchlist)
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie.")
        
        serializer.save(watchlist=watchlist, review_user=review_user)

class ReviewListView(generics.ListAPIView):
    """
    List all reviews.
    """
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        review_id = self.kwargs.get('pk')
        return Review.objects.filter(watchlist = review_id)
        
    
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a review instance.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


""" class ReviewListView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

class ReviewDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs) """

class StreamingPlatformView(APIView):
    """
    List all streaming platforms or create a new one.
    """
    def get(self, request):
        platforms = StreamingPlatform.objects.all()
        serializer = StreamingPlatformSerializer(platforms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StreamingPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StreamingPlatformDetailView(APIView):
    """
    Retrieve, update or delete a streaming platform instance.
    """
    def get_object(self, pk):
        try:
            return StreamingPlatform.objects.get(pk=pk)
        except StreamingPlatform.DoesNotExist:
            return None

    def get(self, request, pk):
        platform = self.get_object(pk)
        if platform is None:
            return Response({'error': 'Streaming Platform not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamingPlatformSerializer(platform)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        platform = self.get_object(pk)
        if platform is None:
            return Response({'error': 'Streaming Platform not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamingPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        platform = self.get_object(pk)
        if platform is None:
            return Response({'error': 'Streaming Platform not found'}, status=status.HTTP_404_NOT_FOUND)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




""" @api_view(['GET','POST'])
def movie_list(request):
    if request.method == 'GET':    
        movies = Movie.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail(request, pk):
    if request.method == 'GET':
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        movie = Movie.objects.get(pk=pk)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)   """

