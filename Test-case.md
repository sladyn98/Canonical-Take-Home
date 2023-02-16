## Test Scenario:
Testing SSH Connectivity using Password and Key-based Authentication

## Description:
This test case aims to verify the ability of a system to connect to a remote server using both password-based and key-based authentication methods for SSH connectivity.

## Setup:

* We need two Linux systems: a local system and a remote server (to connect to)
* SSH server and Client software installed on both systems.The most popular SSH client and server software for Linux systems is `OpenSSH`. It comes pre-installed on most Linux distributions, but you can install it using the package manager of your Linux distribution.
* Network connectivity established between the local system and the remote server
* An SSH user account should be created on the remote server. You can add a user using `adduser` command.
* The SSH user account which is on the remote server should be configured to allow password-based and key-based authentication.To do this, you need to edit the SSH server configuration file (/etc/ssh/sshd_config)
* Test user credentials created for both password-based and key-based authentication


## Teardown:

The test user accounts deleted from the remote server
SSH server and client software uninstalled from both systems

## Tools Used in Testing:

* SSH client (ssh) and server (sshd) software
* ssh-keygen: to generate SSH key pair
* ssh-copy-id: to copy the public key to the remote server
* Password authentication: SSH client will prompt for a password
* Key-based authentication: SSH client will use a private key to authenticate


## Pass/Fail Criteria:

The criteria for pass and fail are quite simple. The test passes if the SSH connection is established successfully using both password-based and key-based authentication methods and the test fails if the SSH connection is not established or the authentication fails.


## Test Scenarios:

### Scenario 1: Test Password-Based Authentication

Open a terminal on the local system.
Run the SSH client command to connect to the remote server using the test user credentials for password-based authentication:

`ssh <username>@<remote-server-ip>`

When you are prompted for the password, enter the test user password for password-based authentication.Verify that the SSH connection is established successfully. Close the SSH session.

### Scenario 2: Test Key-Based Authentication

Open a terminal on the local system.
Generate a new SSH key pair (public and private) using the ssh-keygen command:

`ssh-keygen -t rsa`

Copy the public key to the remote server using the ssh-copy-id command:

`ssh-copy-id <username>@<remote-server-ip>`

Run the SSH client command to connect to the remote server using the test user credentials for key-based authentication:

`ssh -i ~/.ssh/id_rsa <username>@<remote-server-ip>`

Verify that the SSH connection is established successfully and then close the SSH session.

### Scenario 3: Test Password-Based Authentication (with Key-Based Authentication Disabled)

Open a terminal on the local system.
Disable key-based authentication on the remote server by modifying the SSH server settings.
Run the SSH client command to connect to the remote server using the test user credentials for password-based authentication:

`ssh <username>@<remote-server-ip>`

When prompted for the password, enter the test user password for password-based authentication.
Verify that the SSH connection is established successfully and then close the session.

### Scenario 4: Test Key-Based Authentication (with Password-Based Authentication Disabled)

Open a terminal on the local system.
Disable password-based authentication on the remote server by modifying the SSH server settings.
Run the SSH client command to connect to the remote server using the test user credentials for key-based authentication:

`ssh -i ~/.ssh/id_rsa <username>@<remote-server-ip>`

Verify that the SSH connection is established successfully.
Close the SSH session.
