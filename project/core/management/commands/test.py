# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from config.tasks import foodwebsite_task
from core.bl.time_helper import timeit


# @analyze
@timeit
def test_script():
    pass
    # photo_comp = PhotoComparison(photo_id=9)
    # photo_comp.save()

    # ch_photo = ChallengePhoto(challenge_id=49, photo_comparison_id=8)
    # ch_photo.save()

    # init_week_challenge_task()
    # kwargs = {}
    # args = ()
    # try:
    #     t.run_spiders(FoodWebsite, 'scraper', 'scraper_runtime', 'food_spider', *args, **kwargs)
    # except Exception as ex:
    #     print(ex)

    foodwebsite_task()

    # challenge_finish_task()

    # photo = Photo.objects.filter(id=70).first()
    # photo.create_copies()

    # photo_position = PhotoPosition(challenge_id=104)
    # photo_position.update()

    # photo_position = PhotoPosition(vote_id=20)
    # photo_position = PhotoPosition(challenge_id=81)
    # photo_position.update()

    # user = User.objects.filter(email='admin@admin.com').first()
    # comment = PhotoComment.objects.filter(id=1).first()
    # user_notif = AddUserNotif(user.id, Notification.EVENT_NEW_COMMENT, linked_object=comment)
    # user_notif.run()

    # notifications = Notification.objects.filter(user=user).all()
    # for item in notifications:
    #     prn(item)

    # challenge_photos = ChallengePhoto.objects.filter(
    #     photo_comparison__photo__user__email='megajoe17@mail.ru')
    # for challenge_photo in challenge_photos:
    #     ChallengePhotoWinner.get_or_create(challenge_photo)


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Test script started')
        test_script()
        print('Test script finished')
