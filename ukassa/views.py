from django.http import HttpResponse
from rest_framework.views import APIView


# Create your views here.
from yookassa import Configuration, Payment
from yookassa.domain.notification import WebhookNotification, WebhookNotificationEventType

from tgbot.dispatcher import bot


class ProcessUkassaEvent(APIView):
    def post(self, request, *args, **kwargs):
        data = request.body
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
                # Специфичная логика
                # ...
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
            Configuration.configure('845479', 'test_XXXXXXXX')
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

        except Exception:
            # Обработка ошибок
            return HttpResponse(status=400)  # Сообщаем кассе об ошибке

        return HttpResponse(status=200)  # Сообщаем кассе, что все хорошо
