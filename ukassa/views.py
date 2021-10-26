import traceback
import json

from django.http import HttpResponse
from rest_framework.views import APIView


# Create your views here.
from yookassa import Configuration, Payment
from yookassa.domain.notification import WebhookNotification, WebhookNotificationEventType

from tgbot.dispatcher import bot
from tub.settings import UKASSA_SECRET_KEY, SHOP_ID


Configuration.configure(SHOP_ID, UKASSA_SECRET_KEY)


class ProcessUkassaEvent(APIView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        bot.send_message(350490234, f"data2222222222\n{data}")
        try:
            # Создание объекта класса уведомлений в зависимости от события
            notification_object = WebhookNotification(data)
            response_object = notification_object.object
            bot.send_message(350490234, f"response_object={response_object}")
            if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
                some_data = {
                    'paymentId': response_object.id,
                    'paymentStatus': response_object.status,
                }
                # Специфичная логика
                # ...
            elif notification_object.event == WebhookNotificationEventType.PAYMENT_WAITING_FOR_CAPTURE:
                some_data = {
                    'paymentId': response_object.id,
                    'paymentStatus': response_object.status,
                }

                Payment.capture(payment_id=some_data['paymentId'])  # принимаем платеж
            elif notification_object.event == WebhookNotificationEventType.PAYMENT_CANCELED:
                some_data = {
                    'paymentId': response_object.id,
                    'paymentStatus': response_object.status,
                }
                # Специфичная логика
                # ...
            elif notification_object.event == WebhookNotificationEventType.REFUND_SUCCEEDED:
                some_data = {
                    'refundId': response_object.id,
                    'refundStatus': response_object.status,
                    'paymentId': response_object.payment_id,
                }
                # Специфичная логика
                # ...
            else:
                # Обработка ошибок
                return HttpResponse(status=400)  # Сообщаем кассе об ошибке

            # Специфичная логика
            # ...
            # Получим актуальную информацию о платеже
            payment_info = Payment.find_one(some_data['paymentId'])
            bot.send_message(350490234, f"payment_info:\n{payment_info}")
            if payment_info:
                payment_status = payment_info.status
                # Специфичная логика
                # ...
            else:
                # Обработка ошибок
                return HttpResponse(status=400)  # Сообщаем кассе об ошибке

        except Exception as e:
            error_stack = traceback.format_exc()
            bot.send_message(350490234, f"{error_stack} {e}")
            # Обработка ошибок
            return HttpResponse(status=400)  # Сообщаем кассе об ошибке

        return HttpResponse(status=200)  # Сообщаем кассе, что все хорошо
