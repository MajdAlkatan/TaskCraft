# How To Use Pagination
## Paginated Response structure:
```json
{
    "count": "result-objects-count(number)",
    "next": "url-to-next-page",
    "previous": "url-to-previous-page",
    "results": [
        "data"
    ]
}
```
## The GET Request Form:
```http
http://127.0.0.1/api/users/?page=1
```

you can choose the page you want by modifying the page Param.
## Customizing the page size
You can Customize the page size, make it bigger/smaller.

Example:

```http
http://127.0.0.1/api/users/?page=1&size=60
```

That will fetch 60 result object from database.

Of-course there is a limit you can't push over it.