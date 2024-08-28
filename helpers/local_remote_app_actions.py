from subprocess import run

def get_local_user_upn():
    output = run('whoami /upn', capture_output=True, text=True, shell=True)
    if output.returncode == 0:
        return output.stdout.strip().lower()
    else:
        # TODO add logging
        print('Error retrieving local user upn')
        return None


if __name__ == '__main__':
    exit(0)