import random
import time
import logme

from django.core.management.base import BaseCommand, CommandError
from FitnessPersonalArea.models import FitnessUser, FitnessTrainer, TrainerPrice, MedicalNote, UserDiary, BodyParameter,\
    BodyParameterData, TargetBodyParameter
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.utils import timezone

from faker import Faker


@logme.log
class Command(BaseCommand):
    '''
    python3 manage.py filling_data filling_data <amount of users>
    '''

    help = "Populate DB with User`s accounts, and other FAKE data."

    def add_arguments(self, parser):
        parser.add_argument('target_amount', nargs='+', type=int)

    def handle(self, *args, **options):
        start_time = time.clock()
        fake = Faker()
        # получаем кол-во аккаунтов для создания
        target = options['target_amount'][0]
        for user, index in enumerate(range(1, target)):
            try:
                # создаём обычного юзера
                new_user = User.objects.create_user(username = fake.simple_profile()['username'],
                                                    email = fake.safe_email(),
                                                    password = fake.password(),
                                                    first_name = fake.first_name(),
                                                    last_name = fake.last_name())
                # создаём фитнесс-пользователя
                new_fitness_user = FitnessUser.objects.create(user = new_user,
                                                              fitness_user_bdate = fake.date(),
                                                              fitness_user_gender = random.choice(
                                                                  (FitnessUser.male_gender,
                                                                   FitnessUser.female_gender,
                                                                   FitnessUser.secret_gender)
                                                              ),
                                                              fitness_user_type = random.choice(
                                                                  (FitnessUser.ward_user,
                                                                   FitnessUser.teacher_user)
                                                              ),
                                                              fitness_user_destination_city = fake.city()
                                                              )

                # делаем медицинские записи
                new_med_note = MedicalNote.objects.create(user = new_fitness_user,
                                                          medical_note_title = fake.text(max_nb_chars=100),
                                                          medical_note_text = fake.text(max_nb_chars=4000),
                                                          medical_note_show = random.choice((True, False)))
                for tag in fake.words(nb=4):
                    new_med_note.medical_note_tags.add(tag.lower().strip())

                # делаем записи в дневнике
                new_diary_note = UserDiary.objects.create(user = new_fitness_user,
                                                          diary_note_title = fake.text(max_nb_chars=100),
                                                          diary_note_text = fake.text(max_nb_chars=4000),
                                                          diary_note_show = random.choice((True, False)))
                for tag in fake.words(nb=4):
                    new_diary_note.diary_note_tags.add(tag.lower().strip())

                # задание параметров тела
                for param in range(1, 10):
                    new_param = BodyParameter.objects.create(user = new_fitness_user,
                                                             body_title = fake.text(max_nb_chars=100),
                                                             body_show = random.choice((True, False)))

                    for param_data in range(50, 150):
                        BodyParameterData.objects.create(user_parameter = new_param,
                                                         body_data = random.randint(50, 300),
                                                         body_datetime = fake.date_time_ad(tzinfo = timezone.utc))

                    for param_target in range(2, 4):
                        TargetBodyParameter.objects.create(target_parameter = new_param,
                                                           target_body_data = random.randint(45, 320),
                                                           target_body_datetime = fake.date_time_ad(tzinfo = timezone.utc))

                # если пользователь тренер - создаём тренера и задаём его расценки
                if new_fitness_user.fitness_user_type == FitnessUser.teacher_user:
                    # создаём тренера
                    new_fitness_trainer = FitnessTrainer.objects.create(user = new_fitness_user,
                                                                        trainer_employment_status = random.choice((True,
                                                                                                                   False)
                                                                                                                  ),
                                                                        trainer_description = fake.text(max_nb_chars=5000)
                                                                        )
                    # создаём расценки тренера
                    for price in range(1, 20):
                        TrainerPrice.objects.create(user = new_fitness_trainer,
                                                    trainer_price_hour = random.randint(1, 999),
                                                    trainer_price_comment = fake.text(max_nb_chars=100),
                                                    trainer_price_currency = random.choice(('USD',
                                                                                            'RUB',
                                                                                            'BYN',
                                                                                            'GBP',
                                                                                            'EUR')),
                                                    trainer_price_bargaining = random.choice((True, False)),
                                                    trainer_price_actuality = random.choice((True, False)),
                                                    trainer_price_show = random.choice((True, False)))

            except IntegrityError:
                pass
            except Exception as err:
                self.logger.error(f'In - Command.handle; '
                                  f'Error - {err};')
                break
            finally:
                self.logger.info(f'{round(index/target*100, 2)}% выполнено ...')

        self.logger.info(f'\n Наполнение выполнено за {round(time.clock() - start_time, 3)} секунд')
