from django.core.management.base import BaseCommand, CommandError
from askme.models import *
import random
from os import urandom
from django.db.utils import IntegrityError
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = "fill database with data"

    def add_arguments(self, parser):
        parser.add_argument("ratio", nargs=1, type=int)

    def handle(self, *args, **options):
        ratio = options["ratio"][0]
        # print(f"ratio {ratio} {type(ratio)}")

        users_count = ratio
        questions_count = ratio * 10
        answers_count = ratio * 100
        tags_count = ratio
        user_likes_count = ratio * 200

        print("-----------fill db-----------")
        for k, v in locals().items():
            print(k, v)

        print("start create users")
        profiles = self.gen_profiles(users_count)
        Profile.objects.bulk_create(profiles)
        print(f"generated users: {len(profiles)}")
        profiles = Profile.objects.all()

        print("start create tags")
        tags = self.gen_tags(tags_count)
        Tag.objects.bulk_create(tags)
        print(f"generated tags: {len(tags)}")
        tags = Tag.objects.all()

        print("start create questions")
        questions = self.gen_questions(profiles, tags, questions_count)
        # Question.objects.bulk_create(questions)
        for q in questions:
            q.save()
        print(f"generated questions: {len(questions)}")
        self.set_tags(questions, tags)
        questions = Question.objects.all()

        print("start create answers")
        answers = self.gen_answers(profiles, questions, answers_count)
        Answer.objects.bulk_create(answers)
        print(f"generated answers: {len(answers)}")
        answers = Answer.objects.all()

        print("start create question likes")
        question_likes = self.gen_question_likes(profiles, questions, int(user_likes_count * 0.2))
        QuestionLike.objects.bulk_create(question_likes)
        print(f"generated question_likes: {len(question_likes)}")
        question_likes = QuestionLike.objects.all()

        print("start create answer likes")
        answer_likes = self.gen_answer_likes(profiles, answers, int(user_likes_count * 0.8))
        AnswerLike.objects.bulk_create(answer_likes)
        print(f"generated question_likes: {len(answer_likes)}")

    def gen_profiles(self, count):
        names = ["Oleg", "Andrey", "Daniel Machilsky", "PEP8"]
        profiles = []
        users = []
        for i in range(count):
            if i % 50 == 0:
                print(f"create user {i}", end="\r")

            try:
                user = User.objects.create_user(
                    username=f"{random.choice(names)} {i}",
                    password=f"password-{i}",
                    email=f"mail{i}@mail.com"
                )

                # users.append(User(
                #     username=f"{random.choice(names)} {i}",
                #     password=make_password(f"password-{i}"),
                #     email=f"mail{i}@mail.com"
                # ))

                profiles.append(Profile(user=user, avatar=f'upload/kitty{(i % 3) + 1}.jpg'))

                # Profile.objects.create(user=user, avatar=f'media/kitty{(i % 3) + 1}.jpg')
            except IntegrityError:
                pass

        User.objects.bulk_create(users)

        return profiles

    def gen_tags(self, count):
        tag_names = ["c++", "python", "c+-", "workflows", "vk", "haskell", "android", "bmstu", "2023", "2007"]
        arr = []
        for i in range(count):
            if i % 500 == 0:
                print(f"create tag {i}", end="\r")

            arr.append(Tag(name=f"{random.choice(tag_names)}-{i}"))

        return arr

    def gen_questions(self, profiles, tags, count):
        arr = []
        for i in range(count):
            if i % 500 == 0:
                print(f"create question {i}", end="\r")

            arr.append(Question(
                header=f"It is quite interesting question {i}",
                text=f"Here is a bytecode of my pyhon program: {urandom(random.randint(8, 16))}. How can i fix it?",
                author=random.choice(profiles),
            ))

        return arr

    def set_tags(self, questions, tags):
        for q in questions:
            tag_ids = [t.id for t in random.choices(tags, k=random.randint(1, 10))]
            for id_ in tag_ids:
                q.tags.add(id_)
            q.save()

    def gen_answers(self, profiles, questions, count):
        arr = []
        texts = [
            f"Sure! this is your fixed code: {urandom(random.randint(8, 16))}.",
            f"I think your should check {urandom(random.randint(8, 16))} byte :/ .",
            f"Use c++ instead"
        ]
        for i in range(count):
            if i % 500 == 0:
                print(f"create answer {i}", end="\r")

            if i % 50 == 0:
                texts[0] = f"Sure! this is your fixed code: {urandom(random.randint(8, 16))}."
                texts[1] = f"I think your should check {random.randint(8, 16)} byte :/ ."

            arr.append(Answer(
                text=random.choice(texts),
                is_true=False,
                author=random.choice(profiles),
                question=random.choice(questions)
            ))

        return arr

    def gen_question_likes(self, profiles, questions, count):
        arr = []
        for i in range(count):
            if i % 500 == 0:
                print(f"create tag {i}", end="\r")

            arr.append(QuestionLike(
                value=1 if random.random() > 0.3 else -1,
                author=random.choice(profiles),
                question=random.choice(questions)
            ))

        return arr

    def gen_answer_likes(self, profiles, answers, count):
        arr = []
        for i in range(count):
            if i % 500 == 0:
                print(f"create tag {i}", end="\r")

            arr.append(AnswerLike(
                value=1 if random.random() > 0.3 else -1,
                author=random.choice(profiles),
                answer=random.choice(answers)
            ))

        return arr
