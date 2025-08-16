# views.py

# --- Imports ---
# Models for Movies (WatchList), StreamingPlatform, and Review entities
from watchlist_app.models import WatchList, StreamingPlatform, Review

# DRF utilities for raising validation errors and building class-based views
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.views import APIView
from rest_framework.response import Response

# Serializers to convert model instances to/from JSON
from watchlist_app.api.serializers import (
    WatchListSerializer,
    StreamingPlatformSerializer,
    ReviewSerializer,
)

# DRF status codes, generic views, and mixins
from rest_framework import status, generics, mixins,filters

# Custom permission to allow only review owners to modify, others read-only
from watchlist_app.api.permissions import ReviewUserorReadOnly, IsAdminOrReadOnly
# Authentication permission to restrict review creation to logged-in users
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend




class SearchWatchListView(generics.ListAPIView):
    """
    List all movies with optional search by title.
    """
    queryset = WatchList.objects.all()  # Fetch all movies
    serializer_class = WatchListSerializer
    throttle_classes = [AnonRateThrottle]  # Limit requests to prevent abuse
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]  # Enable filtering on this view
    search_fields = ['title','=platform__name']  # Allow searching by movie title
    ordering_fields = ['average_rating']  # Allow ordering by title or release date




# This class is a Django API view that lists user reviews filtered by the username provided in the
# URL.
class UserReviewDetailView(generics.ListAPIView):
    """List reviews created by a specific user.
    """
    serializer_class = ReviewSerializer
    throttle_classes = [UserRateThrottle]  # Custom throttle to limit review listing
    #permission_classes = [IsAuthenticated]  # Only authenticated users can access
    authentication_classes = [TokenAuthentication]  # Use token authentication

    def get_queryset(self):
        username = self.request.query_params.get('username')
        if not username:
            raise ValidationError("Username parameter is required.")
        query_set = Review.objects.filter(review_user__username=username)
        if not query_set.exists():
            raise NotFound(f"No reviews found for user '{username}'.")
        return query_set
        
class WatchListView(APIView):
    """ 
    List all movies or create a new movie.
    """
    permission_classes = [IsAdminOrReadOnly]# Restrict access to authenticated users
    throttle_classes = [UserRateThrottle]  # Limit requests to prevent abuse
    authentication_classes = [TokenAuthentication]  # Use default authentication (e.g., Token, Session)
    def get(self, request):
        # Fetch all WatchList records
        movies = WatchList.objects.all()
        # Serialize the queryset into JSON-friendly data
        serializer = WatchListSerializer(movies, many=True)
        # Return serialized list with HTTP 200 OK
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Deserialize incoming JSON to a WatchList instance (not yet saved)
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            # Persist the new movie if validation passes
            serializer.save()
            # Return created object with HTTP 201 Created
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # If invalid, return errors with HTTP 400 Bad Request
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchListDetailView(APIView):
    """ 
    Retrieve, update or delete a movie instance.
    """
    throttle_classes = [AnonRateThrottle]  # Limit requests to prevent abuse
    def get_object(self, pk):
        # Helper to safely fetch a movie by primary key
        try:
            return WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            # Return None so callers can handle 404 uniformly
            return None

    def get(self, request, pk):
        # Retrieve a single movie
        movie = self.get_object(pk)
        if movie is None:
            # If not found, respond with 404
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        # Serialize and return the movie
        serializer = WatchListSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        
        # Update an existing movie (full update)
        movie = self.get_object(pk)
        if movie is None:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        # Bind incoming data to the existing instance
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            # Save changes if valid
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Return validation errors if any
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Delete a movie
        movie = self.get_object(pk)
        if movie is None:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        # Remove from database
        movie.delete()
        # No content on successful deletion
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class ReviewCreateView(generics.CreateAPIView):
    """
    Create a new review for a movie.
    One user can post only one review per movie.
    """
    # This view only needs the serializer class; queryset is derived per-movie
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewCreateThrottle, UserRateThrottle]  # Custom throttle to limit review creation
    permission_classes = [IsAuthenticated] # Custom permission to restrict access
    authentication_classes = [TokenAuthentication]  # Use default authentication (e.g., Token, Session)
    
    def get_queryset(self):
        # Limit queryset to reviews for the given WatchList (movie) id from URL
        watchlist_id = self.kwargs.get('pk')
        return Review.objects.filter(watchlist=watchlist_id)
    
    def perform_create(self, serializer):
        # Extract the movie (WatchList) we are reviewing from the URL kwarg
        watchlist_id = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=watchlist_id)
        # The user creating the review is the authenticated request user
        review_user = self.request.user

        # Check if this user already reviewed the movie
        if Review.objects.filter(review_user=review_user, watchlist=watchlist).exists():
            # Enforce one-review-per-user-per-movie rule
            raise ValidationError("You have already reviewed this movie.")
        
        # Update average rating (running average formula)
        if watchlist.number_of_reviews == 0:
            # First review sets the average
            watchlist.average_rating = serializer.validated_data['rating']
        else:
            # Recompute average as (sum + new) / (count + 1)
            watchlist.average_rating = (
                watchlist.average_rating * watchlist.number_of_reviews 
                + serializer.validated_data['rating']
            ) / (watchlist.number_of_reviews + 1)
        
        # Increment review count
        watchlist.number_of_reviews += 1
        
        # Persist the updated WatchList aggregate fields
        watchlist.save()
        
        # Save the new Review, linking it to the watchlist and the user
        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewListView(generics.ListAPIView):
    """
    List all reviews.
    """
    # Use the same serializer for listing reviews
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewListThrottle]  # Custom throttle to limit review listing
    filter_backends = [DjangoFilterBackend]  # Enable filtering on this view
    filterset_fields = ['review_user__username', 'watchlist__title']  # Allow filtering by username and movie title
    
    
    def get_queryset(self):
        # Return all reviews for a given watchlist (movie) id from URL
        review_id = self.kwargs.get('pk')
        return Review.objects.filter(watchlist=review_id)
        
    
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a review instance.
    """
    # Base queryset for retrieve/update/delete
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # Only review owners can modify; others have read-only access
    permission_classes = [ReviewUserorReadOnly]
    authentication_classes = [TokenAuthentication]

"""
# Alternative implementation using mixins (commented out but kept for reference)

