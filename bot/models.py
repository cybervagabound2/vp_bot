import datetime
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Lang(models.Model):
    lang = models.CharField(max_length=32)

    def __str__(self):
        return self.lang


class Buttons(models.Model):
    rus = models.CharField(max_length=250)
    eng = models.CharField(max_length=250)
    uzb = models.CharField(max_length=250)


class Users(models.Model):
    ROLES = (
        ('ad', 'administrator'),
        ('md', 'moderator'),
        ('sl', 'seller'),
        ('us', 'user')
    )
    telegram_id = models.IntegerField()
    username = models.CharField(max_length=32, null=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    banned = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)
    invited_by = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)
    balance = models.IntegerField(default=0)
    params = models.CharField(max_length=1000, default='[]')
    role = models.CharField(max_length=2, default='us', choices=ROLES)
    lang = models.ForeignKey(Lang, on_delete=models.SET_NULL, null=True)
    rules = models.BooleanField(default=False)
    last_message_id = models.CharField(max_length=255, null=True)

    def FirstName(self):
        if self.first_name:
            return self.first_name
        else:
            return ''
    def LastName(self):
        if self.last_name:
            return self.last_name
        else:
            return ''

    def GetButtons(self, rus_buttons):
        button = Buttons.objects.get(rus=rus_buttons)
        if self.lang.lang == 'Eng':
            return button.eng
        elif self.lang.lang == 'Rus':
            return button.rus
        elif self.lang.lang == 'Uzb':
            return button.uzb
        else:
            return button.eng

    def DelEndParams(self, count=0):
        if count == 0:
            index = self.params.rfind('/')
            self.params = self.params[:index]
        else:
            while count != 0:
                index = self.params.rfind('/')
                self.params = self.params[:index]
                count -= 1
        self.save()

    def GetEndParams(self):
        index = self.params.rfind('/')
        return self.params[index:]

    def Error(selt, bot, e, patch):
        bot.send_message(text=patch+'\n'+str(e),
                         chat_id=657753504)
        return

    def SendMessage(self, bot, msg, keyboard=None, photo=None, save_massage_id=None):
        try:
            if self.last_message_id:
                bot.delete_message(chat_id=self.telegram_id, message_id=self.last_message_id)
                self.last_message_id = None
                self.save()
        except Exception as e:
            self.Error(bot, e, 'bot.delete_message')
        try:
            if not photo:
                message = bot.send_message(text=msg, parse_mode='HTML',
                                 disable_web_page_preview=True,
                                 chat_id=self.telegram_id,
                                 reply_markup=keyboard)
            else:
                message = bot.send_photo(chat_id=self.telegram_id,caption=msg,
                               photo=photo, parse_mode='HTML', reply_markup=keyboard)
            if save_massage_id:
                self.last_message_id = message.message_id
                self.save()
        except Exception as error:
            if "bot was blocked by the user" in str(error) or "user is deactivated" in str(
                    error) or "chat not found" in str(error):
                self.blocked = True
                self.rules = False
                self.save()


    def __str__(self):
        return self.telegram_id


class MutualPRCategory(MPTTModel):
    category_name = models.CharField(max_length=200)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['category_name']


class Ad(models.Model):
    STATUS = (
        ('rd', 'ready'),
        ('nr', 'not ready')
    )
    creator = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    channel_name = models.CharField(max_length=100, null=True)
    min_count = models.IntegerField(null=True)
    comment = models.CharField(max_length=500, null=True)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS, default='nr')
    localization = models.CharField(max_length=30, null=True)
