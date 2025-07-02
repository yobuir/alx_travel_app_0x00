from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
import random
from listings.models import Listing, Booking, Review


class Command(BaseCommand):
    help = 'Seed the database with sample listings, bookings, and reviews'

    def add_arguments(self, parser):
        parser.add_argument(
            '--listings',
            type=int,
            default=20,
            help='Number of listings to create (default: 20)'
        )
        parser.add_argument(
            '--bookings',
            type=int,
            default=50,
            help='Number of bookings to create (default: 50)'
        )
        parser.add_argument(
            '--reviews',
            type=int,
            default=100,
            help='Number of reviews to create (default: 100)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Review.objects.all().delete()
            Booking.objects.all().delete()
            Listing.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✓ Existing data cleared'))

        # Create listings
        listings_count = options['listings']
        self.stdout.write(f'Creating {listings_count} listings...')
        listings = self.create_listings(listings_count)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(listings)} listings'))

        # Create bookings
        bookings_count = options['bookings']
        self.stdout.write(f'Creating {bookings_count} bookings...')
        bookings = self.create_bookings(bookings_count, listings)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(bookings)} bookings'))

        # Create reviews
        reviews_count = options['reviews']
        self.stdout.write(f'Creating {reviews_count} reviews...')
        reviews = self.create_reviews(reviews_count, listings)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(reviews)} reviews'))

        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Database seeding completed successfully!\n'
                f'   Listings: {len(listings)}\n'
                f'   Bookings: {len(bookings)}\n'
                f'   Reviews: {len(reviews)}'
            )
        )

    def create_listings(self, count):
        """Create sample listings"""
        sample_listings = [
            {
                'title': 'Cozy Beachfront Villa',
                'description': 'Beautiful villa with stunning ocean views, private beach access, and modern amenities. Perfect for a romantic getaway or family vacation.',
                'location': 'Malibu, California',
                'price_per_night': Decimal('250.00')
            },
            {
                'title': 'Mountain Cabin Retreat',
                'description': 'Rustic cabin nestled in the mountains with hiking trails, fireplace, and breathtaking views. Ideal for nature lovers and outdoor enthusiasts.',
                'location': 'Aspen, Colorado',
                'price_per_night': Decimal('180.00')
            },
            {
                'title': 'Urban Loft Downtown',
                'description': 'Modern loft in the heart of the city with rooftop access, high-speed wifi, and walking distance to restaurants and entertainment.',
                'location': 'New York, New York',
                'price_per_night': Decimal('320.00')
            },
            {
                'title': 'Tropical Paradise Bungalow',
                'description': 'Overwater bungalow with crystal clear waters, snorkeling gear included, and 24/7 concierge service.',
                'location': 'Bora Bora, French Polynesia',
                'price_per_night': Decimal('450.00')
            },
            {
                'title': 'Historic Castle Suite',
                'description': 'Stay in a real castle with medieval architecture, grand halls, and beautiful gardens. A unique historical experience.',
                'location': 'Edinburgh, Scotland',
                'price_per_night': Decimal('380.00')
            },
            {
                'title': 'Desert Oasis Resort',
                'description': 'Luxury resort in the desert with spa services, pool, and spectacular sunset views. Perfect for relaxation and rejuvenation.',
                'location': 'Scottsdale, Arizona',
                'price_per_night': Decimal('275.00')
            },
            {
                'title': 'Lakeside Cottage',
                'description': 'Charming cottage by the lake with boat rental, fishing equipment, and peaceful surroundings.',
                'location': 'Lake Tahoe, California',
                'price_per_night': Decimal('195.00')
            },
            {
                'title': 'Penthouse City View',
                'description': 'Luxurious penthouse with panoramic city views, private terrace, and premium furnishings.',
                'location': 'Chicago, Illinois',
                'price_per_night': Decimal('420.00')
            },
            {
                'title': 'Vineyard Estate',
                'description': 'Beautiful estate in wine country with vineyard tours, wine tasting, and gourmet dining.',
                'location': 'Napa Valley, California',
                'price_per_night': Decimal('350.00')
            },
            {
                'title': 'Safari Lodge',
                'description': 'Authentic safari experience with game drives, wildlife viewing, and traditional African cuisine.',
                'location': 'Serengeti, Tanzania',
                'price_per_night': Decimal('500.00')
            }
        ]

        # Additional location and property type combinations
        additional_locations = [
            'Miami, Florida', 'Barcelona, Spain', 'Tokyo, Japan', 'Sydney, Australia',
            'Paris, France', 'London, England', 'Rome, Italy', 'Santorini, Greece',
            'Bali, Indonesia', 'Dubai, UAE', 'Cape Town, South Africa', 'Rio de Janeiro, Brazil'
        ]

        property_types = [
            'Modern Apartment', 'Beach House', 'City Studio', 'Country House',
            'Luxury Villa', 'Cozy Cabin', 'Boutique Hotel', 'Hostel Room',
            'Tree House', 'Boat House', 'Glamping Tent', 'Traditional Riad'
        ]

        descriptions = [
            'Spacious and comfortable accommodation with all modern amenities.',
            'Perfect location with easy access to local attractions and dining.',
            'Beautifully decorated space with attention to every detail.',
            'Ideal for couples, families, or business travelers.',
            'Exceptional hospitality and personalized service included.',
            'Unique architecture and design that captures local culture.',
            'Prime location in the most desirable part of the city.',
            'Peaceful retreat away from the hustle and bustle.',
            'Adventure base camp for exploring the surrounding area.',
            'Luxury meets comfort in this stunning property.'
        ]

        listings = []
        
        # Use predefined listings first
        for i, listing_data in enumerate(sample_listings[:count]):
            available_from = date.today() + timedelta(days=random.randint(1, 30))
            available_to = available_from + timedelta(days=random.randint(30, 365))
            
            listing = Listing.objects.create(
                title=listing_data['title'],
                description=listing_data['description'],
                price_per_night=listing_data['price_per_night'],
                location=listing_data['location'],
                available_from=available_from,
                available_to=available_to
            )
            listings.append(listing)

        # Generate additional listings if needed
        remaining_count = count - len(sample_listings)
        for i in range(remaining_count):
            property_type = random.choice(property_types)
            location = random.choice(additional_locations)
            description = random.choice(descriptions)
            
            available_from = date.today() + timedelta(days=random.randint(1, 30))
            available_to = available_from + timedelta(days=random.randint(30, 365))
            
            listing = Listing.objects.create(
                title=f"{property_type} in {location.split(',')[0]}",
                description=f"{description} Located in the beautiful {location}.",
                price_per_night=Decimal(str(random.randint(50, 600))),
                location=location,
                available_from=available_from,
                available_to=available_to
            )
            listings.append(listing)

        return listings

    def create_bookings(self, count, listings):
        """Create sample bookings"""
        bookings = []
        users = [
            'john.doe@email.com', 'jane.smith@email.com', 'mike.johnson@email.com',
            'sarah.wilson@email.com', 'david.brown@email.com', 'lisa.davis@email.com',
            'mark.taylor@email.com', 'anna.martinez@email.com', 'chris.garcia@email.com',
            'emily.rodriguez@email.com', 'james.lee@email.com', 'maria.gonzalez@email.com'
        ]

        for i in range(count):
            listing = random.choice(listings)
            user = random.choice(users)
            
            # Generate booking dates within listing availability
            max_start_offset = (listing.available_to - listing.available_from).days - 7
            if max_start_offset > 0:
                start_offset = random.randint(0, max_start_offset)
                start_date = listing.available_from + timedelta(days=start_offset)
                
                # Booking duration between 1-14 days
                max_duration = min(14, (listing.available_to - start_date).days)
                duration = random.randint(1, max_duration)
                end_date = start_date + timedelta(days=duration)
                
                total_price = listing.price_per_night * duration
                
                booking = Booking.objects.create(
                    listing=listing,
                    user=user,
                    start_date=start_date,
                    end_date=end_date,
                    total_price=total_price
                )
                bookings.append(booking)

        return bookings

    def create_reviews(self, count, listings):
        """Create sample reviews"""
        reviews = []
        users = [
            'john.doe@email.com', 'jane.smith@email.com', 'mike.johnson@email.com',
            'sarah.wilson@email.com', 'david.brown@email.com', 'lisa.davis@email.com',
            'mark.taylor@email.com', 'anna.martinez@email.com', 'chris.garcia@email.com',
            'emily.rodriguez@email.com', 'james.lee@email.com', 'maria.gonzalez@email.com',
            'alex.thompson@email.com', 'rachel.white@email.com', 'kevin.harris@email.com'
        ]

        positive_comments = [
            "Amazing place! The location was perfect and the host was very responsive.",
            "Beautiful property with stunning views. Would definitely stay again!",
            "Exceeded our expectations in every way. Highly recommended!",
            "Perfect for our family vacation. Clean, spacious, and well-equipped.",
            "The photos don't do it justice - it's even better in person!",
            "Great value for money. Everything was exactly as described.",
            "Fantastic hospitality and attention to detail. Five stars!",
            "Peaceful and relaxing atmosphere. Just what we needed for our getaway.",
            "Excellent location with easy access to attractions and restaurants.",
            "Modern amenities and comfortable furnishings. Very impressed!"
        ]

        neutral_comments = [
            "Good overall experience. Property was as described.",
            "Nice place, though could use some minor updates.",
            "Decent stay. Location was convenient for our needs.",
            "Property was clean and functional. Good value.",
            "Average experience. Nothing special but no complaints.",
            "Acceptable accommodation for the price point.",
            "Met our basic needs for the trip. Would consider again.",
            "Fair property with standard amenities included."
        ]

        negative_comments = [
            "Property wasn't as clean as expected. Disappointing experience.",
            "Location was noisier than anticipated. Difficult to rest.",
            "Several amenities weren't working during our stay.",
            "Property condition didn't match the photos shown.",
            "Poor communication from host. Issues weren't resolved quickly.",
            "Overpriced for what was offered. Expected more."
        ]

        for i in range(count):
            listing = random.choice(listings)
            user = random.choice(users)
            
            # Weight ratings towards positive (more realistic)
            rating_weights = [1, 2, 10, 25, 40, 22]  # 1-star to 5-star weights
            rating = random.choices(range(1, 6), weights=rating_weights)[0]
            
            # Choose comment based on rating
            if rating >= 4:
                comment = random.choice(positive_comments)
            elif rating == 3:
                comment = random.choice(neutral_comments)
            else:
                comment = random.choice(negative_comments)
            
            review = Review.objects.create(
                listing=listing,
                user=user,
                rating=rating,
                comment=comment
            )
            reviews.append(review)

        return reviews