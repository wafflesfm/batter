from django.test import TestCase
from django.contrib.auth.models import User

from .. import models


class AchievementTests(TestCase):
    def setUp(self):
        self.samantha = User.objects.create_user(
            'samantha',
            'samantha@example.com',
            'soliloquy'
        )
        self.bob = User.objects.create_user(
            'bob',
            'bob@example.com',
            'antimony'
        )

    def test_topsecret(self):
        self.ach = models.Achievement(
            slug="topsecret", title="Top Secret",
            description="Uber top secret",
            secrecy_type=models.Achievement.SECRECY_TYPES.invisible
        )
        self.ach.save()
        self.ach.grant(
            self.samantha,
            models.AchievementOwnership.GRANT_REASONS.condition_met
        )
        self.assertTrue(
            self.ach.achievement_is_visible(self.samantha)
        )
        self.assertTrue(
            self.ach.description_is_visible(self.samantha)
        )
        self.assertTrue(
            self.ach.title_is_visible(self.samantha)
        )
        self.assertTrue(
            self.ach.image_is_visible(self.samantha)
        )
        self.assertTrue(
            self.ach.owned_by(self.samantha)
        )

        self.assertFalse(
            self.ach.achievement_is_visible(self.bob)
        )
        self.assertFalse(
            self.ach.description_is_visible(self.bob)
        )
        self.assertFalse(
            self.ach.title_is_visible(self.bob)
        )
        self.assertFalse(
            self.ach.image_is_visible(self.bob)
        )
        self.assertFalse(
            self.ach.owned_by(self.bob)
        )

    def test_topsecret(self):
        self.ach = models.Achievement(
            slug="topsecret", title="Top Secret!!!",
            description="Top secret",
            secrecy_type=models.Achievement.SECRECY_TYPES.all_hidden
        )
        self.ach.save()
        self.ach.grant(
            self.samantha,
            models.AchievementOwnership.GRANT_REASONS.condition_met
        )
        self.assertTrue(
            self.ach.achievement_is_visible(self.samantha)
        )
        self.assertTrue(
            self.ach.description_is_visible(self.samantha)
        )
        self.assertTrue(
            self.ach.title_is_visible(self.samantha)
        )
        self.assertTrue(
            self.ach.image_is_visible(self.samantha)
        )
        self.assertTrue(
            self.ach.owned_by(self.samantha)
        )

        self.assertTrue(
            self.ach.achievement_is_visible(self.bob)
        )
        self.assertFalse(
            self.ach.description_is_visible(self.bob)
        )
        self.assertFalse(
            self.ach.title_is_visible(self.bob)
        )
        self.assertFalse(
            self.ach.image_is_visible(self.bob)
        )
        self.assertFalse(
            self.ach.owned_by(self.bob)
        )

    def test_secret(self):
        self.ach = models.Achievement(
            slug="secret", title="The cat sat on the mat",
            description="Haha, the title has nothing to do with how to get me",
            secrecy_type=models.Achievement.SECRECY_TYPES.image_desc_hidden
        )
        self.ach.save()
        self.ach.grant(
            self.samantha,
            models.AchievementOwnership.GRANT_REASONS.condition_met
        )
        self.assertTrue(
            self.ach.achievement_is_visible(self.samantha)
        )
        self.assertTrue(
            self.ach.description_is_visible(self.samantha)
        )
        self.assertTrue(
            self.ach.title_is_visible(self.samantha)
        )
        self.assertTrue(
            self.ach.image_is_visible(self.samantha)
        )
        self.assertTrue(
            self.ach.owned_by(self.samantha)
        )

        self.assertTrue(
            self.ach.achievement_is_visible(self.bob)
        )
        self.assertFalse(
            self.ach.description_is_visible(self.bob)
        )
        self.assertTrue(
            self.ach.title_is_visible(self.bob)
        )
        self.assertFalse(
            self.ach.image_is_visible(self.bob)
        )
        self.assertFalse(
            self.ach.owned_by(self.bob)
        )

    def test_semisecret(self):
        self.ach = models.Achievement(
            slug="semisecret", title="See the image",
            description="The image just gives it all away :(",
            secrecy_type=models.Achievement.SECRECY_TYPES.description_hidden
        )
        self.ach.save()
        self.ach.grant(
            self.samantha,
            models.AchievementOwnership.GRANT_REASONS.condition_met
        )
        self.assertTrue(
            self.ach.achievement_is_visible(self.samantha)
        )
        self.assertTrue(
            self.ach.description_is_visible(self.samantha)
        )
        self.assertTrue(
            self.ach.title_is_visible(self.samantha)
        )
        self.assertTrue(
            self.ach.image_is_visible(self.samantha)
        )
        self.assertTrue(
            self.ach.owned_by(self.samantha)
        )

        self.assertTrue(
            self.ach.achievement_is_visible(self.bob)
        )
        self.assertFalse(
            self.ach.description_is_visible(self.bob)
        )
        self.assertTrue(
            self.ach.title_is_visible(self.bob)
        )
        self.assertTrue(
            self.ach.image_is_visible(self.bob)
        )
        self.assertFalse(
            self.ach.owned_by(self.bob)
        )

    def test_image_hidden(self):
        self.ach = models.Achievement(
            slug="spooky", title="Scary image, right",
            description="Unlock me",
            secrecy_type=models.Achievement.SECRECY_TYPES.image_hidden
        )
        self.ach.save()
        self.ach.grant(
            self.samantha,
            models.AchievementOwnership.GRANT_REASONS.condition_met
        )
        self.assertTrue(
            self.ach.achievement_is_visible(self.samantha)
        )
        self.assertTrue(
            self.ach.description_is_visible(self.samantha)
        )
        self.assertTrue(
            self.ach.title_is_visible(self.samantha)
        )
        self.assertTrue(
            self.ach.image_is_visible(self.samantha)
        )
        self.assertTrue(
            self.ach.owned_by(self.samantha)
        )

        self.assertTrue(
            self.ach.achievement_is_visible(self.bob)
        )
        self.assertTrue(
            self.ach.description_is_visible(self.bob)
        )
        self.assertTrue(
            self.ach.title_is_visible(self.bob)
        )
        self.assertFalse(
            self.ach.image_is_visible(self.bob)
        )
        self.assertFalse(
            self.ach.owned_by(self.bob)
        )

    def test_public(self):
        self.ach = models.Achievement(
            slug="public", title="BOOORING",
            description="Blergh",
            secrecy_type=models.Achievement.SECRECY_TYPES.public
        )
        self.ach.save()
        self.ach.grant(
            self.samantha,
            models.AchievementOwnership.GRANT_REASONS.condition_met
        )
        self.assertTrue(
            self.ach.achievement_is_visible(self.samantha)
        )
        self.assertTrue(
            self.ach.description_is_visible(self.samantha)
        )
        self.assertTrue(
            self.ach.title_is_visible(self.samantha)
        )
        self.assertTrue(
            self.ach.image_is_visible(self.samantha)
        )
        self.assertTrue(
            self.ach.owned_by(self.samantha)
        )

        self.assertTrue(
            self.ach.achievement_is_visible(self.bob)
        )
        self.assertTrue(
            self.ach.description_is_visible(self.bob)
        )
        self.assertTrue(
            self.ach.title_is_visible(self.bob)
        )
        self.assertTrue(
            self.ach.image_is_visible(self.bob)
        )
        self.assertFalse(
            self.ach.owned_by(self.bob)
        )

    def test_str(self):
        self.ach = models.Achievement(
            slug="public", title="BOOORING",
            description="Blergh",
            secrecy_type=models.Achievement.SECRECY_TYPES.public
        )
        self.assertEquals(str(self.ach), self.ach.title)


class AchievementOwnershipTests(TestCase):
    def setUp(self):
        self.samantha = User.objects.create_user(
            'samantha',
            'samantha@example.com',
            'soliloquy'
        )
        self.bob = User.objects.create_user(
            'bob',
            'bob@example.com',
            'antimony'
        )
        self.ach = models.Achievement(
            slug="public", title="BOOORING",
            description="Blergh",
            secrecy_type=models.Achievement.SECRECY_TYPES.public
        )
        self.sam_ach_own = models.AchievementOwnership(
            user=self.samantha,
            achievement=self.ach
        )

    def test_str(self):
        self.assertEquals(str(self.sam_ach_own), "BOOORING owned by samantha")
