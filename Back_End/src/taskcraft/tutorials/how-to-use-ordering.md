# How To Use Ordering

Example:

```http
http://127.0.0.1/api/users/?ordering=fullname
```
Thats will order the results from less to more.

## Reversing Order:

Example:

```http
http://127.0.0.1/api/users/?ordering=-fullname
```
Thats will order the results from more to less.

## Multiple ordering:

Example:

```http
http://127.0.0.1/api/users/?ordering=-fullname,created_at
```

## Important Notes:
Not all field accept ordering.