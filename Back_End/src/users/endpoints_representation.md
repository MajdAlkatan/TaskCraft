<!-- 2. ## 
    - Method: ``
    - Serializer: ``
    - Functionality: ``
    - Authentication: ``
    - Authorization: ``
    - URL: ``
    - Notes: `No Notes` -->

# End-Points representation
1. ## Registration
   - Method: `POST`
   - Serializer: `RegisterSerializer`
   - Functionality: `creating the user with default workspace`
   - Authentication: `Not required`
   - Authorization: `Not required`
   - URL: `/register/`
   - Notes: `No Notes`
2. ## Get-User-Info
   - Method: `GET`
   - Serializer: `UserSerializer`
   - Functionality: `just getting the user info with his workspaces`
   - Authentication: `required`
   - Authorization: `user: can show just his own info | admin: can show any user info by id`
   - URL: `/users/{id}/`
   - Notes: `admin needs to insert the user-id in the request but the user don't`
3. ## Get-All-Users-Info
    - Method: `GET`
    - Serializer: `UserSerializer`
    - Functionality: `just getting all users info (Paginated respones)`
    - Authentication: `required`
    - Authorization: `Only admins can use this endpoint`
    - URL: `/users/`
    - Notes: `this endpoint can support filtering/searching/ordering`
4. ## Join-Workspace
    - Method: ``
    - Serializer: ``
    - Functionality: ``
    - Authentication: ``
    - Authorization: ``
    - URL: ``
    - Notes: `No Notes`
5. ## Invite-Other-User-To-Workspace
    - Method: ``
    - Serializer: ``
    - Functionality: ``
    - Authentication: ``
    - Authorization: ``
    - URL: ``
    - Notes: `No Notes`
6. ## Change-Invite-status
    - Method: ``
    - Serializer: ``
    - Functionality: ``
    - Authentication: ``
    - Authorization: ``
    - URL: ``
    - Notes: `No Notes`
7. ## Show-Invites
    - Method: ``
    - Serializer: ``
    - Functionality: ``
    - Authentication: ``
    - Authorization: ``
    - URL: ``
    - Notes: `No Notes`
8. ## Login
    - Method: ``
    - Serializer: ``
    - Functionality: ``
    - Authentication: ``
    - Authorization: ``
    - URL: ``
    - Notes: `No Notes`
9. ## Logout
    - Method: ``
    - Serializer: ``
    - Functionality: ``
    - Authentication: ``
    - Authorization: ``
    - URL: ``
    - Notes: `No Notes`
10. ## Change-Workspace-Name-Or-Image
    - Method: ``
    - Serializer: ``
    - Functionality: ``
    - Authentication: ``
    - Authorization: ``
    - URL: ``
    - Notes: `No Notes`
11. ## Update-Profile-Info
    - Method: ``
    - Serializer: ``
    - Functionality: ``
    - Authentication: ``
    - Authorization: ``
    - URL: ``
    - Notes: `No Notes`
12. ## Change-Password
    - Method: ``
    - Serializer: ``
    - Functionality: ``
    - Authentication: ``
    - Authorization: ``
    - URL: ``
    - Notes: `No Notes`
13. ## Change-Image
    - Method: ``
    - Serializer: ``
    - Functionality: ``
    - Authentication: ``
    - Authorization: ``
    - URL: ``
    - Notes: `No Notes`

