from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear existing data
        Leaderboard.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

        # Create Teams
        marvel = Team.objects.create(name='Marvel', description='Marvel superheroes')
        dc = Team.objects.create(name='DC', description='DC superheroes')

        # Create Users
        users = [
            User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel),
            User.objects.create(name='Captain America', email='cap@marvel.com', team=marvel),
            User.objects.create(name='Hulk', email='hulk@marvel.com', team=marvel),
            User.objects.create(name='Superman', email='superman@dc.com', team=dc),
            User.objects.create(name='Batman', email='batman@dc.com', team=dc),
            User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
        ]

        # Create Workouts
        workout1 = Workout.objects.create(name='Pushups', description='Upper body workout')
        workout2 = Workout.objects.create(name='Running', description='Cardio workout')
        workout1.suggested_for.set(users[:3])
        workout2.suggested_for.set(users[3:])

        # Create Activities
        Activity.objects.create(user=users[0], activity_type='Pushups', duration=30, date=timezone.now().date())
        Activity.objects.create(user=users[1], activity_type='Running', duration=45, date=timezone.now().date())
        Activity.objects.create(user=users[3], activity_type='Pushups', duration=20, date=timezone.now().date())
        Activity.objects.create(user=users[4], activity_type='Running', duration=60, date=timezone.now().date())

        # Create Leaderboard
        Leaderboard.objects.create(user=users[0], score=100)
        Leaderboard.objects.create(user=users[3], score=120)
        Leaderboard.objects.create(user=users[1], score=90)
        Leaderboard.objects.create(user=users[4], score=110)

        # Ensure unique index on email field in users collection
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db.user.create_index('email', unique=True)
        self.stdout.write(self.style.SUCCESS('Database populated with test data.'))
