from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from entries.models import Entry

User = get_user_model()
        
ENTRY_DETAIL_ENDPOINT = 'http://127.0.0.1:8000/api/entries/1/'
ENTRY_LIST_ENDPOINT = 'http://127.0.0.1:8000/api/entries/'
LOGIN_ENDPOINT = 'http://127.0.0.1:8000/api/auth/login/'
REGISTER_ENDPOINT = 'http://127.0.0.1:8000/api/auth/register/'

class EntryPointAPITest(APITestCase):

    def setUp(self):
        test_user = User.objects.create(username='test@test.com', email='test@test.com')
        test_user.set_password('password')
        test_user.save()
        super_user = User.objects.create(username='super', email='super@super.com')
        super_user.set_password('password')
        super_user.save()

        supers_entry = Entry.objects.create(
            user=test_user,
            title='super title',
            content='super content').save()
    
    def test_create_entry(self):
        user = User.objects.get(username='test@test.com')
        self.client.force_authenticate(user=user)
        entry_data = {
            "title": 'test ti',
            "content": 'test h'
            }
        create_resp = self.client.post(ENTRY_LIST_ENDPOINT, data=entry_data, format='json')
        print(create_resp.json())
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)

    def test_update_entry(self):
        user = User.objects.get(username='super')
        self.client.force_authenticate(user=user)
        entry_data = {
            "title": 'old title',
            "content": 'old cont',
        }
        create_resp = self.client.post(ENTRY_LIST_ENDPOINT, data=entry_data, format='json')

        NEW_DETAIL_ENDPOINT = 'http://127.0.0.1:8000/api/entries/3/'

        updated_content = {
            "content" : 'better content'
        }
        update_resp = self.client.put(NEW_DETAIL_ENDPOINT, data=updated_content, format='json')

    def test_add_and_delete_entry_to_appreciated_or_changed_perc(self):
        entry_id = Entry.objects.first().id
        user = User.objects.get(username='test@test.com')
        self.client.force_authenticate(user=user)
        USER_ENDPOINT = 'http://127.0.0.1:8000/api/users/test/'

        data = {
            "appr": entry_id,
            "changed_perc": entry_id,
        }
        put_resp = self.client.patch(USER_ENDPOINT, data=data, format='json')
        put_resp_2 = self.client.patch(USER_ENDPOINT, data=data, format='json')

    def test_change_username(self):
        user = User.objects.get(username='test@test.com')
        self.client.force_authenticate(user=user)
        USER_ENDPOINT = 'http://127.0.0.1:8000/api/users/test@test.com/'
        data = {
            "username": 'newusername',
            # "email": 'email2@email.com',
            "country": 'AR', 
        }
        put_resp = self.client.patch(USER_ENDPOINT, data=data, format='json')
        print(put_resp.data)


    # def test_register_get_token(self):
    #     register_data = {
    #         "username": 'test1',
    #         "email": 'test1@test1.com',
    #         "password": 12,
    #         "password2": 12,
    #     }
    #     reg_resp = self.client.post(REGISTER_ENDPOINT, data=register_data)
    #     self.assertEqual(reg_resp.status_code, status.HTTP_201_CREATED)

    # def test_login_get_token(self):
    #     login_data = {
    #         "username": 'test',
    #         "password": 'password',
    #     }
    #     login_resp = self.client.post(LOGIN_ENDPOINT, data=login_data, format='json')
    #     print(login_resp.json())
    #     self.assertEqual(login_resp.status_code, status.HTTP_200_OK)
    


