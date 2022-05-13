<h1>KANVAS</h1>

<h2>O diagrama de relacionamento encontra-se na raiz do projeto.</h2>
</br>
<h2>Método - POST</h2>
<h2>CRIAÇÃO DE USUÁRIO</h2>
Na criação do usuário, se a chave is_admin for colocada como True, o usuário será um instrutor, caso seja colocada como False, o usuário será um aluno.</br>
*endpoint*: /api/accounts/ -> Não precisa de autorização

<pre>
Corpo da requisição:

{
    "first_name": "Roberto",
    "last_name": "Silva",
    "email": "roberto@mail.com",
    "password": "Cat7021?", 
    "is_admin": "False" 
}

Resposta esperada: 201 - CREATED

{
    "uuid": "298e0a8b-f1aa-4396-8fc6-4f08ee69af4c",
    "is_admin": false,
    "email": "roberto@mail.com",
    "first_name": "Roberto",
    "last_name": "Silva"
}


ERROS:

Usuário já cadastrado: 422 - UNPROCESSABLE ENTITY

{
    "message": "User already exists"
}

</pre>
<h2>Método - POST</h2>
<h2>LOGIN DE USUÁRIO CADASTRADO</h2>
*endpoint*: /api/login/ -> Não precisa de autorização

<pre>
Corpo da requisição:

{
    "email": "roberto212@mail.com",
    "password": "Cat7021?"
}

Resposta esperada:

{
    "token": "c921e61e1a27528b6fbfcf5ecbcbff351a187931"
}

ERROS:

Tentativa de login de usuário não cadastrado: 401 - UNAUTHORIZED

</pre>
<h2>Método - GET</h2>
<h2>LISTAGEM DE USUÁRIOS</h2>
*endpoint*: /api/accounts/ -> Precisa de autenticação de instrutor

<pre>
Sem corpo derequisição

Resposta esperada: 200 - OK

[
    {
        "uuid": "c1b2363d-8c00-4d3e-af82-cf2dfd47c6b2",
        "is_admin": true,
        "email": "andre@mail.com",
        "first_name": "Andre",
        "last_name": "Silva"
    },
    {
        "uuid": "99cc3966-a374-43f6-aeee-af04e65e5da6",
        "is_admin": false,
        "email": "ricardo@mail.com",
        "first_name": "Ricardo",
        "last_name": "Silva"
    }
]

Caso o token não seja válido a resposta será:
401 - Unauthorized
{
    "detail": "Invalid token."
}

</pre>

<h2>Método - PUT</h2>
<h2>CADASTRO DE ENDEREÇO PARA USUÁRIO</h2>
*endpoint*: /api/address/ -> Precisa de autenticação de instrutor

<pre>
Corpo de requisição:

{
    "zip_code": "111456009",
    "street": "Rua da Joana",
    "house_number": "123",
    "city": "Curitiba",
    "state": "Paraná",
    "country": "Brasil"
}

Resposta esperada: 200 - OK

[
    {
        "uuid": "552c5ac1-bac6-442a-8d20-7f82f0a8e2f4",
        "street": "Rua das Joana",
        "house_number": 123,
        "city": "Curitiba",
        "state": "Paraná",
        "zip_code": "111456009",
        "country": "Brasil",
        "users": [
            {
                "uuid": "7d7d9020-e689-4f05-9d55-1703add6f9ab",
                "is_admin": false,
                "email": "andre2@mail.com",
                "first_name": "Andre",
                "last_name": "Silva"
            },
            {
                "uuid": "298e0a8b-f1aa-4396-8fc6-4f08ee69af4c",
                "is_admin": false,
                "email": "roberto212@mail.com",
                "first_name": "Roberto",
                "last_name": "Silva"
            }
        ]
    }
]

</pre>


<h2>Método - POST</h2>
<h2>CRIAÇÃO DE CURSOS</h2>
*endpoint*: /api/courses/ -> Autorização de instrutor

<pre>
Corpo de requisição:
{
    "name": "Django",
    "demo_time": "9:00",
    "link_repo": "https://gitlab.com/turma_django/"
}