class ReviewListView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get(self, request, *args, **kwargs):
        # Handle GET to list reviews
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # Handle POST to create a review
        return self.create(request, *args, **kwargs)
    

class ReviewDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get(self, request, *args, **kwargs):
        # Handle GET to retrieve a single review
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        # Handle PUT to update a review
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        # Handle DELETE to remove a review
        return self.destroy(request, *args, **kwargs)
"""


class StreamingPlatformView(APIView):
    """
    List all streaming platforms or create a new one.
    """
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request):
        # Fetch all StreamingPlatform records
        platforms = StreamingPlatform.objects.all()
        # Serialize to JSON-friendly list
        serializer = StreamingPlatformSerializer(platforms, many=True)
        # Return the list with HTTP 200 OK
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Deserialize incoming platform payload
        serializer = StreamingPlatformSerializer(data=request.data)
        if serializer.is_valid():
            # Save the new platform
            serializer.save()
            # Return created object with HTTP 201 Created
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # On validation error, return HTTP 400 with details
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StreamingPlatformDetailView(APIView):
    """
    Retrieve, update or delete a streaming platform instance.
    """
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [ScopedRateThrottle]  # Limit requests to prevent abuse
    throttle_scope = 'streaming_platforms'  # Custom scope for throttling
    
    
    
    def get_object(self, pk):
        # Helper to get a platform by id or None
        try:
            return StreamingPlatform.objects.get(pk=pk)
        except StreamingPlatform.DoesNotExist:
            return None

    def get(self, request, pk):
        # Retrieve a single streaming platform
        platform = self.get_object(pk)
        if platform is None:
            return Response({'error': 'Streaming Platform not found'}, status=status.HTTP_404_NOT_FOUND)
        # Serialize and return
        serializer = StreamingPlatformSerializer(platform)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        # Update an existing streaming platform
        platform = self.get_object(pk)
        if platform is None:
            return Response({'error': 'Streaming Platform not found'}, status=status.HTTP_404_NOT_FOUND)
        # Bind new data to existing instance
        serializer = StreamingPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            # Save and return updated object
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Return any validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Delete a streaming platform
        platform = self.get_object(pk)
        if platform is None:
            return Response({'error': 'Streaming Platform not found'}, status=status.HTTP_404_NOT_FOUND)
        # Remove from database
        platform.delete()
        # Respond with HTTP 204 No Content
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
# Function-based views kept for historical reference (commented out)

@api_view(['GET','POST'])
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
        return Response(status=status.HTTP_204_NO_CONTENT)
"""
