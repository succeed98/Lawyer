from background_task import background
from lawyers.models import User
from schedules.models import Schedule, MeetingSession

import nexmo

client = nexmo.Client(key='81e13046', secret='U21UOjSdcAqpY7l0')

# client.send_message({
#     'from': 'Minkah Premo & Co.',
#     'to': '233555404976',
#     'text': 'Hello from Vonage',
# })


@background(schedule=60)
def notify_user(msg1, msg2, user_id, repeat_until=None): # 16.04.2021
    # lookup user by id and send them a message
    user = User.objects.get(pk=user_id)
    user.email_user(msg1, msg2)


    # Commented out on 20.04.2021 to avoid events other than tasks from sending text notificvations via nexmo api
    # client = nexmo.Client(key='5b2edefc', secret='eh53erLJ6TZcVIj2')

    # client.send_message({
    #     'from': 'Lawyer System.',
    #     'to': user.phone,
    #     'text': msg2,
    # })

    # print('sent')
    
    
# 20.04.2021
# PUrpose of creating this new function is to separate emails from text messages for all other events, but tasks.
# def notify_task .....    
@background(schedule=60)
def notify_task(msg1, msg2, user_id, repeat_until=None): # 16.04.2021
    # lookup user by id and send them a message
    user = User.objects.get(pk=user_id)
    user.email_user(msg1, msg2)


    client = nexmo.Client(key='5b2edefc', secret='eh53erLJ6TZcVIj2')

    client.send_message({
        'from': 'Lawyer System.',
        'to': user.phone,
        'text': msg2,
    })

    print('sent')

@background(schedule=60)
def notify_staff(user_id, msg1, msg2):
    # lookup user by id and send them a message
    user = User.objects.get(pk=user_id)
    user.email_user(msg1, msg2)

    client = nexmo.Client(key='5b2edefc', secret='eh53erLJ6TZcVIj2')

    client.send_message({
        'from': 'Lawyer System.',
        'to': user.phone,
        'text': msg2,
    })
    print('sent')



def notify_approve(user_id, msg1, msg2):
    # lookup user by id and send them a message
    user = User.objects.get(pk=user_id)
    client = nexmo.Client(key='5b2edefc', secret='eh53erLJ6TZcVIj2')

    client.send_message({
        'from': 'Lawyer System.',
        'to': user.phone,
        'text': msg2,
    })
    user.email_user(msg1, msg2)
    print('sent')


@background(schedule=60)
def start_schedule(shedule_id, user_id):
    shedule = MeetingSession.objects.get(id=shedule_id)
    user = User.objects.get(pk=user_id)
    message = 'Dear {}, your session in the {} room will start at {}'.format(
        user.first_name, shedule.room, shedule.start_time)
    client = nexmo.Client(key='5b2edefc', secret='eh53erLJ6TZcVIj2')

    client.send_message({
        'from': 'Lawyer System.',
        'to': user.phone,
        'text': msg2,
    })
    user.email_user("Start Session", message)


# @background
def end_schedule(shedule_id, user_id):
    shedule = MeetingSession.objects.get(id=shedule_id)
    shedule.expired = True
    shedule.save()
    user = User.objects.get(pk=user_id)
    message = 'Dear {} your session ends at {}'.format(
        user.first_name, shedule.end_time)
    client = nexmo.Client(key='5b2edefc', secret='eh53erLJ6TZcVIj2')

    client.send_message({
        'from': 'Lawyer System.',
        'to': user.phone,
        'text': msg2,
    })
    user.email_user("End Session", message)