Resposta esperada: 201 - CREATED

{
    "uuid": "dd748813-55da-4487-9354-74512807dfa6",
    "name": "Django",
    "demo_time": "09:00:00",
    "created_at": "2022-05-11T20:41:41.221468Z",
    "link_repo": "https://gitlab.com/turma_django/",
    "instructor": null,
    "students": []
}

</pre>


<h2>Método - GET</h2>
<h2>LISTAGEM DE CURSOS</h2>
*endpoint*: /api/courses/ -> Não necessita de autorização

<pre>
Sem corpo de requisição

Exemplo de resposta esperada: 200 - OK

{
    "uuid": "b3ba219c-f569-47d7-87c8-af3a7d1778ba",
    "name": "Python and Django 22",
    "demo_time": "09:00:00",
    "created_at": "2022-05-10T18:09:41.238557Z",
    "link_repo": "https://gitlab.com/turma_django/",
    "instructor": null,
    "students": [
        {
            "uuid": "41769111-0fb3-4c1e-8512-2dfb77a61dda",
            "is_admin": false,
            "email": "andre@mail.com",
            "first_name": "Andre",
            "last_name": "Silva"
        },
        {
            "uuid": "de92af42-c7cf-4588-a597-893b482d78d1",
            "is_admin": false,
            "email": "ricardo@mail.com",
            "first_name": "Ricardo",
            "last_name": "Silva"
        }
        ]
}

</pre>


<h2>Método - GET</h2>
<h2>FILTRAGEM DE UM CURSO ESPECÍFICO PELO ID</h2>
*endpoint*: /api/courses/<course_id>/ -> Não precisa de autorização

<pre>
Sem corpo de requisição.
Passar o id do curso no endpoint da rota

Exemplo de resposta esperada: 200 - OK
course_id = b3ba219c-f569-47d7-87c8-af3a7d1778ba: 

{
    "uuid": "b3ba219c-f569-47d7-87c8-af3a7d1778ba",
    "name": "Python and Django 22",
    "demo_time": "09:00:00",
    "created_at": "2022-05-10T18:09:41.238557Z",
    "link_repo": "https://gitlab.com/turma_django/",
    "instructor": null,
    "students": [
        {
            "uuid": "41769111-0fb3-4c1e-8512-2dfb77a61dda",
            "is_admin": false,
            "email": "andre@mail.com",
            "first_name": "Andre",
            "last_name": "Silva"
        },
        {
            "uuid": "de92af42-c7cf-4588-a597-893b482d78d1",
            "is_admin": false,
            "email": "ricardo@mail.com",
            "first_name": "Ricardo",
            "last_name": "Silva"
        }
    ]
}

ERROS

Se o course_id for inválido: 404 - NOT FOUND

{
    "message": "Course does not exist"
}

</pre>


<h2>Método - PATCH</h2>
<h2>ATUALIZAÇÃO DE CURSOS</h2>
*endpoint*: /api/courses/<course_id>/ -> Autorização de instrutor</br>
Informar no endpoint da rota o id do curso a ser atualizado.

<pre>
Endpoint:
/api/courses/b3ba219c-f569-47d7-87c8-af3a7d1778ba/

Exemplo de corpo de requisição para atualização do nome do curso:

{
    "name": "Django avançado"	
}

Resposta esperada: 200 - OK

{
    "uuid": "b3ba219c-f569-47d7-87c8-af3a7d1778ba",
    "name": "Django avançado",
    "demo_time": "09:00:00",
    "created_at": "2022-05-10T18:09:41.238557Z",
    "link_repo": "https://gitlab.com/turma_django/",
    "instructor": null,
    "students": [
        {
            "uuid": "41769111-0fb3-4c1e-8512-2dfb77a61dda",
            "is_admin": false,
            "email": "andre@mail.com",
            "first_name": "Andre",
            "last_name": "Silva"
        },
        {
            "uuid": "de92af42-c7cf-4588-a597-893b482d78d1",
            "is_admin": false,
            "email": "ricardo@mail.com",
            "first_name": "Ricardo",
            "last_name": "Silva"
        }
    ]
}

