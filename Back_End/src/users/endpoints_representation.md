<!-- 2. ## 
    - Method: ``
    - Serializer: ``
    - Functionality: ``
    - Authentication: ``
    - Authorization: ``
    - URL: ``
    - Notes: `No Notes`
    - status: `coming soon...` -->

# User End-Points representation
1. ## Registration
   - Method: `POST`
   - Serializer: `RegisterSerializer`
   - Functionality: `creating the user with default workspace`
   - Authentication: `Not required`
   - Authorization: `Not required`
   - URL: `/register/`
   - Notes: `No Notes`
   - status: `ready`
2. ## Get-User-Info
   - Method: `GET`
   - Serializer: `UserSerializer`
   - Functionality: `just getting the user info with his workspaces`
   - Authentication: `required`
   - Authorization: `only admin can show any user info by id`
   - URL: `/users/{id}/`
   - Notes: `admin needs to insert the user-id in the request`
   - status: `ready`
3. ## Get-All-Users-Info
    - Method: `GET`
    - Serializer: `UserSerializer`
    - Functionality: `just getting all users info (Paginated respones)`
    - Authentication: `required`
    - Authorization: `admin can get all users info | normal-user can get only his own info`
    - URL: `/users/`
    - Notes: `this endpoint can support filtering/searching/ordering`
    - status: `in-development[Pagination/ filtering/searching/ordering]`
4. ## Token
    - Method: `POST`
    - Serializer: `users.CustomTokenObtainPairSerializer`
    - Functionality: `return access_token and refresh_token and information about user such as email and fullname (cause: so the client don't need to send another request for user information)`
    - Authentication: `not required`
    - Authorization: `not required`
    - URL: `/users/token/`
    - Notes: `send 'email' and 'password' in the request body`
    - status: `ready`
5. ## Token-Refresh
    - Method: `POST`
    - Serializer: `TokenRefreshSerializer`
    - Functionality: `refreshes the access token`
    - Authentication: `not required`
    - Authorization: `not required`
    - URL: `/users/token/refresh/`
    - Notes: `send 'refresh = (refresh token)' in the request | the response will return with a new access token`
    - status: `ready`
6.  ## Update-User-Profile-Info
    - Method: `PUT/PATCH`
    - Serializer: `UserSerializer`
    - Functionality: `update the user fields except the password and the image fields (fullname/workspaces)| if there is workspaces in the request will be added and if any workspace already exist it will be updated with the new values`
    - Authentication: `required`
    - Authorization: `normal-user / admin`
    - URL: `/users/{id}`
    - Notes: `No Notes`
    - status: `coming soon...`
7.  ## Change-User-Password
    - Method: `POST`
    - Serializer: `ChangePasswordSerializer`
    - Functionality: `passing the old password and the new one`
    - Authentication: `required`
    - Authorization: `normal-user only`
    - URL: `/users/change_password`
    - Notes: `admin can't change users passwords`
    - status: `ready`
8.  ## Change-User-Image
    - Method: `POST`
    - Serializer: `ChangeImageSerializer`
    - Functionality: `changing the profile image`
    - Authentication: `required`
    - Authorization: `normal-user only`
    - URL: `/users/{id}/change_image`
    - Notes: `No Notes`
    - status: `ready`
<!-- Invites & Workspaces -->
1.  ## Show-Invites
    - Method: ``
    - Serializer: ``
    - Functionality: ``
    - Authentication: ``
    - Authorization: ``
    - URL: ``
    - Notes: `No Notes`
    - status: `coming soon...`
2.  ## Invite-Other-User-To-Workspace
    - Method: ``
    - Serializer: ``
    - Functionality: ``
    - Authentication: ``
    - Authorization: ``
    - URL: ``
    - Notes: `admin/user can't put owner user_role to any other user`
    - status: `coming soon...`
3.  ## Kick-Other-User-From-Workspace
    - Method: ``
    - Serializer: ``
    - Functionality: ``
    - Authentication: ``
    - Authorization: ``
    - URL: ``
    - Notes: `No Notes`
    - status: `coming soon...`
4.  ## Change-Other-User-Role-In-Workspace
    - Method: ``
    - Serializer: ``
    - Functionality: ``
    - Authentication: ``
    - Authorization: ``
    - URL: ``
    - Notes: `admin/user can't put owner user_role to any other user`
    - status: `coming soon...`
5.  ## Change-Invite-status
    - Method: ``
    - Serializer: ``
    - Functionality: ``
    - Authentication: ``
    - Authorization: ``
    - URL: ``
    - Notes: `No Notes`
    - status: `coming soon...`
6. ## Accept-Invite
    - Method: ``
    - Serializer: ``
    - Functionality: ``
    - Authentication: ``
    - Authorization: ``
    - URL: ``
    - Notes: `No Notes`
    - status: `coming soon...`
7. ## Reject-Invite
    - Method: ``
    - Serializer: ``
    - Functionality: ``
    - Authentication: ``
    - Authorization: ``
    - URL: ``
    - Notes: `No Notes`
    - status: `coming soon...`
8. ## Cancel-Invite
    - Method: ``
    - Serializer: ``
    - Functionality: ``
    - Authentication: ``
    - Authorization: ``
    - URL: ``
    - Notes: `No Notes`
    - status: `coming soon...`



