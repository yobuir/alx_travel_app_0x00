from rest_framework import serializers
from .models import Listing, Booking, Review


class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Listing model
    """
    class Meta:
        model = Listing
        fields = [
            'id',
            'title',
            'description',
            'price_per_night',
            'location',
            'available_from',
            'available_to'
        ]
        
    def validate(self, data):
        """
        Check that available_from is before available_to
        """
        if data.get('available_from') and data.get('available_to'):
            if data['available_from'] >= data['available_to']:
                raise serializers.ValidationError(
                    "Available from date must be before available to date."
                )
        return data


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model
    """
    listing_title = serializers.CharField(source='listing.title', read_only=True)
    listing_location = serializers.CharField(source='listing.location', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id',
            'listing',
            'listing_title',
            'listing_location',
            'user',
            'start_date',
            'end_date',
            'total_price'
        ]
        
    def validate(self, data):
        """
        Check that start_date is before end_date and within listing availability
        """
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] >= data['end_date']:
                raise serializers.ValidationError(
                    "Start date must be before end date."
                )
                
        # Check if dates are within listing availability
        if data.get('listing') and data.get('start_date') and data.get('end_date'):
            listing = data['listing']
            if (data['start_date'] < listing.available_from or 
                data['end_date'] > listing.available_to):
                raise serializers.ValidationError(
                    "Booking dates must be within the listing's availability period."
                )
                
        return data


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model
    """
    listing_title = serializers.CharField(source='listing.title', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id',
            'listing',
            'listing_title',
            'user',
            'rating',
            'comment',
            'created_at'
        ]
        read_only_fields = ['created_at']
        
    def validate_rating(self, value):
        """
        Check that rating is between 1 and 5
        """
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )
        return value


class ListingDetailSerializer(ListingSerializer):
    """
    Detailed serializer for Listing with related bookings and reviews
    """
    bookings = BookingSerializer(many=True, read_only=True, source='booking_set')
    reviews = ReviewSerializer(many=True, read_only=True, source='review_set')
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    
    class Meta(ListingSerializer.Meta):
        fields = ListingSerializer.Meta.fields + [
            'bookings',
            'reviews',
            'average_rating',
            'total_reviews'
        ]
        
    def get_average_rating(self, obj):
        """
        Calculate average rating for this listing
        """
        reviews = obj.review_set.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return None
        
    def get_total_reviews(self, obj):
        """
        Get total number of reviews for this listing
        """
        return obj.review_set.count()