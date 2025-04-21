from django.core.management.base import BaseCommand

from users.models import User
from workspaces.models import Workspace , Users_Workspaces

class Command(BaseCommand):
    help = ""

    def create_many_users(self , users):
        created_users = []
        for one in users:
            user = User.objects.create_user(email=one["email"] , fullname=one["fullname"], password=one["password"])
            workspace = Workspace.objects.create(owner=user , name=f'{one["fullname"]}-Default-Workspace')
            membership = Users_Workspaces.objects.create(user=user , workspace=workspace , user_role='owner')
            created_users.append({"user":user , "workspace":workspace})
        return created_users

    def handle(self, *args, **options):
        ######################################### create superuser #########################################
        user = User.objects.filter(email='j@j.com').first()
        if not user:
            user = User.objects.create_superuser(email='j@j.com' , fullname='john-doe' , password='testtest')
            workspace = Workspace.objects.create(owner=user , name='Default-Workspace')
            membership = Users_Workspaces.objects.create(user=user , workspace=workspace , user_role='owner')
        if not user.is_staff:
            user.is_staff = True
            user.is_superuser = True
            user.save()
        #########################################------------------#########################################

        ########################################### create users ###########################################
        users=[
            {"email":"a@a.com", "fullname":"A" , "password":"testtest"},
            {"email":"b@b.com", "fullname":"B" , "password":"testtest"},
            {"email":"c@c.com", "fullname":"C" , "password":"testtest"},
            {"email":"d@d.com", "fullname":"D" , "password":"testtest"},
            {"email":"e@e.com", "fullname":"E" , "password":"testtest"},
            {"email":"f@f.com", "fullname":"F" , "password":"testtest"},
            {"email":"g@g.com", "fullname":"G" , "password":"testtest"},
            {"email":"h@h.com", "fullname":"H" , "password":"testtest"},
            {"email":"i@i.com", "fullname":"I" , "password":"testtest"},
            {"email":"z@z.com", "fullname":"Z" , "password":"testtest"},
            {"email":"k@k.com", "fullname":"K" , "password":"testtest"},
            {"email":"l@l.com", "fullname":"L" , "password":"testtest"},
            {"email":"m@m.com", "fullname":"M" , "password":"testtest"},
            {"email":"n@n.com", "fullname":"N" , "password":"testtest"},
            {"email":"o@o.com", "fullname":"O" , "password":"testtest"},
            {"email":"p@p.com", "fullname":"P" , "password":"testtest"},
            {"email":"q@q.com", "fullname":"Q" , "password":"testtest"},
            {"email":"r@r.com", "fullname":"R" , "password":"testtest"},
            {"email":"s@s.com", "fullname":"S" , "password":"testtest"},
            {"email":"t@t.com", "fullname":"T" , "password":"testtest"},
            {"email":"u@u.com", "fullname":"U" , "password":"testtest"},
        ]
        users = self.create_many_users(users)
        #########################################------------------#########################################

        #######################################-create--memberships-########################################
        memberships=[]
        for i in range(0,len(users)-2):
            memberships.append(Users_Workspaces(user=users[i]['user'] , workspace=users[i+1]['workspace'] , user_role='can_view'))
            memberships.append(Users_Workspaces(user=users[i]['user'] , workspace=users[i+2]['workspace'] , user_role='can_view'))

        memberships.append(Users_Workspaces(user=users[len(users)-2]['user'] , workspace=users[0]['workspace'] , user_role='can_view'))
        memberships.append(Users_Workspaces(user=users[len(users)-2]['user'] , workspace=users[1]['workspace'] , user_role='can_view'))
        memberships.append(Users_Workspaces(user=users[len(users)-1]['user'] , workspace=users[2]['workspace'] , user_role='can_view'))
        memberships.append(Users_Workspaces(user=users[len(users)-1]['user'] , workspace=users[3]['workspace'] , user_role='can_view'))

        Users_Workspaces.objects.bulk_create(memberships)
        #########################################------------------#########################################