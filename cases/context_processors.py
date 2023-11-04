from comment.models import Comment
from cases.models import Case,Timer
from lawyers.models import Lawyer
from resources.models import  Book,BookHistory
from documents.models import Document,RequestArchive,DocumentRecord
from notify.models import Notification

import datetime



def user_messages(request):
    # Create fixed data structures to pass to template
    # data could equally come from database queries
    # web services or social APIs

    """ comment notification variable that is accessible in every django template """

    new_date=datetime.datetime.now() - datetime.timedelta(days=3)


    try:
        lawyer=get_lawyer(request.user)
        x=Case.objects.filter(lawyer=lawyer)
        cases=list(map(lambda i:i.pk,x))
        my_messages=Comment.objects.filter(edited__gte=new_date,object_id__in=cases).order_by('-edited')[:5]

        book_request=BookHistory.objects.filter(approved=False).count()
        approved_request=BookHistory.objects.filter(approved=True).count()

        doc_request=DocumentRecord.objects.filter(approved=False).count()
        doc_approved=DocumentRecord.objects.filter(approved=True).count()

        qs1=Timer.objects.filter(user=request.user)
        qs2=Timer.objects.filter(is_active=True)
        timer_qs=qs2.intersection(qs1)
        print(timer_qs)
        try:
            notifications = Notification.objects.filter(recipient=request.user.pk,read=False)
        except:
            print('')



        completed = Case.objects.filter(closed=True)

        pending = Case.objects.filter(closed=False)
        return {
            'new_comments': my_messages,
            'pending':pending,
            'completed':completed,

            'book_request':book_request,
            'approved_request':approved_request,
            'doc_approved':doc_approved,
            'document_request':doc_request,
            'notifications_':notifications,
            'timer_qs':timer_qs,
        }
    except:
        return {}


def get_lawyer(user):
    """ fetch lawyer instance for the current user. Takes a user instance as a parameter  """
    try:
        qs=Lawyer.objects.get(user=user)
        return qs

    except :
        return None







