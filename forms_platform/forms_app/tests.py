from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from forms_app.models import Formular, Question, Option, FilledForm, Answer

User = get_user_model()


class FormPlatformTests(APITestCase):

    def setUp(self):
        """Priprema test korisnika i tokena"""
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpass"
        )
        self.client.force_authenticate(user=self.user)

    # --------------------------- BASIC CRUD TESTS ---------------------------

    def test_create_form(self):
        """Test kreiranja forme"""
        data = {
            "name": "Test Form",
            "description": "Opis forme",
            "allow_anonymous": True
        }
        response = self.client.post("/api/forms/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Formular.objects.count(), 1)

    def test_create_question_and_option(self):
        """Test dodavanja pitanja i opcije"""
        form = Formular.objects.create(name="Boje", description="Forma o bojama", creator=self.user)
        question = Question.objects.create(form=form, text="Omiljena boja?", type="single_choice")
        data = {"question": question.id, "text": "Plava"}
        response = self.client.post("/api/options/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Option.objects.count(), 1)

    # --------------------------- FILE UPLOAD TESTS ---------------------------

    def test_upload_question_image(self):
        """Test upload slike za pitanje"""
        form = Formular.objects.create(name="Foto forma", creator=self.user)
        q = Question.objects.create(form=form, text="Slika?", type="short_text")
        image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")

        response = self.client.post(
            f"/api/questions/{q.id}/upload_image/",
            {"image": image},
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("image_url", response.data)

    def test_upload_option_image(self):
        """Test upload slike za opciju"""
        form = Formular.objects.create(name="Boje", creator=self.user)
        question = Question.objects.create(form=form, text="Omiljena boja?", type="single_choice")
        option = Option.objects.create(question=question, text="Crvena")
        image = SimpleUploadedFile("option.png", b"img", content_type="image/png")

        response = self.client.post(
            f"/api/options/{option.id}/upload_image/",
            {"image": image},
            format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("image_url", response.data)

    # --------------------------- FILLED FORM TEST ---------------------------

    def test_filled_form_submission(self):
        """Test popunjavanja forme"""
        form = Formular.objects.create(name="Anketa", creator=self.user)
        q1 = Question.objects.create(form=form, text="Ime?", type="short_text")
        q2 = Question.objects.create(form=form, text="Broj godina?", type="numeric")

        filled = FilledForm.objects.create(form=form, user=self.user)
        Answer.objects.create(filled_form=filled, question=q1, value="Aleksandra")
        Answer.objects.create(filled_form=filled, question=q2, value="22")

        self.assertEqual(FilledForm.objects.count(), 1)
        self.assertEqual(Answer.objects.filter(filled_form=filled).count(), 2)

    # --------------------------- AUTH TESTS ---------------------------

    def test_user_register_and_login(self):
        """Test registracije i logina"""
        register = self.client.post("/register/", {
            "username": "newuser",
            "email": "new@example.com",
            "password": "12345"
        })
        self.assertIn(register.status_code, [200, 201])

        login = self.client.post("/login/", {
            "email": "new@example.com",
            "password": "12345"
        })
        self.assertIn(login.status_code, [200, 201])
        self.assertIn("access", login.json())

    def test_token_refresh(self):
        """Test token refresh mehanizma"""
        res = self.client.post("/api/token/", {
            "username": "testuser",
            "password": "testpass"
        })
        self.assertEqual(res.status_code, 200)
        refresh = res.data.get("refresh")

        refresh_res = self.client.post("/api/token/refresh/", {"refresh": refresh})
        self.assertEqual(refresh_res.status_code, 200)
        self.assertIn("access", refresh_res.data)

    # --------------------------- PUBLISH / LOCK TESTS ---------------------------

    def test_publish_and_lock_form(self):
        """Test publish i lock formi"""
        form = Formular.objects.create(name="Form Test", creator=self.user)
        publish = self.client.post(f"/api/forms/{form.id}/publish/")
        self.assertEqual(publish.status_code, 200)

        lock = self.client.post(f"/api/forms/{form.id}/lock/")
        self.assertEqual(lock.status_code, 200)
