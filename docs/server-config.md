# TabPy Server Configuration Instructions

<!-- markdownlint-disable MD004 -->

<!-- toc -->

- [Configuring HTTP vs HTTPS](#configuring-http-vs-https)
- [Authentication](#authentication)
  * [Enabling Authentication](#enabling-authentication)
  * [Password File](#password-file)
  * [Setting Up Environment](#setting-up-environment)
  * [Adding an Account](#adding-an-account)
  * [Updating an Account](#updating-an-account)
  * [Deleting an Account](#deleting-an-account)
- [Logging](#logging)
  * [Request Context Logging](#request-context-logging)
- [Custom Script Timeout](#custom-script-timeout)

<!-- tocstop -->

<!-- markdownlint-enable MD004 -->

Default settings for TabPy may be viewed in the
tabpy_server/common/default.conf file. This file also contains
commented examples of how to set up your TabPy server to only
serve HTTPS traffic and enable authentication.

Change settings by:

1. Adding environment variables:
   - set the environment variable as required by your Operating System. When
     creating environment variables, use the same name as is in the config file
     as an environment variable. The files startup.sh and startup.cmd in the root
     of the install folder have examples of how to set environment variables in
     both Linux and Windows respectively. Set any desired environment variables
     and then start the application.
2. Modifying default.conf.
3. Specifying your own config file as a command line parameter.
   - i.e. Running the command:

     ```sh
     python tabpy.py --config=path\to\my\config
     ```

The default config file is provided to show you the default values but does not
need to be present to run TabPy.

## Configuring HTTP vs HTTPS

By default, TabPy serves only HTTP requests. TabPy can be configured to serve
only HTTPS requests by setting the following parameter in the config file:

```sh
TABPY_TRANSFER_PROTOCOL = https
```

If HTTPS is selected, the absolute paths to the cert and key file need to be
specified in your config file using the following parameters:

```sh
TABPY_CERTIFICATE_FILE = C:/path/to/cert/file.crt
TABPY_KEY_FILE = C:/path/to/key/file.key
```

Note that only PEM-encoded x509 certificates are supported for the secure
connection scenario.

## Authentication

TabPy supports basic access authentication (see
[https://en.wikipedia.org/wiki/Basic_access_authentication](https://en.wikipedia.org/wiki/Basic_access_authentication)
for more details).

### Enabling Authentication

To enable the feature specify the `TABPY_PWD_FILE` parameter in the
TabPy configuration file with a fully qualified name:

```sh
TABPY_PWD_FILE = c:\path\to\password\file.txt
```

### Password File

Password file is a text file containing usernames and hashed passwords
per line separated by single space. For username only ASCII characters
are supported. Usernames are case-insensitive.

Passwords in the password file are hashed with PBKDF2. [See source code
for implementation details](../tabpy-server/tabpy_server/handlers/util.py).

**It is highly recommended to restrict access to the password file
with hosting OS mechanisms. Ideally the file should only be accessible
for reading with the account under which TabPy runs and TabPy admin account.**

There is a `utils/user_management.py` utility to operate with
accounts in the password file. Run `utils/user_management.py -h` to
see how to use it.

After making any changes to the password file, TabPy needs to be restarted.

### Setting Up Environment

Before making any code changes run the environment setup script. For
Windows run this command from the repository root folder:

```sh
utils\set_env.cmd
```

and for Linux or Mac run this command from the repository root folder:

```sh
source utils/set_env.sh
```

### Adding an Account

To add an account run `utils/user_management.py` utility with `add`
command  providing user name, password (optional) and password file:

```sh
python utils/user_management.py add -u <username> -p <password> -f <pwdfile>
```

If the (recommended) `-p` argument is not provided a password for the user name
will be generated and displayed in the command line.

### Updating an Account

To update the password for an account run `utils/user_management.py` utility
with `update` command:

```sh
python utils/user_management.py update -u <username> -p <password> -f <pwdfile>
```

If the (recommended) `-p` agrument is not provided a password for the user name
will be generated and displayed in the command line.

### Deleting an Account

To delete an account open password file in any text editor and delete the
line with the user name.

## Logging

Logging for TabPy is implemented with Python's standard logger and can be configured
as explained in Python documentation at
[Logging Configuration page](https://docs.python.org/3.6/library/logging.config.html).

A default config provided with TabPy is at
[`tabpy-server/tabpy_server/common/default.conf`](tabpy-server/tabpy_server/common/default.conf)
and has a configuration for console and file loggers. Changing the config file
allows the user to modify the log level, format of the logged messages and
add or remove loggers.

### Request Context Logging

For extended logging (e.g. for auditing purposes) additional logging can be turned
on with setting `TABPY_LOG_DETAILS` configuration file parameter to `true`.

With the feature on additional information is logged for HTTP requests: caller ip,
URL, client infomation (Tableau Desktop\Server), Tableau user name (for Tableau Server)
and TabPy user name as shown in the example below:

<!-- markdownlint-disable MD013 -->
<!-- markdownlint-disable MD040 -->

```
2019-05-02,13:50:08 [INFO] (base_handler.py:base_handler:90): Call ID: 934073bd-0d29-46d3-b693-b1e4b1efa9e4, Caller: ::1, Method: POST, Resource: http://localhost:9004/evaluate, Client: Postman for manual testing, Tableau user: ogolovatyi
2019-05-02,13:50:08 [DEBUG] (base_handler.py:base_handler:120): Checking if need to handle authentication, <<
call ID: 934073bd-0d29-46d3-b693-b1e4b1efa9e4>>
2019-05-02,13:50:08 [DEBUG] (base_handler.py:base_handler:120): Handling authentication, <<call ID: 934073bd-
0d29-46d3-b693-b1e4b1efa9e4>>
2019-05-02,13:50:08 [DEBUG] (base_handler.py:base_handler:120): Checking request headers for authentication d
ata, <<call ID: 934073bd-0d29-46d3-b693-b1e4b1efa9e4>>
2019-05-02,13:50:08 [DEBUG] (base_handler.py:base_handler:120): Validating credentials for user name "user1",
 <<call ID: 934073bd-0d29-46d3-b693-b1e4b1efa9e4>>
2019-05-02,13:50:08 [DEBUG] (state.py:state:484): Collecting Access-Control-Allow-Origin from state file...  
2019-05-02,13:50:08 [INFO] (base_handler.py:base_handler:120): function to evaluate=def _user_script(tabpy, _
arg1, _arg2):
 res = []
 for i in range(len(_arg1)):
   res.append(_arg1[i] * _arg2[i])
 return res
, <<call ID: 934073bd-0d29-46d3-b693-b1e4b1efa9e4>>
```

<!-- markdownlint-enable MD040 -->
<!-- markdownlint-enable MD013 -->

No passwords are logged.

NOTE the request context details are logged with INFO level.

## Custom Script Timeout

By default, all custom scripts executed through `POST /evaluate` may run for up
to 30.0 s before being terminated. To configure this timeout, uncomment
`TABPY_EVALUATE_TIMEOUT = 30` in the default config under
`tabpy-server/tabpy_server/common/default.conf` and replace `30` with the float
value of your choice representing the timeout time in seconds, or add such an
entry to your custom config.

This timeout does not apply when evaluating models either through the `/query`
method, or using the `tabpy.query(...)` syntax with the `/evaluate` method.
