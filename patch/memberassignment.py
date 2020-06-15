from hc.accounts.models import Member, Project

class MemberAssignmentMiddleware(object):
    def __init__(self, get_response):
        # One-time configuration and initialization.
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if not request.user.is_authenticated or request.path != "/":
            return self.get_response(request)

        for project in Project.objects.all():
            if is_member_assignment_needed(project, request.user):
                member_assignment(request.user, project)

        # Code to be executed for each request/response after
        # the view is called.
        return self.get_response(request)

def is_member_assignment_needed(project, user):
    return not Member.objects.filter(project=project, user=user)

def member_assignment(member, project):
    Member.objects.create(user=member, project=project)