ERROS

Tentativa de atualizar curso inexistente: 404 - NOT FOUND

{
    "message": "Course does not exist"
}
</pre>

<h2>Método - PUT</h2>
<h2>CADASTRO DE INSTRUTOR NO CURSO</h2>
*endpoint*: /api/courses/<course_id>/registrations/instructor/ -> Autorização de instrutor

<pre>
Corpo de requisição:
{
    "instructor_id": "93161b66-c3db-489a-b329-55e064462133"
}

Exemplo de resposta esperada:

{
    "uuid": "50141964-fae8-44f9-a9f9-c146479fc6ab",
    "name": "Django",
    "demo_time": "09:00:00",
    "created_at": "2022-05-10T20:11:44.731339Z",
    "link_repo": "https://gitlab.com/turma_django/",
    "instructor": {
        "uuid": "93161b66-c3db-489a-b329-55e064462133",
        "is_admin": true,
        "email": "andre255@mail.com",
        "first_name": "Andre",
        "last_name": "Silva"
    },
    "students": []
}


ERROS

1 - Se o id pertencer a um estudante: 422 - UNPROCESSABLE ENTITY

{
    "message": "Instructor id does not belong to an admin"
}
       

2 - Se for informado um course_id inválido: 404 - NOT FOUND

{
    "message": "Course does not exist"
}

3 - Caso seja informado um instructor_id que não pertença a um instrutor: 404 - NOT FOUND

{
    "message": "Invalid instructor_id"
}

</pre>


<h2>Método - PUT</h2>
<h2>CADASTRO DE ESTUDANTES NO CURSO</h2>
*endpoint*: /api/courses/<course_id>/registrations/students/ -> Autorização de instrutor

<pre>
Corpo de requisição:

{
    "students_id": [
        "de92af42-c7cf-4588-a597-893b482d78d1",
        "41769111-0fb3-4c1e-8512-2dfb77a61dda"
    ]
}

Exemplo de resposta: 200 - OK

{
    "uuid": "b3ba219c-f569-47d7-87c8-af3a7d1778ba",
    "name": "Python and Django 22",
    "demo_time": "09:00:00",
    "created_at": "2022-05-10T18:09:41.238557Z",
    "link_repo": "https://gitlab.com/turma_django/",
    "instructor": {
        "uuid": "93161b66-c3db-489a-b329-55e064462133",
        "is_admin": true,
        "email": "andre255@mail.com",
        "first_name": "Andre",
        "last_name": "Silva"
    },
    "students": [
        {
            "uuid": "41769111-0fb3-4c1e-8512-2dfb77a61dda",
            "is_admin": false,
            "email": "andre@mail.com",
            "first_name": "Andre",
            "last_name": "Silva"
        },
        {
            "uuid": "de92af42-c7cf-4588-a597-893b482d78d1",
            "is_admin": false,
            "email": "ricardo@mail.com",
            "first_name": "Ricardo",
            "last_name": "Silva"
        }
    ]
}

Observa-se que o campo 'students' é atualizado todas as vezes, ou seja, os estudantes</br> presentes no curso são removidos e os novos adicionados em seu lugar.

ERROS

1 - Somente usuários do tipo estudante podem ser matriculados no curso.
Caso um id de instrutor seja informado: 422 - UNPROCESSABLE ENTITY

{
    "message": "Some student id belongs to an Instructor"
}

2 - Caso seja informado um course_id inválido: 404 - NOT FOUND

{
    "message": "Course does not exist"
}

3 - Caso informado um stundent_id inválido: 404 - NOT FOUND

{
    "message": "Invalid students_id list"
}

</pre>



<h2>Método - DELETE</h2>
<h2>DELETAR CURSOS</h2>
*endpoint*: /api/courses/<course_id>/ -> Autorização de instrutor

<pre>
Sem corpo de requisição

Sem corpo de resposta: 204 NO CONTENT

ERROS

Caso seja informado um course_id inválido: 404 - NOT FOUND

{
    "message": "Course does not exist"
}


</pre>

