from django.contrib.admin.models import LogEntry,ContentType, ADDITION,CHANGE,DELETION
from django.utils.encoding import force_text


def add_log(user_id,object,message):

    return LogEntry.objects.log_action(
            user_id=user_id,
            content_type_id=ContentType.objects.get_for_model(object).pk,
            object_id=object.pk,
            object_repr=force_text(object),
            action_flag=ADDITION,
            change_message=message


        )



def log_change(user_id,object, message):
    """ triggered when a user makes a change to a model"""


    return LogEntry.objects.log_action(
        user_id=user_id,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=force_text(object),
        action_flag=CHANGE,
        change_message=message
    )

def log_deletion(user_id, object, object_repr):


    return LogEntry.objects.log_action(
            user_id=user_id,
            content_type_id=ContentType.objects.get_for_model(object).pk,
            object_id=object.pk,
            object_repr=force_text(object),
            action_flag=DELETION,
            # change_message = message
        )












