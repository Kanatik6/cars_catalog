from celery import shared_task



@shared_task
def check():
    for i in range(1,21):
        print(i)
    return "Done"