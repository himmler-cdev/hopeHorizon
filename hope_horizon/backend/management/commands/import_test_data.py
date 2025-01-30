import csv
import datetime
import os
import random
from django.core.management.base import BaseCommand, CommandError
import requests
from backend import models
from django.db import migrations
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    '''
    Imports our Test data.
    '''
    help = 'Imports our Test data.'

    def handle(self, *args, **options):
        
        # Create the users and user trackers
        create_users()

        # Create a few user status entries
        create_user_statuse()

        # Create a few blog posts
        posts = create_blog_posts()

        print("Posts: ", posts)

        create_blog_post_comments(posts)

def create_users():
    admin_role = models.UserRole.objects.last()  # Ensure at least one role exists
    user_role = models.UserRole.objects.first()  # Assume another role exists for regular users
    therapist_role = models.UserRole.objects.get(role="Therapist")
    moderator_role = models.UserRole.objects.get(role="Moderator")

    # Superuser
    models.User.objects.create(
        username='admin',
        email='admin@example.com',
        password=make_password('topsecret'),
        is_superuser=True,
        is_staff=True,
        birthdate='2000-01-01',
        user_role_id=admin_role,
    )

    # Therapist
    models.User.objects.create(
        username='therapist',
        email='therapist@example.com',
        password=make_password('password123'),
        is_superuser=False,
        is_staff=True,
        birthdate='1990-01-01',
        user_role_id=therapist_role
    )

    # Moderator
    models.User.objects.create(
        username='moderator',
        email='moderator@example.com',
        password=make_password('password123'),
        is_superuser=False,
        is_staff=True,
        birthdate='1990-01-01',
        user_role_id=moderator_role
    )

    # Regular users
    users = [
        {"username": "user1", "email": "user1@example.com", "password": "password123"},
        {"username": "user2", "email": "user2@example.com", "password": "password123"},
        {"username": "user3", "email": "user3@example.com", "password": "password123"},
        {"username": "user4", "email": "user4@example.com", "password": "password123"},
        {"username": "user5", "email": "user5@example.com", "password": "password123"},
    ]

    for user_data in users:
        models.User.objects.create(
            username=user_data["username"],
            email=user_data["email"],
            password=make_password(user_data["password"]),
            is_superuser=False,
            is_staff=False,
            birthdate='1995-06-15',  # Example birthdate, modify as needed
            user_role_id=user_role,  # Assigning last role found
        )

    for i in range(1, 9):
        models.UserTracker.objects.create(
            user_id=models.User.objects.get(id=i),
            is_enabled=True,
            track_mood=True,
            track_energy_level=True,
            track_sleep_quality=True,
            track_anxiety_level=True,
            track_appetite=True,
            track_content=True,
        )       

def create_user_statuse():
    for i in range(1, 6):
        user = models.User.objects.get(username='user{}'.format(i))
        numOfStatuses = random.randint(20, 100)
        startDate = datetime.date.today()
        for j in range(1,numOfStatuses):
            models.UserStatus.objects.create(
                user_id=user,
                mood=random.randint(0, 10),
                energy_level=random.randint(0, 10),
                sleep_quality=random.randint(0, 10),
                anxiety_level=random.randint(0, 10),
                appetite=random.randint(0, 10),
                content=random.randint(0, 10),
                date=startDate.strftime('%Y-%m-%d'),
            )
            startDate = startDate - datetime.timedelta(days=1)

def create_blog_posts():
    posts = 0
    for i in range(1, 6):
        user = models.User.objects.get(username='user{}'.format(i))
        numOfPosts = random.randint(5, 15)
        posts += numOfPosts-1
        for j in range(1, numOfPosts):
            words = random.randint(10, 100)
            models.BlogPost.objects.create(
                user_id=user,
                title='Post Title {}'.format(j),
                blog_post_type_id=models.BlogPostType.objects.get(id=random.randint(1, 3)),
                content=fetch_random_words(words),
                date=datetime.date.today().strftime('%Y-%m-%d'),
            )

    return posts

def create_blog_post_comments(posts):
    for i in range(1, posts):
        user = models.User.objects.get(username='user{}'.format(random.randint(1, 5)))
        post = models.BlogPost.objects.get(id=i)
        print(post.id)
        numOfComments = random.randint(1, 10)
        for j in range(1, numOfComments):
            words = random.randint(5, 20)
            models.Comment.objects.create(
                user_id=user,
                blog_post_id=post,
                content=fetch_random_words(words),
                date=datetime.date.today().strftime('%Y-%m-%d'),
            )
        
def fetch_random_words(words):
    url = "https://random-word-api.vercel.app/api?words=" + str(words)
    response = requests.get(url)
    return " ".join(response.json())

