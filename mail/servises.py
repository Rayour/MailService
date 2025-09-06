import datetime
import logging
import os

from django.core.mail import send_mail

from config.settings import BASE_DIR, DEFAULT_FROM_EMAIL

from .models import Attempt

date_today = datetime.datetime.today().strftime("%d-%m-%Y")
file_name = f"{date_today}_logs.log"
log_path = os.path.join(BASE_DIR, "logs", file_name)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=log_path,
    filemode="a",
    encoding="utf-8",
)
logger = logging.getLogger("services")


class MailService:
    """Класс для описания бизнес-логики отправки писем"""

    @staticmethod
    def send_email(newsletter, user):
        """Метод отправки сообщения"""

        newsletter.start_send_time = datetime.datetime.now()
        logger.info(f"Дата и время начала рассылки {newsletter.start_send_time}")
        newsletter.status = "started"
        logger.info(f"Статус рассылки {newsletter.status}")
        from_email = DEFAULT_FROM_EMAIL
        for customer in newsletter.customers.all():
            recipient_list = [customer.email]
            try:
                logger.info(f"Попытка отправки письма {newsletter.message.topic} на почту {customer.email}")
                send_mail(newsletter.message.topic, newsletter.message.text, from_email, recipient_list)
            except Exception as e:
                logger.warning(f"Ошибка при отправке письма {newsletter.message.topic} на почту {customer.email}: {e}")
                attempt = Attempt(
                    status="fail",
                    customer=customer,
                    newsletter=newsletter,
                    server_response=e,
                    owner=user)
                attempt.save()
                logger.info("Создана запись о попытке отправки")
            else:
                attempt = Attempt(
                    status="success",
                    customer=customer,
                    newsletter=newsletter,
                    owner=user)
                attempt.save()
                logger.info("Создана запись об отправке")

        newsletter.finish_send_time = datetime.datetime.now()
        logger.info(f"Дата и время окончания рассылки {newsletter.finish_send_time}")
        newsletter.status = "finished"
        logger.info(f"Статус рассылки {newsletter.status}")
        newsletter.save()
