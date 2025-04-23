from django.core.management.base import BaseCommand

from users.models import User
from workspaces.models import Workspace , Users_Workspaces
from tasks.models import Task_Category , Category_Option , workspace_category_option

class Command(BaseCommand):
    help = "populate the database with fake data for testing and debugging"

    def create_category_if_not_exist(self , category_name):
        category = Task_Category.objects.filter(name=category_name).first()
        if not category:
            category = Task_Category.objects.create(name=category_name)
        return category
    def create_category_option_if_not_exist(self , option_name):
        option = Category_Option.objects.filter(name=option_name).first()
        if not option:
            option = Category_Option.objects.create(name=option_name)
        return option
    def add_main_categories_to_workspace(self, workspace):
        #####################################  create main categories ######################################
        status_category = self.create_category_if_not_exist(category_name='status')
        status_category_pending = self.create_category_option_if_not_exist(option_name='pending')
        status_category_in_progress = self.create_category_option_if_not_exist(option_name='in progress')
        status_category_completed = self.create_category_option_if_not_exist(option_name='completed')

        priority_category = self.create_category_if_not_exist(category_name='priority')
        priority_category_low = self.create_category_option_if_not_exist(option_name='low')
        priority_category_medium = self.create_category_option_if_not_exist(option_name='medium')
        priority_category_high = self.create_category_option_if_not_exist(option_name='high')

        # Creating the relations between admin workspace-categories-options
        relations=[
                workspace_category_option(workspace=workspace , task_category=status_category , category_option=status_category_pending),
                workspace_category_option(workspace=workspace , task_category=status_category , category_option=status_category_in_progress),
                workspace_category_option(workspace=workspace , task_category=status_category , category_option=status_category_completed),
                
                workspace_category_option(workspace=workspace , task_category=priority_category , category_option=priority_category_low),
                workspace_category_option(workspace=workspace , task_category=priority_category , category_option=priority_category_medium),
                workspace_category_option(workspace=workspace , task_category=priority_category , category_option=priority_category_high),
            ]
        workspace_category_option.objects.bulk_create(relations)

    def create_many_users(self , users):
        created_users = []
        for one in users:
            user = User.objects.create_user(email=one["email"] , fullname=one["fullname"], password=one["password"])
            workspace = Workspace.objects.create(owner=user , name=f'{one["fullname"]}-Default-Workspace')
            membership = Users_Workspaces.objects.create(user=user , workspace=workspace , user_role='owner')
            # Creating Main Categories and Assign them to workspace
            self.add_main_categories_to_workspace(workspace)
            created_users.append({"user":user , "workspace":workspace})
        return created_users

    def handle(self, *args, **options):
        ######################################### create superuser #########################################
        user = User.objects.filter(email='j@j.com').first()
        if not user:
            user = User.objects.create_superuser(email='j@j.com' , fullname='john-doe' , password='testtest')
            workspace = Workspace.objects.create(owner=user , name='Default-Workspace')
            membership = Users_Workspaces.objects.create(user=user , workspace=workspace , user_role='owner')
            # Creating Main Categories and Assign them to workspace
            self.add_main_categories_to_workspace(workspace)
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