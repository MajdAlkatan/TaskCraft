<!-- 2. ## 
    - Method: ``
    - Serializer: ``
    - Functionality: ``
    - Authentication: ``
    - Authorization: ``
    - URL: ``
    - Notes: `No Notes`
    - status: `coming soon...` -->

# Workspace End-Points representation
1. ## Get-Workspace-info
    - Method: `GET`
    - Serializer: `WorkspaceSerializer`
    - Functionality: `just getting the workspace by primary-key`
    - Authentication: `required`
    - Authorization: `admin can get any workspace info | normal-user can just get his own workspace info`
    - URL: ``
    - Notes: `No Notes`
    - status: `ready`
2. ## Get-All-Workspaces
    - Method: `GET`
    - Serializer: `WorkspaceSerializer`
    - Functionality: `just getting all workspaces (Paginated response)`
    - Authentication: `required`
    - Authorization: `admin can get all workspaces info | normal-user can get only his own workspaces info`
    - URL: ``
    - Notes: `this endpoint can support filtering/searching/ordering`
    - status: `ready`
3. ## Create-Workspace
    - Method: `POST`
    - Serializer: `WorkspaceSerializer`
    - Functionality: `simply creating the workspace with name and image for authenticated user (or specific user if authenticated admin)`
    - Authentication: `require client + Authorization_Header`
    - Authorization: `normal-user`
    - URL: ``
    - Notes: `No Notes`
    - status: `ready`
4. ## Change-Workspace-Name-Or-Image
    - Method: `PATCH`
    - Serializer: `WorkspaceSerializer`
    - Functionality: `Partial-Update workspace info if the authenticated user is the owner or an admin`
    - Authentication: `required`
    - Authorization: `admin/normal-user`
    - URL: ``
    - Notes: `No Notes`
    - status: `ready`
5. ## Get-User-Workspaces
    - Method: `GET`
    - Serializer: `WorkspaceSerializer`
    - Functionality: `just getting the workspaces belongs to user_id`
    - Authentication: `required`
    - Authorization: `normal-user can get his own workspaces info`
    - URL: `/workspaces/owned/`
    - Notes: `No Notes`
    - status: `ready`
6. ## Get-Workspace-Members
    - Method: `GET`
    - Serializer: `WorkspaceSerializer`
    - Functionality: `getting the workspace members`
    - Authentication: `required`
    - Authorization: `client / authenticated user but has to be a member of the required workspace`
    - URL: `/workspaces/{id}/members/`
    - Notes: `No Notes`
    - status: `ready`
7. ## Get-Workspace-Owner
    - Method: ``
    - Serializer: ``
    - Functionality: ``
    - Authentication: ``
    - Authorization: ``
    - URL: ``
    - Notes: `No Notes`
    - status: `coming soon...`
8. ## Leave_Workspace
    - Method: ``
    - Serializer: ``
    - Functionality: ``
    - Authentication: ``
    - Authorization: ``
    - URL: ``
    - Notes: `No Notes`
    - status: `coming soon...`







