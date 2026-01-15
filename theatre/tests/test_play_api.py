import tempfile
from PIL import Image
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from theatre.models import Play, Genre, Actor


class PlayApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="user@test.com",
            password="password123"
        )
        self.admin = get_user_model().objects.create_superuser(
            email="admin@test.com",
            password="adminpassword"
        )

        self.genre = Genre.objects.create(name="Drama")
        self.actor = Actor.objects.create(
            first_name="Tom",
            last_name="Hanks"
        )

        self.play = Play.objects.create(
            title="Hamlet",
            description="Classic"
        )
        self.play.genres.add(self.genre)
        self.play.actors.add(self.actor)

        self.url = reverse("theatre:play-list")

    def test_filter_plays_by_genre(self):
        res = self.client.get(self.url, {"genre": f"{self.genre.id}"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_retrieve_play_detail(self):
        url = reverse("theatre:play-detail", args=[self.play.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        genres = res.data["genres"]
        self.assertEqual(genres[0], "Drama")

    def test_create_play_forbidden(self):
        self.client.force_authenticate(self.user)
        payload = {"title": "Forbidden", "description": "Should fail"}
        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PlayImageUploadTests(APITestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            "admin_img@t.com", "pass123"
        )
        self.client.force_authenticate(self.admin)
        self.play = Play.objects.create(title="Poster Test", description="Desc")

    def test_upload_poster_to_play(self):
        url = reverse("theatre:play-upload-poster", args=[self.play.id])

        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(url, {"poster": ntf},
                                   format="multipart")

        self.play.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("poster", res.data)
